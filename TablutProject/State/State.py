from enum import Enum
import copy


class State:
    # Enum per i turni del gioco
    class Turn(Enum):
        WHITE = "W"
        BLACK = "B"
        WHITEWIN = "WW"
        BLACKWIN = "BW"
        DRAW = "D"

        def __str__(self):
            return self.value

        def equals_turn(self, other_name):
            return self.value == other_name

    # Enum per i pezzi sulla scacchiera
    class Pawn(Enum):
        EMPTY = "O"
        WHITE = "W"
        BLACK = "B"
        THRONE = "T"
        KING = "K"

        def __str__(self):
            return self.value

        @staticmethod
        def from_string(s):
            if s == "O":
                return State.Pawn.EMPTY
            elif s == "W":
                return State.Pawn.WHITE
            elif s == "B":
                return State.Pawn.BLACK
            elif s == "K":
                return State.Pawn.KING
            elif s == "T":
                return State.Pawn.THRONE
            else:
                return None

        def equals_pawn(self, other_pawn):
            return self.value == other_pawn

    def __init__(self):
        self.board = [[State.Pawn.EMPTY for _ in range(9)] for _ in range(9)]
        self.turn = State.Turn.WHITE

        self.board[4][4] = State.Pawn.THRONE

        self.turn = State.Turn.BLACK

        self.board[4][4] = State.Pawn.KING

        self.board[2][4] = State.Pawn.WHITE
        self.board[3][4] = State.Pawn.WHITE
        self.board[5][4] = State.Pawn.WHITE
        self.board[6][4] = State.Pawn.WHITE
        self.board[4][2] = State.Pawn.WHITE
        self.board[4][3] = State.Pawn.WHITE
        self.board[4][5] = State.Pawn.WHITE
        self.board[4][6] = State.Pawn.WHITE

        self.board[0][3] = State.Pawn.BLACK
        self.board[0][4] = State.Pawn.BLACK
        self.board[0][5] = State.Pawn.BLACK
        self.board[1][4] = State.Pawn.BLACK
        self.board[8][3] = State.Pawn.BLACK
        self.board[8][4] = State.Pawn.BLACK
        self.board[8][5] = State.Pawn.BLACK
        self.board[7][4] = State.Pawn.BLACK
        self.board[3][0] = State.Pawn.BLACK
        self.board[4][0] = State.Pawn.BLACK
        self.board[5][0] = State.Pawn.BLACK
        self.board[4][1] = State.Pawn.BLACK
        self.board[3][8] = State.Pawn.BLACK
        self.board[4][8] = State.Pawn.BLACK
        self.board[5][8] = State.Pawn.BLACK
        self.board[4][7] = State.Pawn.BLACK

    def get_board(self):
        return self.board

    def board_string(self):
        result = ""
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                result += str(self.board[i][j])
                if j == 8:
                    result += "\n"
        return result

    def __str__(self):
        result = self.board_string()
        result += "-"
        result += "\n"
        result += str(self.turn)
        return result

    def to_linear_string(self):
        result = self.board_string().replace("\n", "")
        result += str(self.turn)
        return result

    def get_pawn(self, row, column):
        return self.board[row][column]

    def remove_pawn(self, row, column):
        self.board[row][column] = State.Pawn.EMPTY

    def set_board(self, board):
        self.board = board

    def get_turn(self):
        return self.turn

    def set_turn(self, turn):
        self.turn = turn

    def ammissible_actions(self, color):
        ammissible_actions = []
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == color:
                    
                    ...
        ...

    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        if self.board != other.board:
            return False
        if self.turn != other.turn:
            return False
        return True

    def __hash__(self):
        return hash((tuple(tuple(row) for row in self.board), self.turn))

    def get_box(self, row, column):
        col = chr(column + 97)
        return f"{col}{row + 1}"

    def clone(self):
        # Crea una copia profonda dell'oggetto
        clone = copy.deepcopy(self)
        return clone

    def get_number_of(self, color):
        count = 0
        for row in self.board:
            for cell in row:
                if cell == color:
                    count += 1
        return count
