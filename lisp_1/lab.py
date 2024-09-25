"""
6.101 Lab:
LISP Interpreter Part 1
"""


import sys
import doctest

sys.setrecursionlimit(20_000)

# NO ADDITIONAL IMPORTS!

def test():
    """
    >>> string = "(define circle-area (lambda (r) (* 3.14 (* r r))))"
    >>> tokenize(string)
    ['(', 'define', 'circle-area', '(', 'lambda', '(', 'r', ')', '(', '*', '3.14', '(', '*', 'r', 'r', ')', ')', ')', ')']
    >>> parse(tokenize(string))
    ['define', 'circle-area', ['lambda', ['r'], ['*', 3.14, ['*', 'r', 'r']]]]
    """

#############################
# Scheme-related Exceptions #
#############################


class SchemeError(Exception):
    """
    A type of exception to be raised if there is an error with a Scheme
    program.  Should never be raised directly; rather, subclasses should be
    raised.
    """

    pass


class SchemeSyntaxError(SchemeError):
    """
    Exception to be raised when trying to evaluate a malformed expression.
    """

    pass


class SchemeNameError(SchemeError):
    """
    Exception to be raised when looking up a name that has not been defined.
    """

    pass


class SchemeEvaluationError(SchemeError):
    """
    Exception to be raised if there is an error during evaluation other than a
    SchemeNameError.
    """

    pass


############################
# Tokenization and Parsing #
############################


def number_or_symbol(value):
    """
    Helper function: given a string, convert it to an integer or a float if
    possible; otherwise, return the string itself

    >>> number_or_symbol('8')
    8
    >>> number_or_symbol('-5.32')
    -5.32
    >>> number_or_symbol('1.2.3.4')
    '1.2.3.4'
    >>> number_or_symbol('x')
    'x'
    """
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value


def tokenize(source):
    """
    Splits an input string into meaningful tokens (left parens, right parens,
    other whitespace-separated values).  Returns a list of strings.
    Approach: go from start to end. 
    - if sees bracket, add.
    - if ";", find next newline, move there.
    - else find next whitespace or newline or bracket, add the between.

    Arguments:
        source (str): a string containing the source code of a Scheme
                      expression
    """
    
    out = []
    i = 0
    while i < len(source):
        char = source[i]
        #print(char)
        if char == "(" or char == ")":
            out.append(char)
        elif char == ";":
            j = i + 1
            while j < len(source) and repr(source[j]) != repr("\n"):
                j += 1
            i = j+1
            continue
        elif char != " " and repr(char) != repr("\n"):
            j = i+1
            while j < len(source) and source[j] != " " and repr(source[j]) != repr("\n") and source[j] != ")" and source[j] != "(":
                j += 1
            out.append(source[i:j])
            i = j
            continue
        i += 1

    return out


def parse(tokens):
    """
    Parses a list of tokens, constructing a representation where:
        * symbols are represented as Python strings
        * numbers are represented as Python ints or floats
        * S-expressions are represented as Python lists

    Arguments:
        tokens (list): a list of strings representing tokens
    """
    #print(tokens)
    if (tokens[0] == "(") != (tokens[len(tokens)-1]  == ")"): raise SchemeSyntaxError
    if tokens[0] != "(" and tokens[len(tokens)-1] != ")":
        if len(tokens)  == 1: return number_or_symbol(tokens[0])
        raise SchemeSyntaxError

    left = 1
    out = []

    while left < len(tokens)-1:
        if tokens[left] ==  ")": raise SchemeSyntaxError
        elif tokens[left] != "(": 
            out.append(number_or_symbol(tokens[left]))
            left += 1
        else: 
            right = left + 1
            bracket_count = 1
            while right < len(tokens)-1:
                if tokens[right] == "(": bracket_count += 1
                elif tokens[right] == ")": 
                    bracket_count -= 1
                    if bracket_count == 0:
                        result = parse(tokens[left:right+1])
                        out.append(result)
                        break
                right += 1
            if right == len(tokens)-1: raise SchemeSyntaxError
            left = right + 1
    return out
            
            

    """def helper(index):
        token = tokens[index]
        print(token)
        if token != "(" and token != ")":
            return number_or_symbol(token), index+1
        
        if token == "(": 
            out = []
            index += 1
        while (index < len(tokens) and tokens[index] != ")"):
            result, next = helper(index)
            out.append(result)
            index = next
        if tokens[index] == ")":
            try:
                return out, index+1
            except: raise SchemeSyntaxError
        raise SchemeSyntaxError
    
    return helper(0)[0]
    raise NotImplementedError
    """


