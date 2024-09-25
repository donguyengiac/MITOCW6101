"""
6.101 Lab:
SAT Solver
"""


import sys
import typing

sys.setrecursionlimit(10_000)
# NO ADDITIONAL IMPORTS

def update(old_formula, variable, value):
    #print(old_formula)
    formula = [old_formula[r][:] for r in range(len(old_formula))]
    i = 0
    while i < len(formula):
        #clause = formula[i]
        # if clause is true, remove clause. if clause is false (clause empty), return [[]]
        clause_true = False
        j = 0
        while j < len(formula[i]):
            # if 1 literal in clause is true, then whole clause is true
            # if 1 literal in clause is false, then remove literal from clause.
            literal = formula[i][j]
            #print("testpt")
            if literal[0] == variable:
                #print("true")
                if literal[1] == value: 
                    clause_true = True
                    break
                else:    
                    formula[i].pop(j)
                    j-= 1
            j += 1
        if len(formula[i]) == 0: return [[]] 
        if clause_true:
            formula.pop(i)
            i-= 1
        i+= 1
    return formula

def find_variable(formula):
    """
    return a tuple containing var name, var value, and whether unit clause
    """
    for clause in formula:
        if len(clause) == 1: return (clause[0][0], clause[0][1], True)
    for clause in formula:
        for literal in clause:
            return (literal[0], literal[1], False)
    return None



def satisfying_assignment(formula):
    #print(formula)
    """
    Find a satisfying assignment for a given CNF formula.
    Returns that assignment if one exists, or None otherwise.

    Approach: 
    - loop through all variables
    - pick a random variable, set True
    - update formula accordingly
    - if update not [[]]: return update.append((variable, True))
    - if update == [[]] set False
    - update formula accordingly
    yadda yadda yadda


    >>> satisfying_assignment([])
    {}
    >>> x = satisfying_assignment([[('a', True), ('b', False), ('c', True)]])
    >>> x.get('a', None) is True or x.get('b', None) is False or x.get('c', None) is True
    True
    >>> satisfying_assignment([[('a', True)], [('a', False)]])
    """
    out_dict = {}
    i = 0
    while i < len(formula):
        clause = formula[i]
        if len(clause) == 1:
            out_dict.update({clause[0][0]: clause[0][1]})
            formula = update(formula, clause[0][0], clause[0][1])
            i = 0
        else: i+=1

    if formula == []: return out_dict
    if formula == [[]]: return None

    #find & propagate through removing unit clause
    


    variable_tuple = find_variable(formula)
    print(variable_tuple)
    #for var in variable_set:
        #print(var)
    var = variable_tuple[0]
    state = variable_tuple[1]
    unit_clause = variable_tuple[2]
    
    #print(var)
    new_formula = update(formula, var, state)
    """if var in find_variables(new_formula): 
        print(f"{var}, True")
        return None
    #if new_formula == formula: continue
    """
    other_dict = satisfying_assignment(new_formula)
    if other_dict is not None:
        out_dict.update({var: state})
        other_dict.update(out_dict)
        return other_dict
    if unit_clause is True: return None
    state = not state
    new_formula = update(formula, var, state)
    """if var in find_variables(new_formula): 
        print(f"{var}, False")
        return None
    """
    other_dict = satisfying_assignment(new_formula)
    if other_dict is not None:
        out_dict.update({var: state})
        other_dict.update(out_dict)
        return other_dict
    return None

    
    raise NotImplementedError

def get_pair(room_list):
    out = []
    for i in range(len(room_list)):
        for j in range(i+1, len(room_list)):
            out.append((room_list[i], room_list[j]))
    return out

def get_group(student_list, capacity):
    all_group = []
    
    if capacity == 0: return [[]]
    for i in range(len(student_list)):
        student0 = student_list[i]
        #print(student0)
        students_rest = student_list[i+1:]
        results = get_group(students_rest, capacity-1)
        #print(f"{student0}, {results}")
        for group in results:
            group.append(student0)
            all_group.append(group)
        #print(all_group)
    return all_group

