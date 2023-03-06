# Assignment 02: Barber shop

The goal of the assignment is to implement a solution to the **Sleeping Barber Problem**.

## Usage

The program is used by running the `main` function. You can modify global constants to use different values:
    
    CUSTOMERS_NUM: uint -- number of customers coming to barber shop
    ROOM_SIZE: uint -- room size (maximum number of customers in waiting room)
    VERBOSE: int (1-3) -- more/less information printed

## Implementation

### Structure `Shared`
The `Shared` class represents a shared object between all threads.
In its `init` function, we initialize a shared **Mutex** object, customer and barber states and waiting room counter.
Customer and barber states are represented by a **Semaphore** object. Both Semaphore and Mutex implementations are taken
from the **fei.ppds** library.

### Structure `Format`
The `Format` structure is used purely to introduce simple text formatting like **bold**, *italic* and
<ins>underlined</ins> to printed output. This is to make it more comprehensible.

### Function `main`

In the `main` function we create CUSTOMERS_NUM number of threads and each runs the `customer` function. These represent
each customer coming into the barber shop. We also create one thread with function `barber`, representing the barber
who runs the shop. The implementation of Thread is taken from the **fei.ppds** library.

### Function `customer`

Function `customer` implements behavior of a customer coming to the barber shop.

#### Parameters:

    i -- customer id, integer
    shared -- object shared between threads, class Shared

#### Behavior:

First, customer waits until waiting room is not full. This is done by checking the **shared.waiting_room** counter
against the ROOM_SIZE constant and calling the `balk` function (line 114).

When the room is no longer full, customer enters the waiting room. They increase the **shared.waiting_room** counter
(line 118) and print a message. This piece of code is protected by a *mutex lock* to maintain counter integrity.

Once in waiting room they wake up the barber using **signal** function from the Semaphore object. They wait for a
response from barber (using **wait** function from Semaphore). This was the first *rendezvous*.

After receiving the response from barber, they call the `get_haircut` function (line 127) and continue onto the
second rendezvous.

In the second rendezvous, the customer **wait**s for barber to finish work. After they receive the response, they
**signal** the barber that they are also done.

After the haircut, customer leaves the waiting room by decreasing the **shared.waiting_room** counter (line 135), again
protected by a *mutex lock*.

In the end, customer calls function `growing hair` and then repeats the whole process again infinitely.

### Function `barber`

Function `barber` implements behavior of a barber running the barber shop.

#### Parameters:

    shared -- object shared between threads, class Shared

#### Behavior:

Function consists mainly of the two rendezvouses with the customer.

In the first rendezvous, barber is sleeping (**wait**ing for a customer). Once they receive a signal, they **signal**
the customer.

They call the `cut_hair` function (line 161) and continue to the second rendezvous.

When they are done cutting customer's hair, they **signal** it, **wait** for response from customer and after that,
barber's job is done, and they fall asleep again (and repeat the process infinitely).

### Other functions

These functions are used to print information about changing states throughout the program's runtime, and to simulate
the time it takes to perform the corresponding tasks. They use **print** from the **fei.ppds** library. And **sleep**
function from **time**, combined with random numbers in a set range. The prints also use the `Format` class and
unicode symbols to make the output more comprehensible (and fun).

#### Function `get_haircut`

Simulates time and prints info when customer gets haircut.

#### Function `cut_hair`

Simulates time and prints info when barber cuts customer's hair.

#### Function `balk`

Represents situation when waiting room is full and print info.

#### Function `growing_hair`

Represents situation when customer waits after getting a haircut.
