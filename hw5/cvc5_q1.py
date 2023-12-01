from cvc5 import *

a = Int('a')
print(solve(a > 0, a < 2))