# Name : Md Ashiqur Rahman
# Student Number : 998419242

'''Classes for variable elimination Routines 
   A) class Variable
      This class allows one to define Bayes Net variables.

      On initialization the variable object can be given a name and a
      domain of values. This list of domain values can be added to or
      deleted from in support of an incremental specification of the
      variable domain.

      The variable can be assigned a value. These assigned values are used
      by the factor class objects. It can also be given an evidence
      value. This is used when doing Variable Elimination. 


    B) class Factor

      This class allows one to define a factor specified by a table
      of values. 

      On initialization the variables the factor is over is
      specified. This must be a list of variables. This list of
      variables cannot be changed once the Factor object is
      created.

      Once created the factor can be incrementally initialized with a
      list of values which specify the factor's numeric value on 
      various assignments to the variables in its scope.
      There are two ways to set the factor's values.
      (a) a list of lists. Each list in this list specifies the
      value of each variable in the factor's scope followed by
      the numeric value for the factor on this sequence of variable
      values.

      (b) one can set the assigned value for every variable in the 
      factor's scope then add the number associated with that setting
      of its variables. 

      Getting the factor's values has two similar interfaces. 

      Initially, one creates a factor object for every conditional
      probability table (CPT) in the bayes-net. Then one initializes the
      factor with the specified values of these CPTs.


    C) class BN This class allows one to put factors and variables
       together to form a Bayes net.  It serves as a convenient place
       to store all of the factors and variables associated with a
       Bayes Net in one place.

    '''

class Variable:
    '''Class for defining Bayes Net variables. '''
    
    def __init__(self, name, domain=[]):
        '''Create a variable object, specifying its name (a
        string). Optionally specify the initial domain.
        '''
        self.name = name                #text name for variable
        self.dom = list(domain)         #Make a copy of passed domain
        self.evidence_index = 0         #evidence value (stored as index into self.dom)
        self.assignment_index = 0       #For use by factors. We can assign variables values
                                        #and these assigned values can be used by factors
                                        #to index into their tables.

    def add_domain_values(self, values):
        '''Add domain values to the domain. values should be a list.'''
        for val in values: self.dom.append(val)

    def value_index(self, value):
        '''Domain values need not be numbers, so return the index
           in the domain list of a variable value'''
        return self.dom.index(value)

    def domain_size(self):
        '''Return the size of the domain'''
        return(len(self.dom))

    def domain(self):
        '''return the variable domain'''
        return(list(self.dom))

    def set_evidence(self,val):
        '''set this variable's value when it operates as evidence'''
        self.evidence_index = self.value_index(val)

    def get_evidence(self):
        '''gets this variable's evidence vaalue'''
        return(self.dom[self.evidence_index])

    def set_assignment(self, val):
        '''Set this variable's assignment value for factor lookups'''
        self.assignment_index = self.value_index(val)

    def get_assignment(self):
        '''Get this variable's assignment value for factor lookups'''
        return(self.dom[self.assignment_index])

    ##These routines special low-level routines used directly by the
    ##factor objects
    def set_assignment_index(self, index):
        '''This routine is used by the factor objects'''
        self.assignment_index = index

    def get_assignment_index(self):
        '''This routine is used by the factor objects'''
        return(self.assignment_index)

    def __repr__(self):
        '''string to return when evaluating the object'''
        return("{}".format(self.name))
    
    def __str__(self):
        '''more elaborate string for printing'''
        return("{}, Dom = {}".format(self.name, self.dom))


