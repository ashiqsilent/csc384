

for i in range(0,9):
    if (i % 3) + 1 < 3:
        state = range(0,9)
        n = state[0:i] + [state[i+1]] + [state[i]] + state[i+2:]
        print n
    else:
        print "cannot move"
    #i=4   
    #state = range(0,9)
    #n = state[0:i-1] + [state[i]] + [state[i-1]] + state[i+1:]
    #print n    