#Main file
from expr import *

e1 = Sum(Prod(Val(4), Val(5)), Val(32))

print(e1.eval())