class Factor: 
    '''Class for defining factors. A factor is a function that is over
    an ORDERED sequence of variables called its scope. It maps every
    assignment of values to these variables to a number. In a Bayes
    Net initially every CPT is represented as a factor. Pr(A|B,C) for
    example will be represented by a factor over the variables
    (A,B,C). If we assign A = a, B = b, and C = c, then the factor
    will map this assignment, A=a, B=b, C=c, to a number that is equal
    to Pr(A=a| B=b, C=c). During variable elimination, however, the
    factors we compute when variables are eliminated are no longer
    conditional probabilities. However, the factors still map
    assignments of values to the variables in their scope to numbers.

    Note that if the factor's scope is empty it is a constaint factor
    that stores only one value. add_values would be passed something
    like [[0.25]] to set the factor's single value the get_value
    functions will still work.  E.g., get_value([]) will return the
    factor's single value. Constant factors can be generated during
    variable elimination when a factor is restricted.'''

    def __init__(self, name, scope):
        '''create a Factor object, specify the Factor name (a string)
        and its scope (an ORDERED list of variable objects).'''
        self.scope = list(scope)
        self.name = name
        size = 1
        for v in scope:
            size = size * v.domain_size()
        self.values = [0]*size  #initialize values to be long list of zeros.

    def get_scope(self):
        return list(self.scope)

    def add_values(self, values):
        '''This routine can be used to initialize the factor. We pass
        it a list of lists. Each sublist is a ORDERED sequence of
        values, one for each variable in self.scope followed by a
        number that is the factor's value when its variables are
        assigned these values. For example, if self.scope = [A, B, C],
        and A.domain() = [1,2,3], B.domain() = ['a', 'b'], and
        C.domain() = ['heavy', 'light'], then we could pass add_values the
        following list of lists
        [[1, 'a', 'heavy', 0.25], [1, 'a', 'light', 1.90],
         [1, 'b', 'heavy', 0.50], [1, 'b', 'light', 0.80],
         [2, 'a', 'heavy', 0.75], [2, 'a', 'light', 0.45],
         [2, 'b', 'heavy', 0.99], [2, 'b', 'light', 2.25],
         [3, 'a', 'heavy', 0.90], [3, 'a', 'light', 0.111],
         [3, 'b', 'heavy', 0.01], [3, 'b', 'light', 0.1]]
         Note that these numbers need not be probabilities.

         This list initializes the factor so that, e.g., its value on
         (A=2,B=b,C='light) is 2.25'''

        for t in values:
            index = 0
            for v in self.scope:
                index = index * v.domain_size() + v.value_index(t[0])
                t = t[1:]
            self.values[index] = t[0]
         
    def add_value_at_current_assignment(self, number):
        '''This is a special purpose function for initializing a
        factor. We pass it only a single number. It then looks at the
        assigned values of the variables in its scope and initializes
        the factor to have that value on the current assignment of its
        variables. Hence, to use this function one first must set the
        assigned values of the variables in its scope.

        For example, if self.scope = [A, B, C], and A.domain() =
        [1,2,3], B.domain() = ['a', 'b'], and C.domain() = ['heavy',
        'light'], and we invoke A.set_assignment(1),
        B.set_assignment('a') and C.set_assignment('heavy'), then call
        this function with the value 0.33, we would have initialized
        this factor to have the value 0.33 on the assigments (A=1,
        B='1', C='heavy')'''

        index = 0
        for v in self.scope:
            index = index * v.domain_size() + v.get_assignment_index()
        self.values[index] = number

    def get_value(self, variable_values):
        '''This function is used to retrieve a value from the
        factor. We pass it an ordered list of values, one for every
        variable in self.scope. It then returns the factor's value on
        that set of assignments.  For example, if self.scope = [A, B,
        C], and A.domain() = [1,2,3], B.domain() = ['a', 'b'], and
        C.domain() = ['heavy', 'light'], and we invoke this function
        on the list [1, 'b', 'heavy'] we would get a return value
        equal to the value of this factor on the assignment (A=1,
        B='b', C='light')'''
        index = 0
        for v in self.scope:
            index = index * v.domain_size() + v.value_index(variable_values[0])
            variable_values = variable_values[1:]
        return self.values[index]

    def get_value_at_current_assignments(self):
        '''This function is used to retrieve a value from the
        factor. The value retrieved is the value of the factor when
        evaluated at the current assignment to the variables in its
        scope.

        For example, if self.scope = [A, B, C], and A.domain() =
        [1,2,3], B.domain() = ['a', 'b'], and C.domain() = ['heavy',
        'light'], and we had previously invoked A.set_assignment(1),
        B.set_assignment('a') and C.set_assignment('heavy'), then this
        function would return the value of the factor on the
        assigments (A=1, B='1', C='heavy')'''
        
        index = 0
        for v in self.scope:
            index = index * v.domain_size() + v.get_assignment_index()
        return self.values[index]

    def print_table(self):
        '''print the factor's table'''
        saved_values = []  #save and then restore the variable assigned values.
        for v in self.scope:
            saved_values.append(v.get_assignment_index())

        self.recursive_print_values(self.scope)

        for v in self.scope:
            v.set_assignment_index(saved_values[0])
            saved_values = saved_values[1:]
        
    def recursive_print_values(self, vars):
        if len(vars) == 0:
            print "[",
            for v in self.scope:
                print "{} = {},".format(v.name, v.get_assignment()),
            print "] = {}".format(self.get_value_at_current_assignments())
        else:
            for val in vars[0].domain():
                vars[0].set_assignment(val)
                self.recursive_print_values(vars[1:])

    def __repr__(self):
        return("{}({})".format(self.name, map(lambda x: x.name, self.scope)))

