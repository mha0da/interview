import copy


def reverse_list(l: list):
    """

    TODO: Reverse a list without using any built in functions

    The function should return a sorted list.

    Input l is a list which can contain any type of data.

    """

    # Get reversed list
    for i in range(len(l) // 2):
        l[i], l[-i - 1] = l[-i - 1], l[i]
    reversed_list = copy.deepcopy(l)

    # Get sorted list
    count = 0
    while count < len(l):
        for i in range(len(l) - 1):
            if l[i] > l[i + 1]:
                l[i], l[i + 1] = l[i + 1], l[i]
        count += 1
    sorted_list = l

    return (reversed_list, sorted_list)


def solve_sudoku(matrix):
    """

    TODO: Write a programme to solve 9x9 Sudoku board.



    Sudoku is one of the most popular puzzle games of all time. The goal of Sudoku is to fill a 9×9 grid with numbers so that each row, column and 3×3 section contain all of the digits between 1 and 9. As a logic puzzle, Sudoku is also an excellent brain game.



    The input matrix is a 9x9 matrix. You need to write a program to solve it.

    """

    # Try all the possible num in the box, if all num failed in a certain box then backtrack to the last box.
    def solve(row: int, col: int):
        if row == 9:
            return True
        if col == 9:
            return solve(row + 1, 0)

        if matrix[row][col] != ".":
            return solve(row, col + 1)

        for i in range(1, 10):
            if is_valid(row, col, i):
                matrix[row][col] = str(i)

                if solve(row, col + 1):
                    return True
                else:
                    matrix[row][col] = "."

        return False

    # Check if the num is valid in current box.
    def is_valid(row: int, col: int, num: int):
        num = str(num)

        if num in matrix[row]:
            return False

        for i in range(9):
            if num == matrix[i][col]:
                return False

        small_row, small_col = row // 3 * 3, col // 3 * 3
        for i in range(small_row, small_row + 3):
            for j in range(small_col, small_col + 3):
                if num == matrix[i][j]:
                    return False

        return True
    

    solve(0, 0)