######################
# Built-in Functions #
######################

def mul(args):
    if len(args) == 0: return 0
    if len(args) == 1: return args[0]
    return args[0] * mul(args[1:])

def div(args):
    if len(args) == 0: raise SchemeEvaluationError
    if len(args) == 1: return args[0]
    return args[0]/mul(args[1:])

scheme_builtins = {
    "+": sum,
    "-": lambda args: -args[0] if len(args) == 1 else (args[0] - sum(args[1:])),
    "*": mul,
    "/": div
}

##############
# Evaluation #
##############
def define(tree, frame):
    
    if isinstance(tree[1], list): 
        name = tree[1][0]
        params = tree[1][1:]
        print(params)
        expr = tree[2]
        eval = Function(params, expr, frame)
    else:
        name = tree[1]
        eval = evaluate(tree[2], frame)
        
    frame.store(name, eval)
    return eval

def lambd(tree, frame):
    #print(tree)
    return Function(tree[1], tree[2], frame)

def keyword_func(keyword):
    keywords = {"define": define, 
                "lambda": lambd,
    }
    if keyword in keywords: return keywords[keyword]
    return False


def evaluate(tree, frame = None):
    """
    Evaluate the given syntax tree according to the rules of the Scheme
    language.

    Arguments:
        tree (type varies): a fully parsed expression, as the output from the
                            parse function
    """
    if frame is None: frame = make_initial_frame()

    if isinstance(tree, (int, float)): return tree
    if isinstance(tree, list):

        if not isinstance(tree[0], list):
            eval = keyword_func(tree[0])    #check if keyword
            if eval: return eval(tree, frame)

        try:
            function = evaluate(tree[0], frame)
        except: raise SchemeEvaluationError

        if isinstance(function, (int, float)): raise SchemeEvaluationError
        return function([evaluate(tree[i], frame) for i in range(1, len(tree))])
    else:
        return frame.lookup(tree)


##############
#   Frames   #
##############

class Frame:
    def __init__(self, parent = None):
        self.bindings = {}
        if parent is not None:
            self.parent = parent

    def lookup(self, name):
            #print(self.bindings)
            if name in self.bindings: return self.bindings[name]
            else: 
                try:
                    return self.parent.lookup(name)
                except: raise SchemeNameError
    
    def store(self, name, eval):
        self.bindings.update({name: eval})

    def __iter__(self):
        yield (i for i in self.bindings)

class Built_in_Frame(Frame):
    def __init__(self):
        self.bindings = scheme_builtins
    
def make_initial_frame():
    return Frame(Built_in_Frame())



##############################
#   User-Defined Functions   #
##############################

class Function:
    def __init__(self, params, expression, enclosing_frame):
        self.params = params
        self.expression = expression
        self.enclosing_frame = enclosing_frame
    
    def __call__(self, args):
        """evaluated_args = []
        for arg in args:
            evaluated_args.append(evaluate(arg, current_frame))
        """    
        if len(args) != len(self.params): raise SchemeEvaluationError
        function_frame = Frame(self.enclosing_frame)
        for param, arg in zip(self.params, args):
            #print(param, arg)
            function_frame.store(param, arg) 
        return evaluate(self.expression, function_frame)







if __name__ == "__main__":
    # code in this block will only be executed if lab.py is the main file being
    # run (not when this module is imported)

    
    import os
    sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
    import schemerepl
    schemerepl.SchemeREPL(sys.modules[__name__], use_frames=True, verbose=False).cmdloop()
    
    #print(Built_in_Frame().lookup("+"))
    #doctest.testmod()
    #string = "(define circle-area (lambda (r) (* 3.14 (* r r))))"
    #print(parse(tokenize(string)))
    #print(evaluate('+'))
    #print(evaluate(3.14))
    #print(evaluate(['+', 3, 7, 2]))
    #print(evaluate(['+', 3, ['-', 7, 5]]))
    """tim = Frame()
    tim.store("x", 3)
    print(tim.bindings)
    tam = Frame()
    print(f"tam{tam.bindings}")
    evaluate(["define", "x", 3])
    evaluate(['+', "x", "x"])
    """
    
