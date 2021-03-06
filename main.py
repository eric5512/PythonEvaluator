#Main file
from expr import *
from sys import getsizeof


e = MathExpr("4*(10/(x*(5+x)))*(4+x)")

print(e.eval({"x": 1}))
print(e.get_vars())
print(getsizeof(e))
e2 = MathExpr("x1x1x+2")
e3 = MathExpr("2*x")
e4 = MathExpr("x*2")
e5 = MathExpr("4*x")
print(f"MathExpr(\"2*x\") == MathExpr(\"x*2\") = {e3 == e4}")
print(f"MathExpr(\"2*x\") == MathExpr(\"4*x\") = {e3 == e5}")
print(str(e2))
print(e2.eval({"x1x1x":-4}))