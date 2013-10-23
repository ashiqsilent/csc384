# Name : Md Ashiqur Rahman
# Student Number : 998419242

#Look for <<<...>>> tags in this file. These tags indicate changes in the 
#file to implement the required routines. 

'''
bicycle STATESPACE 
'''
#<<<You may add only standard python imports---i.e., ones that are automatically
#   available on CDF.
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

from search import *
from math import *

#>>>


class bicycle(StateSpace):
    StateSpace.n = 0

    def __init__(self, action, gval, job_list, current_location, current_time, profit, job_done, parent=None): 
        """
        Initialize a bicycle search state object. Take as input the information
        you need to build a new state. 
        """
        #init the base class members.
        StateSpace.__init__(self, action, gval, parent)
        self.gval = gval
        self.job_list = job_list
        self.current_time = current_time
        self.profit = profit
        self.job_done = job_done
        self.current_location = current_location
    def successors(self) :
        """Implement the transitions of the bicycle search space"""

#<<<: Your successor state function code below
        States = []
        for job in self.job_list:
            new_job_list = self.job_list[0:]
            new_job_list.remove(job)
            location = job[3]
            time = self.current_time + journey_time(self.current_location, job[1])
            time = format_time(time)
            if time > job[2]:
                time += format_time(journey_time(job[1], job[3]))
                time = format_time(time)
            else:
                time = format_time(job[2] + journey_time(job[1], job[3]))
            if time > 19:
                continue
            profit = calculate_profit(job[4:], time)
            gval = job[4][1] - profit + self.gval
            States.append(bicycle("Complete " + job[0], gval, new_job_list, location, round(time, 2), profit, job[0], self))
        return States
#>>>: Your successor state function code above


    def hashable_state(self) :
        #Return a hashable data item representing the state. 
        #>>>Implement hashable_state

        #<<<: Your hashable_state code above
        print (self.current_location, self.current_time, self.profit, self.job_done, "gval={}, id={}, pid={}".format(self.gval, self.index, self.parent.index))

    def print_state(self):
    #>>> Implement a print state function. Output enough information
    #    so that you can trace the search during debugging.
        job_list = ""
        for job in self.job_list:
            job_list += str(job) + "\n"
        if self.parent:
            print "Action= \"{}\", S{}, g-value = {}, (From S{})\nTime: {}, Location: {}\nPending Jobs:\n{}".format(self.action, self.index, self.gval, self.parent.index, self.current_time, self.current_location, job_list.strip())
        else:
            print "Action= \"{}\", S{}, g-value = {}, (Initial State)\nTime: {}, Location: {}\nPending Jobs:\n{}".format(self.action, self.index, self.gval, self.current_time, self.current_location, job_list.strip())
    #<<<: Your print_state code above.
        
bicycle.map_list = []
bicycle.goal_state = False
bicycle.max_profit = 0

def h0(state):
    '''Null Heuristc'''
    return 0

#<<<: Implement an heuristic function. Use the name h1
def h1(state):
    '''Logisitics Heuristic 1'''
    profit = 0
    while state != None:
        profit += state.profit
        state = state.parent
    bicycle.max_profit = max(bicycle.max_profit, profit)
    return profit
#>>>

#<<<Implement these two functions which will define an interface to your
#   search space routines and allow us to automatically test your
#   implementation.

def bicycle_goal_fn(state):
    return state.job_list == [] and h1(state) >= bicycle.max_profit

def make_start_state(map, job_list):
    '''Input a map list and a job_list. Return a bicycle StateSpace object
       with action "START", gval = 0, and initial location "HOME" that represents the 
       starting configuration for the scheduling problem specified'''

