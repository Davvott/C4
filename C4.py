#! Connect4.py
# ! Connect4.py
# import pygame


# Constants, inc. string values printed to board
NONE = '.'
RED = 'R'
YELLOW = 'Y'

COLS = 7
ROWS = 6
required_to_win = 4


# Cursory board initialisation
def board_init():
    board = [[NONE] * ROWS for _ in range(COLS)]
    return board


# Inserts 'piece' from users turn to board, returns is_winner()
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

    # TODO check if shallow copies are redundant/efficient
    item = board[pos_col][pos_row]
    row_bound = len(board[0])
    col_bound = len(board)

    # Defines (x,y) pair directions vert, horz, left diag, right diag
    for delta_col, delta_row in [(0, 1), (1, 0), (1, 1), (-1, 1)]:
        consecutive_items = 1

        # Check loop for directions via each +- iterations
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
    for y in range(ROWS - 1, -1, -1):
        print('  '.join(str(board[x][y]) for x in range(COLS)))

    # print header /footer of column numbers (col index)
    print('__'.join(map(str, range(COLS))))
    print()


def turn_check(player):
    check_loop = True
    while check_loop:
        user_play = input("{}'s turn: ".format('Red' if player == RED else 'Yellow'))

        if user_play.isnumeric() and 0 <= int(user_play) <= (COLS-1):
            col = board[int(user_play)]
            if col[-1] == NONE:
                break
            else:
                print('Column is full. Try again!')
        else:
            print("Please enter a valid number!")

    return user_play


board = board_init()


def main():

    # Start on player Red
    player_color = RED
    game_loop = True

    # Main game loop
    while game_loop:
        print_board()

        # Prompt and check user turn
        user_play = turn_check(player_color)

        # Apply turn play to board
        inserted_piece = insert_piece(int(user_play), player_color)
        if inserted_piece == True:
            print("We have a winner! Congratulations {}".format(player_color))

            game_loop = False
            print_board()

        player = YELLOW if player_color == RED else RED


main()
