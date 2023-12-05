
# %% [markdown]
# # lab2 
# ## DES for the traffic light between a main road and a secondary road
# 
# The model has two simple parameters T_a  and T_b .
# The two parameters represent unit of time in seconds. The first parameter is the time latency to change the traffic lights from red to green once a car is found waiting in the queue. The second parameter T_b  is the time required for a car to cross the intersection. So once the lights change from red to green, the lights will stay green for an amount of time equals to T_b times the number of cars waiting. The model also assumes that once the lights change from red to green, all cars waiting pass through immediately and at the same time.
# 
# ## This project has two parts:
# 
# First, you need to complete the lines of code after //TODO. Indication on what to do on these lines is given into the code. Once you have correctly inserted the Python code on these lines. You can run the program and it will solve the “Evolution example” shown in the tutorial. In particular, the last event print should be a G2R event at time 115.
# 
# For the second part of this project, you will need to uncomment the lines in the second main. This section of the code will then add randomly an additional hundred cars into the queue event. Also, change the passage time T_b to 15 seconds. The question is at what time the last event is now taking place?

# %%
#your names and ids
#1)
#2)

# %%
from heapq import *
from numpy import random

# %%
### STATE ##########################################

class State:
    def __init__(self):
        self.green = False
        self.cars = 0
    def is_green(self):
        """
        True if the light is green
        """
        return self.green
    def add_car(self):
        """
        Adds a car in the queue
        """
        self.cars = self.cars + 1
    def purge_cars(self):
        """
        Empty waiting cars
        """
        self.cars = 0
    def waiting_cars(self):
        """
        Returns the number of car waiting
        """
        return self.cars
    def turn_green(self):
        """
        The light turns green
        """
        self.green = True
    def turn_red(self):
        """
        The light turns red
        """
        self.green = False
    def __str__(self):
        """
        Displays the status of the crossroads
        """
        return "Green light =" + str(self.green) + ", cars=" + str(self.cars)


# %%
### EVENTS ###########################################

Ta = 30 # Time latency to change the traffic lights from red to green once a car is found waiting in the queue
Tb = 15 # Passage time


# %%
class Event:
    def time(self):
        """
        Returns the time at which the event will be processed
        """
        return self.t
    def __str__(self):
        """
        Displays Event
        """
        return self.name + "(" + str( self.t ) + ")"
    def __lt__(self, other):
        """
        Compares the event with another sorted by processing order priority
        """
        return self.t < other.t

# %%
class CAR(Event):
    def __init__(self,time):
        self.t = time
        self.name = "CAR"
    def action(self,queue,state):
        if not state.is_green():
            #TODO On this line, change the state and add a car.
            state.add_car()
            if state.waiting_cars() == 1:
                #TODO On this line, insert into the queue a R2G event at the time (self.t + Ta)
                queue.insert(R2G(self.t + Ta))


# %%
class R2G(Event):
    def __init__(self,time):
        self.t = time
        self.name = "R2G"
    def action(self,queue,state):
        queue.insert( G2R( self.t + state.waiting_cars() * Tb ) )
        #TODO On this line, change the state and turn the light to green
        state.turn_green()
        state.purge_cars()
    

# %%
class G2R(Event):
    def __init__(self,time):
        self.t = time
        self.name = "G2R"
    def action(self,queue,state):
        #TODO On this line, change the state and turn the light to red
        state.turn_red()

# %%
### EVENT QUEUE ##############################################

class EventQueue:
    def __init__(self):
        self.q = []
    def notEmpty(self):
        """
        Returns true if the queue is not empty
        """
        return len(self.q) > 0
    def remaining(self):
        """
        Returns the number of events awaiting processing
        """
        return len(self.q)
    def insert(self, event):
        """ 
        Create a new event in the queue
        """
        heappush( self.q, event )
    def next(self):
        """
        Returns and removes from the queue the next event to be processed
        """
        return heappop( self.q )

# %%
### MAIN #####################################################

Q = EventQueue()

Q.insert( CAR(10) ) 
Q.insert( CAR(25) )
Q.insert( CAR(35) )
Q.insert( CAR(60) )
Q.insert( CAR(75) )


S = State()

# Processing events until the queue is Q is empty
while Q.notEmpty():
    e = Q.next()
    print( e )
    e.action(Q,S)

# %%

### second MAIN #####################################################

Q = EventQueue()

Q.insert( CAR(10) ) 
Q.insert( CAR(25) )
Q.insert( CAR(35) )
Q.insert( CAR(60) )
Q.insert( CAR(75) )

#TODO To answer the second part of this project, uncomment the following five lines  and change
# the passage time Tb to 15 seconds 
random.seed(1)
additionalNumCarInQueue=100
tRandom = 80
for i in range(1, additionalNumCarInQueue):
    tRandom = random.randint(tRandom+1, tRandom+10)
    Q.insert( CAR(tRandom) )  
    

S = State()

# Processing events until the queue is Q is empty
while Q.notEmpty():
    e = Q.next()
    print( e )
    e.action(Q,S)


# %%
 #The question is at what time the last event is now taking place?
 # your answer: 

# %% [markdown]
# # this part is related to requirement 2
# - use the same structure as in requirement 1 to simulate the post office example illustrated in the tutorial.
# - use the below main to test your requirement.
# - also make sure to claculate the total waiting time for all customers and the customer numbers so that you can print the last statement.
#     wait time for one customer = finish time - arrival time.
# - if the window close time arrives while the window is processing a customer , then it should complete the customer processsing  first then closes.
# 
# ## note: dont change the following code 

# %%
### MAIN #####################################################

Q = EventQueue()

Q.insert( CUSTOMER(0,2) ) #a customer arrives at t=0 , and requires 2 t to finish his processing.
Q.insert( CUSTOMER(1,1) ) 
Q.insert( CUSTOMER(1.1,3) ) 
Q.insert( WOPEN(2,5) )  # the window opens at 2 and closes after 5 t i.e closes at 7 or if it processes a customer then after the customer finishes.
Q.insert( CUSTOMER(2,1) ) 
Q.insert( CUSTOMER(3,1) ) 
Q.insert( WOPEN(10,5) ) 
    
S = State()

# Processing events until the queue is Q is empty
while Q.notEmpty():
    e = Q.next()
    print( e )
    e.action(Q,S)
print(S.total_wait / S.total_customers)


# %%



