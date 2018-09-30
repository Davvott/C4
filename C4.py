#! Connect4.py
# ! Connect4.py
import pygame

NONE = '.'
RED = 'R'
YELLOW = 'Y'

columns = 7
rows = 6
required_to_win = 4

board = [[NONE] * rows for _ in range(columns)]


def insert_piece(column, color):
    col = board[column]
    row = 0
    while col[row] != NONE:
        row += 1
    board[column][row] = color
    winner = is_position_winner(column, row)
    return winner


# function works when insert piece() adds to column[row] from 0 +=1
def is_position_winner(pos_col, pos_row):
    item = board[pos_col][pos_row]
    row_bound = len(board[0])
    col_bound = len(board)

    for delta_col, delta_row in [(0, 1), (1, 0), (1, 1), (-1, 1)]:
        consecutive_items = 1

        for delta in (1, -1):
            delta_col *= delta
            delta_row *= delta
            next_col = pos_col + delta_col
            next_row = pos_row + delta_row

            while 0 <= next_row < row_bound and 0 <= next_col < col_bound:
                if board[next_col][next_row] == item:
                    consecutive_items += 1
                else:
                    break
                if consecutive_items == 4:
                    return True
                next_row += delta_row
                next_col += delta_col
    return False


def print_board():
    for y in range(rows - 1, -1, -1):
        print('  '.join(str(board[x][y]) for x in range(columns)))

    # print header /footer of column numbers (col index)
    print('__'.join(map(str, range(columns))))
    print()


def turn_check(player):
    check_loop = True
    while check_loop:
        user_play = input("{}'s turn: ".format('Red' if player == RED else 'Yellow'))

        if user_play.isnumeric() and 0 <= int(user_play) <= 6:
            col = board[int(user_play)]
            if col[-1] == NONE:
                break
            else:
                print('Column is full. Try again!')
        else:
            print("Please enter a valid number!")

    return user_play


def main():
    player = RED
    game_loop = True
    while game_loop:
        print_board()

        user_play = turn_check(player)

        inserted_piece = insert_piece(int(user_play), player)
        if inserted_piece == True:
            print("We have a winner! Congratulations {}".format(player))

            game_loop = False
            print_board()

        player = YELLOW if player == RED else RED


main()