class BN:
    '''Class for defining a Bayes Net.'''
    def __init__(self, name, Vars, Factors):
        self.name = name
        self.Variables = list(Vars)
        self.Factors = list(Factors)
        for f in self.Factors:
            for v in f.get_scope():     
                if not v in self.Variables:
                    print "Bayes net initialization error"
                    print "Factor scope {} has variable {} that",
                    print " does not appear in list of variables {}.".format(map(lambda x: x.name, f.get_scope()), v.name, map(lambda x: x.name, Vars))

    def factors(self):
        '''Return a new list of the factors. So we don't modify BN'''
        return list(self.Factors)

    def variables(self):
        return list(self.Variables)


###########################################

def min_fill_ordering(Factors, QueryVar):
    '''Compute a min fill ordering given a list of factors. Return
    ordered list of variables from the scopes of the factors in
    Factors. The QueryVar will NOT be part of the returned ordering.
    The ordering is the min-fill ordering.'''
    scopes = []
    for f in Factors:
        scopes.append(list(f.get_scope()))
    Vars = []
    for s in scopes:
        for v in s:
            if not v in Vars and v != QueryVar:
                Vars.append(v)
    
    ordering = []
    while Vars:
        (var,new_scope) = min_fill_var(scopes,Vars)
        ordering.append(var)
        if var in Vars:
            Vars.remove(var)
        scopes = remove_var(var, new_scope, scopes)
    return ordering

def min_fill_var(scopes, Vars):
    '''Given a set of scopes (lists of lists of variables) compute and
    return the variable with minimum fill in. This is the variable that
    generates a factor of smallest scope when eliminated from the set
    of scopes. Also return the new scope generated from eliminating
    that variable.'''

    minv = Vars[0]
    (minfill,min_new_scope) = compute_fill(scopes,Vars[0])
    for v in Vars[1:]:
        (fill, new_scope) = compute_fill(scopes, v)
        if fill < minfill:
            minv = v
            minfill = fill
            min_new_scope = new_scope
    return (minv, min_new_scope)

def compute_fill(scopes, var):
    '''Return the fill in scope generated by eliminating var from
    scopes along with the size of this new scope'''
    union = []
    for s in scopes:
        if var in s:
            for v in s:
                if not v in union:
                    union.append(v)
    if var in union: union.remove(var)
    return (len(union), union)

