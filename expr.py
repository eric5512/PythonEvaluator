#Class file
from re import findall, search, split

class MathExpr:
    __slots__ = {'__repr', '__parsed_tree'}

    def __init__(self, string):
        self.__repr = string
        self.__parsed_tree = self.__parse(string)

    def eval(self, env = {}):
        for var in env:
            if not var in self.get_vars():
                raise RuntimeError(f"The function has no variable named: {var}")
        return self.__parsed_tree.eval(env)

    def get_vars(self):
        return set(findall(r"[a-zA-Z]+[0-9a-zA-z]*", self.__repr))

    class __Operator:
        __slots__ = {'_left', '_right'}
        def __init__(self, left, right):
            self._left = left
            self._right = right

    class __Prod(__Operator):
        def eval(self, env):
            return self._left.eval(env) * self._right.eval(env)

        def recHash(self):
            return hash(self._left.recHash() * self._right.recHash())

    class __Sum(__Operator):
        def eval(self, env):
            return self._left.eval(env) + self._right.eval(env)

        def recHash(self):
            return hash(self._left.recHash() * self._right.recHash())

    class __Pow(__Operator):
        def eval(self, env):
            return self._left.eval(env) ** self._right.eval(env)

        def recHash(self):
            return hash(self._left.recHash() ** self._right.recHash())

    class __Div(__Operator):
        def eval(self, env):
            return self._left.eval(env) / self._right.eval(env)

        def recHash(self):
            return hash(self._left.recHash() // self._right.recHash())


    class __Sub(__Operator):
        def eval(self, env):
            return self._left.eval(env) - self._right.eval(env)

        def recHash(self):
            return hash(self._left.recHash() - self._right.recHash())

    class __Val:
        def __init__(self, val):
            self.__val = val

        def eval(self, env):
            return self.__val

        def recHash(self):
            return hash(self.__val)


    class __Var:
        def __init__(self, name):
            self.__name = name
        
        def eval(self, env):
            return env[self.__name]

        def recHash(self):
            return hash(self.__name)


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
            return self.__Var(string)
        elif findall(r"[0-9]+", string):
            return self.__Val(float(string))


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