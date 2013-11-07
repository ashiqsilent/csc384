from cspbase import *
from sudoku_csp import *
import math

def create_tuples(values):
    to_permute = []
    for num in range(1,10):
        if num not in values:
            to_permute.append(num)
    permutations = all_permutaions(to_permute)
    tuples = []
    for perm in permutations:
        tup = values[:]
        for val in perm:
            tup[tup.index(0)] = val
        tuples.append(tup)
    return tuples

def all_permutaions(l):
    queue = [l]
    result = [l]
    while queue and len(result) < math.factorial(len(l)):
        member = queue.pop(0)
        i = 0
        while i < len(member) - 1:
            j = i + 1
            while j < len(l):
                permute = member[0:i]+[member[j]] + member[i+1:j] + [member[i]] + member[j+1:]
                if permute not in result:
                    result.append(permute)
                    queue.append(permute)
                j += 1
            i += 1
    return result

def create_constraints(variables, board):
    

b1 = [[0,0,2,0,9,0,0,6,0], [0,4,0,0,0,1,0,0,8], [0,7,0,4,2,0,0,0,3], [5,0,0,0,0,0,3,0,0], [0,0,1,0,6,0,5,0,0],  [0,0,3,0,0,0,0,0,6], [1,0,0,0,5,7,0,4,0], [6,0,0,9,0,0,0,2,0], [0,2,0,0,8,0,1,0,0]]

v = create_variables(b1)
c.print_constraint_all()