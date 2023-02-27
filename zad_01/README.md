# Assignment 01: Bakery Algorithm

The goal of the assignment is to implement the **Bakery Algorithm**.

## Usage

The program is used by running the `main` function. Number of threads the process will run on can by changed by
modifying the *N_THREADS* constant.

## Implementation

### Global variables

The implementation uses 2 global variables:

    turn: array[integer]    -- array of numbers representing turns at which treads should run the critical section
                            -- default values: 0
                            
    doorway: array[boolean] -- true if thread is currently changing its turn
                            -- default values: false

### Function `main`

In the `main` function we create **N** threads and each thread the `process` function. The implementation of a thread
is taken from the **fei.ppds** library.

### Function `process`

The `process` function simulates a process that is run by each thread.

Mutual exclusion is achieved using the Bakery Algorithm.

Parameters:

    thread_id -- unique thread identifier, integer
    
## Theory

### Bakery Algorithm

Lamport's Bakery Algorithm was developed by computer scientist and mathematician Leslie B. Lamport. Its purpose is to
improve safety of shared resources accessed by multiple **threads**, using the concept of
**mutual exclusion** [[1]](#1).

The algorithm can be divided into three parts:

***Lock:*** Thread increases its turn number and then waits to access the critical section,
while other threads are currently in the critical section, or have lower turn numbers.

***Critical section:*** The thread with the lowest turn number is allowed entry to the critical section. Only one
thread at a time has access.

***Unlock:*** Unlock the thread by setting its turn number to 0. 

### Mutual exclusion
Mutual exclusion is used to prevent **race conditions**. In principle it disallows multiple **threads** to enter the
**critical section** at the same time.

Bakery algorithm is a viable solution to this problem. Here's why:

1. **In the critical section, there's only one process running at any given time.**

    This is achieved by the usage of turn numbers, which increase with each incoming process. Only the process
    with the lowest non-zero turn number can enter the critical section. Other processes wait for their turn, until
    their turn number is the lowest. After a process exits the critical section, its unlocked by setting its turn
    number to 0, and now the second lowest non-zero number is free to enter the critical section.

2. **Process running outside of the critical section doesn't prevent other processes to enter it.**

    This is achieved by waiting for processes while they're changing turn numbers to ensure clarity in which process'
    turn it is. Also, every process is eventually guaranteed to have a turn.

3. **The decision about entry has to be made in finite time.**

    When the process with the lowest non-zero turn number reaches the end of ***lock*** (it has compared itself to all
    other processes), it will always be allowed entry.

4. **When entering the critical section, processes can't assume anything about mutual timing / planning.**
    
    A process doesn't assume anything of this sort, because its entrance is predetermined by its turn number.
    


## References
<a id="1">[1] 
Lamport's bakery algorithm. In: Wikipedia: the free encyclopedia [online].
San Francisco (CA): Wikimedia Foundation, 2001- [cit. 2023-02-27].
Available at: https://en.wikipedia.org/wiki/Lamport%27s_bakery_algorithm
