"""This module implements a solution to the Dining Savages Problem."""

__author__ = "Maty Masaryk, Marián Šebeňa, Matúš Jokay"
__email__ = "xmasarykm1@stuba.sk"
__license__ = "MIT"

from fei.ppds import Thread, Mutex, Semaphore, Event, print
from time import sleep
from random import randint

POT_CAPACITY = 5
NUM_SAVAGES = 4
NUM_COOKS = 3


class Shared:
    """Represents shared data for all threads."""

    def __init__(self):
        """Initialize an instance of Shared."""
        self.savage_mutex = Mutex()
        self.pot_mutex = Mutex()
        self.cook_mutex = Mutex()
        self.servings = 0
        self.fullPot = Semaphore(0)
        self.emptyPot = Event()
        self.barrier = Barrier()


class Barrier:
    """Represents shared data for all threads."""

    def __init__(self):
        self.mutex = Mutex()
        self.count = 0
        self.turnstile1 = Semaphore(0)
        self.turnstile2 = Semaphore(0)

    def wait1(self, i):
        self.mutex.lock()
        self.count += 1
        if self.count == NUM_SAVAGES:
            self.turnstile1.signal(NUM_SAVAGES)
        self.mutex.unlock()
        self.turnstile1.wait()
        print(f'➜ Savage {i}: arrived to the feast')

    def wait2(self, i):
        self.mutex.lock()
        self.count -= 1
        if self.count == 0:
            print(f'✔ Savage {i}: is the last one, feast can start\n')
            self.turnstile2.signal(NUM_SAVAGES)
        self.mutex.unlock()
        self.turnstile2.wait()


def get_serving_from_pot(i: int, shared: Shared):
    shared.pot_mutex.lock()
    print(f'🍴 Savage {i}: takes a portion')
    sleep(0.1)
    shared.servings -= 1
    shared.pot_mutex.unlock()


def feast(i: int, shared: Shared):
    print(f'🍴 Savage {i}: is feasting')
    sleep(1)


def put_serving_in_pot(i: int, shared: Shared):
    sleep(0.1)
    shared.servings += 1
    print(f'🍲 Cook {i}: put portion in pot')


def savage(i: int, shared: Shared):
    while True:

        shared.barrier.wait1(i)
        shared.barrier.wait2(i)

        shared.savage_mutex.lock()
        print(f'❓ Savage {i}: number of servings left in pot: {shared.servings}')
        if shared.servings == 0:
            print(f'⏰ Savage {i}: wakes up the cook\n')
            shared.emptyPot.signal()
            shared.fullPot.wait()

        get_serving_from_pot(i, shared)
        shared.savage_mutex.unlock()

        feast(i, shared)


def cook(i: int, shared: Shared):
    while True:
        shared.cook_mutex.lock()
        shared.emptyPot.wait()
        shared.pot_mutex.lock()
        if shared.servings >= POT_CAPACITY:
            shared.pot_mutex.unlock()
            shared.cook_mutex.unlock()
            continue

        put_serving_in_pot(i, shared)

        if shared.servings >= POT_CAPACITY:
            print(f'Cooks finished cooking: number of servings in pot:', shared.servings, '\n')
            shared.fullPot.signal()
            shared.emptyPot.clear()
            shared.pot_mutex.unlock()
            shared.cook_mutex.unlock()
            continue
        shared.pot_mutex.unlock()
        shared.cook_mutex.unlock()
        sleep(0.01)  # force re-planning


def main():
    """Create and run threads."""
    shared: Shared = Shared()
    savages: list[Thread] = [
        Thread(savage, i, shared) for i
        in range(NUM_SAVAGES)
    ]
    cooks: list[Thread] = [
        Thread(cook, i, shared) for i
        in range(NUM_COOKS)
    ]

    for sc in savages + cooks:
        sc.join()


if __name__ == "__main__":
    main()
