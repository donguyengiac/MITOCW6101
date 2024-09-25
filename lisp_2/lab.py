"""
6.101 Lab:
LISP Interpreter Part 2
"""

import sys
import operator
sys.setrecursionlimit(20_000)



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

def equal(args):
    return compare_args(operator.ne, args)

def gt(args):
    return compare_args(operator.le, args)

def ge(args):
    return compare_args(operator.lt, args)

def lt(args):
    return compare_args(operator.ge, args)

def le(args):
    return compare_args(operator.gt, args)


def compare_args(func, args):
    for i in range(len(args)-1):
        if func(args[i], args[i+1]): return "#f"
    return "#t"

def no(args):
    if len(args) != 1: raise SchemeEvaluationError
    if args[0] == "#t": return "#f"
    return "#t"

def car(args):
    if len(args) != 1 or not isinstance(args[0], Pair): raise SchemeEvaluationError
    return args[0].car

def cdr(args): 
    if len(args) != 1 or not isinstance(args[0], Pair): raise SchemeEvaluationError
    return args[0].cdr

def islist(args):
    if len(args) != 1: raise SchemeEvaluationError
    if args[0] == "#none": return "#t"
    if isinstance(args[0], Pair) and islist([args[0].cdr]) == "#t": return "#t"
    return "#f"

def list_length(args):
    if len(args) != 1 : raise SchemeEvaluationError
    if args[0] == "#none": return 0
    if isinstance(args[0], Pair): return 1 + list_length([args[0].cdr])
    raise SchemeEvaluationError

def get_index(args):
    if len(args) != 2: raise SchemeEvaluationError
    list = args[0]
    index = args[1]
    if not isinstance(index, int): raise SchemeEvaluationError
    if not isinstance(list, Pair) or list == "#none": raise SchemeEvaluationError
    if index == 0:
        try: return list.car
        except: return list
    return get_index([list.cdr, index-1])

def get_pair(args):
    if len(args) != 2: raise SchemeEvaluationError
    list = args[0]
    index = args[1]
    if not isinstance(index, int): raise SchemeEvaluationError
    if islist([list]) == "#f": raise SchemeEvaluationError
    if index == 0:
        return list
    return get_pair([list.cdr, index-1])

def deepcopy(list):
    if islist(list) == "#t": 
        if list == "#none": return Pair("#none", "#none")
        #print(args[0].car, args[0].cdr)
        out = Pair(list.car, "#none")
        current = out
        for i in range(list_length(list)):
            current.cdr = Pair(list)
            current = current.cdr

    raise SchemeEvaluationError

def append(args):
    if len(args) == 0: return "#none"
    if len(args) == 1: 
        if islist([args[0]]) == "#t": 
            if args[0] == "#none": return "#none"
            #print(args[0].car, args[0].cdr)
            return Pair(args[0].car, append([args[0].cdr]))
        raise SchemeEvaluationError
    list0 = append([args[0]])
    #list0 = deepcopy(args[0])
    list1 = append(args[1:])
    if list0 == "#none": return list1
    if list1 == "#none": return list0
    final_pointer = get_pair([list0, list_length([list0])-1])
    final_pointer.cdr = list1
    return list0

def begin(args):
    return args[len(args)-1]

scheme_builtins = {
    "+": sum,
    "-": lambda args: -args[0] if len(args) == 1 else (args[0] - sum(args[1:])),
    "*": mul,
    "/": div,
    "equal?": equal,
    ">": gt, 
    ">=": ge,
    "<": lt, 
    "<=": le,
    "not": no,
    "#t": "#t",
    "#f": "#f",
    "#none": "#none",
    "car": car,
    "cdr": cdr,
    "list?": islist,
    "length": list_length,
    "list-ref": get_index,
    "append": append,
    "begin": begin,
}


##############
# Evaluation #
##############
def define(tree, frame):
    if isinstance(tree[0], list): 
        name = tree[0][0]
        params = tree[0][1:]
        #print(params)
        expr = tree[1]
        eval = Function(params, expr, frame)
    else:
        name = tree[0]
        eval = evaluate(tree[1], frame)
        
    frame.store(name, eval)
    return eval

