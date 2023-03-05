"""
This module implements the "Sleeping Barber Problem",
utilizing the usage of mutex locks.

University: STU Slovak Technical University in Bratislava
Faculty: FEI Faculty of Electrical Engineering and Information Technology
Year: 2023
"""

__authors__ = "Maty Masaryk, Marián Šebeňa"
__email__ = "xmasarykm1@stuba.sk"
__license__ = "MIT"

from fei.ppds import Mutex, Thread
from time import sleep
from random import randint

CUSTOMERS_NUM = 5
ROOM_SIZE = 3


class Shared(object):

    def __init__(self):
        # TODO : Initialize patterns we need and variables
        self.mutex = Mutex()
        self.waiting_room = 0
        # self.customer = Rendezvous is implemented as ?
        # self.barber = Rendezvous is implemented as ?
        # self.customer_done = Rendezvous is implemented as ?
        # self.barber_done = Rendezvous is implemented as ?


def get_haircut(i):
    """
    Simulate time and print info when customer gets haircut.

    Parameters:
        i -- customer id, integer
    """
    print(f'Customer {i} is getting their hair cut...')
    sleep(1)


def cut_hair():
    """
    Simulate time and print info when barber cuts customer's hair.

    Parameters:
        i -- customer id, integer
    """
    print('Barber is now cutting hair...')
    sleep(1)


def balk(i):
    """
    Represents situation when waiting room is full and print info.

    Parameters:
        i -- customer id, integer
    """
    print(f'Customer {i} can\'t get in. Room full.')
    sleep(0.9)


def growing_hair(i):
    """
    Represents situation when customer wait after getting haircut.
    So hair is growing and customer is sleeping for some time.

    Parameters:
        i -- customer id, integer
    """
    print(f'Customer {i}\'s hair is slowly growing back...')
    sleep(15)


def customer(i, shared):
    # TODO: Function represents customers behaviour. Customer come to waiting if room is full sleep.
    # TODO: Wake up barber and waits for invitation from barber. Then gets new haircut.
    # TODO: After it both wait to complete their work. At the end waits to hair grow again

    while True:
        # TODO: Access to waiting room. Could customer enter or must wait? Be careful about counter integrity :)

        # TODO: Rendezvous 1
        get_haircut(i)
        # TODO: Rendezvous 2

        # TODO: Leave waiting room. Integrity again
        growing_hair(i)


def barber(shared):
    # TODO: Function barber represents barber. Barber is sleeping.
    # TODO: When customer come to get new hair wakes up barber.
    # TODO: Barber cuts customer hair and both wait to complete their work.

    while True:
        # TODO: Rendezvous 1
        cut_hair()
        # TODO: Rendezvous 2


def main():
    shared = Shared()
    customers = []

    for i in range(CUSTOMERS_NUM):
        customers.append(Thread(customer, i, shared))
    hair_stylist = Thread(barber, shared)

    for t in customers + [hair_stylist]:
        t.join()


if __name__ == "__main__":
    main()
