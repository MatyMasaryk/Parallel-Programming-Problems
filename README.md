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
philosopher function. Threads represent  each philosopher dining at the table. Implementation of Thread is taken from
the **fei.ppds** library.

### The philosopher functions
Philosopher functions (`philosopher_waiter`, `philosopher_leftie` and `philosopher_token`) implement the behavior of a
philosopher. Philosopher first thinks by calling the function `think`. Then they try to take right and left forks.
This is done by calling *shared.forks[\<number\>].lock()* and locking first the fork on their right, and then on their
left side. When philosopher has both forks in hand, he eats by calling `eat` and in our case also calculates hunger
by calling `calc_hunger`. Lastly, philosophers lets go of both forks by unlocking them with *shared.forks[\<number\>].lock()*.
This general behavior is then expanded upon in each variant.

### Function `philosopher_waiter`

Function `philosopher_waiter` implements behavior of a philosopher using the *waiter variant*.

#### Parameters:

    i -- philosopher id, integer
    shared -- object shared between threads, class Shared

#### Behavior:

Only NUM_PHILOSOPHERS - 1 number of philosophers is allowed to eat at any given moment. This is achieved by implementing
a "waiter", who is represented by a **Semaphore** object with initial value NUM_PHILOSOPHERS - 1. Waiter calls *wait()*
at the start and *signal()* at the end. After NUM_PHILOSOPHERS - 1 philosophers pass the *wait()* function, the last one
has to wait for another philosopher to pass *signal()*, only then can they continue.

### Function `philosopher_leftie`

Function `philosopher_leftie` implements behavior of a philosopher using the *leftie variant*.

#### Parameters:

    i -- philosopher id, integer
    shared -- object shared between threads, class Shared

#### Behavior:

One of the philosophers (chosen randomly) is "left-handed" or a "leftie". This is done by finding out which one is the
leftie every time a philosopher takes (line 162), or returns (174) forks. This special philosopher first takes the **left** fork
and then the **right** one. Others act normally. This prevents a deadlock where everyone would take the *right* fork at the
same time and no forks would be left to take.

### Function `philosopher_token`

Function `philosopher_token` implements behavior of a philosopher using the *token variant*.

#### Parameters:

    i -- philosopher id, integer
    shared -- object shared between threads, class Shared

#### Behavior:

Before lifting forks, philosopher looks at their neighbours. If they are eating, he waits. Otherwise he can eat.
This is done by implementing an array of boolean *shared.eating*. Philosopher waits while neighbours are eating 
(line 196). After that, they change *shared.eating* on their number to **True** (line 201). This means they are eating.
After they are finished and return both forks, they set *shared.eating* on their number back to **False** (line 216).

### Other functions

These functions are used to print information about changing states throughout the program's runtime, and to simulate
the time it takes to perform the corresponding tasks. They use **print** from the **fei.ppds** library. And **sleep**
function from **time**, combined with random numbers in a set range.

#### Function `think`

Simulates time and prints info when philosopher is thinking.

#### Function `eat`

Simulates time and prints info when philosopher is eating.

#### Function `take_return`

Represents situation when philosopher takes or returns a fork.

#### Function `balk`

Represents situation when neighbouring philosopher is eating so this one must wait.

#### Function `calc_hunger`

Calculates current hunger and max hunger of philosopher. Uses an instance of `Shared` class to store both.
Each time a philosopher eats, their hunger becomes 0 and hunger of others is increased by one. Max hunger is overwritten
when a new high is reached. Body of this function is locked by a mutex lock to retain counter integrity.

#### Function `print_hunger`

Prints max hunger of philosophers at the end of experiment.

## Comparison

![waiter](https://github.com/MatyMasaryk/Masaryk_103043_feippds/blob/03/images/waiter.png)
![leftie](https://github.com/MatyMasaryk/Masaryk_103043_feippds/blob/03/images/leftie.png)
![token](https://github.com/MatyMasaryk/Masaryk_103043_feippds/blob/03/images/token.png)

We tried running all 3 variants with 1000 runs. We established that both leftie and token are better variants
than waiter, because they significantly lower the hunger of philosophers.

In the *waiter variant* the last philosopher (who doesn't eat) is heavily disadvantaged by the **planner**. What often
happens is that last philosopher would finish waiting, but other philosopher already occupies the waiter again.
This could be mitigated a bit by making each philosopher sleep after calling *signal()* for the waiter.

In the *leftie variant* we see a big jump in effectivity. This is because no one is waiting for a waiter, everyone waits
**only** when their fork is locked.

In the *token variant* we see another improvement. This is due to the fact, that at each moment, 2
philosophers are **allowed** to eat, because neighbors of eating philosophers are locked and and therefore, no one is
taking each other's forks. This improves effectiveness and balance significantly.