#Main file
from expr import *

e = parse("4*(10/(x*(5+x)))*(4+x)")

print(e.eval({"x": 1}))