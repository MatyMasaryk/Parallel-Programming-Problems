"""
This module implements the "Sleeping Barber Problem",
utilizing the usage of mutex locks and signaling (rendezvous).

University: STU Slovak Technical University in Bratislava
Faculty: FEI Faculty of Electrical Engineering and Information Technology
Year: 2023
"""

__authors__ = "Maty Masaryk, Marián Šebeňa"
__email__ = "xmasarykm1@stuba.sk"
__license__ = "MIT"

from fei.ppds import Mutex, Thread, Semaphore, print as print_t
from time import sleep
from random import randint

CUSTOMERS_NUM = 5  # change for a different number of customers
ROOM_SIZE = 3  # change for different room size
VERBOSE = 2  # change for more/less information printed 1-3


class Shared(object):
    """Object Shared for all threads"""

    def __init__(self):
        """
        Initialize shared Mutex object, customer and barber states
        and waiting room counter.
        """
        self.mutex = Mutex()
        self.waiting_room = 0
        self.customer = Semaphore(0)
        self.barber = Semaphore(0)
        self.customer_done = Semaphore(0)
        self.barber_done = Semaphore(0)


class Format:
    """Used for formatting printed output"""
    bold = '\033[1m'
    italic = '\x1B[3m'
    underline = '\033[4m'
    end = '\033[0m'


def get_haircut(i):
    """
    Simulate time and print info when customer gets haircut.

    Parameters:
        i -- customer id, integer
    """
    print_t(f'✂ CUSTOMER {Format.bold}{i}{Format.end} is getting '
            f'their {Format.underline}hair cut{Format.end}...')
    sleep(randint(5, 15) * 0.1)


def cut_hair():
    """
    Simulate time and print info when barber cuts customer's hair.

    Parameters:
        i -- customer id, integer
    """
    print_t(f'\n✂ BARBER is now {Format.underline}'
            f'cutting hair{Format.end}...\n')
    sleep(randint(5, 15) * 0.1)


def balk(i):
    """
    Represents situation when waiting room is full and print info.

    Parameters:
        i -- customer id, integer
    """
    print_t(f'✖ CUSTOMER {Format.bold}{i}{Format.end} can\'t get in. '
            f'{Format.underline}Room full{Format.end}.')
    sleep(randint(10, 30) * 0.1)


def growing_hair(i):
    """
    Represents situation when customer wait after getting haircut.
    So hair is growing and customer is sleeping for some time.

    Parameters:
        i -- customer id, integer
    """
    if VERBOSE >= 3:
        print_t(f'⌂ {Format.italic}Customer {i}\'s hair is slowly '
                f'growing back...{Format.end}')
    sleep(randint(50, 150) * 0.1)


def customer(i, shared):
    """
    Represents customer's behaviour.

    Customer comes to waiting room when room is not full.
    Wakes up barber and waits for invitation from barber.
    Then gets new haircut. Both sides wait for completion.
    In the end waits to grow their hair back.

    Parameters:
        i -- customer id, integer
        shared -- object shared between threads, class Shared
    """

    while True:
        # Wait for waiting room not to be full
        while shared.waiting_room >= ROOM_SIZE:
            balk(i)

        # Enter waiting room
        shared.mutex.lock()
        shared.waiting_room += 1
        print_t(f'➜ CUSTOMER {Format.bold}{i}{Format.end} '
                f'{Format.underline}entered{Format.end} the waiting room')
        shared.mutex.unlock()

        # Rendezvous: wake up barber
        shared.barber.signal()
        shared.customer.wait()

        get_haircut(i)

        # Rendezvous: wait for barber to finish and also finish
        shared.barber_done.wait()
        shared.customer_done.signal()

        # Leave waiting room
        shared.mutex.lock()
        shared.waiting_room -= 1
        if VERBOSE >= 2:
            print_t(f'↩ CUSTOMER {Format.bold}{i}{Format.end} '
                    f'{Format.underline}left{Format.end} the barber shop,'
                    f' {shared.waiting_room} customer(s) in waiting room')
        shared.mutex.unlock()

        growing_hair(i)


def barber(shared):
    """
    Represents barber's behaviour.

    Barber is sleeping. When customer comes to get a haircut, they wake up
    the barber. Barber cuts customer's hair and both sides wait for completion.

    Parameters:
        shared -- object shared between threads, class Shared
    """

    while True:
        # Rendezvous: wait to be woken up and take in a customer
        shared.barber.wait()
        shared.customer.signal()

        cut_hair()
        # Rendezvous: finish the work and wait for customer finish as well
        shared.barber_done.signal()
        shared.customer_done.wait()


def main():
    """
    Main function, creates N customers
    who endlessly enter a barber shop run by one barber.
    """
    shared = Shared()
    customers = []

    for i in range(CUSTOMERS_NUM):
        customers.append(Thread(customer, i, shared))
    hair_stylist = Thread(barber, shared)

    for t in customers + [hair_stylist]:
        t.join()


if __name__ == "__main__":
    main()