# map:  is a list of two lists 
#
# [[location-names], [location-travel-time-pairs]]
#    location-names
#          is a list of strings specifying
#          the locations for the deliveries. Each location has a unique name.
#    location-travel-time-pairs
#          a list of location-travel-time-pair-items 
#        each location-travel-time-pair-item is
#           a list of three elements [location1, location2, traveltime]
#           where location1 and location2 are members of location-names
#           and travel time is a positive integer specifying the time 
#           it takes to go from location1 to location2 in minutes.
#           a. The travel time from location2 to location1 is the same
#              as the travel time from location1 to location2
#           b. The travel time from a location back to itself is zero
#    The location-travel-time-pairs along with rules (a) and (b) must
#    determine the travel time between every pair of locations in location-names
#
#   Example: 
#  map = [
#         ['locA', 'locB', 'locC', 'locD'],
#         [['locA', 'locB', 15], ['locA', 'locC', 25], ['locA', 'locD', 10], 
#          ['locB', 'locC', 10], ['locB', 'locD', 13], ['locC', 'locD', 20]]
#        ]
# 
#  job_list: a list of jobs
#    each job is a list of 5 or more items
#    1. a string that is the job name. Each job has a unique name.
#    2. Pickup location, a location from location-names
#    3. pickup time. A number in the format hh.mm (h=hour, m=minute)
#    4. Dropoff location, a location from location-names
#    5. A time-payoff pair
#    6,7,..: the job-list can contain an arbitrary number of time-payoff pairs.
#
#       time-payoff pair:
#       a list of two items, [time, payoff]
#       time is a number in the format hh.mm
#       payoff is an integer specifying the number of dollars paid. 
#    You may assume that each subsequent time-payoff pair in the job-list has
#      a higher time and a lower payoff. 
# 
# Example:
# job_list =
# [['Job1', 'locA', 8.00, 'locC', [8.30, 25], [9.30, 20], [10.00, 10], [11.00, 5]],
#  ['Job2', 'locB', 10.00, 'locC', [10.30, 25], [12.00, 5]],
#   ['Job3', 'locC', 9.00, 'locD', [9.05, 50], [9.30, 25], [10.00, 5]]
# ]
#
# See the assignment specification for more information about what these
# lists specify. 

    bicycle.map_list = map
    return bicycle("START", 0, job_list, "HOME", 0.0, 0, "none")

def solve(bicycle_start_state):
    '''Compute a delivery schedule given an initial bicycle search state that has been
       computed from make_start_state (above). Output the computed sequence of deliveries'''

# This function should invoke the search routines to find a solution to the delivery
# scheduling problem that executes all of the delivery jobs specified by the
# bicycle_start_state
# It should return a list of deliveries
# deliveries = [delivery1, delivery2, ... ]
# 
# each delivery is a list
# [job_name, initial_location, start_time, final_location, end_time, payment]
#  job_name: the job name from job_list
#  initial_location: your location when you started working on the job
#  start_time: the time when you started riding from initial_location to 
#              the job's pickup location
#  final_location: the delivery location of the job
#  end_time: the time when you delivered the job's package 
#  payment: the money earned for this job
#
# For example, the returned list of deliveries
# for the schedule given in the assignment specification would be
# [ ['Job1', 'home', 8.00, 'locC', 8.25, 25]
#   ['Job3', 'locC', 8.25, 'locD', 9.20, 25]
#   ['Job2', 'locD', 9.20, 'locC', 10:10, 25]
# ]
#
    se = SearchEngine("astar", "none")
    se.trace_off();
    s = se.search(bicycle_start_state, bicycle_goal_fn, h1)
    
    answer = []
    while s != None:
        part = [s.action, "time_completed="+str(s.current_time), "profit="+str(s.profit)]
        answer.append(part)
        s = s.parent
    answer.pop()
    answer.reverse()
    print answer
    
def journey_time(locA, locB):
    if locA == locB:
        return 0.0
    for loc in bicycle.map_list[1]:
        if(locA in loc) and (locB in loc):
            return loc[2] / 100.0
    return 0.0

def calculate_profit(job, time):
    for t in job:
        if time <= t[0]:
            return t[1]
    return 0

def format_time(time):
    
    minutes = time - floor(time)    
    if minutes > 0.59:
        return floor(time) + 1 + (minutes - 0.6)
    return time
        