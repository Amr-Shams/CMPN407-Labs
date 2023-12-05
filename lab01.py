from heapq import heappush, heappop
from numpy import random

currtime = 0
exp_term = -1
open_time = -1
curr_state = "Close"

class State:
    def __init__(self):
        self.window = "Close"
        self.total_customers = 0
        self.total_wait = 0
        self.waitings = []

    def get_window_state(self):
        return self.window

    def add_customer(self):
        self.total_customers += 1

    def remove_customer(self):
        self.total_customers -= 1

    def turn_open(self):
        self.window = "Open"

    def turn_close(self):
        self.window = "Close"

    def turn_busy(self):
        self.window = "Busy"

    def add_wait_time(self, amount):
        self.total_wait += amount
        self.waitings.append(amount)

    def __str__(self):
        return f"Window state is {self.window}, customers count = {self.total_customers}"

class Event:
    def time1(self):
        return self.time1

    def time2(self):
        return self.time2

    def __str__(self):
        return f"{self.name}({self.time1},{self.time2})"

    def __lt__(self, other):
        return self.time1 < other.time1

class CUSTOMER(Event):
    def __init__(self, time1, time2):
        self.time1 = time1
        self.time2 = time2
        self.__stime = -1
        self.__dtime = -1
        self.name = "Customer"

    def action(self, queue, state):
        global currtime
        global exp_term
        global open_time
        global curr_state

        state.add_customer()

        if state.get_window_state() == "Open":
            state.turn_busy()
            self.__stime = currtime
            self.__dtime = self.__stime + self.time2
            currtime = self.__dtime

            if self.__dtime >= open_time:
                state.turn_close()
                curr_state = "Close"
                queue.insert(WCLOSE(currtime, 0))
            else:
                state.turn_open()

            state.add_wait_time(self.__dtime - self.time1)

    def __str__(self):
        return f"{self.name}({self.time1},{self.time2 + currtime})"

class WOPEN(Event):
    def __init__(self, time1, time2):
        self.time1 = time1
        self.time2 = time2
        self.name = "WOPEN"

    def action(self, queue, state):
        global curr_state
        global currtime
        global open_time

        if state.get_window_state() == "Close":
            state.turn_open()
            exp_term = self.time2
            currtime = self.time1
            curr_state = "Open"
            open_time = self.time1 + self.time2

class WCLOSE(Event):
    def __init__(self, time1, time2):
        self.time1 = time1
        self.time2 = time2
        self.name = "WCLOSE"

    def action(self, queue, state):
        if state.get_window_state() == "Open":
            state.turn_close()

    def __str__(self):
        return f"{self.name}({self.time1})"

class WBUSY(Event):
    def __init__(self, time1, time2):
        self.time1 = time1
        self.time2 = time2
        self.name = "WBUSY"

    def action(self, queue, state):
        state.turn_busy()

class EventQueue:
    def __init__(self):
        self.customers = []
        self.windows = []

    def not_empty(self):
        return len(self.customers) > 0 or len(self.windows) > 0

    def remaining_customers(self):
        return len(self.customers)

    def remaining_windows(self):
        return len(self.windows)

    def insert(self, event):
        if event.name == "WCLOSE":
            self.windows.insert(0, event)
        else:
            if event.name == "Customer":
                heappush(self.customers, event)
            else:
                heappush(self.windows, event)

    def next(self):
        global curr_state
        global open_time

        if curr_state == "Close" and len(self.windows) > 0:
            return heappop(self.windows)
        elif len(self.customers) > 0:
            return heappop(self.customers)

Q = EventQueue()

Q.insert(CUSTOMER(0, 2))
Q.insert(CUSTOMER(4, 1))
Q.insert(CUSTOMER(1.1, 3))
Q.insert(WOPEN(2, 5))
Q.insert(CUSTOMER(2, 1))
Q.insert(CUSTOMER(3, 1))
Q.insert(WOPEN(10, 5))

S = State()

while Q.not_empty():
    e = Q.next()
    print(e)
    e.action(Q, S)

print(S.total_wait, S.total_customers, S.total_wait / S.total_customers)
print(S.waitings)
