import pygame
import sys
import math

from board import Board
import tests

pygame.init()


# Run tests
tests.run_tests()

# initialize game
board = Board()


SQUARESIZE = 100
ROW_COUNT = 6
COLUMN_COUNT = 7
WIDTH = SQUARESIZE*COLUMN_COUNT
HEIGHT = SQUARESIZE*(ROW_COUNT+1)
SIZE = (WIDTH, HEIGHT)
RADIUS = int(SQUARESIZE/2 - 5)
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)


def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
     
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):      
            if board.board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE*(3/2))), RADIUS)
            elif board.board[r][c] == 2: 
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE*(3/2))), RADIUS)
    pygame.display.update()


screen = pygame.display.set_mode(SIZE)
#Calling function draw_board again
draw_board(board)
pygame.display.update()
myfont = pygame.font.SysFont("monospace", 75)

game_over = False
while not game_over:
    
    if not board.player1_turn():
        column = 0
        # column = Board.compute_best_move(board)
        board.drop_token(column)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and board.player1_turn():
            posx = event.pos[0]
            posy = event.pos[1]
            if posy > SQUARESIZE and posy < SIZE[1]:
                column = int(math.floor(posx/SQUARESIZE))
                success = board.drop_token(column)
                if not success: continue

    game_over = board.is_game_over()
    if game_over:
        label = myfont.render("Player {} wins!".format(2-board.turn), 1, RED)
        screen.blit(label, (40,10))
        game_over = True

    draw_board(board)
    pygame.display.update()

    if game_over:
        pygame.time.wait(3000)