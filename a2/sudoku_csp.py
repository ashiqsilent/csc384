# Name: Md Ashiqur Rahman
# Student Number: 998419242

from cspbase import *
import math, itertools

def enforce_gac(constraint_list):
    '''Input a list of constraint objects, each representing a constraint, then 
       enforce GAC on them pruning values from the variables in the scope of
       these constraints. Return False if a DWO is detected. Otherwise, return True. 
       The pruned values will be removed from the variable object cur_domain. 
       enforce_gac modifies the variable objects that are in the scope of
       the constraints passed to it.'''

#<<<your implemenation of enforce_gac below
    pruned = False
    for c in constraint_list:
        for var in c.scope:
            for val in var.cur_domain():
                if not c.has_support(var, val):
                    var.prune_value(val)
                    pruned = True
                    if var.cur_domain() == []:
                        # DWO found
                        return False
    # This means the solution is still incomplete so run enforce_gac again
    if pruned:    
        return enforce_gac(constraint_list)
    return True
                    
        
#>>>your implemenation of enforce_gac above

                            
def sudoku_enforce_gac_model_1(initial_sudoku_board):
    '''The input board is specified as a list of 9 lists. Each of the
       9 lists represents a row of the board. If a 0 is in the list it
       represents an empty cell. Otherwise if a number between 1--9 is
       in the list then this represents a pre-set board
       position. E.g., the board
    
       -------------------  
       | | |2| |9| | |6| |
       | |4| | | |1| | |8|
       | |7| |4|2| | | |3|
       |5| | | | | |3| | |
       | | |1| |6| |5| | |
       | | |3| | | | | |6|
       |1| | | |5|7| |4| |
       |6| | |9| | | |2| |
       | |2| | |8| |1| | |
       -------------------
       would be represented by the list of lists
       
       [[0,0,2,0,9,0,0,6,0],
       [0,4,0,0,0,1,0,0,8],
       [0,7,0,4,2,0,0,0,3],
       [5,0,0,0,0,0,3,0,0],
       [0,0,1,0,6,0,5,0,0],
       [0,0,3,0,0,0,0,0,6],
       [1,0,0,0,5,7,0,4,0],
       [6,0,0,9,0,0,0,2,0],
       [0,2,0,0,8,0,1,0,0]]
       
       
       In model_1 you should create a variable for each cell of the
       board, with domain equal to {1-9} if the board has a 0 at that
       position, and domain equal {i} if the board has a fixed number i
       at that cell. 
       
       Model_1 should create BINARY CONSTRAINTS OF NOT-EQUAL between all
       relevant variables (e.g., all pairs of variables in the same
       row), then invoke enforce_gac on those constraints. All of the
       constraints of Model_1 MUST BE binary constraints (i.e.,
       constraints whose scope includes two and only two variables).
       
       This function outputs the GAC consistent domains after
       enforce_gac has been run. The output is a list with the same
       layout as the input list: a list of nine lists each
       representing a row of the board. However, now the numbers in
       the positions of the input list are to be replaced by LISTS
       which are the corresponding cell's pruned domain (current
       domain) AFTER gac has been performed.
       
       For example, if GAC failed to prune any values the output from
       the above input would result in an output would be: NOTE I HAVE
       PADDED OUT ALL OF THE LISTS WITH BLANKS SO THAT THEY LINE UP IN
       TO COLUMNS. Python would not output this list of list in this
       format.
       
       
       [[[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                2],[1,2,3,4,5,6,7,8,9],[                9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                6],[1,2,3,4,5,6,7,8,9]],
       [[1,2,3,4,5,6,7,8,9],[                4],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                1],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                8]],
       [[1,2,3,4,5,6,7,8,9],[                7],[1,2,3,4,5,6,7,8,9],[                4],[                2],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                3]],
       [[                5],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                3],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9]],
       [[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                1],[1,2,3,4,5,6,7,8,9],[                6],[1,2,3,4,5,6,7,8,9],[                5],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9]],
       [[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                3],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                6]],
       [[                1],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                5],[                7],[1,2,3,4,5,6,7,8,9],[                4],[1,2,3,4,5,6,7,8,9]],
       [[                6],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                2],[1,2,3,4,5,6,7,8,9]],
       [[1,2,3,4,5,6,7,8,9],[                2],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                8],[1,2,3,4,5,6,7,8,9],[                1],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9]]]
       
       Of course, GAC would prune some variable domains so this would
       not be the outputted list.

    '''

#<<<your implemenation of model_1  below
    # 9X9 square matrix representing the board
    variables = create_variables(initial_sudoku_board)
    constraints = create_binary_constraints(variables)
    if not enforce_gac(constraints):
        print "unsolvable sudoku"
    return show_solution(variables)
#>>>your implemenation of model_1 above

##############################

def sudoku_enforce_gac_model_2(initial_sudoku_board):
    '''This function takes the same input format (a list of 9 lists
    specifying the board, and generates the same format output as
    sudoku_enforce_gac_model_1.
    
    The variables of model_2 are the same as for model_1: a variable
    for each cell of the board, with domain equal to {1-9} if the
    board has a 0 at that position, and domain equal {i} if the board
    has a fixed number i at that cell.

    However, model_2 has different constraints. In particular, instead
    of binary non-equals constaints model_2 has 27 all-different
    constraints: all-different constraints for the variables in each
    of the 9 rows, 9 columns, and 9 sub-squares. Each of these
    constraints is over 9-variables (some of these variables will have
    a single value in their domain). model_2 should create these
    all-different constraints between the relevant variables,
    invoke enforce_gac on those constraints, and then output the list of gac 
    consistent variable domains in the same format as for model_1.
    '''
     
    