def remove_var(var, new_scope, scopes):
    '''Return the new set of scopes that arise from eliminating var
    from scopes'''

    new_scopes = []
    for s in scopes:
        if not var in s:
            new_scopes.append(s)
    new_scopes.append(new_scope)
    return new_scopes
            

###########################################
def VE(Net, QueryVar, EvidenceVars, orderingFn):
    '''
    Input: Net---a BN object (a Bayes Net)
           QueryVar---a Variable object (the variable whose distribution
                      we want to compute)
           EvidenceVars---a LIST of Variable objects. Each of these
                          variables has had its evidence set to a particular
                          value from its domain using set_evidence. 
           orderingFn---a FUNCTION that whose prototype is identical to
                        min_fill_ordering, i.e.:
                        order = orderingFn(Factors, QueryVar)
                        where Factors is a list of factor objects, and
                        QueryVar is a variable.
                        This function is returns an ordered list 
                        of variables from the scopes of Factors (not
                        including QueryVar). VE will follow this
                        ordering when eliminating its variables. That is
                        VE will eliminate order[0] first then order[1] ...

                        NOTE you should first restrict the Net's factors
                        by the Evidence Variables (thus removing these
                        variables) before you compute an elimination 
                        ordering of the remaining variables.


   VE returns a distribution over the values of QueryVar, i.e., a list
   of numbers one for every value in QueryVar's domain. These numbers
   sum to one, and the i'th number is the probability that QueryVar is
   equal to its i'th value given the setting of the evidence
   variables. For example if QueryVar = A with Dom[A] = ['a', 'b',
   'c'], EvidenceVars = [B, C], and we have previously called
   B.set_evidence(1) and C.set_evidence('c'), then VE would return a
   list of three numbers. E.g. [0.5, 0.24, 0.26]. These numbers would
   mean that Pr(A='a'|B=1, C='c') = 0.5 Pr(A='a'|B=1, C='c') = 0.24
   Pr(A='a'|B=1, C='c') = 0.26
 
    '''

#<<<Your implementation below

    factors = Net.factors()
    order = Net.variables()
    # restrict factors by evidence variables
    restrict_factors(factors, EvidenceVars)
    # get the elimination order
    order = orderingFn(factors, QueryVar)
    for var in order:
        # get all the factors whose scope contains var
        factors_to_change = find_factors(factors, var)
        flag = False
        if len(factors_to_change) > 1:
            # join the factors first and then sum out the variables
            new_factor = join_factors(factors_to_change)
            if len(new_factor.get_scope()) > 1:
                new_factor = sum_out_factors(new_factor, var)
                flag = True
        
        elif len(factors_to_change) == 1:
            #only one factor. so just sum out variable
            if factors_to_change[0].get_scope() > 1:
                new_factor = sum_out_factors(factors_to_change[0], var)
                if (new_factor): # check if the scope is wiped out
                    flag = True                
        # Remove the factors that were changed
        [factors.remove(f) for f in factors_to_change]
        if (flag):
            # Add the new factor in factors
            factors.append(new_factor)
    # join the remaining factors
    if len(factors) > 1:
        factor = join_factors(factors)
    elif len(factors) == 1:
        factor = factors[0]
    else:
        # something wrong with my code above
        factor = []
    # safety guard
    if not factor:
        return [0.0, 0.0]
    # normalise the result
    alpha = sum(factor.values) * 1.0
    if (alpha  == 0):
        return [0.0, 0.0]
    return [val/alpha for val in factor.values]
#>>>Your implementation above

#Advice: Define a collection of helper functions for generating new factors
#        from old factors. You will need to at least provide the following
#        functionality: (a) generate a new factor by restricting an old 
#        factor by an evidence variable/value pair. (b) generate a new factor
#        by multipying out a list of old factors. (c) generate a new factor
#        by eliminating a variable from an old factor. With these function
#        VE is easy to write. Note it is important that these function do not
#        change the inputted factors. So a new factor object should be created
#        and initialized with *copies* of the old factor member items.
#
#        Further hint. Look carefully at add/get_value_at_current_assignment 
#        These routines provide a convenient way to index into a factor for
#        setting/getting its values at particular variable assignments.


