import json
import string
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
        from_ : str = action.get_from() 
        to_ : str   = action.get_to()
        turn : str  = action.get_turn()

        to_send = json.dumps({"from": from_,
                              "to": to_,
                              "turn": turn})

        socket.sendall(struct.pack('>I', len(to_send)))
        socket.sendall(to_send.encode('utf-8'))

    @staticmethod
    def read_state(socket):
        '''# Ricevi prima la lunghezza del messaggio
        length_bytes = socket.recv(4)  # Supponiamo che la lunghezza sia inviata come un intero di 4 byte
        if not length_bytes:
            raise ConnectionError("Connessione interrotta")

        # Converti la lunghezza da byte (big-endian) a un intero
        length = int.from_bytes(length_bytes, 'big')
        '''

        print("Ricevo")
        # Ricevi il messaggio JSON basato sulla lunghezza
        len_bytes = struct.unpack('>i', recvall(socket, 4))[0]
        current_state_server_bytes = socket.recv(len_bytes)
        print("Ricevuto")

        json_state = json.loads(current_state_server_bytes)

        #########################################################################
        # Convert to list
        data = list(json_state.items())
        # Convert to array
        ar = np.array(data, dtype=object)
        # Selecting board (the array is (2,2) matrix, it has board and turn info)
        board_array = np.array(ar[0, 1], dtype=object)
        turn = ar[1, 1]
        print(turn)
        # Converting in a numerical matrix
        board = np.zeros((9, 9), dtype=str)
        for i in range(0, 9):
            for j in range(0, 9):
                if board_array[i, j] == 'EMPTY':            # qua abbiamo supposto che ci diano 'EMPTY', 'WHITE', ecc
                    board[i, j] = "O" #State.State.Pawn.EMPTY#.value
                elif board_array[i, j] == 'WHITE':
                    board[i, j] = "W" #State.State.Pawn.WHITE#.value
                elif board_array[i, j] == 'BLACK':
                    board[i, j] = "B" #State.State.Pawn.BLACK#.value
                elif board_array[i, j] == 'KING':
                    board[i, j] = "K" #State.State.Pawn.KING#.value
                    king_position = (i, j)

        print(board)

        return board, turn


def recvall(sock, n):
    # Funzione ausiliaria per ricevere n byte o restituire None se viene raggiunta la fine del file (EOF)
    try:
        data = b''
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data += packet
        print(data)
        return data
    except ConnectionResetError:
        print("Partita finita")



