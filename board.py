class Board:

    def __init__(self):
        self.board = [[0 for _ in range(8)] for _ in range(8)]


    def debug_board(self):
        print_dictionary = {1: "#", 2:"."}

        for row in self.board:
            for token in row:
                if token in print_dictionary:
                    print(print_dictionary[token] + " ", end="")
                else:
                    print("  ", end="")
            print()


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
        # check for horizontal win
        for row in self.board:
            if Board._check_four_in_a_row(row):
                return True

        # check for vertical win
        for column in range(8):
            if Board._check_four_in_a_row([self.board[row][column] for row in range(8)]):
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
    

    def dump_token(self, token, col):
        """
        Returns 0 if successful, -1 if column is full
        """
        for row in range(8):
            if self.board[row][col] != 0:
                if row != 7:
                    self.board[row-1][col] = token
                    return 0
                else:
                    return -1