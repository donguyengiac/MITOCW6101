"""
6.101 Lab:
Symbolic Algebra
"""

import doctest
# NO ADDITIONAL IMPORTS ALLOWED!
# You are welcome to modify the classes below, as well as to implement new
# classes and helper functions as necessary.

def test():
    """
    >>> z = Add(Var('x'), Sub(Var('y'), Mul(Var('z'), Num(2))))
    >>> z.eval({'x': 7, 'y': 3, 'z': 9})
    -8
    >>> z.eval({'x': 3, 'y': 10, 'z': 2})
    9
    >>> Sub(Num(4), Var('y')) == Sub(Num(4), Var('y'))
    True
    >>> Add(Num(4), Num(1)) == Num(5)
    False
    >>> Mul(Num(4), Var('y')) == Mul(Var('y'), Num(4))
    False
    >>> Div(Num(1), Add(Num(4.0), Var('z'))) == Div(Num(1.0), Add(Num(4), Var('z')))
    True
    >>> Num(4) != Var('z')
    True
    >>> x = Var('x')
    >>> y = Var('y')
    >>> z = 2*x - x*y + 3*y
    >>> print(z.deriv('x'))  # unsimplified, but the following gives us (2 - y)
    2 * 1 + x * 0 - (x * 0 + y * 1) + 3 * 0 + y * 0
    >>> print(z.deriv('y'))  # unsimplified, but the following gives us (-x + 3)
    2 * 0 + x * 0 - (x * 1 + y * 0) + 3 * 1 + y * 0
    >>> w = Div(x, y)
    >>> print(w.deriv('x'))
    (y * 1 - x * 0) / (y * y)
    >>> print(repr(w.deriv('x')))  # deriv always returns a new Symbol object
    Div(Sub(Mul(Var('y'), Num(1)), Mul(Var('x'), Num(0))), Mul(Var('y'), Var('y')))
    >>> z = 2*x - x*y + 3*y
    >>> print(z.simplify())
    2 * x - x * y + 3 * y
    >>> print(z.deriv('x'))
    2 * 1 + x * 0 - (x * 0 + y * 1) + 3 * 0 + y * 0
    >>> print(z.deriv('x').simplify())
    2 - y
    >>> print(z.deriv('y'))
    2 * 0 + x * 0 - (x * 1 + y * 0) + 3 * 1 + y * 0
    >>> print(z.deriv('y').simplify())
    0 - x + 3
    >>> Add(Add(Num(2), Num(-2)), Add(Var('x'), Num(0))).simplify()
    Var('x')
    """
    
    pass

def expression(string):
    tokens = tokenize(string)
    return parse(tokens)

def tokenize(string):
    out = []
    i = 0
    while i < len(string):
        if string[i].isnumeric() or string[i] == "-":
            j = i+1
            while j < len(string) and (string[j].isnumeric() or string[j] == "."):
                j += 1
            out.append(string[i:j])
            i = j
        elif not string[i].isnumeric() and string[i] != " ": 
            out.append(string[i])
            i += 1
        else: i+= 1
    return out                

def parse(tokens):
    """
    >>> tokens = tokenize("(x * (2 + 3))")
    >>> parse(tokens)
    Mul(Var('x'), Add(Num(2), Num(3)))
    """
    
    def parse_expression(index):
        #print(tokens)
        token = tokens[index]
        try:
            num = float(token) 
            return Num(num), index+1
        except ValueError:
            if token.isalpha(): return Var(token), index + 1

            ops = {"+": Add, "-": Sub, "*": Mul, "/": Div}
            
            left = index + 1
            #print(tokens[left])
            bracket_count = 0
            idx = left
            while idx < len(tokens) and (tokens[idx] not in ops or bracket_count != 0):
                if tokens[idx] == "(": bracket_count += 1
                if tokens[idx] == ")": bracket_count -= 1
                idx += 1
            op = ops[tokens[idx]]
            right = idx + 1
            parse_left, left_end = parse_expression(left)
            parse_right, right_end = parse_expression(right)
            return op(parse_left, parse_right), right_end

    parsed_expression, next_index = parse_expression(0)
    return parsed_expression

class Symbol:
    precedence = None
    def __add__(self, other):
        return Add(self, other)
    def __radd__(self, other):
        return Add(other, self)
    def __sub__(self, other):
        return Sub(self, other)
    def __rsub__(self, other):
        return Sub(other, self)
    def __mul__(self, other):
        return Mul(self, other)
    def __rmul__(self, other):
        return  Mul(other, self)
    def __truediv__(self, other):
        return Div(self, other)
    def __rtruediv__(self, other):
        return Div(other, self)
    
    def __eq__(self, other):
        if type(self) != type(other): return False
        if isinstance(self, Num) and isinstance(other, Num):
            if self.n == other.n: return True
            return False
        if isinstance(self, Var) and isinstance(other, Var):
            if self.name == other.name: return True
            return False
        if self.left == other.left and self.right == other.right: return True
        return False
    
