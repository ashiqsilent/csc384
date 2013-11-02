# Name : Md Ashiqur Rahman
# Student Number : 998419242

#Look for <<<...>>> tags in this file. These tags indicate changes in the 
#file to implement the required routines. Some mods have been made some others
#you have to make. Don't miss addressing each <<<...>>> tag in the file!


'''
8-Puzzle STATESPACE 

State Space Representation: 
<<<8-Puzzle: 
Give a brief description of the state
space representation you have choosen in your implementation
>>>8-Puzzle:

'''
from search import *

class eightPuzzle(StateSpace):

    StateSpace.n = 0
    
    def __init__(self, action, gval, state, parent = None):
        """state is supplied as a list of 9 numbers in the range [0-8]
           generate an eightPuzzle state. Create an eightPuzzle state
           object.
        
           The 9 numbers in state specify the position of the tiles in the puzzle from the
           top left corner, row by row, to the bottom right corner. E.g.:

           [2, 4, 5, 0, 6, 7, 8, 1, 3] represents the puzzle configuration

           |-----------|
           | 2 | 4 | 5 |
           |-----------|
           |   | 6 | 7 |
           |-----------|
           | 8 | 1 | 3 |
           |-----------|
           
           """

        StateSpace.__init__(self, action, gval, parent)
#<<<8-Puzzle: build your state representation from the passed data below
        self.state = state
#>>>8-Puzzle: build your state representation from the passed data above

    def successors(self) :
        """Implement the actions of the 8-puzzle search space."""
#<<<8-Puzzle: Your successor state function code below
#   IMPORTANT. The list of successor states returned must be in the ORDER
#   Move blank down move, move blank up, move blank right, move blank left
#   (with some successors perhaps missing if they are not available
#   moves from the current state, but the remaining ones in this  
#   order!)

#>>>8-Puzzle: Your successor state function code above
        States = []
        i = self.state.index(0)
        # check for down
        if i + 3 < 9:
            new_state = self.state[0:i] + [self.state[i+3]] + self.state[i+1:i+3] + [self.state[i]] + self.state[i+4:]
            States.append(eightPuzzle('Move blank down', self.gval+1, new_state, self))
        # check for up
        if i - 3 > -1:
            new_state = self.state[0:i-3] + [self.state[i]] + self.state[i-2:i] + [self.state[i-3]] + self.state[i+1:]
            States.append(eightPuzzle('Move blank up', self.gval+1, new_state, self))
        # check for right:
        if (i % 3) + 1 < 3:
            new_state = self.state[0:i] + [self.state[i+1]] + [self.state[i]] + self.state[i+2:]
            States.append(eightPuzzle('Move blank right', self.gval+1, new_state, self))
        # check for left
        if (i % 3) - 1 > -1:
            new_state = self.state[0:i-1] + [self.state[i]] + [self.state[i-1]] + self.state[i+1:]
            States.append(eightPuzzle('Move blank left', self.gval+1, new_state, self))
        return States
    
    def hashable_state(self) :
#<<<8-Puzzle: your hashable_state implementation below
        return tuple(self.state)
#>>>8-Puzzle: your hashable_state implementation above

    def print_state(self):
        if self.parent:
            print "Action= \"{}\", S{}, g-value = {}, (From S{})".format(self.action, self.index, self.gval, self.parent.index)
        else:
            print "Action= \"{}\", S{}, g-value = {}, (Initial State)".format(self.action, self.index, self.gval)

#<<<8-Puzzle: print the state in an informative way below


#>>>8-Puzzle: print the state in an informative way above



#<<<8-Puzzle: below you will place your implementation of the misplaced 
#tiles heuristic and the manhattan distance heuristic
#You can alter any of the routines below to aid in your implementation. 
#However, mark all changes between 
#<<<8-Puzzle ... and >>>8-Puzzle tags.
#>>>8-Puzzle

eightPuzzle.goal_state = False

def eightPuzzle_set_goal(state):
    '''set the goal state to be state. Here state is a list of 9
       numbers in the same format as eightPuzzle.___init___'''
    eightPuzzle.goal_state = state
#<<<8-Puzzle: store additional information if wanted below

#>>>8-Puzzle: store additional information if wanted above

def eightPuzzle_goal_fn(state):
#Assume that the goal is a fully specified state.
#<<<8-Puzzle: your implementation of the goal test function below
    return state.state == eightPuzzle.goal_state
#>>>8-Puzzle: your implementation of the goal test function above

def h0(state):
    #a null heuristic (always returns zero)
    return 0

def h_misplacedTiles(state):
    #return a heurstic function that given as state returns the number of
    #tiles (NOT INCLUDING THE BLANK!) in that state that are
    #not in their goal position 

#<<<8-Puzzle: your implementation of this function below
    misplaced_tiles = 0
    for i in range(0,9):
        if (state.state[i] != eightPuzzle.goal_state[i] and state.state[i] != 0):
            misplaced_tiles += 1
    return misplaced_tiles
#>>>8-Puzzle: your implementation of this function above
    
def h_MHDist(state):
    #return a heurstic function that given as state returns 
    #the sum of the manhattan distances each tile (NOT INCLUDING
    #THE BLANK) is from its goal configuration. 
    #The manhattan distance of a tile that is currently in row i column j
    #and that has to be in row i" j" in the goal is defined to be
    #  abs(i - i") + abs(j - j")
#<<<8-Puzzle: your implementation of this function below
    index_to_cordinate = [[1,1], [1,2], [1,3], [2,1], [2,2], [2,3], [3,1], [3,2], [3,3]]
    distance = 0
    for i in range(0,9):
        index_actual = eightPuzzle.goal_state.index(state.state[i])
        if (index_actual != i and state.state[i] != 0):
            distance += abs(index_to_cordinate[i][0] - index_to_cordinate[index_actual][0]) + abs(index_to_cordinate[i][1] - index_to_cordinate[index_actual][1])
    return distance
#>>>8-Puzzle: your implementation of this function above


#<<<8-Puzzle: Make sure the sample code below works when it is uncommented

#se = SearchEngine('astar', 'none')
#s0 = eightPuzzle("START", 0, [1, 0, 2, 3, 4, 5, 6, 7, 8])
#eightPuzzle_set_goal([0, 1, 2, 3, 4, 5, 6, 7, 8])
#se.trace_on(1)
#print '1'
#se.search(s0, eightPuzzle_goal_fn, h0)

#print '2'
#se.search(s0, eightPuzzle_goal_fn, h_misplacedTiles)

#print '3'
#s1 = eightPuzzle("START", 0, [8, 7, 6, 0, 4, 1, 2, 5, 3])
#se.search(s1, eightPuzzle_goal_fn, h_MHDist)

#print '4'
#se.set_strategy('astar', 'full')
#se.search(s1, eightPuzzle_goal_fn, h_MHDist)

## Note that this problem can take a long time...30 seconds of CPU on my mac-mini.
#print '5'
#se.search(s1, eightPuzzle_goal_fn, h_misplacedTiles)


#>>>8-Puzzle: Make sure the sample code above works when it is uncommented


