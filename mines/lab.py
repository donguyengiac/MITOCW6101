"""
6.101 Lab:
Mines
"""

import typing
import doctest

# NO ADDITIONAL IMPORTS ALLOWED!


def dump(game):
    """
    Prints a human-readable version of a game (provided as a dictionary)
    """
    keys = ("board", "dimensions", "state", "visible")
    # ^ Uses only default game keys. If you modify this you will need
    # to update the docstrings in other functions!
    for key in keys:
        val = game[key]
        if isinstance(val, list) and val and isinstance(val[0], list):
            print(f"{key}:")
            for inner in val:
                print(f"    {inner}")
        else:
            print(f"{key}:", val)


# 2-D IMPLEMENTATION


def new_game_2d(nrows, ncolumns, mines):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'visible' fields adequately initialized.

    Parameters:
       nrows (int): Number of rows
       ncolumns (int): Number of columns
       mines (list): List of mines, given in (row, column) pairs, which are
                     tuples

    Returns:
       A game state dictionary

    >>> dump(new_game_2d(2, 4, [(0, 0), (1, 0), (1, 1)]))
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    state: ongoing
    visible:
        [False, False, False, False]
        [False, False, False, False]
    """
    board = []
    for r in range(nrows):
        row = []
        for c in range(ncolumns):
            if [r, c] in mines or (r, c) in mines:
                row.append(".")
            else:
                row.append(0)
        board.append(row)
    visible = []
    for r in range(nrows):
        row = []
        for c in range(ncolumns):
            row.append(False)
        visible.append(row)
    for r in range(nrows):
        for c in range(ncolumns):
            if board[r][c] == 0:
                neighbor_mines = 0
                if 0 <= r - 1 < nrows:
                    if 0 <= c - 1 < ncolumns:
                        if board[r - 1][c - 1] == ".":
                            neighbor_mines += 1
                if 0 <= r < nrows:
                    if 0 <= c - 1 < ncolumns:
                        if board[r][c - 1] == ".":
                            neighbor_mines += 1
                if 0 <= r + 1 < nrows:
                    if 0 <= c - 1 < ncolumns:
                        if board[r + 1][c - 1] == ".":
                            neighbor_mines += 1
                if 0 <= r - 1 < nrows:
                    if 0 <= c < ncolumns:
                        if board[r - 1][c] == ".":
                            neighbor_mines += 1
                if 0 <= r < nrows:
                    if 0 <= c < ncolumns:
                        if board[r][c] == ".":
                            neighbor_mines += 1
                if 0 <= r + 1 < nrows:
                    if 0 <= c < ncolumns:
                        if board[r + 1][c] == ".":
                            neighbor_mines += 1
                if 0 <= r - 1 < nrows:
                    if 0 <= c + 1 < ncolumns:
                        if board[r - 1][c + 1] == ".":
                            neighbor_mines += 1
                if 0 <= r < nrows:
                    if 0 <= c + 1 < ncolumns:
                        if board[r][c + 1] == ".":
                            neighbor_mines += 1
                if 0 <= r + 1 < nrows:
                    if 0 <= c + 1 < ncolumns:
                        if board[r + 1][c + 1] == ".":
                            neighbor_mines += 1
                board[r][c] = neighbor_mines
    return {
        "dimensions": (nrows, ncolumns),
        "board": board,
        "visible": visible,
        "state": "ongoing",
    }


def dig_2d(game, row, col):
    """
    Reveal the cell at (row, col), and, in some cases, recursively reveal its
    neighboring squares.

    Update game['visible'] to reveal (row, col).  Then, if (row, col) has no
    adjacent mines (including diagonally), then recursively reveal (dig up) its
    eight neighbors.  Return an integer indicating how many new squares were
    revealed in total, including neighbors, and neighbors of neighbors, and so
    on.

    The state of the game should be changed to 'defeat' when at least one mine
    is visible on the board after digging (i.e. game['visible'][mine_location]
    == True), 'victory' when all safe squares (squares that do not contain a
    mine) and no mines are visible, and 'ongoing' otherwise.

    Parameters:
       game (dict): Game state
       row (int): Where to start digging (row)
       col (int): Where to start digging (col)

    Returns:
       int: the number of new squares revealed

    >>> game = {'dimensions': (2, 4),
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'visible': [[False, True, False, False],
    ...                  [False, False, False, False]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 3)
    4
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    state: victory
    visible:
        [False, True, True, True]
        [False, False, True, True]

    >>> game = {'dimensions': [2, 4],
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'visible': [[False, True, False, False],
    ...                  [False, False, False, False]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 0)
    1
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: [2, 4]
    state: defeat
    visible:
        [True, True, False, False]
        [False, False, False, False]
    """
    if game["state"] == "defeat" or game["state"] == "victory":
        game["state"] = game["state"]  # keep the state the same
        return 0

    if game["board"][row][col] == ".":
        game["visible"][row][col] = True
        game["state"] = "defeat"
        return 1

    num_revealed_mines = 0
    num_revealed_squares = 0
    for r in range(game["dimensions"][0]):
        for c in range(game["dimensions"][1]):
            if game["board"][r][c] == ".":
                if game["visible"][r][c] == True:
                    num_revealed_mines += 1
            elif game["visible"][r][c] == False:
                num_revealed_squares += 1
    if num_revealed_mines != 0:
        # if num_revealed_mines is not equal to zero, set the game state to
        # defeat and return 0
        game["state"] = "defeat"
        return 0
    if num_revealed_squares == 0:
        game["state"] = "victory"
        return 0

    if game["visible"][row][col] != True:
        game["visible"][row][col] = True
        revealed = 1
    else:
        return 0

    if game["board"][row][col] == 0:
        nrows, ncolumns = game["dimensions"]
        if 0 <= row - 1 < nrows:
            if 0 <= col - 1 < ncolumns:
                if game["board"][row - 1][col - 1] != ".":
                    if game["visible"][row - 1][col - 1] == False:
                        revealed += dig_2d(game, row - 1, col - 1)
        if 0 <= row < nrows:
            if 0 <= col - 1 < ncolumns:
                if game["board"][row][col - 1] != ".":
                    if game["visible"][row][col - 1] == False:
                        revealed += dig_2d(game, row, col - 1)
        if 0 <= row + 1 < nrows:
            if 0 <= col - 1 < ncolumns:
                if game["board"][row + 1][col - 1] != ".":
                    if game["visible"][row + 1][col - 1] == False:
                        revealed += dig_2d(game, row + 1, col - 1)
        if 0 <= row - 1 < nrows:
            if 0 <= col < ncolumns:
                if game["board"][row - 1][col] != ".":
                    if game["visible"][row - 1][col] == False:
                        revealed += dig_2d(game, row - 1, col)
        if 0 <= row < nrows:
            if 0 <= col < ncolumns:
                if game["board"][row][col] != ".":
                    if game["visible"][row][col] == False:
                        revealed += dig_2d(game, row, col)
        if 0 <= row + 1 < nrows:
            if 0 <= col < ncolumns:
                if game["board"][row + 1][col] != ".":
                    if game["visible"][row + 1][col] == False:
                        revealed += dig_2d(game, row + 1, col)
        if 0 <= row - 1 < nrows:
            if 0 <= col + 1 < ncolumns:
                if game["board"][row - 1][col + 1] != ".":
                    if game["visible"][row - 1][col + 1] == False:
                        revealed += dig_2d(game, row - 1, col + 1)
        if 0 <= row < nrows:
            if 0 <= col + 1 < ncolumns:
                if game["board"][row][col + 1] != ".":
                    if game["visible"][row][col + 1] == False:
                        revealed += dig_2d(game, row, col + 1)
        if 0 <= row + 1 < nrows:
            if 0 <= col + 1 < ncolumns:
                if game["board"][row + 1][col + 1] != ".":
                    if game["visible"][row + 1][col + 1] == False:
                        revealed += dig_2d(game, row + 1, col + 1)

    num_revealed_mines = 0  # set number of mines to 0
    num_revealed_squares = 0
    for r in range(game["dimensions"][0]):
        # for each r,
        for c in range(game["dimensions"][1]):
            # for each c,
            if game["board"][r][c] == ".":
                if game["visible"][r][c] == True:
                    # if the game visible is True, and the board is '.',
                    # add 1 to mines revealed
                    num_revealed_mines += 1
            elif game["visible"][r][c] == False:
                num_revealed_squares += 1
    bad_squares = num_revealed_mines + num_revealed_squares
    if bad_squares > 0:
        game["state"] = "ongoing"
        return revealed
    else:
        game["state"] = "victory"
        return revealed


def render_2d_locations(game, all_visible=False):
    """
    Prepare a game for display.

    Returns a two-dimensional array (list of lists) of '_' (hidden squares),
    '.' (mines), ' ' (empty squares), or '1', '2', etc. (squares neighboring
    mines).  game['visible'] indicates which squares should be visible.  If
    all_visible is True (the default is False), game['visible'] is ignored
    and all cells are shown.

    Parameters:
       game (dict): Game state
       all_visible (bool): Whether to reveal all tiles or just the ones allowed
                    by game['visible']

    Returns:
       A 2D array (list of lists)

    >>> game = {'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'visible':  [[False, True, True, False],
    ...                   [False, False, True, False]]}
    >>> render_2d_locations(game, False)
    [['_', '3', '1', '_'], ['_', '_', '1', '_']]

    >>> render_2d_locations(game, True)
    [['.', '3', '1', ' '], ['.', '.', '1', ' ']]
    """
    height = game["dimensions"][0]
    width = game["dimensions"][1]
    out = [[0] * width for _ in range(height)]

    for row in range(height):
        for col in range(width):
            if not game["visible"][row][col] and not all_visible:
                out[row][col] = "_"
            else:
                if game["board"][row][col] == 0:
                    out[row][col] = " "
                else:
                    out[row][col] = str(game["board"][row][col])

    return out
    raise NotImplementedError


def render_2d_board(game, all_visible=False):
    """
    Render a game as ASCII art.

    Returns a string-based representation of argument 'game'.  Each tile of the
    game board should be rendered as in the function
        render_2d_locations(game)

    Parameters:
       game (dict): Game state
       all_visible (bool): Whether to reveal all tiles or just the ones allowed
                           by game['visible']

    Returns:
       A string-based representation of game

    >>> render_2d_board({'dimensions': (2, 4),
    ...                  'state': 'ongoing',
    ...                  'board': [['.', 3, 1, 0],
    ...                            ['.', '.', 1, 0]],
    ...                  'visible':  [[True, True, True, False],
    ...                            [False, False, True, False]]})
    '.31_\\n__1_'
    """
    out = ""
    height = game["dimensions"][0]
    width = game["dimensions"][1]
    for row in range(height):
        for col in range(width):
            if not game["visible"][row][col] and not all_visible:
                out = out + "_"
            else:
                if game["board"][row][col] == 0:
                    out = out + " "
                else:
                    out = out + str(game["board"][row][col])
        if row != height - 1:
            out = out + "\n"
    return out

    raise NotImplementedError


# N-D IMPLEMENTATION


def around(location):
    """
    take in location tuple
    return list of locations (list of tuples) around this location
    """
    location0 = location[0]
    # print(location0)
    DIR = [-1, 0, 1]
    out = []
    if len(location) == 1:
        return [(location0 - 1,), (location0,), (location0 + 1,)]
    location_rest = location[1:]
    for locations in around(location_rest):
        for i in DIR:
            out.append((location0 + i,) + locations)
    return out


def new_game_nd(dimensions, mines):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'visible' fields adequately initialized.

    Args:
       dimensions (tuple): Dimensions of the board
       mines (list): mine locations as a list of tuples, each an
                     N-dimensional coordinate

    Returns:
       A game state dictionary

    >>> g = new_game_nd((2, 4, 2), [(0, 0, 1), (1, 0, 0), (1, 1, 1)])
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    state: ongoing
    visible:
        [[False, False], [False, False], [False, False], [False, False]]
        [[False, False], [False, False], [False, False], [False, False]]
    """

    def generate_empty_board(dimensions):
        dimension0 = dimensions[0]
        if len(dimensions) == 1:
            return [0] * dimension0
        dimension_rest = dimensions[1:]
        return [generate_empty_board(dimension_rest) for _ in range(dimension0)]

    def generate_none_visible(dimensions):
        dimension0 = dimensions[0]
        if len(dimensions) == 1:
            return [False] * dimension0
        dimension_rest = dimensions[1:]
        return [generate_none_visible(dimension_rest) for _ in range(dimension0)]

    def set_mine_location(board, location, mine=False):
        location0 = location[0]
        if location0 not in range(len(board)):
            return
        if len(location) == 1:
            if not mine and isinstance(board[location0], int):
                board[location0] += 1
            else:
                board[location0] = "."
            return
        location_rest = location[1:]
        set_mine_location(board[location0], location_rest, mine)

    def populate_board(mines):
        if not mines:
            return
        first_mine = mines[0]
        other_mines = mines[1:]
        for location in around(first_mine):
            # print(location)
            set_mine_location(board, location)
        set_mine_location(board, first_mine, True)
        populate_board(other_mines)
        return

    def volume(dimensions):
        dimension = dimensions[0]
        if len(dimensions) == 1:
            return dimension
        rest = dimensions[1:]
        return dimension * volume(rest)

    board = generate_empty_board(dimensions)
    populate_board(mines)

    unopened = volume(dimensions)
    out = {
        "board": board,
        "dimensions": dimensions,
        "state": "ongoing",
        "unopened": unopened - len(mines),
        "visible": generate_none_visible(dimensions),
    }
    return out
    raise NotImplementedError


def get_value(board, coordinates):
    """
    get value of board at coordinates. board can be visible board or game board.
    """
    coord0 = coordinates[0]
    if coord0 not in range(len(board)):
        return -1
    if len(coordinates) == 1:
        return board[coord0]
    coord_rest = coordinates[1:]
    return get_value(board[coord0], coord_rest)


def set_visible(board, coordinates):
    """
    set value of visible board.
    """
    coord0 = coordinates[0]
    if coord0 not in range(len(board)):
        return
    if len(coordinates) == 1:
        board[coord0] = True
        return 0
    coord_rest = coordinates[1:]
    set_visible(board[coord0], coord_rest)


def dig_nd(game, coordinates):
    """
    Recursively dig up square at coords and neighboring squares.

    Update the visible to reveal square at coords; then recursively reveal its
    neighbors, as long as coords does not contain and is not adjacent to a
    mine.  Return a number indicating how many squares were revealed.  No
    action should be taken and 0 returned if the incoming state of the game
    is not 'ongoing'.

    The updated state is 'defeat' when at least one mine is visible on the
    board after digging, 'victory' when all safe squares (squares that do
    not contain a mine) and no mines are visible, and 'ongoing' otherwise.

    Args:
       coordinates (tuple): Where to start digging

    Returns:
       int: number of squares revealed

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'visible': [[[False, False], [False, True], [False, False],
    ...                [False, False]],
    ...               [[False, False], [False, False], [False, False],
    ...                [False, False]]],
    ...      'unopened': 13,
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 3, 0))
    8
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    state: ongoing
    visible:
        [[False, False], [False, True], [True, True], [True, True]]
        [[False, False], [False, False], [True, True], [True, True]]
    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'visible': [[[False, False], [False, True], [False, False],
    ...                [False, False]],
    ...               [[False, False], [False, False], [False, False],
    ...                [False, False]]],
    ...      'unopened': 12,
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 0, 1))
    1
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    state: defeat
    visible:
        [[False, True], [False, True], [False, False], [False, False]]
        [[False, False], [False, False], [False, False], [False, False]]
    """
    out = 0
    if (
        get_value(game["visible"], coordinates) == -1
        or get_value(game["visible"], coordinates) == True
        or game["state"] == "defeat"
    ):
        return out
    visible_board = game["visible"]

    set_visible(visible_board, coordinates)
    out += 1
    if get_value(game["board"], coordinates) == ".":
        game["state"] = "defeat"
        return out
    game["unopened"] -= 1
    if get_value(game["board"], coordinates) == 0:
        for coordinate in around(coordinates):
            out += dig_nd(game, coordinate)
    if game["unopened"] == 0:
        game["state"] = "victory"
    return out
    raise NotImplementedError


def render_nd(game, all_visible=False):
    """
    Prepare the game for display.

    Returns an N-dimensional array (nested lists) of '_' (hidden squares), '.'
    (mines), ' ' (empty squares), or '1', '2', etc. (squares neighboring
    mines).  The game['visible'] array indicates which squares should be
    visible.  If all_visible is True (the default is False), the game['visible']
    array is ignored and all cells are shown.

    Args:
       all_visible (bool): Whether to reveal all tiles or just the ones allowed
                           by game['visible']

    Returns:
       An n-dimensional array of strings (nested lists)

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'visible': [[[False, False], [False, True], [True, True],
    ...                [True, True]],
    ...               [[False, False], [False, False], [True, True],
    ...                [True, True]]],
    ...      'state': 'ongoing'}
    >>> render_nd(g, False)
    [[['_', '_'], ['_', '3'], ['1', '1'], [' ', ' ']],
     [['_', '_'], ['_', '_'], ['1', '1'], [' ', ' ']]]

    >>> render_nd(g, True)
    [[['3', '.'], ['3', '3'], ['1', '1'], [' ', ' ']],
     [['.', '3'], ['3', '.'], ['1', '1'], [' ', ' ']]]
    """
    board = game["board"]
    visible = game["visible"]

    def render(board, visible, all_visible):
        out = []
        if not isinstance(board, list):
            if not visible and not all_visible:
                return "_"
            else:
                if board == 0:
                    return " "
                return str(board)
        for i in range(len(board)):
            out.append(render(board[i], visible[i], all_visible))
        return out

    return render(board, visible, all_visible)
    raise NotImplementedError


if __name__ == "__main__":
    # Test with doctests. Helpful to debug individual lab.py functions.
    # _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    # doctest.testmod(optionflags=_doctest_flags)  # runs ALL doctests

    # Alternatively, can run the doctests JUST for specified function/methods,
    # e.g., for render_2d_locations or any other function you might want.  To
    # do so, comment out the above line, and uncomment the below line of code.
    # This may be useful as you write/debug individual doctests or functions.
    # Also, the verbose flag can be set to True to see all test results,
    # including those that pass.
    #
    """
    doctest.run_docstring_examples(
       new_game_2d,
       globals(),
       optionflags=_doctest_flags,
       verbose=True
    )
    """

    game = new_game_nd((3, 3, 2), [(1, 2, 0)])
    for i in render_nd(game):
        print(i)
    print(dig_nd(game, (2, 1, 0)))
    for i in render_nd(game):
        print(i)
    print(dig_nd(game, (0, 0, 0)))
    for i in render_nd(game):
        print(i)
    print(dig_nd(game, (1, 2, 0)))
    for i in render_nd(game):
        print(i)
    """

    game = new_game_nd((10, ), [(1, ), (6, )])
    dump(game)"""
