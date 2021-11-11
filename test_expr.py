# Main file
from expr import *


e  = MathExpr("4*(10/(x*(5+x)))*(4+x)^2")
e2 = MathExpr("x1x1x+2")
e3 = MathExpr("2*y")
e4 = MathExpr("y*2")
e5 = MathExpr("4*y^2")
e6 = MathExpr("x*2+x/2-x^2")
e7 = MathExpr("cos(x)^2+sin(x)^2")


def test_eval():
    assert e.eval({'x': 0}) == float("inf")
    assert e.eval({'x': 5}) == 64.8
    assert e2.eval({"x1x1x": 2}) == 4.0


def test_get_vars():
    assert e.get_vars() == {'x'}
    assert e2.get_vars() == {'x1x1x'}


def test_equalty():
    assert e3 == e4
    assert e3 != e5


def test_multiple_eval():
    assert e3.eval({'y': [10, 20, 30]}) == [20, 40, 60]


def test_derivate():
    assert f"{e.derivate('x').eval({'x': 5}):.2f}" == "-5.04"  # Problem with aproximation
    assert e6.derivate('x').eval({'x': 5}) == -7.5


def test_make_string():
    assert f"{MathExpr(str(e.derivate('x'))).eval({'x': 5}):.2f}" == "-5.04"

def test_unary_op():
    assert e7.eval({'x': 1}) == 1
    ok = False
    try:
        MathExpr("aaaa()")
    except:
        ok = True
    assert ok
    