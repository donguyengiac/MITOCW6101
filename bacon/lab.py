"""
6.101 Lab:
Bacon Number
"""

import pickle

# NO ADDITIONAL IMPORTS ALLOWED!

with open("resources/names.pickle", "rb") as f:
        name_map = pickle.load(f)


def transform_data(raw_data):
    transformed = [{},{}]
    for data in raw_data:
        if data[0] not in transformed[0]: transformed[0][data[0]] = {(data[1], data[2])}
        else: transformed[0][data[0]].add((data[1], data[2]))
        if data[1] not in transformed[0]: transformed[0][data[1]] = {(data[0], data[2])}
        else: transformed[0][data[1]].add((data[0], data[2]))
        if data[2] not in transformed[1]: transformed[1][data[2]] = {data[1], data[0]}
        else: 
            transformed[1][data[2]].add(data[1])
            transformed[1][data[2]].add(data[0])

        
    return transformed


def acted_together(transformed_data, actor_id_1, actor_id_2):
    if (actor_id_1 == actor_id_2): return True
    if any(actor_id_1 in t for t in transformed_data[0][actor_id_2]):
        return True
    return False



def actors_with_bacon_number(transformed_data, n):
    visited = {4724}

    def degrees(old_set):
        out = set()
        for id in old_set:
            personal_set = transformed_data[0][id]
            #print(f"{id}:{personal_set}")
            for person in personal_set:
                if person[0] not in visited: 
                    out.add(person[0])
                    visited.add(person[0])
        return out
    
    out = {4724}
    for i in range(n):
        if (len(out) == 0):
            return set()
        out = degrees(out)
    return out
    raise NotImplementedError("Implement me!")



def bacon_path(transformed_data, actor_id):
    return actor_to_actor_path(transformed_data, 4724, actor_id)
    raise NotImplementedError("Implement me!")


def actor_to_actor_path(transformed_data, actor_id_1, actor_id_2):
    return actor_path(transformed_data, actor_id_1, lambda y: y == actor_id_2)
    raise NotImplementedError("Implement me!")


def get_movie_path(transformed_data, actor_id_1, actor_id_2):
    actor_path = actor_to_actor_path(transformed_data, actor_id_1, actor_id_2)
    #print([list(name_map)[list(name_map.values()).index(i)] for i in actor_path])
    movie_path = []
    for i in range(1, len(actor_path)):
        for t in transformed_data[0][actor_path[i-1]]:
            if t[0] == actor_path[i]:
                movie_path.append(t[1])
    return movie_path



def actor_path(transformed_data, actor_id_1, goal_test_function):
    path_list = [[actor_id_1]]
    end_cell = actor_id_1
    visited = {actor_id_1}
    while True:
        if len(path_list) == 0: return None
        path = path_list.pop(0)
        end_cell = path[len(path)-1]
        if (goal_test_function(end_cell)): break
        connected = transformed_data[0][end_cell]
        #print(connected)
        for id in connected:
            if (id[0] not in visited):
                path.append(id[0])
                #print(path)
                path_list.append(path[:])
                path.pop()
                visited.add(id[0])
    return path
    raise NotImplementedError("Implement me!")


def actors_connecting_films(transformed_data, film1, film2):
    path_list = []
    film1_actors = transformed_data[1][film1]
    for actor in film1_actors:
        if (film2 in transformed_data[1]):
            path_list.append(actor_path(transformed_data, actor, lambda y: y in transformed_data[1][film2]))
    if len(path_list) != 0: return min(path_list, key = lambda k: len(k))
    else: return None
    raise NotImplementedError("Implement me!")


if __name__ == "__main__":
    with open("resources/tiny.pickle", "rb") as f:
        tinydb = pickle.load(f)
    with open("resources/small.pickle", "rb") as f:
        smalldb = pickle.load(f)
    with open("resources/large.pickle", "rb") as f:
        largedb = pickle.load(f)
    
    with open("resources/names.pickle", "rb") as f:
        name_map = pickle.load(f)
    with open("resources/movies.pickle", "rb") as f:
        movie_map = pickle.load(f)


    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.
    transformed = transform_data(tinydb)
    #print(transformed)
    #print(actors_connecting_films(transformed, 74881, 31933))
    #print([x for x in movie_map if movie_map[x] == 31932])
    #print(acted_together(transformed, 27422, 64517))
    #first_set = actors_with_bacon_number(transformed, 1)
    #second_set = actors_with_bacon_number(transformed, 2)
    #print(first_set)
    #print(bacon_path(transformed, 1640))
    #test = {
    #    1234: ({5678: 9101112,}, {1314: 151617,}, {1819: 202122,})
    #}
    #print("done" if {1819: 202122} in test[1234] else "dfdfd")
    #print(movie_map)
    #print([list(movie_map)[list(movie_map.values()).index(i)] for i in get_movie_path(transformed, name_map["Kevin Bacon"], name_map["Julia Roberts"])])
    pass
