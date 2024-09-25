"""
6.101 Lab:
Recipes
"""

import pickle
import sys

sys.setrecursionlimit(20_000)
# NO ADDITIONAL IMPORTS!


def atomic_ingredient_costs(recipes):
    """
    Given a recipes list, make and return a dictionary mapping each atomic food item
    name to its cost.
    """
    out = {}
    for i in recipes:
        if i[0] == "atomic":
            out.update({i[1]: i[2]})
    return out
    raise NotImplementedError


def compound_ingredient_possibilities(recipes):
    """
    Given recipes, a list containing compound and atomic food items, make and
    return a dictionary that maps each compound food item name to a list
    of all the ingredient lists associated with that name.
    """
    out = {}
    for i in recipes:
        if i[0] == "compound":
            # if i[1] == 'ap': print('found')
            if i[1] in out:
                out[i[1]].append(i[2])
            else:
                out[i[1]] = [i[2]]
    return out
    raise NotImplementedError


def lowest_cost(recipes, food_item, forbidden=[]):
    """
    Given a recipes list and the name of a food item, return the lowest cost of
    a full recipe for the given food item.
    """
    if food_item in forbidden:
        return None
    atomic_list = atomic_ingredient_costs(recipes)
    if food_item in atomic_list:
        return atomic_list[food_item]
    this_dict = compound_ingredient_possibilities(recipes)
    # print(f"thisdict{this_dict}")
    # print(f"atomic{atomic_list}")
    # print(f"fooditem{food_item}")
    # print(f"forbidden: {forbidden}")
    if food_item not in this_dict and food_item not in atomic_list:
        return None
    option_list = this_dict[food_item]
    component_cost = []
    # print(f"optionlist: {option_list}")
    for ingredient_list in option_list:
        sum = 0
        for ingredient in ingredient_list:
            # print(ingredient)
            cost = lowest_cost(recipes, ingredient[0], forbidden)
            if cost == None:
                sum = None
                break
            sum += cost * ingredient[1]
        if sum != None:
            component_cost.append(sum)
    if component_cost:
        return min(component_cost)
    return None
    raise NotImplementedError


def scaled_flat_recipe(flat_recipe, n):
    """
    Given a dictionary of ingredients mapped to quantities needed, returns a
    new dictionary with the quantities scaled by n.
    """
    out = {}
    for i in flat_recipe:
        out.update({i: flat_recipe[i] * n})
    return out
    raise NotImplementedError


def add_flat_recipes(flat_recipes):
    """
    Given a list of flat_recipe dictionaries that map food items to quantities,
    return a new overall 'grocery list' dictionary that maps each ingredient name
    to the sum of its quantities across the given flat recipes.

    For example,
        add_flat_recipes([{'milk':1, 'chocolate':1}, {'sugar':1, 'milk':2}])
    should return:
        {'milk':3, 'chocolate': 1, 'sugar': 1}
    """
    out = {}
    for flat_recipe in flat_recipes:
        for i in flat_recipe:
            if i not in out:
                out.update({i: flat_recipe[i]})
            else:
                out.update({i: out[i] + flat_recipe[i]})
    return out
    raise NotImplementedError


def cheapest_flat_recipe(recipes, food_item, forbidden=[]):
    """
    Given a recipes list and the name of a food item, return a dictionary
    (mapping atomic food items to quantities) representing the cheapest full
    recipe for the given food item.

    Returns None if there is no possible recipe.
    """

    def helper(recipes, food_item, forbidden):
        if food_item in forbidden:
            return None
        atomic_list = atomic_ingredient_costs(recipes)
        if food_item in atomic_list:
            return (atomic_list[food_item], {food_item: 1})
        this_dict = compound_ingredient_possibilities(recipes)
        # print(f"thisdict{this_dict}")
        # print(f"atomic{atomic_list}")
        # print(f"fooditem{food_item}")
        # print(f"forbidden: {forbidden}")
        if food_item not in this_dict and food_item not in atomic_list:
            return None
        option_list = this_dict[food_item]
        component_cost = []
        # print(f"optionlist: {option_list}")
        for ingredient_list in option_list:
            sum = 0
            old_list = {}
            for ingredient in ingredient_list:
                # print(ingredient)
                temp = helper(recipes, ingredient[0], forbidden)
                if temp == None:
                    sum = None
                    break
                cost = temp[0]
                list = temp[1]  # {food: quantity}
                sum += cost * ingredient[1]
                old_list = add_flat_recipes(
                    [old_list, scaled_flat_recipe(list, ingredient[1])]
                )
            if sum != None:
                component_cost.append((sum, old_list))
        if component_cost:
            return min(component_cost)
        return None

    out = helper(recipes, food_item, forbidden)
    # print(out)
    if out != None:
        return out[1]
    return None
    raise NotImplementedError


