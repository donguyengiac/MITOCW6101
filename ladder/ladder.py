import string

with open('words.txt') as f:
    ALL_WORDS = {i.strip() for i in f}

start_state = "patties"

def goal_test(word):
    if word == "foaming": return True
    return False

def find_path(get_next, start_state, goal_test):
    agenda = [(start_state, )]
    visited = {start_state}

    if goal_test(start_state): return (start_state, )
    while agenda:
        path = agenda.pop(0)
        end_node = path[-1]

        for i in get_next(end_node):
            if i not in visited:
                new_path = path + (i, )
                if (goal_test(i)): return new_path
                agenda.append(new_path)
                visited.add(i)
    return None

def get_next(word):
    next_list = []
    for i, c in enumerate(word):
        for replace in string.ascii_lowercase:
            new_word = word[:i] + replace + word[i+1:]
            print(new_word)
            if new_word in ALL_WORDS: 
                next_list.append(new_word)
    return next_list
    
print(find_path(get_next, start_state, goal_test))