class Var(Symbol):
    precedence = 0
    
    def __init__(self, n):
        """
        Initializer.  Store an instance variable called `name`, containing the
        value passed in to the initializer.
        """
        self.name = n

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Var('{self.name}')"
    
    
    def eval(self, mapping = None):
        if self.name in mapping:
            return mapping[self.name]
        raise NameError
    
    def deriv(self, var):
        if self.name == var:
            return Num(1)
        return Num(0)
    
    def simplify(self):
        return self
         
class Num(Symbol):
    precedence = 0
    
    def __init__(self, n):
        """
        Initializer.  Store an instance variable called `n`, containing the
        value passed in to the initializer.
        """
        if int(n) == n: n = int(n)
        self.n = n

    def __str__(self):
        return str(self.n)

    def __repr__(self):
        return f"Num({self.n})"
    
    
    def eval(self, mapping = None):
        return self.n
    
    def deriv(self, var):
        return Num(0)
    
    def simplify(self):
        return self
    
class BinOp(Symbol):
    def __init__(self, left, right):
        if isinstance(left, (float, int)):
            left = Num(left)
        if isinstance(left, str):
            left = Var(left)
        if isinstance(right, (float, int)):
            right = Num(right)
        if isinstance(right, str):
            right = Var(right)
        
        self.left = left
        self.right = right

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.left)}, {repr(self.right)})"

    def __str__(self):
        left_str = str(self.left)
        right_str = str(self.right)
        if self.left.precedence and self.precedence > self.left.precedence:
            left_str = "(" + left_str + ")"
        if (self.right.precedence and self.precedence > self.right.precedence or (self.precedence == self.right.precedence and self.wrap_right_at_same_precedence)):
            right_str = "(" + right_str + ")"
        
        return f"{left_str} {self.operator} {right_str}"
    
class Add(BinOp):
    operator = "+"
    precedence = 1
    wrap_right_at_same_precedence = False
    
    def eval(self, mapping = None):
        return self.left.eval(mapping) + self.right.eval(mapping)
    
    def deriv(self, var):
        return Add(self.left.deriv(var), self.right.deriv(var))
    
    def simplify(self):
        if isinstance(self.left, Num) and isinstance(self.right, Num):
            return Num(self.eval())
        if self.left == Num(0):
            return self.right.simplify()
        if self.right == Num(0):
            return self.left.simplify()
        left = self.left.simplify()
        right = self.right.simplify()
        if left == self.left and right == self.right:
            return self
        return Add(left, right).simplify()        

class Sub(BinOp):
    operator = "-"
    precedence = 1
    wrap_right_at_same_precedence = True

    def eval(self, mapping = None):
        return self.left.eval(mapping) - self.right.eval(mapping)
    
    def deriv(self, var):
        return Sub(self.left.deriv(var), self.right.deriv(var))
    
    def simplify(self):
        if isinstance(self.left, Num) and isinstance(self.right, Num):
            return Num(self.eval())
        if self.right == Num(0):
            return self.left.simplify()
        left = self.left.simplify()
        right = self.right.simplify()
        if left == self.left and right == self.right:
            return self
        return Sub(left, right).simplify()
        
class Mul(BinOp):
    operator = "*"
    precedence = 2
    wrap_right_at_same_precedence = False

    def eval(self, mapping = None):
        return self.left.eval(mapping) * self.right.eval(mapping)
    
    def deriv(self, var):
        return Add(Mul(self.left, self.right.deriv(var)), Mul(self.right, self.left.deriv(var)))
    
    def simplify(self):
        if isinstance(self.left, Num) and isinstance(self.right, Num):
            return Num(self.eval())
        if self.left == Num(1):
            return self.right.simplify()
        if self.right == Num(1):
            return self.left.simplify()
        if self.left == Num(0) or self.right == Num(0):
            return Num(0)
        left = self.left.simplify()
        right = self.right.simplify()
        if left == self.left and right == self.right:
            return self
        return Mul(left, right).simplify()
        
class Div(BinOp):
    operator = "/"
    precedence = 2
    wrap_right_at_same_precedence = True
    
    def eval(self, mapping = None):
        return self.left.eval(mapping) / self.right.eval(mapping)
    
    def deriv(self, var):
        return Div(Sub(Mul(self.right, self.left.deriv(var)), Mul(self.left, self.right.deriv(var))), Mul(self.right, self.right))
    
    def simplify(self):
        if isinstance(self.left, Num) and isinstance(self.right, Num):
            return Num(self.eval())
        if self.right == Num(1):
            return self.left.simplify()
        if self.left == Num(0):
            return Num(0)
        left = self.left.simplify()
        right = self.right.simplify()
        if left == self.left and right == self.right:
            return self
        return Div(left, right).simplify()
    
if __name__ == "__main__":
    doctest.testmod()
    tokens = tokenize("x")
    print(tokens)
    print(f"{parse(tokens)}")
    """x = Var('x')
    y = Var('y')
    z = 2*x - x*y + 3*y
    print(z.deriv('x').simplify())
    z = 2*x - x*y + 3*y
    print(z.simplify())
    """


    """E1 = Var('x')
    E2 = Var('y')
    E3 = E1 + "t"
    E4 =  3 - E2
    z = E3 - E4
    print(repr(z))
    print(z)
    print(Num(3) + 'x')"""

    