#<<<your implemenation of model_2  below
    variables = create_variables(initial_sudoku_board)
    constraints = create_alldiff_constraints(variables, initial_sudoku_board)
    if not enforce_gac(constraints):
        print "unsolvable sudoku"
    return show_solution(variables)    
#>>>your implemenation of model_2 above

###################################################################################

def create_variables(board):
    '''Create 81 variable object each representing a cell in the sudoky board.
    Assume the board is 9X9'''
    # i is the row number and j is the column number of the variable
    i = 1
    # Return the variables in the same format as the parameter. So
    # variable matrix will also be 9X9 matrix
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

def create_binary_tuples(dom1, dom2):
    '''dom1 and dom2 are list of ints. Return all possible combinations
    of [v1, v2] s.t. v1 is in dom1 and v2 is in dom2 but v1 != v2.'''
    tuples = []
    for v1 in dom1:
        for v2 in dom2:
            if v1 != v2:
                tuples.append([v1,v2])
    return tuples

def extract_column(i, j, matrix):
    '''Return the column starting at matrix[i][j] as a list'''
    col = [matrix[i][j]]
    i += 1
    while i < 9:
        col.append(matrix[i][j])
        i += 1
    return col

def extract_sub_square(i,j,matrix):
    '''Return the sub_square starting at matrix[i][j] as a list'''
    sub_square = [matrix[i][j]]
    i += 1
    while i%3 != 0:
        col = j - j%3
        while (col%3 != 0) or (col <= j):
            if col != j:
                sub_square.append(matrix[i][col])
            col += 1
        i += 1
    return sub_square

def add_binary_constraints(variables):
    '''Variable is a one dimensional list of variable objects. Create 
    constraint between the first variable and each of the remaining variables
    and return them as a list'''
    constraints = []
    var1 = variables[0]
    i = 1
    while i < len(variables):
        var2 = variables[i]
        c = Constraint("C_{}{}".format(var1.name, var2.name), [var1, var2])
        c.add_satisfying_tuples(create_binary_tuples(c.scope[0].domain(), c.scope[1].domain()))
        constraints.append(c)
        i += 1
    return constraints

def create_binary_constraints(variables):
    '''Create all possible constraints between all the relevent pair of 
    variables and return them as one big list'''
    constraints = []
    for row in variables:
        for cell in row:
            # create the row constraints
            constraints += add_binary_constraints(row[row.index(cell):])
            # create the column constraints
            column = extract_column(variables.index(row), row.index(cell), variables)
            constraints += add_binary_constraints(column)
            # create the sub-square constraints
            sub_square = extract_sub_square(variables.index(row), row.index(cell), variables)
            constraints += add_binary_constraints(sub_square)
    return constraints

def show_solution(variables):
    '''Find the cur_domain of each variable in variables and return then in 
    the same format as variables'''
    solution = []
    for row in variables:
        row_solution = []
        for cell in row:
            row_solution.append(cell.cur_domain())
        solution.append(row_solution)
    return solution

################################################################################

def create_alldiff_constraints(variables, board):
    '''Create all 27 constraints as specified in model2 and return them as list'''
    constraints = []
    # create the row constraints
    i = 0
    for row in variables:
        c = Constraint("C_Row{}".format(i+1), row)
        c.add_satisfying_tuples(create_alldiff_tuples(board[i]))
        constraints.append(c)
        i += 1
    # create the column constraints
    columns = find_columns(variables)
    i = 1
    for col in columns:
        c = Constraint("C_Col{}".format(i), col)
        c.add_satisfying_tuples(create_alldiff_tuples(convert_var_to_num(col)))
        constraints.append(c)
        i += 1
    # create the column constraints
    i = 1
    sub_squares = find_sub_squares(variables)
    for ss in sub_squares:
        c = Constraint("C_SS{}".format(i), ss)
        c.add_satisfying_tuples(create_alldiff_tuples(convert_var_to_num(ss)))
        constraints.append(c)
        i += 1    
    
    return constraints

def create_alldiff_tuples(values):
    to_permute = []
    for num in range(1,10):
        if num not in values:
            to_permute.append(num)
    permutations = all_permutations(to_permute)
    tuples = []
    for perm in permutations:
        tup = values[:]
        for val in perm:
            tup[tup.index(0)] = val
        tuples.append(tup)
    return tuples

def all_permutations(to_permute):
    
    return itertools.permutations(to_permute)

def convert_var_to_num(variables):
    numbers = []
    for var in variables:
        dom = var.domain()
        if len(dom) == 1:
            numbers.append(dom[0])
        else:
            numbers.append(0)
    return numbers

def find_columns(matrix):
    columns = []
    j = 0
    while j < 9:
        columns.append(extract_column(0, j, matrix))
        j += 1
    return columns

def find_sub_squares(matrix):
    sub_squares = []
    i = 0
    while i < 9:
        j = 0
        while j < 9:
            sub_squares.append(find_sub_squares_helper(i, j, matrix))
            j += 3
        i += 3    
    return sub_squares
    
def find_sub_squares_helper(i, j, matrix):
    ss = []
    row = i
    while row%3 != 0 or row <= i:
        col = j
        while col%3 != 0 or col <= j:
            ss.append(matrix[row][col])
            col += 1
        row += 1
    return ss