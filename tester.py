from bicycle import *

a = [["locA", "locB", "locC", "locD"],[["locA", "locB", 15], ["locA", "locC", 25], ["locA", "locD", 10],["locB", "locC", 10], ["locB", "locD", 13], ["locC", "locD", 20]]]

s = [["Job1", "locA", 8.00, "locC",[8.30, 25], [9.30, 20], [10.00, 10], [11.00, 5]],["Job2", "locB", 10.00, "locC",[10.30, 25], [12.00, 5]],["Job3", "locC", 9.00, "locD",[9.05, 50], [9.30, 25], [10.00, 5]]]

y = solve(make_start_state(a, s))
print y