import random, copy, sys, pygame, math
from pygame.locals import *

WIN_WIDTH = 640  # width of the program's window, in pixels
WIN_HEIGHT = 480  # height in pixels
COLS = 7  # how many spaces wide the board is
ROWS = 6  # how many spaces tall the board is
P_SIZE = 50  # size of the tokens and individual board spaces in pixels
X_MARG = int((WIN_WIDTH - COLS * P_SIZE) / 2)
Y_MARG = int((WIN_HEIGHT - ROWS * P_SIZE) / 2)

board_width = COLS * P_SIZE
board_height = ROWS * P_SIZE

NONE = None
RED_TKN = 'R'
YELLOW_TKN = 'Y'
REQ_TO_WIN = 4
assert COLS >= 4 and ROWS >= 4, 'Board must be at least 4x4.'

FPS = 30  # frames per second to update the screen

# Colours
BRIGHTBLUE = (0, 50, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BGCOLOR = BRIGHTBLUE
TEXTCOLOR = WHITE


def main():
    global screen, clock, font
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    font = pygame.font.SysFont('Calibri', 25, True, False)
    pygame.display.set_caption('ALLYOURBASEABELONGTOUS')
    main_board = get_new_board()

    turn = "player"

    carry_on = True
    while carry_on:

        # --- Game logic should go here

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            # User pressed down on a key
        screen.fill(WHITE)
        draw_board(main_board)

        if turn == "player":
            # Human player's turn.
            # TEST FOR CORRECT COLOR TILE??
            xy_pos = get_player_move(main_board)

            if is_position_winner(xy_pos[0], xy_pos[1], main_board):
                text = font.render("You WIN!", True, BLACK)
                # test = len(text)
                screen.blit(text, [WIN_WIDTH // 2, WIN_HEIGHT - P_SIZE])

                # break to outside Main Loop for reset or quit
                carry_on = False
                break
            # switch to other player's turn
            turn = "computer"

        if turn == "computer":
            # index of poss_moves is COL, value is fitness
            computer_move = get_computer_move(main_board, YELLOW_TKN)
            print("COmp move {}".format(computer_move))
            comp_row = get_lowest_row(main_board, computer_move)
            main_board[computer_move][comp_row] = YELLOW_TKN

            if is_position_winner(computer_move, comp_row, main_board):
                text = font.render("You WIN!", True, BLACK)
                screen.blit(text, [WIN_WIDTH // 2, WIN_HEIGHT - P_SIZE])
                # break to outside Main Loop for reset or quit
                carry_on = False
                break
            turn = "player"

        # --- Screen-clearing code goes here

        # Here, we clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.

        # If you want a background image, replace this clear with blit'ing the
        # background image.
        screen.fill(WHITE)

        # --- Drawing code should go here
        draw_board(main_board)

        # --- Go ahead and update the screen with what we've drawn.

        pygame.display.flip()

        # --- Limit to 60 frames per second
        clock.tick(60)

        # Close the window and quit.
    pygame.quit()
    sys.exit()


def make_move(board, col, tile):
    row = get_lowest_row(board, col)
    board[col][row] = tile
    return calc_consecutive(col, row, board)


# basic algo to check each column move, and every counter move from that
def get_computer_move(board, color):
    # Set colors
    if color == YELLOW_TKN:
        other_color = RED_TKN
    else:
        other_color = YELLOW_TKN

    # possible_moves index is col, val is strength
    possible_moves = [0] * COLS
    for col in range(COLS):
        dupe_board = copy.deepcopy(board)

        if not is_valid_move(board, col):
            possible_moves[col] = -1
            continue

        # Strength is consecutive tiles for that color
        lowest_row = get_lowest_row(dupe_board, col)
        dupe_board[col][lowest_row] = color
        initial_strength = calc_consecutive(col, lowest_row, dupe_board)
        initial_strength = make_move(dupe_board, col, color)

        # Check is winner
        if is_position_winner(col, lowest_row, dupe_board):
            possible_moves[col] = REQ_TO_WIN
            return col

        # Check is winner for other color
        dupe_board2 = copy.deepcopy(dupe_board)
        dupe_board2[col][lowest_row] = other_color
        if is_position_winner(col, lowest_row, dupe_board2):
            return col

        # Check opponent's counter moves
        for counter_col in range(COLS):
            dupe_board2 = copy.deepcopy(dupe_board)

            if not is_valid_move(dupe_board2, counter_col):
                # counter move is worthless
                continue

            counter_row = get_lowest_row(dupe_board2, counter_col)

            # Play other_color tile for each potential counter
            dupe_board2[counter_col][counter_row] = other_color
            counter_row = get_lowest_row(dupe_board2, counter_col)
            counter_strength = calc_consecutive(counter_col, counter_row, dupe_board2)

            # Check is_valid() for playing other_color
            if not is_valid_move(dupe_board2, counter_col):
                continue

            # Is winner, then don't play init col
            # This can produce deviant results - where counter col is same as col
            if is_position_winner(counter_col, counter_row, dupe_board2):
                possible_moves[col] = -1
                # += poss_moves[col]?
                possible_moves[counter_col] = counter_strength
            else:
                if counter_strength >= initial_strength:
                    # Defensive - Play counter col not init col
                    possible_moves[counter_col] = counter_strength

        # After checking all counters
        if possible_moves[col] < initial_strength:
            possible_moves[col] = initial_strength

    # PROBLEM - with is_valid() check for counter moves --- reassigning existing tiles!!!
    best_moves = []
    max_str = max(possible_moves)

    for i in range(len(possible_moves)):
        if possible_moves[i] == max_str:
            # Append index value
            best_moves.append(i)

    return best_moves[random.randrange(len(best_moves))]


def get_player_move(board):
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN:
                pos_x, pos_y = event.pos

            elif event.type == MOUSEMOTION:
                pos_x, pos_y = event.pos

            elif event.type == MOUSEBUTTONUP:
                if X_MARG < pos_x < (WIN_WIDTH - X_MARG):

                    column = int((pos_x - X_MARG) / P_SIZE)

                    if is_valid_move(board, column):
                        animate_falling_token(board, column, RED)
                        row = get_lowest_row(board, column)

                        # update board
                        board[column][row] = RED_TKN
                        draw_board(board)
                        pygame.display.update()
                        xy_human_pos = [column, row]
                        return xy_human_pos
        draw_board(board)
        pygame.display.update()
        clock.tick()


# returns max items in a line 1, 2, 3, or 4
# use as strength of move
def calc_consecutive(pos_col, pos_row, board):
    # item = board[pos_col][pos_row]
    row_bound = len(board[0])
    col_bound = len(board)

    max_consecutive = 1
    temp_con = 1
    for delta_col, delta_row in [(0, 1), (1, 0), (1, 1), (-1, 1)]:
        consecutive_items = 1
        for delta in (1, -1):
            delta_col *= delta
            delta_row *= delta
            next_col = pos_col + delta_col
            next_row = pos_row + delta_row

            while 0 <= next_row < row_bound and 0 <= next_col < col_bound:
                if board[next_col][next_row] == board[pos_col][pos_row]:
                    consecutive_items += 1
                    temp_con = consecutive_items
                else:
                    # if not consecutive, reset and break
                    consecutive_items = 1
                    break
                next_row += delta_row
                next_col += delta_col
                if consecutive_items == 4:
                    print("RETURNING BLANK IN A ROW")
                    return 4
                if temp_con > max_consecutive:
                    max_consecutive = temp_con

    print("Max Consecutive {} temp con {}".format(max_consecutive, temp_con))
    return max_consecutive


def is_position_winner(pos_col, pos_row, board):
    # item = board[pos_col][pos_row]
    row_bound = len(board[0])
    col_bound = len(board)

    # pos_row = get_lowest_row(board, pos_col)

    for delta_col, delta_row in [(0, 1), (1, 0), (1, 1), (-1, 1)]:
        consecutive_items = 1

        for delta in (1, -1):
            delta_col *= delta
            delta_row *= delta
            next_col = pos_col + delta_col
            next_row = pos_row + delta_row

            while 0 <= next_row < row_bound and 0 <= next_col < col_bound:
                if board[next_col][next_row] == board[pos_col][pos_row]:
                    consecutive_items += 1
                else:
                    break
                if consecutive_items == 4:
                    return True
                next_row += delta_row
                next_col += delta_col
    return False


def animate_falling_token(board, column, color):
    lowest_space = get_lowest_row(board, column)
    radius = 24
    # column += 1
    x = X_MARG + column * P_SIZE
    y = Y_MARG + radius
    drop_speed = 0.05
    # get_lowest already vetted in main

    while True:
        y += int(drop_speed)
        drop_speed += 0.01
        if int((y - Y_MARG) / P_SIZE) >= lowest_space:
            return
        draw_board(board)
        pygame.draw.circle(screen, color, (x + radius, y), radius)
        pygame.display.update()
        clock.tick()


def get_lowest_row(board, col):
    row = 5
    while board[col][row] != NONE and row > -1:
        row -= 1
    return row


def is_valid_move(board, col):
    lowest_row = get_lowest_row(board, col)
    if lowest_row == -1:
        return False
    else:
        return True


def get_new_board():
    board = [[NONE] * ROWS for _ in range(COLS)]
    return board


# Board draw requires updated board
def draw_board(board):
    screen.fill(WHITE)
    # Start x, y
    x = int(X_MARG + (P_SIZE / 2))
    y = int(Y_MARG + (P_SIZE / 2))
    pygame.draw.rect(screen, BGCOLOR, [X_MARG, Y_MARG, COLS * P_SIZE, ROWS * P_SIZE])

    # Loop provides i, j of Board[i][j]
    for i in range(COLS):  # i = 0,1,2,3...
        pygame.draw.circle(screen, WHITE, (x, y), 24)
        # init y coord
        y = int(Y_MARG + (P_SIZE / 2))

        for j in range(ROWS):  # j = 0,1,2,3...
            # iterate rows downwards for first col
            # next centre at y += 52
            if board[i][j] == RED_TKN:
                pygame.draw.circle(screen, RED, (x, y), 24)
            elif board[i][j] == YELLOW_TKN:
                pygame.draw.circle(screen, YELLOW, (x, y), 24)
            else:
                pygame.draw.circle(screen, WHITE, (x, y), 24)
            y += 50

            # Render the text. "True" means anti-aliased text.

            text = font.render(str(i + 1), True, BLACK)

            # Put the image of the text on the screen at 250x250
            # screen.blit(text, [x, y])
            screen.blit(text, [x, y])
        x += 50


main()