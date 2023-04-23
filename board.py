import random
import math



class Board:

    MAX_NUMBER_OF_TURNS = 64
    ROWS = 6
    COLS = 7
    COMPUTER_TURN_NUMBER = 1
    # the table is given by: {board: [[loss, num_moves, column 1], [draw, num_moves, column 2], [win, num_moves, column 3], ...]}
    transposition_table = dict()

    def __init__(self, board=None):
        self.turn = 0

        self.board = [[-1 for _ in range(Board.COLS)] for _ in range(Board.ROWS)]


    @staticmethod
    def player1_turn(board):
        return board.turn % 2 == 0


    @staticmethod
    def check_four_in_a_row(array):
        prev_color = array[0]
        counter = 0

        for color in array:

            if color == -1:
                counter = 0
            elif color == prev_color:
                counter += 1
            else:
                counter = 1

            if counter == 4:
                return [True, prev_color]
            prev_color = color

        return [False, -1]


    
    @staticmethod
    def game_over(board_obj):
        """
        Returns
        [game_is_over, player token of whoever won]
        """
        board = board_obj.board

        # check for horizontal win
        for row in board:
            win = Board.check_four_in_a_row(row)
            if win[0]:
                return [True, win[1]]

        # check for vertical win
        for column in range(Board.COLS):
            win = Board.check_four_in_a_row([board[row][column] for row in range(Board.ROWS)])
            if win[0]:
                return [True, win[1]]

        # check for diagonal win
        h, w = len(board), len(board[0])
        diagonals = [[board[h - p + q - 1][q] for q in range(max(p-h+1, 0), min(p+1, w))] for p in range(h + w - 1)]
        sdiagonals = [[board[p - q][q] for q in range(max(p-h+1,0), min(p+1, w))] for p in range(h + w - 1)]
        diagonals.extend(sdiagonals)

        for diagonal in diagonals:
            if len(diagonal) < 4:
                continue
            win = Board.check_four_in_a_row(diagonal)
            if win[0]:
                return [True, win[1]]
            
        if Board.board_is_full(board_obj):
            return [True, -1]

        return [False, None, None]
    

    
    @staticmethod
    def increment_turn(board):
        board.turn += 1
        board.turn %= 2
    

    @staticmethod
    def drop_token(board, col):
        """
        Returns True if successful, False if column is full
        """
        for row in reversed(list(range(Board.ROWS))):
            current_token = board.board[row][col]
            if current_token == -1:
                board.board[row][col] = board.turn
                return True
            elif row == 0:
                return False
            

    @staticmethod
    def minimize(elem1: list, elem2: int, index: int) -> list:
        if elem1[0] > elem2:
            elem1 = [elem2, index]
        return elem1
    

    @staticmethod
    def maximize(elem1: list, elem2: int, index: int) -> list:
        if elem1[0] < elem2:
            elem1 = [elem2, index]
        return elem1
            

    @staticmethod
    def board_is_full(board):
        """
        there's a sneaky trick here to see if the board is full. Just check if the top row is full
        """
        for col in range(Board.COLS):
            if board.board[0][col] == -1:
                return False
        return True
            

    @staticmethod
    def copy_board(board):
        copied_board = [[board.board[r][c] for c in range(Board.COLS)] for r in range(Board.ROWS)]
        copy_board = Board()
        copy_board.board = copied_board
        return copy_board
    

    @staticmethod
    def get_fours(window):
        # 0 1 2 3 4 5 6
        fours = []
        for i in range(len(window) - 4):
            fours.append(window[i:i+4])
        return fours


    @staticmethod
    def has_space(window, maximizing_player):
        color = (maximizing_player+1)%2
        for token in window:
            if token == color:
                return False
        return True


    @staticmethod
    def heuristic(board, maximizing_player):
        # if maximizing_player is 1, then a good board is where player 2 has good chances
        windows = board

        cols = [[board[row][col] for row in range(Board.ROWS)] for col in range(Board.COLS)]
        h, w = len(board), len(board[0])
        diagonals = [[board[h - p + q - 1][q] for q in range(max(p-h+1, 0), min(p+1, w))] for p in range(h + w - 1)]
        sdiagonals = [[board[p - q][q] for q in range(max(p-h+1,0), min(p+1, w))] for p in range(h + w - 1)]
        diagonals.extend(sdiagonals)
        windows.extend(cols)
        windows.extend(diagonals)

        score = 0
        num_opportunities = 0
        opportunity_cost = 1000
        num_opportunities_cost = 100
        for window in windows:
            for four in Board.get_fours(window):
                if len(four) != 4:
                    print(len(four))
                if Board.has_space(four, maximizing_player):
                    score += opportunity_cost
                    num_opportunities += 1
        # score += num_opportunities * num_opportunities_cost

        return score
    

    @staticmethod
    def valid_cols(board):
        valid = []
        for col in range(Board.COLS):
            if board.board[0][col] == -1:
                valid.append(col)
        return valid


    @staticmethod
    def minimax(board, depth, maximizing_player) -> list:
        """
        the return value is given by [column, value]
        """

        # Returns
        # [game_is_over, draw=-1 / computer_won=1 / player_won = 0]
        game_over = Board.game_over(board)
        if game_over[0]:
            if game_over[1] == 1:
                return (None, math.inf)
            if game_over[1] == 0:
                return (None, -math.inf)
            else:
                return (None, 0)

        if depth == 0:
            return (None, Board.heuristic(board.board, maximizing_player))
        

        if maximizing_player:
            value = -math.inf
            valid = Board.valid_cols(board)
            column = random.choice(valid)

            for col in Board.valid_cols(board):
                # print(col)
                board_copy = Board.copy_board(board)
                board_copy.turn = 1
                if Board.drop_token(board_copy, col):
                    new_score = Board.minimax(board_copy, depth-1, (maximizing_player+1)%2)
                    # print(new_score)
                    if new_score[1] > value:
                        column = col
                        value = new_score[1]
            return column, value
        
        else:
            value = math.inf
            column = None

            for col in Board.valid_cols(board):
                # print(col)
                board_copy = Board.copy_board(board)
                board_copy.turn = 0
                if Board.drop_token(board_copy, col):
                    new_score = Board.minimax(board_copy, depth-1, (maximizing_player+1)%2)
                    # print(new_score)
                    if new_score[1] < value:
                        column = col
                        value = new_score[1]
            return column, value