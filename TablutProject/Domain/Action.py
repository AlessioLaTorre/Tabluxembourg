import copy
import json
from dataclasses import dataclass
from typing import Union
import random
import os


parent_folder = os.path.abspath(os.getcwd())
#print('parent_folder: '+parent_folder)
statesValuesPath = os.path.join(parent_folder, 'TABLUT','Tabluxembourg','TablutProject','statesValues.json')
#print('states       : '+statesValuesPath)

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
        # impongo il movimento solo verticale o orizzontale
        if (self.from_[0] != self.to[0]) and (self.from_[1] != self.to[1]):
            raise InvalidParameterException(
                "The pawns can move just horizontally or vertically"
            )
        if len(self.from_) != 2 or len(self.to) != 2:
            raise InvalidParameterException(
                "The FROM and TO strings must have a length of 2"
            )
        # avrebbe senso verificare se effettivamente
        # abbiamo una pedina nella casella del from_?

    def get_from(self) -> str:
        # codifica la tupla di int in una stringa 'lettera int'
        letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
        # le lettere indicano la colonna
        # e.g. (3, 1) -> 'B4' 
        return letters[self.from_[1]] + str(self.from_[0] + 1)
    
    
    '''def set_from(self, from_: str):
        self.from_ = from_'''

    def get_to(self) -> str:
        # codifica la tupla di int in una stringa 'lettera int'
        letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
        # le lettere indicano la colonna
        # e.g. (3, 1) -> 'B4' 
        return letters[self.to[1]] + str(self.to[0] + 1)

    '''def set_to(self, to: str):
        self.to = to'''

    def get_turn(self) -> str:
        return self.turn

    '''def set_turn(self, turn: str):
        self.turn = turn'''

    def __str__(self):
        return f"Turn: {self.turn}. Pawn from {self.from_} to {self.to}"


    def get_column_from(self) -> int:
        """Restituisce l'indice della colonna da cui si muove il pedone."""
        # return ord(self.from_[0].lower()) - 97
        return self.from_[1]

    def get_column_to(self) -> int:
        """Restituisce l'indice della colonna a cui si muove il pedone."""
        # return ord(self.to[0].lower()) - 97
        return self.to[1]

    def get_row_from(self) -> int:
        """Restituisce l'indice della riga da cui si muove il pedone."""
        # return int(self.from_[1]) - 1
        return self.from_[0]

    def get_row_to(self) -> int:
        """Restituisce l'indice della riga a cui si muove il pedone."""
        # return int(self.to[1]) - 1
        return self.to[0]

    # togliamo color tutte le volte che c'è is_good_enough
    def is_good_enough(self, state, list_of_state_reached, isLast): #abbiamo tolto color (primo arg)
        with open(statesValuesPath, 'r') as f:
            file = json.load(f)
        stateCopy = state.clone()
        pawn_eaten = self.apply_action(stateCopy)

        '''#pawn_eaten = self.pawn_eaten(color, stateCopy, state)
        #king_safety = self.king_safety(color, stateCopy, state)'''

        hstate = hash(stateCopy)
        try:
            if file[hstate] > 0 and self.turn == 'WHITE':
                if random.random() > 0.6:
                    return True
            elif file[hstate] < 0 and self.turn == 'BLACK':
                if random.random() > 0.6:
                    return True
        except KeyError:
            pass
        if random.random() < 0.7 or isLast:
            list_of_state_reached.append(hstate)
            return True
        return False

    '''def king_safety(self, color, stateCopy, originalState):
        new_board = stateCopy.board
        old_board = originalState.board'''

    '''def pawn_eaten(self, stateCopy, originalState):
        color = originalState.turn
        if color == "W":
            opponent_color = "B"
            return stateCopy.get_number_of(opponent_color) - originalState.get_number_of(opponent_color)
        else:
            opponent_color = "W"
            return stateCopy.get_number_of(opponent_color) - originalState.get_number_of(opponent_color)'''

    def apply_action(self, state):
        color = state.turn
        board = state.board
        if color == "WHITE":
            opponent_color = "BLACK"
        else:
            opponent_color = "WHITE"

        camp =  [
            #Starting black + throne
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
        
        # coordinate da cui parte la pedina
        row_from    = self.get_row_from()
        column_from = self.get_column_from()
        row_to      = self.get_row_to()
        column_to   = self.get_column_to()

        state.remove_pawn(row_from, column_from)
        
        # aggiungi la pedina nella casella del to
        board[row_to][column_to] = color

        num_pawn_eaten = 0

        # definiamo le caselle in cui il re non viene mangiato come negli altri
        throne = [(4,4)]
        around_throne = [(4,3), (4,5), (3,4), (5,4)]

        # per capire se si mangiano delle pedine con la mossa
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Alto, basso, sinistra, destra
        for dr, dc in directions:
            riga_intermedia     = row_to + dr
            colonna_intermedia  = column_to + dc
            riga_opposta        = row_to + 2 * dr
            colonna_opposta     = column_to + 2 * dc

            # Controlla che le coordinate siano valide
            if 0 <= riga_intermedia < len(board) and 0 <= colonna_intermedia < len(board[0]) and \
                    0 <= riga_opposta < len(board) and 0 <= colonna_opposta < len(board[0]):

                # Verifica se c'è una pedina avversaria circondata
                if board[riga_intermedia][colonna_intermedia] == opponent_color and \
                        board[riga_opposta][colonna_opposta] == color or (riga_opposta, colonna_opposta) in camp:
                    # "Mangia" la pedina avversaria
                    #board[riga_intermedia][colonna_intermedia] = "O"

                    # verifichiamo se la pedina è il re
                    if board[riga_intermedia][colonna_intermedia] == "K":
                        # il K può esser mangiato normalmente se non è nelle caselle attorno al trono e sul trono
                        if (riga_intermedia, colonna_intermedia) not in throne + around_throne:
                            print("BLACK player wins")
                            return 100
                        
                    state.remove_pawn(row = riga_intermedia, column = colonna_intermedia)
                    num_pawn_eaten += 1

                # per verificare se il K è circondato nelle caselle speciali
                if color == "B":
                    if board[4][4] == "K":
                        # qua non so se va bene perché ho considerato che la casella fosse già "B"
                        # la seconda riga della condizione if è superflua se viene già cambiata la "O" in "B"
                        # sennò si può forse fare sum([board[r][c]=="B" for r,c in around_throne])>=3 and \....
                        if [board[r][c] for r,c in around_throne] == 4*["B"] and \
                            (row_to, column_to) in around_throne:
                            print("BLACK player wins")
                            return 100
                    # manca qui il caso in cui il re sia attorno a trono, i.e 
                    # if "K" in [board[r][c] for r,c in around_throne]:
                    #   e poi mettere le tre caselle adiacenti (forse è comodo sapere quali sono gli r,c per cui si verifica la condizione)
                
                            


                
                '''if color == "B":
                    
                    upr     = riga_intermedia - 1
                    upc     = colonna_intermedia
                    downr   = riga_intermedia + 1
                    downc   = colonna_intermedia
                    lr  = riga_intermedia
                    lc  = colonna_intermedia - 1
                    rr  = riga_intermedia
                    rc  = colonna_intermedia + 1
                    if board[riga_intermedia][colonna_intermedia] == "K" and \
                            (board[upr][upc] == color or (upr, upc) in camp) and \
                            (board[downr][downc] == color or (downr, downc) in camp) and \
                            (board[lr][lc] == color or (lr, lc) in camp) and \
                            (board[rr][rc] == color or (rr,rc) in camp):
                        return 100'''
        return num_pawn_eaten




    #SOLO PER PROVA PER VEDERE SE AGGIUNGE STATI AL FILE
    def win(self, state):
        if self.turn == "WHITE":
            winning_position = [
                (0, 1),
                (0, 2),
                (0, 6),
                (0, 7),
                (8, 1),
                (8, 2),
                (8, 6),
                (8, 7),
                (1, 0),
                (2, 0),
                (6, 0),
                (7, 0),
                (1, 8),
                (2, 8),
                (6, 8),
                (7, 8),
            ]
            if state.board[self.from_[0]][self.from_[1]] == "K" and \
                    self.to in winning_position:
                return True
        else:
            stateCopy = state.clone()
            king_eaten = self.apply_action(stateCopy)
            if king_eaten == 100:
                return True
            return False






