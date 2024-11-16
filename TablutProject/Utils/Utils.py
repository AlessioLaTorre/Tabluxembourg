import json
import struct
from TablutProject.State import State
import numpy as np

class StreamUtils:
    @staticmethod
    def write_string(socket, string):
        """
        Scrive una stringa su una socket.
        Invio prima la lunghezza in byte della stringa e poi la stringa stessa in UTF-8.
        """
        # Converti la stringa in byte UTF-8
        bytes_data = string.encode('utf-8')
        # Calcola la lunghezza dei byte
        length = len(bytes_data)
        # Invia la lunghezza come un intero a 4 byte (big-endian)
        socket.sendall(struct.pack('>I', length))
        # Invia i byte della stringa
        socket.sendall(bytes_data)

    @staticmethod
    def read_string(socket):
        """
        Legge una stringa da una socket.
        Legge prima la lunghezza in byte della stringa e poi la stringa stessa in UTF-8.
        """
        # Leggi i primi 4 byte (lunghezza della stringa)
        length_data = socket.recv(4)
        if not length_data:
            raise ConnectionError("La connessione è stata chiusa durante la lettura della lunghezza.")
        # Decodifica la lunghezza (big-endian)
        length = struct.unpack('>I', length_data)[0]
        # Leggi i byte della stringa
        string_data = socket.recv(length)
        if len(string_data) < length:
            raise IOError("Errore durante la lettura dei dati: numero di byte inferiore a quello atteso.")
        # Decodifica i byte in una stringa UTF-8
        return string_data.decode('utf-8')

    @staticmethod
    def send_action(socket, action):
        from_ = action.get_from()
        to_ = action.get_to()
        turn = action.get_turn()

        to_send = json.dumps({"from": from_,
                              "to": to_,
                              "turn": turn})

        socket.send(struct.pack('>I', len(to_send)))
        socket.send(to_send.encode('utf-8'))

    @staticmethod
    def read_state(socket):
        '''# Ricevi prima la lunghezza del messaggio
        length_bytes = socket.recv(4)  # Supponiamo che la lunghezza sia inviata come un intero di 4 byte
        if not length_bytes:
            raise ConnectionError("Connessione interrotta")

        # Converti la lunghezza da byte (big-endian) a un intero
        length = int.from_bytes(length_bytes, 'big')
        '''

        # Ricevi il messaggio JSON basato sulla lunghezza
        json_state = recvall(socket, 4)


        #########################################################################
        # Convert to list
        data = list(json_state.items())
        # Convert to array
        ar = np.array(data, dtype=object)
        # Selecting board (the array is (2,2) matrix, it has board and turn info)
        board_array = np.array(ar[0, 1], dtype=object)
        turn = ar[1, 1]
        # Converting in a numerical matrix
        board = np.zeros((9, 9), dtype=State.Pawn)
        for i in range(0, 9):
            for j in range(0, 9):
                if board_array[i, j] == 'EMPTY':
                    board[i, j] = State.Pawn.EMPTY.value
                elif board_array[i, j] == 'WHITE':
                    board[i, j] = State.Pawn.WHITE.value
                elif board_array[i, j] == 'BLACK':
                    board[i, j] = State.Pawn.BLACK.value
                elif board_array[i, j] == 'KING':
                    board[i, j] = State.Pawn.KING.value
                    king_position = (i, j)


        return board, turn


def recvall(sock, n):
    # Funzione ausiliaria per ricevere n byte o restituire None se viene raggiunta la fine del file (EOF)
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data