def boolify_scheduling_problem(student_preferences, room_capacities):
    """
    Convert a quiz-room-scheduling problem into a Boolean formula.

    student_preferences: a dictionary mapping a student name (string) to a set
                         of room names (strings) that work for that student

    room_capacities: a dictionary mapping each room name to a positive integer
                     for how many students can fit in that room

    Returns: a CNF formula encoding the scheduling problem, as per the
             lab write-up

    We assume no student or room names contain underscores.
    """
    formula = []
    student_list = list(student_preferences.keys())
    for i in range(len(student_list)):
        formula.append([])
        student = student_list[i]
        for room in student_preferences[student]:
            formula[i].append((student + "_" + room, True))
    room_list = list(room_capacities.keys())

    for student in student_preferences:
        for pair in get_pair(room_list):
            formula.append([(student + "_" + pair[0], False), (student + "_" + pair[1], False)])
    
    for room in room_capacities:
        capacity = room_capacities[room]
        if capacity >= len(student_list):
            continue
        for group in get_group(student_list, capacity+1):
            clause = []
            for student in group:
                clause.append((student + "_" + room, False))
            formula.append(clause)
    return formula
    raise NotImplementedError


if __name__ == "__main__":
    """import doctest
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags)

    rule1 = [[('duane', True), ('adam', True), ('jonathan', True),
          ('saman', True), ('tim', True)]]

    rule2 = [[('duane', False), ('adam', False)],
            [('duane', False), ('jonathan', False)],
            [('duane', False), ('saman', False)],
            [('duane', False), ('tim', False)],
            [('adam', False), ('jonathan', False)],
            [('adam', False), ('saman', False)],
            [('adam', False), ('tim', False)],
            [('jonathan', False), ('saman', False)],
            [('jonathan', False), ('tim', False)],
            [('saman', False), ('tim', False)]]


    rule3 = [[('chocolate', False), ('vanilla', False), ('pickles', False)],
            [('chocolate', True), ('vanilla', True)],
            [('chocolate', True), ('pickles', True)],
            [('vanilla', True), ('pickles', True)]]

    rule4 = [[('duane', False), ('pickles', True)],
            [('duane', False), ('chocolate', False)],
            [('duane', False), ('vanilla', False)]]

    rule5 = [[('jonathan', False), ('saman', True)],
            [('saman', False), ('jonathan', True)]]

    rule6 = [[('adam', False), ('chocolate', True)],
            [('adam', False), ('vanilla', True)],
            [('adam', False), ('pickles', True)]]

    rules = rule1 + rule2 + rule3 + rule4 + rule5 + rule6
    print(satisfying_assignment(rules))
    formula = [[('a', True), ('b', True), ('c', False)], [('c', True), ('d', True)]]
    print(satisfying_assignment(formula))
    """
    #test.test_unit_clause()
    
    #formula = test._open_case("J")[0]
    #var = list(find_variables(formula))[0]
    #new_formula = update(formula, var, True)
    #print(var)
    #print(new_formula)
    #if var in find_variables(new_formula): print("found")
        #print(cnf)
    #print(satisfying_assignment(formula))
    #print(get_group(["alex", "blake", "chris", "diana"], 3))
    print(boolify_scheduling_problem({'Alex': {'basement', 'penthouse'},
                            'Blake': {'kitchen'},
                            'Chris': {'basement', 'kitchen'},
                            'Dana': {'kitchen', 'penthouse', 'basement'}},
                           {'basement': 1,
                            'kitchen': 2,
                            'penthouse': 4}))
    
    """
    list = [0, 3, 4, 0, 6, 8, 9, 10, 0, 0, 0, 0]
    i = 0
    while i < len(list):
        if list[i] == 0:
            list.pop(i)
            i-=1
        i+=1

    print(list)"""
        