def combined_flat_recipes(flat_recipes):
    """
    Given a list of lists of dictionaries, where each inner list represents all
    the flat recipes for a certain ingredient, compute and return a list of flat
    recipe dictionaries that represent all the possible combinations of
    ingredient recipes.
    """
    out = []
    if len(flat_recipes) == 0:
        return out
    # print(flat_recipes)
    for option in flat_recipes[0]:
        # tmp_dict = {option}
        # print(f"option {option}")
        other_list = combined_flat_recipes(flat_recipes[1:])
        if other_list == []:
            return flat_recipes[0]
        for other_dict in other_list:
            tmp_dict = add_flat_recipes([option, other_dict])
            # print(tmp_dict)
            out.append(tmp_dict)
    return out
    raise NotImplementedError


def all_flat_recipes(recipes, food_item, forbidden=[]):
    """
    Given a list of recipes and the name of a food item, produce a list (in any
    order) of all possible flat recipes for that category.

    Returns an empty list if there are no possible recipes
    """
    # print(f"food item: {food_item}")
    # print(f"item{food_item}")

    if food_item in forbidden:
        return []
    atomic_list = atomic_ingredient_costs(recipes)
    """for i in atomic_list:
        print(i)
    """
    # if 'ap' in atomic_list:
    #    print(f'yes{food_item}')
    if food_item in atomic_list:
        return [{food_item: 1}]

    """
    for i in compound_ingredient_possibilities(recipes):
        print(f"{i}: {compound_ingredient_possibilities(recipes)[i]}")
    print()
    """
    compound_list = compound_ingredient_possibilities(recipes)
    if food_item not in compound_list:
        return []
    option_list = compound_list[food_item]
    output = []
    # print(f'optionlists are:{option_list}')
    for option in option_list:
        # print(f'options are:{option}')
        next_option = False
        small_out = []
        for component_tuple in option:
            to_make = all_flat_recipes(recipes, component_tuple[0], forbidden)
            if len(to_make) == 0:
                next_option = True
                break
            # print(f'tomake{to_make}')
            new_list = []
            for thisdict in to_make:
                # print(f"food{food_item}, tomake{to_make}, tuple{component_tuple}")
                new_list.append(scaled_flat_recipe(thisdict, component_tuple[1]))
            small_out.append(new_list)
        # print(small_out)
        # print(1)
        if next_option == True:
            continue
        tmp = combined_flat_recipes(small_out)
        # print(tmp)
        output = output + tmp
    # print(f'output: {output}')
    return output
    raise NotImplementedError


if __name__ == "__main__":
    # load example recipes from section 3 of the write-up
    with open("test_recipes/example_recipes.pickle", "rb") as f:
        example_recipes = pickle.load(f)

    dairy_recipes = [
        ("compound", "milk", [("cow", 2), ("milking stool", 1)]),
        ("compound", "cheese", [("milk", 1), ("time", 1)]),
        ("compound", "cheese", [("cutting-edge laboratory", 11)]),
        ("atomic", "milking stool", 5),
        ("atomic", "cutting-edge laboratory", 1000),
        ("atomic", "time", 10000),
        ("atomic", "cow", 100),
    ]
    cookie_recipes = [
        ("compound", "cookie sandwich", [("cookie", 2), ("ice cream scoop", 3)]),
        ("compound", "cookie", [("chocolate chips", 3)]),
        ("compound", "cookie", [("sugar", 10)]),
        ("atomic", "chocolate chips", 200),
        ("atomic", "sugar", 5),
        ("compound", "ice cream scoop", [("vanilla ice cream", 1)]),
        ("compound", "ice cream scoop", [("chocolate ice cream", 1)]),
        ("atomic", "vanilla ice cream", 20),
        ("atomic", "chocolate ice cream", 30),
    ]
    soup = {
        "carrots": 5,
        "celery": 3,
        "broth": 2,
        "noodles": 1,
        "chicken": 3,
        "salt": 10,
    }
    carrot_cake = {
        "carrots": 5,
        "flour": 8,
        "sugar": 10,
        "oil": 5,
        "eggs": 4,
        "salt": 3,
    }
    bread = {"flour": 10, "sugar": 3, "oil": 3, "yeast": 15, "salt": 5}
    grocery_list = [soup, carrot_cake, bread]

    cake_recipes = [{"cake": 1}, {"gluten free cake": 1}]
    icing_recipes = [{"vanilla icing": 1}, {"cream cheese icing": 1}]
    topping_recipes = [{"sprinkles": 20}]

    burger_dict = compound_ingredient_possibilities(example_recipes)["burger"]
    # print(burger_dict[0])
    # print(cheapest_flat_recipe(example_recipes, "burger"))
    for i in all_flat_recipes(example_recipes, "cow"):
        print(i)
    print("ok")
    for i in all_flat_recipes(example_recipes, "cheese", ("milking stool",)):
        print(i)
    # you are free to add additional testing code here!
