from z3 import *

x = Int('x')
y = Int('y')
solve(x>2, y<10, x+2*y == 7)