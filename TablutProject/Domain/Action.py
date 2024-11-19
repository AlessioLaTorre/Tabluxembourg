import copy
from dataclasses import dataclass
from typing import Union
import random


class InvalidParameterException(Exception):
    """Eccezione personalizzata per parametri non validi."""

    pass


@dataclass
class Action:
    from_: tuple  # Usato `from_` perché `from` è una parola riservata in Python
    to: tuple
    turn: str  # `turn` rappresenterà una stringa che indica il turno (ad esempio "WHITE" o "BLACK")

    def __post_init__(self):
        # Validazione delle stringhe `from_` e `to`
        if len(self.from_) != 2 or len(self.to) != 2:
            raise InvalidParameterException(
                "The FROM and TO strings must have a length of 2"
            )

    def get_from(self) -> str:
        letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
        return letters[self.from_[0]] + str(self.from_[1] + 1)

    def set_from(self, from_: str):
        self.from_ = from_

    def get_to(self) -> str:
        letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
        return letters[self.to[0]] + str(self.to[1] + 1)

    def set_to(self, to: str):
        self.to = to

    def get_turn(self) -> str:
        return self.turn

    def set_turn(self, turn: str):
        self.turn = turn

    def __str__(self):
        return f"Turn: {self.turn} Pawn from {self.from_} to {self.to}"

    def get_column_from(self) -> int:
        """Restituisce l'indice della colonna da cui si muove il pedone."""
        return ord(self.from_[0].lower()) - 97

    def get_column_to(self) -> int:
        """Restituisce l'indice della colonna a cui si muove il pedone."""
        return ord(self.to[0].lower()) - 97

    def get_row_from(self) -> int:
        """Restituisce l'indice della riga da cui si muove il pedone."""
        return int(self.from_[1]) - 1

    def get_row_to(self) -> int:
        """Restituisce l'indice della riga a cui si muove il pedone."""
        return int(self.to[1]) - 1


    def is_good_enough(self, color, state, list_of_state_reached):
        file = ...
        stateCopy = state.clone()
        pawn_eaten = self.apply_action(color, state)

        '''#pawn_eaten = self.pawn_eaten(color, stateCopy, state)
        #king_safety = self.king_safety(color, stateCopy, state)'''

        if random.Random.random() < 0.9:
            list_of_state_reached.append(hash(stateCopy))
            return True
        return False
        ...

    def king_safety(self, color, stateCopy, originalState):
        new_board = stateCopy.board
        old_board = originalState.board




    # Questo può essere fatto direttamente nell'apply action
    def pawn_eaten(self, color, stateCopy, originalState):
        if color == "W":
            opponent_color = "B"
            return stateCopy.get_number_of(opponent_color) - originalState.get_number_of(opponent_color)
        else:
            opponent_color = "W"
            return stateCopy.get_number_of(opponent_color) - originalState.get_number_of(opponent_color)

    def apply_action(self, color, state):
        board = state.board
        if color == "W" or color == "K":
            opponent_color = "B"
        else:
            opponent_color = "W"

        camp =  [
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
            (4, 4)
        ]

        row_from = self.get_row_from()
        column_from = self.get_column_from()
        row_to = self.get_row_to()
        column_to = self.get_column_to()

        board[row_from][column_from] = "O"
        board[row_to][column_to] = color

        num_pawn_eaten = 0

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Alto, basso, sinistra, destra
        for dr, dc in directions:
            riga_intermedia = row_to + dr
            colonna_intermedia = column_to + dc
            riga_opposta = row_to + 2 * dr
            colonna_opposta = column_to + 2 * dc

            # Controlla che le coordinate siano valide
            if 0 <= riga_intermedia < len(board) and 0 <= colonna_intermedia < len(board[0]) and \
                    0 <= riga_opposta < len(board) and 0 <= colonna_opposta < len(board[0]):

                # Verifica se c'è una pedina avversaria circondata
                if board[riga_intermedia][colonna_intermedia] == opponent_color and \
                        board[riga_opposta][colonna_opposta] == color or (riga_opposta, colonna_opposta) in camp:
                    # "Mangia" la pedina avversaria
                    board[riga_intermedia][colonna_intermedia] = "O"
                    num_pawn_eaten += 1

                if color == "B":
                    upr = riga_intermedia - 1
                    upc = colonna_intermedia
                    downr = riga_intermedia + 1
                    downc = colonna_intermedia
                    lr = riga_intermedia
                    lc = colonna_intermedia - 1
                    rr = riga_intermedia
                    rc = colonna_intermedia + 1
                    if board[riga_intermedia][colonna_intermedia] == "K" and \
                            (board[upr][upc] == color or (upr, upc) in camp) and \
                            (board[downr][downc] == color or (downr, downc) in camp) and \
                            (board[lr][lc] == color or (lr, lc) in camp) and \
                            (board[rr][rc] == color or (rr,rc) in camp):
                        return 100
        return num_pawn_eaten



