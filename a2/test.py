from cspbase import *

def create_variables(board):
    i = 1
    variable_matrix = []
    for row in board:
        j = 1
        variable_row = []
        for cell in row:
            if cell == 0:
                variable_row.append(Variable("V{}{}".format(i, j), range(1,10)))
            else:
                variable_row.append(Variable("V{}{}".format(i, j), [cell]))
            j += 1
        variable_matrix.append(variable_row)
        i += 1
    return variable_matrix

def create_constraint(variables):
    constraint_list = []
    
    return constraint_list

board = [[0,0,2,0,9,0,0,6,0], [0,4,0,0,0,1,0,0,8], [0,7,0,4,2,0,0,0,3], [5,0,0,0,0,0,3,0,0], [0,0,1,0,6,0,5,0,0],  [0,0,3,0,0,0,0,0,6], [1,0,0,0,5,7,0,4,0], [6,0,0,9,0,0,0,2,0], [0,2,0,0,8,0,1,0,0]]

var = create_variables(board)
c = Constraint("C1", [var[0][0], var[0][1]])

c.add_satisfying_tuples([[], []])
c.add_satisfying_tuples([[2], []])
c.print_constraint_all()