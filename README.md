# Assignment 04: Feasting Savages

The goal of the assignment is to implement a solution to the **modified Dining Savages Problem**.

## Usage

The program is used by running the `main` function. You can modify global constants to use different values:
    
    POT_CAPACITY: int -- maximum number of servings in the pot
    NUM_SAVAGES: int -- number of savage threads
    NUM_COOKS: int -- number of cook threads

## Implementation

### Class `Shared`
The `Shared` class represents a shared object between all threads.

#### Function `init`
In its `init` function, we initialize:
 
***savage_mutex***: Mutex object used to only let one savage at a time take a serving,

***cook_mutex***: Mutex object used to only let one cook at a time cook a serving,

***servings***: servings counter (integer),

***fullPot***: Semaphore object representing a situation when pot is full,

***emptyPot***: Event object representing an event which start when savage finds out that the pot is empty,

***barrier***: an instance of the `Barrier` class.

The Semaphore, Mutex and Event implementations are taken from the **fei.ppds** library.

### Class `Barrier`
The `Barrier` class represents a reusable barrier synchronization pattern.

#### Function `init`
In its `init` function, we initialize:
 
***mutex***: Mutex object used to ensure integrity of *count*,

***count***: counter for savages arriving to the barrier (integer),

***turnstile1***: Semaphore object representing first turnstile,

***turnstile2***: Semaphore object representing second turnstile,

The Semaphore and Mutex implementations are taken from the **fei.ppds** library.

#### Functions `wait1` and `wait2`
In these 2 functions we implement the behavior of the barrier.

In `wait1`, we increase the ***count*** until all savages are present. The last savage signals to ***turnstile1***,
that it can let the savages through.

In `wait2`, we restore the barrier to a reusable state. This is done by decreasing ***count*** until it's zero. Last
signals to ***turnstile2***, that it can let the savages through and the barrier is ready for another use.

### Function `main`

In the `main` function we create NUM_SAVAGES number of threads representing savages and NUM_COOKS number of threads
representing cooks. Savage threads call the `savage` function, while cook threads call the `cook` function. 
Implementation of Thread is taken from the **fei.ppds** library.

### Function `savage`

Function `savage` implements behaviour of a savage.

#### Parameters:

    i -- savage id, integer
    shared -- object shared between threads, class Shared

#### Behavior:

First, uses Reusable barrier to wait for all savages to arrive. (line 128) 
When everyone is ready, one savage locks the ***savage_mutex***. They find out the number of servings in the pot. If pot is
empty, savage wakes up the cooks, by signalling the ***emptyPot*** event (line 138). Then waits for cooks to signal ***fullPot***.
When pot is not empty, savage takes a serving by calling the `get_serving_from_pot` function. After this, savage unlocks
the ***savage_mutex***, they are free to eat their serving (by calling `feast` function) and other savages are allowed 
to take their servings (again one at a time).

### Function `cook`

Function `cook` implements behaviour of a cook.

#### Parameters:

    i -- cook id, integer
    shared -- object shared between threads, class Shared

#### Behavior:

Cooks first locks the ***cook_mutex***, then waits until the pot is empty (savages signal the ***emptyPot*** event).
Cook prepares one serving by calling the `put_serving_in_pot` function. Then he unlocks the ***cook_mutex*** and
other cooks can enter and cook servings. They will be allowed to do so while the ***emptyPot*** event is active.
The cook that cooks the last serving signals to the savages that pot is now full (line 178). They clear the ***emptyPot***
event, which means cooks will now not try to cook, until the savages eat all the servings again.

### Other functions

These functions are used to print information about events happening throughout the program's runtime, and to simulate
the time it takes to perform the corresponding tasks. They use **print** from the **fei.ppds** library. And **sleep**
function from **time**, combined with random numbers in a set range.

#### Function `get_serving_from_pot`

Simulate savage taking a serving from the pot.

#### Function `feast`

Simulate savage feasting.

#### Function `put_serving_in_pot`

Simulate cook preparing a serving and putting it in the pot.

## Theory

### The modified Dining Savages Problem 
The modified Dining Savages Problem is a synchronization problem which can be defined as follows:

There's a tribe of savages who want to eat from a pot. They always start feasting at the same time. Last one to arrive
lets the others know the feast can start.

Savages take one serving at a time while the pot is not empty. If a savage finds out the pot is empty, he tells the
cooks to prepare food again. Savages wait until the cooks cook a full pot.

Cook always cooks one serving and puts it in the pot.

When the pot is full, savages continue feasting.

The whole process repeats infinitely.

### Used synchronization patterns

#### Barrier:
Used to wait for all threads.

Example: wait for all savages to arrive (wait1, wait2 = implementation, savage = usage).

    def wait1(self, i: int):
        self.mutex.lock()
        self.count += 1
        if self.count == NUM_SAVAGES:
            self.turnstile1.signal(NUM_SAVAGES)
        self.mutex.unlock()
        self.turnstile1.wait()
        print(f'Savage {i}: arrived to the feast')

    def wait2(self, i: int):
        self.mutex.lock()
        self.count -= 1
        if self.count == 0:
            print(f'Savage {i}: everyone is ready, feast can start\n')
            self.turnstile2.signal(NUM_SAVAGES)
        self.mutex.unlock()
        self.turnstile2.wait()
        
    def savage(i: int, shared: Shared):
        while True:
            shared.barrier.wait1(i)
            shared.barrier.wait2(i)
            ...
        
#### Mutex:
Used to ensure counter integrity and mutual exclusion.

Example: ***savage_mutex*** used in `savage` function to ensure integrity of ***servings*** and mutual exclusion of savages.
    
    def savage(i: int, shared: Shared):
        while True:
            ...
            shared.savage_mutex.lock()
            print(f'❓ Savage {i}: number of servings left in pot: '
                      f'{shared.servings}')
            if shared.servings == 0:
                ...
            ...
            # inside function get_serving_from_pot
                shared.servings += 1
            ...
            shared.savage_mutex.unlock()

#### Event:
Used to represent an event that is active after signalling.

Example: ***emptyPot*** event activated by savage. Lets cooks cook food until the ***emptyPot***.clear() call.

    def savage(i: int, shared: Shared):
        while True:
            ...
            if shared.servings == 0:
                print(f'Savage {i}: wakes up the cook\n')
                shared.emptyPot.signal()
                ...
            ...
        
    def cook(i: int, shared: Shared):
        while True:
            shared.cook_mutex.lock()
            shared.emptyPot.wait()
            ...
            if shared.servings >= POT_CAPACITY:
                ...
                shared.emptyPot.clear()
                shared.cook_mutex.unlock()
                continue
            ...

#### Rendezvous, Event and Semaphore:
Rendezvous: Two threads use signal and wait to exchange information.

Event: Used to represent an event that is active after signalling.

Semaphore: Uses wait and signal to direct thread flow.

Example: *emptyPot* **Event** activated by savage. Lets cooks cook food until the *emptyPot*.clear() call.
Savages wait for *fullPot* **Semaphore** signal which is given by a cook. This rendezvous has an extra step
(of calling clear()), due to the nature of Event.

    def savage(i: int, shared: Shared):
        while True:
            ...
            if shared.servings == 0:
                shared.emptyPot.signal()
                shared.fullPot.wait()
            ...
            
     def cook(i: int, shared: Shared):
        while True:
            ...
            shared.emptyPot.wait()
            ...
            if shared.servings >= POT_CAPACITY:
                shared.fullPot.signal()
                shared.emptyPot.clear()
                ...
            ...