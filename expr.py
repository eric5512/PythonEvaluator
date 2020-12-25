#Class file
from re import findall, search, sub, escape

class Operator:
    def __init__(self, left, right):
        self._left = left
        self._right = right

    def __add__(self, other):
        return Sum(self, other)

    def __mul__(self, other):
        return Prod(self, other)

    def __truediv__(self, other):
        return Div(self, other)

    def __sub__(self, other):
        return Sub(self, other)

    def __pow__(self, other):
        return Pow(self, other)

class Prod(Operator):
    def eval(self, env):
        return self._left.eval(env) * self._right.eval(env)

    def __str__(self):
        return str(self._left) + "*" + str(self._right)

class Sum(Operator):
    def eval(self, env):
        return self._left.eval(env) + self._right.eval(env)

    def __str__(self):
        return str(self._left) + "+" + str(self._right)

class Pow(Operator):
    def eval(self, env):
        return pow(self._left.eval(env), self._right.eval(env))

    def __str__(self):
        return str(self._left) + "^" + str(self._right)

class Div(Operator):
    def eval(self, env):
        return self._left.eval(env) / self._right.eval(env)

    def __str__(self):
        return str(self._left) + "/" + str(self._right)

class Sub(Operator):
    def eval(self, env):
        return self._left.eval(env) - self._right.eval(env)

    def __str__(self):
        return str(self._left) + "-" + str(self._right)

class Val:
    def __init__(self, val):
        self.__val = val

    def eval(self, env):
        return self.__val

    def __str__(self):
        return str(self.__val)

class Var:
    def __init__(self, name):
        self.__name = name
    
    def eval(self, env):
        return env[self.__name]

    def __str__(self):
        return self.__name

def parse(expr):
    return parse_rec(expr, [])

def parse_rec(string, parenthesis):
    divmul = search(r"[\*\/]", string[::-1])
    if findall(r"\-", string):
        new = string.split("-", 1)
        return Sub(parse_rec(new[0], parenthesis), parse_rec(new[1], parenthesis))
    elif findall(r"\+", string):
        new = string.split("+", 1)
        return Sum(parse_rec(new[0], parenthesis), parse_rec(new[1], parenthesis))
    elif divmul:
        new = string.split(divmul[0], 1)
        if divmul[0] == "*":
            return Prod(parse_rec(new[0], parenthesis), parse_rec(new[1], parenthesis))
        if divmul[0] == "/":
            return Div(parse_rec(new[0], parenthesis), parse_rec(new[1], parenthesis))
    elif findall(r"\^", string):
        new = string.split("^", 1)
        return Pow(parse_rec(new[0], parenthesis), parse_rec(new[1], parenthesis))
    elif string[0] == ";":
        return parse(parenthesis[int(string[1:-1])][1:-1])
    elif findall(r"[0-9]+", string):
        return Val(float(string))
    elif findall(r"[a-zA-Z]+", string):
        return Var(string)

def findpar(expr):
    pass