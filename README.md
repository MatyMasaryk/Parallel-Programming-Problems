# Assignment 03: Dining Philosophers

The goal of the assignment is to implement a solution to the **Dining Philosophers Problem**.

## Usage

The program is used by running the `main` function. You can modify global constants to use different values:
    
    VARIANT: int (1-3) -- choose from 3 variants - 0: waiter // 1: leftie // 2: token
    NUM_PHILOSOPHERS: int -- number of philosophers at the table
    NUM_RUNS: int -- number of times the program runs

## Implementation

### Class `Shared`
The `Shared` class represents a shared object between all threads.
In its `init` function, we initialize **forks**: a list of Mutex objects representing forks used by philosophers,

**waiter**: a Semaphore object representing the waiter used in *waiter variant*,

**eating**: a list used to store info about which philosophers are currently eating, and

**mutex**: Mutex object used to lock **eating** list while its values are changing.

**eating** and **mutex** are used in the *token variant*.
Semaphore and Mutex implementations are taken from the **fei.ppds** library.


### Function `main`

In the `main` function we create NUM_PHILOSOPHERS number of threads and each runs the selected variant of the
philosopher function (`philosopher_waiter`, `philosopher_leftie`, or `philosopher_token`). Threads represent
each philosopher dining at the table. Implementation of Thread is taken from the **fei.ppds** library.

### Function `philosopher_waiter`

Function `philosopher_waiter` implements behavior of a philosopher using the *waiter variant*.

#### Parameters:

    i -- philosopher id, integer
    shared -- object shared between threads, class Shared

#### Behavior:

TODO: behavior waiter

### Function `philosopher_leftie`

Function `philosopher_leftie` implements behavior of a philosopher using the *leftie variant*.

#### Parameters:

    i -- philosopher id, integer
    shared -- object shared between threads, class Shared

#### Behavior:

TODO: behavior leftie

### Function `philosopher_token`

Function `philosopher_token` implements behavior of a philosopher using the *token variant*.

#### Parameters:

    i -- philosopher id, integer
    shared -- object shared between threads, class Shared

#### Behavior:

TODO: behavior token

### Other functions

These functions are used to print information about changing states throughout the program's runtime, and to simulate
the time it takes to perform the corresponding tasks. They use **print** from the **fei.ppds** library. And **sleep**
function from **time**, combined with random numbers in a set range.

#### Function `think`

Simulates time and prints info when philosopher thinks.

#### Function `eat`

Simulates time and prints info when philosopher thinks.

#### Function `take_return`

Represents situation when philosopher takes or returns a fork.

#### Function `balk`

Represents situation when neighbouring philosopher is eating so this one must wait.

## Comparison

TODO: vs.
