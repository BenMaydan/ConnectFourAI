import pygame
import os
import sys
import math
import json
import argparse

from board import Board
import tests


argument_parser = argparse.ArgumentParser("Parsing how many turns you want the computer to think ahead")
argument_parser.add_argument("-t", "--turns", type=int, default=7, help="How many turns the computer thinks ahead. Recommended for speed and difficulty is 7")
args = argument_parser.parse_args()


# Run tests
tests.run_tests()

# initialize game
pygame.init()
board = Board()
check_file = os.stat("table.json").st_size
if check_file != 0:
    with open("table.json", "r") as infile:
        board.transposition_table = json.load(infile)


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
            if board.board[r][c] == 0:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE*(3/2))), RADIUS)
            elif board.board[r][c] == 1: 
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE*(3/2))), RADIUS)
    pygame.display.update()


screen = pygame.display.set_mode(SIZE)
#Calling function draw_board again
draw_board(board)
pygame.display.update()
myfont = pygame.font.SysFont("monospace", 75)

game_over = False
while not game_over:
    
    if not Board.player1_turn(board):
        move = Board.minimax(board, args.turns, -math.inf, math.inf, 1) # 3rd and 4th arguments: alpha, beta
        print("Column: {}, Score: {}".format(move[0], move[1]))
        Board.drop_token(board, move[0])
        Board.increment_turn(board)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            posx = event.pos[0]
            xy = ((SQUARESIZE*(math.floor(posx/SQUARESIZE) + 0.5), int(SQUARESIZE/2)))
            pygame.draw.rect(screen, BLACK, (0,0, WIDTH, SQUARESIZE))
            if board.turn == 0:
                pygame.draw.circle(screen, RED, xy, RADIUS)

        if event.type == pygame.MOUSEBUTTONDOWN and Board.player1_turn(board):
            posx = event.pos[0]
            column = int(math.floor(posx/SQUARESIZE))
            success = Board.drop_token(board, column)
            Board.increment_turn(board)
            if not success: continue

    win = Board.game_over(board)
    game_over = win[0]
    if game_over:
        text = "Player {} wins!".format(win[1]+1)
        if win[1] == -1:
            text = "It's a draw!"
        pygame.draw.rect(screen, BLACK, (0,0, WIDTH, SQUARESIZE))
        label = myfont.render(text, 1, RED)
        screen.blit(label, (40,10))

    draw_board(board)
    pygame.display.update()

    if game_over:
        pygame.time.wait(3000)


pygame.quit()
pygame.display.quit()


# Resave the transposition table to use for next time
table = board.transposition_table
with open("table.json", "w") as outfile:
    json.dump(table, outfile)