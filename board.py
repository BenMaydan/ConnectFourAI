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
    def check_in_a_row(array, num_in_a_row=4):
        prev_color = array[0]
        counter = 0

        for color in array:

            if color == -1:
                counter = 0
            elif color == prev_color:
                counter += 1
            else:
                counter = 1

            if counter == num_in_a_row:
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
            win = Board.check_in_a_row(row)
            if win[0]:
                return [True, win[1]]

        # check for vertical win
        for column in range(Board.COLS):
            win = Board.check_in_a_row([board[row][column] for row in range(Board.ROWS)])
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
            win = Board.check_in_a_row(diagonal)
            if win[0]:
                return [True, win[1]]
            
        if Board.board_is_full(board_obj):
            return [True, -1]

        return [False, None]
    

    
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
    def heuristic_four_score(four, num_tokens):
        """
        We already checked there is only one opponent's tokens in here, so we just need to count how many there are and check that == num_tokens
        """
        num = 0
        token_type = -1
        for token in four:
            if token != -1:
                token_type = token
                num += 1
        
        if num == num_tokens:
            return token_type
        return -1
    

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
        threes = 10
        twos = 5
        one = 1
        opponent_opportunity_cost = 1
        for window in windows:
            for four in Board.get_fours(window):
                if Board.has_space(four, maximizing_player) or Board.has_space(four, (maximizing_player+1)%2):
                    three_token_type = Board.heuristic_four_score(four, 3)
                    two_token_type = Board.heuristic_four_score(four, 2)
                    one_token_type = Board.heuristic_four_score(four, 1)
                    if three_token_type != -1:
                        if three_token_type == 1:
                            score += threes
                        elif three_token_type == 0:
                            score -= 3*opponent_opportunity_cost
                        continue
                    if two_token_type != -1:
                        if two_token_type == 1:
                            score += twos
                        elif two_token_type == 0:
                            score -= 2*opponent_opportunity_cost
                        continue
                    if one_token_type != -1:
                        if one_token_type == 1:
                            score += one
                        elif one_token_type == 0:
                            score -= opponent_opportunity_cost
                        continue
        # score += num_opportunities * num_opportunities_cost

        return score
    

    @staticmethod
    def optimal_depth(board, original_depth):
        num_valid_cols = len(Board.valid_cols(board))
        original_num_states = 7**original_depth
        if num_valid_cols == 1:
            return 6
        if num_valid_cols**original_depth < original_num_states:
            # num_valid^new_depth = 7^original_depth
            # new_depth = log_(num_valid) (7**original_depth)
            return int(math.log(original_num_states) / math.log(num_valid_cols))
        return original_depth
    

    @staticmethod
    def shuffle(valid):
        random.shuffle(valid)
        return valid
    

    @staticmethod
    def valid_cols(board):
        valid = []
        for col in range(Board.COLS):
            if board.board[0][col] == -1:
                valid.append(col)
        return valid


    @staticmethod
    def minimax(board, depth, alpha, beta, maximizing_player) -> list:
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
            cols = Board.shuffle(Board.valid_cols(board))
            column = random.choice(cols)

            for col in cols:
                # print(col)
                board_copy = Board.copy_board(board)
                board_copy.turn = 1
                if Board.drop_token(board_copy, col):
                    new_score = Board.minimax(board_copy, depth-1, alpha, beta, (maximizing_player+1)%2)
                    if new_score[1] > value:
                        column = col
                        value = new_score[1]
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value, depth
        
        else:
            value = math.inf
            cols = Board.shuffle(Board.valid_cols(board))
            column = random.choice(cols)

            for col in cols:
                board_copy = Board.copy_board(board)
                board_copy.turn = 0
                if Board.drop_token(board_copy, col):
                    new_score = Board.minimax(board_copy, depth-1, alpha, beta, (maximizing_player+1)%2)
                    if new_score[1] < value:
                        column = col
                        value = new_score[1]
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value, depth