def lambd(tree, frame):
    #print(tree)
    return Function(tree[0], tree[1], frame)

def ampersand(tree, frame):
    for arg in tree:
        if evaluate(arg, frame) == "#f": return "#f"
    return "#t"

def either(tree, frame):
    for arg in tree:
        if evaluate(arg, frame) == "#t": return "#t"
    return "#f"

def iff(tree, frame):
    pred = tree[0]
    true_exp = tree[1]
    false_exp = tree[2]
    if evaluate(pred, frame) == "#t":
        return evaluate(true_exp, frame)
    return evaluate(false_exp, frame)

def cons(tree, frame):
    if len(tree) != 2: raise SchemeEvaluationError
    return Pair(evaluate(tree[0], frame), evaluate(tree[1], frame))

def listt(tree, frame):
    if len(tree) == 0: return "#none"
    return Pair(evaluate(tree[0], frame), listt(tree[1:], frame))

def delete(tree, frame):
    #tree is [var], var is the variable to delete binding in current frame
    if len(tree) != 1: raise SchemeEvaluationError
    var = tree[0]
    if var not in frame.bindings: raise SchemeNameError
    out = frame.bindings[var]
    del frame.bindings[var]
    return out

def local_def(tree, frame):
    #tree is [[[var1, val1], [var2, val2], ...], body]
    if len(tree) != 2: raise SchemeEvaluationError
    key_value = tree[0]
    body = tree[1]
    new_frame = Frame(frame)
    for pairing in key_value:
        new_frame.store(pairing[0], evaluate(pairing[1], frame))
    return evaluate(body, new_frame)

def set_bang(tree, frame):
    #tree is [var, expression]
    if len(tree) != 2: raise SchemeEvaluationError
    var = tree[0]
    expression = tree[1]
    evaluation = evaluate(expression, frame)
    bindings = frame.lookup(var, "return_bindings")
    bindings[var] = evaluation
    return evaluation
    
    

def keyword_func(keyword):
    keywords = {"define": define, 
                "lambda": lambd,
                "and": ampersand,
                "or": either,
                "if": iff,
                "cons": cons,
                "list": listt,
                "del": delete,
                "let": local_def,
                "set!": set_bang
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
        if len(tree) == 0: return "#none"
        if not isinstance(tree[0], list):
            eval = keyword_func(tree[0])    #check if keyword
            if eval: return eval(tree[1:], frame)

        #try:
        function = evaluate(tree[0], frame)
        #except: raise SchemeEvaluationError

        if isinstance(function, (int, float)): raise SchemeEvaluationError
        return function([evaluate(tree[i], frame) for i in range(1, len(tree))])
    else:
        return frame.lookup(tree)

def evaluate_file(filename, frame = None):
    if frame is None: frame = make_initial_frame()

    with open(filename) as f:
        return evaluate(parse(tokenize(f.read())), frame)

##############
#   Frames   #
##############

class Frame:
    def __init__(self, parent = None):
        self.bindings = {}
        if parent is not None:
            self.parent = parent

    def lookup(self, name, string = None):
            #print(self.bindings)
            if name in self.bindings: 
                if string is None: return self.bindings[name]
                elif string == "return_bindings": return self.bindings
            else: 
                try:
                    return self.parent.lookup(name, string)
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


##############
#    Lists   #
##############

class Pair:
    def __init__(self, car, cdr):
        self.car = car
        self.cdr = cdr

    def __repr__(self):
        return f"{self.car} {self.cdr}"



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
    # NOTE THERE HAVE BEEN CHANGES TO THE REPL, KEEP THIS CODE BLOCK AS WELL
    # code in this block will only be executed if lab.py is the main file being
    # run (not when this module is imported)

    import os
    sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
    global_frme = make_initial_frame()
    for arg in sys.argv[1:]:
        evaluate_file(arg, global_frme)
    import schemerepl
    schemerepl.SchemeREPL(sys.modules[__name__], use_frames=True, verbose=True, global_frame=global_frme).cmdloop()
