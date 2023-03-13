"""This module implements the Dining philosophers problem."""

__author__ = "Maty Masaryk, Tomáš Vavro"
__email__ = "xmasarykm1@stuba.sk"
__license__ = "MIT"

from fei.ppds import Thread, Mutex, Semaphore, print
from time import sleep
from random import randint

VARIANT: int = 2  # 0: waiter // 1: leftie // 2: token
NUM_PHILOSOPHERS: int = 5
NUM_RUNS: int = 4  # number of repetitions of think-eat cycle of philosophers
SLEEP_CONSTANT: float = 0.1

leftie: int = randint(0, NUM_PHILOSOPHERS - 1)


class Shared:
    """Represents shared data for all threads."""

    def __init__(self):
        """Initialize an instance of Shared."""
        self.forks = [Mutex() for _ in range(NUM_PHILOSOPHERS)]
        self.waiter = Semaphore(NUM_PHILOSOPHERS - 1)
        self.mutex = Mutex()
        self.eating = [False for _ in range(NUM_PHILOSOPHERS)]
        self.hunger = [0 for _ in range(NUM_PHILOSOPHERS)]
        self.maxHunger = [-1 for _ in range(NUM_PHILOSOPHERS)]


def think(i: int):
    """Simulate thinking.

    Args:
        i -- philosopher's id
    """
    print(f"🧠 Philosopher {i} is thinking!\n")
    sleep(randint(1, 10) * SLEEP_CONSTANT)


def eat(i: int):
    """Simulate eating.

    Args:
        i -- philosopher's id
    """
    print(f"🍴 Philosopher {i} is eating!\n")
    sleep(randint(1, 10) * SLEEP_CONSTANT)


def take_return(i: int, right: bool, take: bool):
    """
    Print info when philosopher is taking or returning a fork.

    Parameters:
        i -- philosopher's id, integer
        right -- true: right fork, false: left fork, boolean
        take -- true: take fork, false: return fork, boolean
    """
    print(f"{'➜' if take else '↩'} Philosopher {i} "
          f"{'took' if take else 'returned'} "
          f"{'right' if right else 'left'} fork.")


def balk(i):
    """
    Represents situation when neighbor is eating.

    Parameters:
        i -- philosopher's id, integer
    """
    print(f'✖ Philosopher {i} can\'t eat now.')
    sleep(randint(10, 30) * SLEEP_CONSTANT)


def calc_hunger(i, shared: Shared):
    """
    Calculates hunger and max hunger of philosopher.

    Parameters:
        i -- philosopher's id, integer
        shared -- shared data, class Shared
    """
    shared.mutex.lock()
    shared.hunger[i] = 0
    for j in range(NUM_PHILOSOPHERS):
        if j != i:
            shared.hunger[j] += 1
            if shared.hunger[j] > shared.maxHunger[j]:
                shared.maxHunger[j] = shared.hunger[j]

    for j in range(NUM_PHILOSOPHERS):
        if shared.hunger[j] > shared.maxHunger[j]:
            shared.maxHunger[j] = shared.hunger[j]
    shared.mutex.unlock()


def print_hunger(shared: Shared):
    """
    Prints hunger of philosophers at the end of experiment.

    Parameters:
        i -- philosopher's id, integer
        shared -- shared data, class Shared
    """
    variant: str
    if VARIANT == 0:
        variant = "Waiter"
    elif VARIANT == 1:
        variant = "Leftie"
    else:
        variant = "Pseudo-Token"
    print(f'\n----------------------------------------\n'
          f'VARIANT: {variant}\n'
          f'NUMBER OF RUNS: {NUM_RUNS}\n'
          f'S----------------------------------------')

    for i in range(NUM_PHILOSOPHERS):
        print(f'Philosopher {i}: max hunger = {shared.maxHunger[i]}')

    print(f'----------------------------------------\n'
          f'HIGHEST HUNGER: {max(shared.maxHunger)}\n'
          f'LOWEST HUNGER: {min(shared.maxHunger)}\n'
          f'----------------------------------------')


