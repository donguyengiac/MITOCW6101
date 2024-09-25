"""
6.1010 Lab:
Snekoban Game
"""

import json
import typing

# NO ADDITIONAL IMPORTS!


direction_vector = {
    "up": (-1, 0),
    "down": (+1, 0),
    "left": (0, -1),
    "right": (0, +1),
}


def make_new_game(level_description):
    """
    Given a description of a game state, create and return a game
    representation of your choice.

    The given description is a list of lists of lists of strs, representing the
    locations of the objects on the board (as described in the lab writeup).

    For example, a valid level_description is:

    [
        [[], ['wall'], ['computer']],
        [['target', 'player'], ['computer'], ['target']],
    ]

    The exact choice of representation is up to you; but note that what you
    return will be used as input to the other functions.
    """
    game = {
        "height": len(level_description),
        "width": len(level_description[0]),
        "wall": set(),
        "computer": set(),
        "target": set()
    }

    for row in range(game["height"]):
        for col in range(game["width"]):
            cell = level_description[row][col]
            for i in cell:
                if i != "player":
                    game[i].add((row, col))
                else:
                    game[i] = (row, col)
    return game
    raise NotImplementedError


def victory_check(game):
    """
    Given a game representation (of the form returned from make_new_game),
    return a Boolean: True if the given game satisfies the victory condition,
    and False otherwise.
    """
    if len(game["computer"]) == 0 or len(game["target"]) == 0: return False
    for i in game["computer"]:
        if i not in game["target"]: return False
    return True
    raise NotImplementedError


def step_game(game, direction):
    """
    Given a game representation (of the form returned from make_new_game),
    return a new game representation (of that same form), representing the
    updated game after running one step of the game.  The user's input is given
    by direction, which is one of the following:
        {'up', 'down', 'left', 'right'}.

    This function should not mutate its input.
    """
    new_game = {
        "height": game["height"],
        "width": game["width"],
        "wall": game["wall"].copy(),
        "target": game["target"].copy(),
        "computer": set()
    }
    new_player_pos = (game["player"][0] + direction_vector[direction][0], game["player"][1] + direction_vector[direction][1])
    new_game["player"] = new_player_pos
    if new_player_pos in game["wall"]: #check hit wall, then dont move, copy all computer pos
        new_game["player"] = game["player"]
        new_game["computer"] = game["computer"].copy()
    else: #if player dont hit wall then check for changed computer position
        for i in game["computer"]: #loop through all computer pos
            if i != new_player_pos: #if no conflict between conputer pos & new player position (player dont push), just add to list
                new_game["computer"].add(i)
            else: # if new player pos lands on computer
                new_computer_pos = (i[0] + direction_vector[direction][0], i[1] + direction_vector[direction][1]) #get new position of computer
                if new_computer_pos not in game["wall"] and new_computer_pos not in game["computer"]: #check if new computer position lands on wall or another computer
                    new_game["computer"].add(new_computer_pos) # if not then valid move, add new pos of computer & valid pos of player
                else: 
                    new_game["computer"] = game["computer"].copy() #if conflict then no change pos for both computer & player
                    new_game["player"] =  game["player"]
                    break

    return new_game
    raise NotImplementedError

def dump_game(game):
    """
    Given a game representation (of the form returned from make_new_game),
    convert it back into a level description that would be a suitable input to
    make_new_game (a list of lists of lists of strings).

    This function is used by the GUI and the tests to see what your game
    implementation has done, and it can also serve as a rudimentary way to
    print out the current state of your game for testing and debugging on your
    own.
    """
    out = [[[] for _ in range(game["width"])] for _ in range(game["height"])]
    for name in ["wall", "target", "computer"]:
        for pos in game[name]:
            out[pos[0]][pos[1]].append(name)
    out[game["player"][0]][game["player"][1]].append("player")
    return out
    raise NotImplementedError

def hash(game):
    hash_string = "player " + str(game["player"][0]) + " " + str(game["player"][1]) + " computer " + str(sorted(game["computer"]))
    return hash_string


def solve_puzzle(game):
    """
    Given a game representation (of the form returned from make_new_game), find
    a solution.

    Return a list of strings representing the shortest sequence of moves ("up",
    "down", "left", and "right") needed to reach the victory condition.

    If the given level cannot be solved, return None.
    """
    game_hashable = hash(game)
    agenda = [(game, [])]
    visited = {game_hashable}
    if (victory_check(game)): return []
    DIR = ["up", "down", "left", "right"]
    while agenda:
        this_game = agenda.pop(0)
        #print(this_game)
        #print()
        game_state = this_game[0]
        moves = this_game[1]
        #print(moves)
        for i in DIR:
            next_state = step_game(game_state, i)
            moves.append(i)
            hash_check = hash(next_state)
            if hash_check not in visited:
                if (victory_check(next_state)): return moves
                agenda.append((next_state, moves[:]))
                visited.add(hash_check)
            moves.pop(-1)
    return None

    raise NotImplementedError


if __name__ == "__main__":
    with open("puzzles/t_001.json") as f:
        level = json.load(f)
    game = make_new_game(level)
    print(solve_puzzle(game))
    pass
