# import pygame
from board import Board
import tests

# pygame.init()
# pygame.font.init()


# Run tests
tests.run_tests()

# initialize game
board = Board()


# game loop
try:
    game_over = False
    board.print_board()
    
    while not game_over:
        player = board.player_number()
        column = input("Player {}, enter a column: ".format(player))

        if column in ["quit", "q", "exit", "e", "quit()", "exit()"]:
            game_over = True
            print("You have quit the game!")
            break

        if not column.isdigit() or int(column) < 1 or int(column) > 8:
            print("Column \"{}\" is not a valid integer from 1 to 8!".format(column))
            continue

        column = int(column) - 1
        success = board.drop_token(column)
        if not success:
            print("Column is already full!")
            continue

        board.print_board()
        game_over = board.is_game_over()

except KeyboardInterrupt:
    print("You have quit the game!")