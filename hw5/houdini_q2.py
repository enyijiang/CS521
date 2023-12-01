from z3 import *
from copy import deepcopy

# Create Z3 variables
x = Int('x')
y = Int('y')
z = Int('z')
i = Int('i')
tmp = Int('tmp')

s = Solver()

# add predicates
preds = [x != y]
pred_before_loop = []

# before the loop
s.push()
s.add(x == 1)
s.add(y == 2)
s.add(z == 3)
s.add(i == 0)

for invariant in preds:
    s.push()
    s.add(invariant)

    # check the invariants
    if s.check() == sat:
        print(f"Loop invariant {invariant} holds.")
        pred_before_loop.append(invariant)
    else:
        print(f"Loop invariant {invariant} does not hold.")
    s.pop()
s.pop()

print(pred_before_loop) # [And(i == 0), And(i < 10), And(i <= 10), And(x != y)]

# for pred in pred_before_loop:
#     s.add(pred)

# Define loop invariant and loop transition
# for idx, pred2 in enumerate(pred_before_loop[-1:]):
# s.add(x != y)
s.add(And(z != x, z != y, x != y))
for val in range(10):
    # create a new view
    s.push()
    s.add(i == val+1)
    tmp = x
    x = y
    y = z
    z = tmp

    print(x, y, z)

    s.add(Not(And(x != y, y != z, x != z)))

    # check the invariants
    if s.check() == unsat:
        print(f"Loop invariant {x != y} holds with i={val+1}.")
    else:
        print(s.model())        
        print(f"Loop invariant {x != y} does not hold with i={val+1}.")
        break
    # return back to the old view
    s.pop()