#Class file
class Expr:
    def __init__(self, string):
        self.__string = string

class Operator:
    def __init__(self, left, right):
        self._left = left
        self._right = right

class Prod(Operator):
    def eval(self):
        return self._left.eval() * self._right.eval()
    
class Sum(Operator):
    def eval(self):
        return self._left.eval() + self._right.eval()

class Pow(Operator):
    def eval(self):
        return pow(self._left.eval(), self._right.eval())

class Val:
    def __init__(self, val):
        self.__val = val

    def eval(self):
        return self.__val