from dataclasses import dataclass
from typing import Union


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
