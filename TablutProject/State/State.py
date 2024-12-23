from enum import Enum
import copy
import numpy as np
from TablutProject.Domain.Action import Action


class State:
    # Enum per i turni del gioco
    class Turn(Enum):
        WHITE = "WHITE"
        BLACK = "BLACK"
        WHITEWIN = "WHITEWIN"
        BLACKWIN = "BLACKWIN"
        DRAW = "DRAW"

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

    def get_moves(self, board, i, j):

        list_moves_banned = [
            # Starting black
            (3, 0),
            (4, 0),
            (5, 0),
            (4, 1),
            (3, 8),
            (4, 8),
            (5, 8),
            (4, 7),
            (0, 3),
            (0, 4),
            (0, 5),
            (1, 4),
            (8, 3),
            (8, 4),
            (8, 5),
            (7, 4)]

        # Verifica che ci sia una pedina nella posizione
        color = self.turn
        if board[i, j] == 0:
            return []
        ret = []
        board[board == "O"] = 0
        board[board == "B"] = 2
        board[board == "W"] = 1
        board[board == "K"] = 1

        #Tolgo tutte le linee dove c'è in mezzo un camp nero
        for pos in list_moves_banned:
            board[pos] = 2

        # Matrice booleana delle caselle vuote
        is_empty = board == "0"


        #print(board)

        # Righe e colonne pertinenti
        row = is_empty[i, :]
        col = is_empty[:, j]

        # Trova i limiti sulle righe
        left_limit = max(np.where(~row[:j])[0], default=-1) + 1
        right_limit = min(np.where(~row[j + 1 :])[0], default=row.size - j - 1) + j

        # Trova i limiti sulle colonne
        top_limit = max(np.where(~col[:i])[0], default=-1) + 1
        bottom_limit = min(np.where(~col[i + 1 :])[0], default=col.size - i - 1) + i

        # Genera le posizioni valide
        moves = []

        # Aggiungi mosse nella riga
        moves.extend((i, x) for x in range(left_limit, right_limit + 1) if x != j)
        # Aggiungi mosse nella colonna
        moves.extend((y, j) for y in range(top_limit, bottom_limit + 1) if y != i)
        # devo convertire una move in action
        list_king_banned = [
            #Starting black
            (3, 0),
            (4, 0),
            (5, 0),
            (4, 1),
            (3, 8),
            (4, 8),
            (5, 8),
            (4, 7),
            (0, 3),
            (0, 4),
            (0, 5),
            (1, 4),
            (8, 3),
            (8, 4),
            (8, 5),
            (7, 4),
        ]

        ''',
            #update
            #First Row
            (0, 0),
            (0, 1),
            (0, 2),
            (0, 6),
            (0, 7),
            (0, 8),
            #First column
            (1, 0),
            (2, 0),
            (6, 0),
            (7, 0),
            (8, 0),
            #Last Row
            (8, 1),
            (8, 2),
            (8, 6),
            (8, 7),
            (8, 8),
            #Last Column
            (1, 8),
            (2, 8),
            (6, 8),
            (7, 8),'''

        if color == "WHITE" or color == "BLACK":
            for r, c in moves:
                if (r, c) not in list_moves_banned:
                    ret.append(Action((i, j), (r, c), color))
        else:
            for r, c in moves:
                if (r, c) not in list_king_banned:
                    ret.append(Action((i, j), (r, c), color))
        return ret

    def ammissible_actions(self):
        color = self.turn
        if color == "WHITE":
            color = ["W", "K"]
        else:
            color = ["B"]
        print("BUH")
        ammissible_actions = []
        for i in range(9):
            for j in range(9):
                if self.board[i][j] in color:
                    ammissible_actions += self.get_moves(
                        np.array(self.board), i, j
                    )
        return ammissible_actions

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

