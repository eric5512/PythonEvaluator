#Class file
from re import findall, search, split
from typing import Dict

class MathExpr:
    __slots__ = {'__repr', '__parsed_tree', '__vars'}

    def __init__(self, string: str):
        self.__vars = set()
        self.__parsed_tree = self.__parse(string)
        self.__repr = string
        n = self.__max_depth()
        for _ in range(n):
            self.__parsed_tree = self.__parsed_tree.simplify()

    def eval(self, env: Dict[str, float] = {}) -> float:
        for var in env:
            if not var in self.get_vars():
                raise RuntimeError(f"The function has no variable named: {var}")
        if env != {} and type(list(env.values())[0]) == list:
            new_env = [dict(zip(list(env.keys()), list(map(lambda x: x[value], list(env.values()))))) for value in range(len(list(env.values())[0]))]
            return [self.__parsed_tree.eval(i) for i in new_env]
        return self.__parsed_tree.eval(env)

    def derivate(self, var: str):
        derivate = MathExpr("0")
        derivate._MathExpr__parsed_tree = self.__parsed_tree.derivate(var)
        derivate.__vars = self.__vars
        derivate._MathExpr__repr = ""
        n = derivate.__max_depth()
        for _ in range(n):
            derivate.__parsed_tree = derivate.__parsed_tree.simplify()
        return derivate

    def get_vars(self):
        return self.__vars

    class __Operator:
        __slots__ = {'_left', '_right'}
        def __init__(self, left, right):
            self._left = left
            self._right = right

        def max_depth(self):
            return max(self._left.max_depth(), self._right.max_depth())+1

    class __Prod(__Operator):
        def eval(self, env: Dict[str, float]) -> float:
            return self._left.eval(env) * self._right.eval(env)

        def recHash(self) -> int:
            return hash(self._left.recHash() * self._right.recHash())

        def derivate(self, var: str):
            return MathExpr._MathExpr__Sum(MathExpr._MathExpr__Prod(self._left.derivate(var), self._right), 
                MathExpr._MathExpr__Prod(self._left, self._right.derivate(var)))

        def make_string(self):
            return str(self._left) + '*' + str(self._right)

        def simplify(self):
            if MathExpr._MathExpr__Val(1) == self._right:
                return self._left.simplify()
            if MathExpr._MathExpr__Val(1) == self._left:
                return self._right.simplify()
            if MathExpr._MathExpr__Val(0) == self._right:
                return MathExpr._MathExpr__Val(0)
            if MathExpr._MathExpr__Val(0) == self._left:
                return MathExpr._MathExpr__Val(0)
            else:
                return MathExpr._MathExpr__Prod(self._left.simplify(), self._right.simplify())
            

    class __Sum(__Operator):
        def eval(self, env: Dict[str, float]) -> float:
            return self._left.eval(env) + self._right.eval(env)

        def recHash(self) -> int:
            return hash(self._left.recHash() * self._right.recHash())

        def derivate(self, var: str):
            return MathExpr._MathExpr__Sum(self._left.derivate(var), self._right.derivate(var))

        def make_string(self):
            return str(self._left) + '+' + str(self._right)

        def simplify(self):
            if MathExpr._MathExpr__Val(0) == self._left:
                return self._right.simplify()
            if MathExpr._MathExpr__Val(0) == self._right:
                return self._left.simplify()
            else:
                return MathExpr._MathExpr__Sum(self._left.simplify(), self._right.simplify())

    class __Pow(__Operator):
        def eval(self, env: Dict[str, float]) -> float:
            return self._left.eval(env) ** self._right.eval(env)

        def recHash(self) -> int:
            return hash(self._left.recHash() ** self._right.recHash())

        def derivate(self, var: str):
            if type(self._right) == MathExpr._MathExpr__Val:
                return MathExpr._MathExpr__Prod(self._right, MathExpr._MathExpr__Prod(MathExpr._MathExpr__Pow(self._left, MathExpr._MathExpr__Sub(self._right, MathExpr._MathExpr__Val(1.0))), self._left.derivate(var)))

        def make_string(self):
            return str(self._left) + '^' + str(self._right)

        def simplify(self):
            if MathExpr._MathExpr__Val(0) == self._right:
                return MathExpr._MathExpr__Val(1)
            if MathExpr._MathExpr__Val(0) == self._left:
                return MathExpr._MathExpr__Val(0)
            if MathExpr._MathExpr__Val(1) == self._right:
                return self._left
            if MathExpr._MathExpr__Val(1) == self._left:
                return MathExpr._MathExpr__Val(1)
            else:
                return MathExpr._MathExpr__Pow(self._left.simplify(), self._right.simplify())

    class __Div(__Operator):
        def eval(self, env: Dict[str, float]) -> float:
            return self._left.eval(env) / self._right.eval(env)

        def recHash(self) -> int:
            return hash(self._left.recHash() // self._right.recHash())

        def derivate(self, var: str):
            return MathExpr._MathExpr__Div(MathExpr._MathExpr__Sub(MathExpr._MathExpr__Prod(self._left.derivate(var), self._right), MathExpr._MathExpr__Prod(self._left, self._right.derivate(var))), MathExpr._MathExpr__Pow(self._right, MathExpr._MathExpr__Val(2.0)))

        def make_string(self):
            return str(self._left) + '/' + str(self._right)

        def simplify(self):
            if MathExpr._MathExpr__Val(0) == self._right:
                return MathExpr._MathExpr__Val(float("inf"))
            if MathExpr._MathExpr__Val(0) == self._left:
                return MathExpr._MathExpr__Val(0)
            if MathExpr._MathExpr__Val(1) == self._right:
                return self._left
            else:
                return MathExpr._MathExpr__Div(self._left.simplify(), self._right.simplify())

    class __Sub(__Operator):
        def eval(self, env: Dict[str, float]) -> float:
            return self._left.eval(env) - self._right.eval(env)

        def recHash(self) -> int:
            return hash(self._left.recHash() - self._right.recHash())

        def derivate(self, var: str):
            return MathExpr._MathExpr__Sub(self._left.derivate(var), self._right.derivate(var))

        def make_string(self):
            return str(self._left) + '-' + str(self._right)

        def simplify(self):
            if MathExpr._MathExpr__Val(0) == self._left:
                return MathExpr._MathExpr__Prod(MathExpr._MathExpr__Val(-1), self._right.simplify())
            if MathExpr._MathExpr__Val(0) == self._right:
                return self._left.simplify()
            else:
                return MathExpr._MathExpr__Sub(self._left.simplify(), self._right.simplify())

    class __Val:
        def __init__(self, val):
            self.val = val

        def eval(self, env: Dict[str, float]) -> float:
            return self.val

        def recHash(self) -> int:
            return hash(self.val)

        def derivate(self, var: str):
            return MathExpr._MathExpr__Val(0)

        def simplify(self):
            return self

        def max_depth(self):
            return 1

        def make_string(self):
            return str(self.val)

        def __eq__(self, other):
            if type(other) == type(self):
                return other.val == self.val
            return False

    class __Var:
        def __init__(self, name):
            self.name = name
        
        def eval(self, env: Dict[str, float]) -> float:
            return env[self.name]

        def recHash(self) -> int:
            return hash(self.name)

        def derivate(self, var: str):
            if var == self.name:
                return MathExpr._MathExpr__Val(1)
            return MathExpr._MathExpr__Val(0)

        def simplify(self):
            return self

        def max_depth(self):
            return 1

        def make_string(self):
            return self.var

        def __eq__(self, other):
            if type(other) == type(self):
                return self.name == other.name
            return False

    def __add__(self, other):
        ret = MathExpr("0")
        ret.__repr = self.__repr + '+' + str(other)
        ret.__parsed_tree = self.__Sum(self.__parsed_tree, other.__parsed_tree)
        return ret

    def __mul__(self, other):
        ret = MathExpr("0")
        ret.__repr = (self.__repr if type(self.__parsed_tree) == self.__Var or type(self.__parsed_tree) == self.__Val else f"({self.__repr})") + '*' + (str(other) if type(other.__parsed_tree) == self.__Var or type(other.__parsed_tree) == self.__Val else f"({str(other)})")
        ret.__parsed_tree = self.__Prod(self.__parsed_tree, other.__parsed_tree)
        return ret

    def __truediv__(self, other):
        ret = MathExpr("0")
        ret.__repr = (self.__repr if type(self.__parsed_tree) == self.__Var or type(self.__parsed_tree) == self.__Val else f"({self.__repr})") + '/' + (str(other) if type(other.__parsed_tree) == self.__Var or type(other.__parsed_tree) == self.__Val else f"({str(other)})")
        ret.__parsed_tree = self.__Div(self.__parsed_tree, other.__parsed_tree)
        return ret

    def __sub__(self, other):
        ret = MathExpr("0")
        ret.__repr = self.__repr  + '-' + (str(other) if type(other.__parsed_tree) == self.__Var or type(other.__parsed_tree) == self.__Val else f"({str(other)})")
        ret.__parsed_tree = self.__Sub(self.__parsed_tree, other.__parsed_tree)
        return ret

    def __pow__(self, other):
        ret = MathExpr("0")
        ret.__repr = (self.__repr if type(self.__parsed_tree) == self.__Var or type(self.__parsed_tree) == self.__Val else f"({self.__repr})") + '^' + (str(other) if type(other.__parsed_tree) == self.__Var or type(other.__parsed_tree) == self.__Val else f"({str(other)})")
        ret.__parsed_tree = self.__Pow(self.__parsed_tree, other.__parsed_tree)
        return ret

    def __str__(self):
        return self.__repr
    
    def __hash(self):
        return self.__parsed_tree.recHash()

    def __eq__(self, expr2):
        return self.__hash() == expr2.__hash()

    def __parse(self, expr):
        expr = "".join(filter(lambda x: x != ' ', expr))
        self.__check_string(expr)
        return self.__parse_rec(expr, [])

    def __parse_rec(self, string, parenthesis):
        count_par = 0
        first_pos = string.find('(')

        while first_pos != -1:
            for i in range(first_pos + 1, len(string)):
                if string[i] == '(':
                    count_par += 1
                elif string[i] == ')':
                    if count_par == 0:
                        parenthesis.append(string[first_pos+1:i])
                        string = string.replace('('+parenthesis[-1]+')', '#'+str(len(parenthesis)-1)+'#')
                        break
                    else:
                        count_par -= 1
            first_pos = string.find('(')

        divmul = search(r"[\*\/]", string[::-1])
        par = findall(r"#[0-9]+#", string)
        if findall(r"\-", string):
            new = string.split("-", 1)
            return self.__Sub(self.__parse_rec(new[0], parenthesis), self.__parse_rec(new[1], parenthesis))
        elif findall(r"\+", string):
            new = string.split("+", 1)
            return self.__Sum(self.__parse_rec(new[0], parenthesis), self.__parse_rec(new[1], parenthesis))
        elif divmul:
            new = string.split(divmul[0], 1)
            if divmul[0] == "*":
                return self.__Prod(self.__parse_rec(new[0], parenthesis), self.__parse_rec(new[1], parenthesis))
            if divmul[0] == "/":
                return self.__Div(self.__parse_rec(new[0], parenthesis), self. __parse_rec(new[1], parenthesis))
        elif findall(r"\^", string):
            new = string.split("^", 1)
            return self.__Pow(self.__parse_rec(new[0], parenthesis), self.__parse_rec(new[1], parenthesis))
        elif par:
            return self.__parse_rec(parenthesis[int(par[0][1:-1])], parenthesis)
        elif findall(r"[a-zA-Z]+[0-9a-zA-z]*", string):
            self.__vars.add(string)
            return self.__Var(string)
        elif findall(r"[0-9]+", string):
            return self.__Val(float(string))

    def __max_depth(self):
        return self.__parsed_tree.max_depth()

    def __make_string(self):
        return self.__parsed_tree.make_string()

    def __check_string(self, string):
        if string == '':
            raise RuntimeError("Error at prasing empty string")
        elif len(findall(r"\(", string)) != len(findall(r"\)", string)):
            raise RuntimeError("Parenthesis error")
        elif len(findall(r"[a-zA-z0-9\(\)\^\+\-\*\/]", string)) != len(string):
            raise RuntimeError("Found illegal character in string while parsing")
        elif findall(r"\+{2,}|\-{2,}|\*{2,}|\/{2,}|\^{2,}", string):
            raise RuntimeError("Illegal operation")
        for var in split(r"[\+\*\-\/\^]", string):
            try:
                int(var)
            except:
                if '0' < var[0] < '9':
                    raise RuntimeError("Variable name cannot begin with a number")