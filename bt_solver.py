def find_next_empty_position(board, row, col):
    while row < len(board):
        while col < len(board):
            if not board[row][col]:
                return (row, col)
            else:
                col += 1
        col = 0
        row += 1
    return None, None


def get_box_around(row, col, n):
    sqrt_n = int(n**0.5)
    base_r = (row/sqrt_n)*sqrt_n
    base_c = (col/sqrt_n)*sqrt_n
    for r in xrange(base_r, base_r+sqrt_n):
        for c in xrange(base_c, base_c+sqrt_n):
            yield r, c


def is_violation(board, row, col, candidate):
    for r in xrange(0, len(board)):
        if r == row:
            continue
        if board[r][col] == candidate:
            return True
    for c in xrange(0, len(board)):
        if c == col:
            continue
        if board[row][c] == candidate:
            return True
    for r, c in get_box_around(row, col, len(board)):
        if r == row and c == col:
            continue
        if board[r][c] == candidate:
            return True
    return False

def generate_valid_candidate(board, n, row, col, prev_candidate):
    for candidate in xrange(prev_candidate+1, n+1):
        if not is_violation(board, row, col, candidate):
            yield candidate

def solve_sudoku(board, n, row, col, candidate):
    if not candidate:
        (row, col) = find_next_empty_position(board, row, col)
        for candidate in generate_valid_candidate(board, n, row, col, 0):
            ret = solve_sudoku(board, n, row, col, candidate)
            if ret:
                return True
        return False

    board[row][col] = candidate

    (next_row, next_col) = find_next_empty_position(board, row, col)
    if next_row is not None:
        for next_candidate in generate_valid_candidate(board, n, next_row, next_col, 0):
            ret = solve_sudoku(board, n, next_row, next_col, next_candidate)
            if ret:
                return True
    else:
        return True
    board[row][col] = 0
    return False


def print_board(board):
    for line in board:
        print line


def board_from_txt(txt, n):
    ret = []
    line = []
    for i,c in enumerate(txt):
        if not i%n and i > 0:
            ret.append(line)
            line = []
        line.append(int(c))
    ret.append(line)
    return ret


if __name__ == '__main__':
    if False:
        board = [[1,0,0,0],[0,2,0,0],[0,0,3,0],[0,0,0,4]]
        n = 4
    else:
        #board = board_from_txt('001700509573024106800501002700295018009400305652800007465080071000159004908007053',9)
        board = board_from_txt('209030700405060000000700906000006007001800020300000400050000002004020009702000300', 9)
        n = 9

    ret = solve_sudoku(board, n, 0, 0, 0)
    if ret:
        print_board(board)
    else:
        print "Oops! no solution"
