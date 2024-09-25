def solve_sudoku(board):
    """
    board is 2d array, unfilled is 0
    pick any cell with 0, replace with 1, then check if still valid, if yes then try to solve the board
    if cant solve then go to next digit repeat all the way to the end
    """
    #print(board)
    #find first 0
    zero = find_zero(board)
    #print(zero)
    if zero is None: return board

    for i in range(1, 10):
        
        newboard = [[board[r][c] for c in range(9)] for r in range(9)]
        newboard[zero[0]][zero[1]] = i
        
        if valid(newboard, zero):
            result = solve_sudoku(newboard)
            if result is not None: return result
    return None
        
def valid(board, position):
    #check row
    row = board[position[0]]
    #print(f'row{row}')
    if not check(row): return False
    #check col
    col = [board[i][position[1]] for i in range(9)]
    if not check(col): return False
    #print("col")
    #check 3x3
    down = position[0] // 3
    across = position[1] // 3
    tmplist = []
    for i in range(3):
        for j in range(3):
            tmplist.append(board[down*3+i][across*3+j])
    #print(tmplist)
    if not check(tmplist): return False
    return True

def check(list):
    for i in range(len(list)):
        if list[i] != 0:
            for j in range(i+1, len(list)):
                if list[i] == list[j]: return False
    return True

def find_zero(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0: return row, col
    return None


def format_sudoku(board):
    """
    Format a sudoku board to be printed to the screen
    """
    if not board:
        return 'Failed'
    _divider = '+'+''.join('-+' if i%3==2 else '-' for i in range(9))
    lines = []
    for i in range(9):
        if i % 3 == 0:
            lines.append(_divider)
        line = '|'
        for j in range(9):
            line += ' ' if board[i][j] == 0 else str(board[i][j])
            if j % 3 == 2:
                line += '|'
        lines.append(line)
    lines.append(_divider)
    return '\n'.join(lines)

grid1 = [[5,1,7,6,0,0,0,3,4],
        [2,8,9,0,0,4,0,0,0],
        [3,4,6,2,0,5,0,9,0],
        [6,0,2,0,0,0,0,1,0],
        [0,3,8,0,0,6,0,4,7],
        [0,0,0,0,0,0,0,0,0],
        [0,9,0,0,0,0,0,7,8],
        [7,0,3,4,0,0,5,6,0],
        [0,0,0,0,0,0,0,0,0]]

grid2 = [[5,1,7,6,0,0,0,3,4],
        [0,8,9,0,0,4,0,0,0],
        [3,0,6,2,0,5,0,9,0],
        [6,0,0,0,0,0,0,1,0],
        [0,3,0,0,0,6,0,4,7],
        [0,0,0,0,0,0,0,0,0],
        [0,9,0,0,0,0,0,7,8],
        [7,0,3,4,0,0,5,6,0],
        [0,0,0,0,0,0,0,0,0]]

grid3 = [[0,0,1,0,0,9,0,0,3], # http://www.extremesudoku.info/sudoku.html
        [0,8,0,0,2,0,0,9,0],
        [9,0,0,1,0,0,8,0,0],
        [1,0,0,5,0,0,4,0,0],
        [0,7,0,0,3,0,0,5,0],
        [0,0,6,0,0,4,0,0,7],
        [0,0,8,0,0,5,0,0,6],
        [0,3,0,0,7,0,0,4,0],
        [2,0,0,3,0,0,9,0,0]]
import time
for grid in [grid1, grid2, grid3]:
    print(format_sudoku(grid))
    t = time.time()
    res = solve_sudoku(grid)
    elapsed = time.time() - t
    if res:
        print(format_sudoku(res))
    else:
        print('Failed')
    print(elapsed, 'seconds')
    print()