def philosopher_waiter(i: int, shared: Shared):
    """Run philosopher's code, with a waiter.

    Args:
        i -- philosopher's id, integer
        shared -- shared data, class Shared
    """
    for _ in range(NUM_RUNS):
        shared.waiter.wait()
        think(i)
        # get forks
        shared.forks[i].lock()
        take_return(i, True, True)
        shared.forks[(i + 1) % NUM_PHILOSOPHERS].lock()
        take_return(i, False, True)
        calc_hunger(i, shared)
        eat(i)
        shared.forks[i].unlock()
        take_return(i, True, False)
        shared.forks[(i + 1) % NUM_PHILOSOPHERS].unlock()
        take_return(i, False, False)
        shared.waiter.signal()


def philosopher_leftie(i: int, shared: Shared):
    """Run philosopher's code, with a leftie.

    Args:
        i -- philosopher's id, integer
        shared -- shared data, class Shared
    """
    global leftie
    for _ in range(NUM_RUNS):
        think(i)
        if i == leftie:
            shared.forks[(i + 1) % NUM_PHILOSOPHERS].lock()
            take_return(i, False, True)
            shared.forks[i].lock()
            take_return(i, True, True)
        else:
            shared.forks[i].lock()
            take_return(i, True, True)
            shared.forks[(i + 1) % NUM_PHILOSOPHERS].lock()
            take_return(i, False, True)
        calc_hunger(i, shared)
        eat(i)
        if i == leftie:
            shared.forks[(i + 1) % NUM_PHILOSOPHERS].unlock()
            take_return(i, False, False)
            shared.forks[i].unlock()
            take_return(i, True, False)
        else:
            shared.forks[i].unlock()
            take_return(i, True, False)
            shared.forks[(i + 1) % NUM_PHILOSOPHERS].unlock()
            take_return(i, False, False)


def philosopher_token(i: int, shared: Shared):
    """Run philosopher's code, using token .

    Args:
        i -- philosopher's id, integer
        shared -- shared data, class Shared
    """
    for _ in range(NUM_RUNS):
        think(i)

        while shared.eating[(NUM_PHILOSOPHERS + i - 1) % NUM_PHILOSOPHERS] \
                or shared.eating[(i + 1) % NUM_PHILOSOPHERS]:
            balk(i)

        shared.mutex.lock()
        shared.eating[i] = True
        shared.mutex.unlock()

        shared.forks[i].lock()
        take_return(i, True, True)
        shared.forks[(i + 1) % NUM_PHILOSOPHERS].lock()
        take_return(i, False, True)
        calc_hunger(i, shared)
        eat(i)
        shared.forks[i].unlock()
        take_return(i, True, False)
        shared.forks[(i + 1) % NUM_PHILOSOPHERS].unlock()
        take_return(i, False, False)

        shared.mutex.lock()
        shared.eating[i] = False
        shared.mutex.unlock()


def main():
    """Run main."""
    shared: Shared = Shared()
    if VARIANT == 0:
        print(f'\n----------------------------------------\n'
              f'Starting, with a WAITER.'
              f'\n----------------------------------------\n')
        philosophers: list[Thread] = [
            Thread(philosopher_waiter, i, shared) for i in range(NUM_PHILOSOPHERS)
        ]
    elif VARIANT == 1:
        global leftie
        print(f'----------------------------------------\n'
              f'Starting, with LEFT HANDED philosopher {leftie}.'
              f'\n----------------------------------------\n')
        philosophers: list[Thread] = [
            Thread(philosopher_leftie, i, shared) for i in range(NUM_PHILOSOPHERS)
        ]
    else:
        print(f'----------------------------------------\n'
              f'Starting, with TOKEN.'
              f'\n----------------------------------------\n')
        philosophers: list[Thread] = [
            Thread(philosopher_token, i, shared) for i in range(NUM_PHILOSOPHERS)
        ]

    for p in philosophers:
        p.join()

    print_hunger(shared)


if __name__ == "__main__":
    main()
