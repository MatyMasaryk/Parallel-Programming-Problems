"""This module implements the Dining philosophers problem."""

__author__ = "Maty Masaryk, Tomáš Vavro"
__email__ = "xmasarykm1@stuba.sk"
__license__ = "MIT"

from fei.ppds import Thread, Mutex, print
from time import sleep

VARIANT: int = 1  # 0: waiter // 1: leftie // 2: token
NUM_PHILOSOPHERS: int = 5
NUM_RUNS: int = 4  # number of repetitions of think-eat cycle of philosophers


class Shared:
    """Represents shared data for all threads."""

    def __init__(self):
        """Initialize an instance of Shared."""
        self.forks = [Mutex() for _ in range(NUM_PHILOSOPHERS)]
        self.waiter = Mutex()


def think(i: int):
    """Simulate thinking.

    Args:
        i -- philosopher's id
    """
    print(f"Philosopher {i} is thinking!")
    sleep(0.1)


def eat(i: int):
    """Simulate eating.

    Args:
        i -- philosopher's id
    """
    print(f"Philosopher {i} is eating!")
    sleep(0.1)


def philosopher_waiter(i: int, shared: Shared):
    """Run philosopher's code, with a waiter.

    Args:
        i -- philosopher's id
        shared -- shared data
    """
    for _ in range(NUM_RUNS):
        shared.waiter.lock()
        think(i)
        # get forks
        shared.forks[i].lock()
        shared.forks[(i + 1) % NUM_PHILOSOPHERS].lock()
        eat(i)
        shared.forks[i].unlock()
        shared.forks[(i + 1) % NUM_PHILOSOPHERS].unlock()
        shared.waiter.unlock()


def philosopher_leftie(i: int, shared: Shared):
    """Run philosopher's code, with a leftie.

    Args:
        i -- philosopher's id
        shared -- shared data
    """
    for _ in range(NUM_RUNS):
        think(i)
        # get forks
        if i == 0:
            shared.forks[(i + 1) % NUM_PHILOSOPHERS].lock()
            shared.forks[i].lock()
        else:
            shared.forks[i].lock()
            shared.forks[(i + 1) % NUM_PHILOSOPHERS].lock()
        eat(i)
        if i == 0:
            shared.forks[(i + 1) % NUM_PHILOSOPHERS].unlock()
            shared.forks[i].unlock()
        else:
            shared.forks[i].unlock()
            shared.forks[(i + 1) % NUM_PHILOSOPHERS].unlock()


def philosopher_token(i: int, shared: Shared):
    """Run philosopher's code, using token .

    Args:
        i -- philosopher's id
        shared -- shared data
    """
    # TODO: token


def main():
    """Run main."""
    shared: Shared = Shared()
    if VARIANT == 0:
        philosophers: list[Thread] = [
            Thread(philosopher_waiter, i, shared) for i in range(NUM_PHILOSOPHERS)
        ]
    elif VARIANT == 1:
        philosophers: list[Thread] = [
            Thread(philosopher_leftie, i, shared) for i in range(NUM_PHILOSOPHERS)
        ]
    else:
        philosophers: list[Thread] = [
            Thread(philosopher_token, i, shared) for i in range(NUM_PHILOSOPHERS)
        ]

    for p in philosophers:
        p.join()


if __name__ == "__main__":
    main()
