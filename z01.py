"""
This module contains an implementation of the Bakery Algorithm.

It assures mutual exclusion of N threads.
"""

__author__ = "Maty Masaryk, Tomáš Vavro"
__email__ = "xmasarykm1@stuba.sk"
__license__ = "MIT"

import numpy as np
from fei.ppds import Thread
from time import sleep

N_THREADS = 10  # change constant for a different number of threads

turn: np.ndarray[int] = np.zeros((N_THREADS,), dtype=int)
doorway: np.ndarray[bool] = np.zeros((N_THREADS,), dtype=bool)


def process(thread_id: int):
    """
    Simulates a process that is run by each thread.

    Mutual exclusion is achieved using the Bakery Algorithm.

    Parameters:
        thread_id -- unique thread identifier, integer
    """
    global turn, doorway
    i: int = thread_id

    # Lock process
    doorway[i] = True  # true while thread is changing its turn
    turn[i] = 1 + max(turn)
    doorway[i] = False
    for j in range(N_THREADS):
        while doorway[j]:
            continue
        while turn[j] != 0 \
                and (turn[j] < turn[i] or (turn[j] == turn[i] and j < i)):
            continue

    # Critical section
    print(f"Process {thread_id} runs a complicated computation!")
    sleep(0.2)

    # Unlock process
    turn[i] = 0


if __name__ == '__main__':
    print(__doc__)
    threads = [Thread(process, i) for i in range(N_THREADS)]
    [t.join() for t in threads]