##################restrict_factors#############################

def restrict_factors(factors, evidenceVars):
    '''Restrict all the factors in factors by the evidence in the evidenceVars. 
    Modify factors instead of returning it.'''    
    for f in factors:
        # determine whether f has any evidence variable. If yes, then get the 
        # evidence variable(s) present in f
        evidence = find_evidence(f.get_scope(), evidenceVars)
        if (evidence):
            new_factor = restrict_factors_helper(f, evidence)
            if (new_factor):
                factors[factors.index(f)] = new_factor
            else:
                factors.remove(f)
def restrict_factors_helper(factor, evidence):
    '''Return a new factor object by changing the given factor according to the 
    evidence'''      
    scope = factor.get_scope()
    name = factor.name
    for e in evidence:
        scope.remove(e)
        e.set_assignment(e.get_evidence())
        name = name.replace(repr(e), e.get_evidence())
    if (len(scope) == 0):
        return []
    new_factor = Factor(name, scope)
    recursive_restrict_variable(scope, new_factor, factor)
    return new_factor

def recursive_restrict_variable(variables, factor, old_factor):
    '''Recursively add values in factor fron old_factor. This is similar
    to Factor.recursive_print_values'''
    if len(variables) == 0:
        for v in factor.scope:
            factor.add_value_at_current_assignment(old_factor.get_value_at_current_assignments())
    else:
        for val in variables[0].domain():
            variables[0].set_assignment(val)
            recursive_restrict_variable(variables[1:], factor, old_factor)    

def find_evidence(variables, evidenceVars):
    '''Return the variables that are common in variables and evidenceVars'''
    result = []
    for e in evidenceVars:
        for var in variables:
            if e == var:
                result.append(e)
    return result

###################join factors##########################

def join_factors(factors):
    scope = []
    name = ""
    for f in factors:
        for v in f.get_scope():
            if v not in scope:
                name += v.name + ","
                scope.append(v)
    name = name.strip(",")
    name = "P({})".format(name)
    new_factor = Factor(name, scope)
    recursive_join_factors(scope, new_factor, factors)
    return new_factor

def recursive_join_factors(variables, factor, factors):
    if len(variables) == 0:
        for v in factor.scope:
            factor.add_value_at_current_assignment(product(factors))
    else:
        for val in variables[0].domain():
            variables[0].set_assignment(val)
            recursive_join_factors(variables[1:], factor, factors)      

def product(factors):
    result = 1
    for f in factors:
        result *= f.get_value_at_current_assignments()
    return result

##################sum_out_factor########################

def sum_out_factors(factor, var):
    scope = factor.get_scope()
    scope.remove(var)
    if not (scope):
        return []
    name = ""
    for v in factor.get_scope():
        name += v.name + ","
    name = name.strip(",")
    name = "P({})".format(name)
    new_factor = Factor(name, scope)
    recursive_sum_out_factors(scope, new_factor, factor, var)
    return new_factor

def recursive_sum_out_factors(variables, factor, old_factor, var):
    if len(variables) == 0:
        for v in factor.scope:
            factor.add_value_at_current_assignment(add(old_factor, var))
    else:
        for val in variables[0].domain():
            variables[0].set_assignment(val)
            recursive_sum_out_factors(variables[1:], factor, old_factor, var)   

def add(factor, var):
    result = 0
    for val in var.domain():
        var.set_assignment(val)
        result += factor.get_value_at_current_assignments()
    return result
###################common helpers####################### 

def find_factors(factors, var):
    '''Return a list of factor from factors whose factor constains var in their 
    scope'''    
    result = []
    for f in factors:
        if var in f.get_scope():
            result.append(f)
    return result