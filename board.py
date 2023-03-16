class Board:

    MAX_NUMBER_OF_TURNS = 64
    ROWS = 6
    COLS = 7

    def __init__(self):
        self.turn = 0
        self.token_dictionary = {0: "Player 1", 1: "Player 2"}

        self.board = [[0 for _ in range(Board.COLS)] for _ in range(Board.ROWS)]


    def player1_turn(self):
        return self.turn % 2 == 0


    def print_board(self):
        for row in self.board:
            for token in row:
                if token in self.token_dictionary:
                    print(self.token_dictionary[token] + " ", end="")
                else:
                    print("  ", end="")
            print()


    def player_number(self, number):
        return 1 if number == 0 else 2


    def _check_four_in_a_row(array):
        prev_color = array[0]
        counter = 0

        for color in array:

            if color == 0:
                counter = 0
            elif color == prev_color:
                counter += 1
            else:
                counter = 1

            if counter == 4:
                return True
            prev_color = color

        return False


    
    def is_game_over(self):
        """
        Returns -1 if nobody won, otherwise player token if player x won
        """
        # check for horizontal win
        for row in self.board:
            if Board._check_four_in_a_row(row):
                return True

        # check for vertical win
        for column in range(Board.COLS):
            if Board._check_four_in_a_row([self.board[row][column] for row in range(Board.ROWS)]):
                return True

        # check for diagonal win
        h, w = len(self.board), len(self.board[0])
        diagonals = [[self.board[h - p + q - 1][q] for q in range(max(p-h+1, 0), min(p+1, w))] for p in range(h + w - 1)]
        sdiagonals = [[self.board[p - q][q] for q in range(max(p-h+1,0), min(p+1, w))] for p in range(h + w - 1)]
        diagonals.extend(sdiagonals)

        for diagonal in diagonals:
            if len(diagonal) < 4:
                continue
            if Board._check_four_in_a_row(diagonal):
                return True
            
        return False
    

    def drop_token(self, col):
        """
        Returns True if successful, False if column is full
        """
        for row in reversed(list(range(Board.ROWS))):
            current_token = self.board[row][col]
            if current_token == 0:
                self.board[row][col] = self.player_number(self.turn)
                self.turn += 1
                self.turn %= 2
                return True
            elif row == 0:
                return False
            

    @staticmethod
    def compute_best_move(board, max_depth, current_depth, score, turn):
        return 0