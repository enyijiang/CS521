# z3 solver for the constrains
from z3 import *
# Create a solver
solver = Solver()

# Define variables
c0, c1, c2, c3 = Reals('c0 c1 c2 c3')
d0, d1, d2, d3 = Reals('d0 d1 d2 d3')
e1, e2, e3, e4, e5, e6, e7, e8 = Reals('e1 e2 e3 e4 e5 e6 e7 e8')

# Define constraints
constraint1 = And(c0 + c1 + c2 + e1 * c3 == 6, d0 + d1 + d2 + e1 * d3 == 2, Or(e1 ==-1, e1 ==1))
constraint2 = And(c0 + c1 + c2 + e2 * c3 == 0, d0 + d1 + d2 + e2 * d3 == 2, Or(e2 ==-1, e2 ==1))
# constraint3 = And(c0 + c1 - c2 + e3 * c3 == 2, d0 + d1 - d2 + e3 * d3 == 0, e3 >=-1, e3 <=1)
# constraint4 = And(c0 + c1 - c2 + e4 * c3 == -2, d0 + d1 - d2 + e4 * d3 == 0, e4 >=-1, e4 <=1)
# constraint5 = And(c0 - c1 + c2 + e5 * c3 == 4, d0 - d1 + d2 + e5 * d3 == 0, e5 >=-1, e5 <=1)
# constraint6 = And(c0 - c1 - c2 + e6 * c3 == 0, d0 - d1 - d2 + e6 * d3 == -2, e6 >=-1, e6 <=1)
constraint7 = And(c0 - c1 - c2 + e7 * c3 == 2, d0 - d1 - d2 + e7 * d3 == -2, Or(e7 ==-1, e7 ==1))
constraint8 = And(c0 - c1 - c2 + e8 * c3 == -4, d0 - d1 - d2 + e8 * d3 == -2, Or(e8 ==-1, e8 ==1))

# Add constraints to the solver
solver.add(constraint1, constraint2, constraint8, constraint7) #, constraint8)

# Check if the problem is satisfiable
if solver.check() == sat:
    model = solver.model()
    print(f'Solution c: {model[c0]}, {model[c1]}, {model[c2]}, {model[c3]}')
    print(f'Solution d: {model[d0]}, {model[d1]}, {model[d2]}, {model[d3]}')
else:
    print("The problem is unsatisfiable.")