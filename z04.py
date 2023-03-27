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
SLEEP_CONSTANT: float = 0.1


class Shared:
    """Represents shared data between threads."""
    def __init__(self):
        """Initialize an instance of Shared."""
        self.savage_mutex = Mutex()
        self.cook_mutex = Mutex()
        self.servings = 0
        self.fullPot = Semaphore(0)
        self.emptyPot = Event()
        self.barrier = Barrier()


class Barrier:
    """Represents a reusable barrier synchronization pattern."""
    def __init__(self):
        """Initialize an instance of Barrier."""
        self.mutex = Mutex()
        self.count = 0
        self.turnstile1 = Semaphore(0)
        self.turnstile2 = Semaphore(0)

    def wait1(self, i: int):
        """
        Use barrier to wait for all savages.

        Parameters:
            i -- savage id, integer
        """
        self.mutex.lock()
        self.count += 1
        if self.count == NUM_SAVAGES:
            self.turnstile1.signal(NUM_SAVAGES)
        self.mutex.unlock()
        self.turnstile1.wait()
        print(f'➜ Savage {i}: arrived to the feast')

    def wait2(self, i: int):
        """
        Prepare barrier for future use.

        Parameters:
            i -- savage id, integer
        """
        self.mutex.lock()
        self.count -= 1
        if self.count == 0:
            print(f'✔ Savage {i}: everyone is ready, feast can start\n')
            self.turnstile2.signal(NUM_SAVAGES)
        self.mutex.unlock()
        self.turnstile2.wait()


def get_serving_from_pot(i: int, shared: Shared):
    """
    Simulate savage taking a serving from the pot.

    Parameters:
        i -- savage id, integer
        shared -- shared data, class Shared
    """
    print(f'🍴 Savage {i}: takes a serving')
    sleep(randint(1, 3) * SLEEP_CONSTANT)
    shared.servings -= 1


def feast(i: int):
    """
    Simulate savage feasting.

    Parameters:
        i -- savage id, integer
    """
    print(f'🍴 Savage {i}: is feasting')
    sleep(randint(5, 25) * SLEEP_CONSTANT)


def put_serving_in_pot(i: int, shared: Shared):
    """
    Simulate cook preparing a serving and putting it in the pot.

    Parameters:
        i -- cook id, integer
        shared -- shared data, class Shared
    """
    sleep(randint(1, 8) * SLEEP_CONSTANT)
    shared.servings += 1
    print(f'🍲 Cook {i}: put serving in pot')


def savage(i: int, shared: Shared):
    """
    Implement behaviour of a savage.

    All savages arrive. When everyone is ready, one savage
    finds out the number of servings in the pot. If pot is
    empty, savage wakes up the cooks. Cooks cook a full pot.
    When pot is not empty, savage takes a serving. After
    this, savage is free to eat his serving and other savages
    are allowed to take their servings (again one at a time).

    Uses Reusable barrier to wait for all savages to arrive.
    Uses Mutex lock to ensure servings counter integrity and
    mutual exclusion of savages.
    Uses Event to signal that the pot is empty.

    Parameters:
        i -- savage id, integer
        shared -- shared data, class Shared
    """
    while True:
        # Reusable barrier: wait for all savages
        shared.barrier.wait1(i)
        shared.barrier.wait2(i)

        # Mutex: savages take servings one savage at a time
        shared.savage_mutex.lock()
        print(f'❓ Savage {i}: number of servings left in pot: '
              f'{shared.servings}')
        if shared.servings == 0:
            # Pot is empty: signal the cooks and wait for full pot
            print(f'⏰ Savage {i}: wakes up the cook\n')
            shared.emptyPot.signal()
            shared.fullPot.wait()
        # Pot is not empty: savage takes serving
        get_serving_from_pot(i, shared)
        shared.savage_mutex.unlock()

        # Savages eat their servings
        feast(i)


def cook(i: int, shared: Shared):
    """
    Implement behaviour of a cook.

    Cooks waits until the pot is empty (savages wake him up).
    One cook prepares one serving at a time. The cook that
    cooks the last serving signals to the savages that pot is
    now full. He clears the Event of an empty pot, which
    means other cooks will no longer try to cook, until the
    savages eat all the servings again.

    Uses mutex lock to ensure integrity of the servings counter,
    as well as mutual exclusion of cooks.

    Parameters:
        i -- cook id, integer
        shared -- shared data, class Shared
    """
    while True:
        # Mutex: one cook enters
        shared.cook_mutex.lock()
        # Waits if empty pot Event is not started
        shared.emptyPot.wait()
        # Event is started, cooks a serving, puts it in the pot
        put_serving_in_pot(i, shared)

        if shared.servings >= POT_CAPACITY:
            # Cook cooked the last serving, signal savages, clear Event
            print(f'Cooks finished cooking: number of servings in pot:',
                  shared.servings, '\n')
            shared.fullPot.signal()
            shared.emptyPot.clear()
            shared.cook_mutex.unlock()
            continue
        shared.cook_mutex.unlock()
        sleep(0.01)     # encourage re-planning to a different cook


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
