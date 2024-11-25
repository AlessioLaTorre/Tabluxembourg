import socket
import json
import struct

from TablutProject.Utils.Utils import StreamUtils
from TablutProject.State import State


class TablutClient:
    def __init__(self, player, name, timeout=60, ip_address="localhost"):
        """
        Initializes a new player, setting up sockets and configuration.

        :param player: Role of the player ("black" or "white")
        :param name: Name of the player
        :param timeout: Timeout in seconds (default is 60)
        :param ip_address: IP address of the server (default is "localhost")
        """
        self.list_of_state_reached = []
        self.name = name
        self.timeout = timeout
        self.server_ip = ip_address
        self.current_state: State = State.State() # (prima era None)

        if player.lower() == "white":
            self.player = "WHITE"
            self.port = Configuration.white_port
        elif player.lower() == "black":
            self.player = "BLACK"
            self.port = Configuration.black_port
        else:
            raise ValueError("Player role must be 'black' or 'white'")

        # Setting up the socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(self.timeout)
        print(f"Connessione al server {self.server_ip}:{self.port}")
        self.socket.connect((self.server_ip, self.port))
        print("Connessione effettuata")

    def write(self, action):
        """
        Sends an action to the server.

        :param action: The action to send (dictionary or object serializable to JSON)
        """
        StreamUtils.send_action(self.socket, action)

    def declare_name(self):
        """
        Sends the player's name to the server.
        """
        print(f"Invio nome {self.name}")
        #json_name = json.dumps(self.name)
        #self.socket.sendall(json_name.encode('utf-8'))
        encoded_string = self.name.encode('utf-8')

        # Calcola la lunghezza della stringa
        length = len(encoded_string)

        # Invia la lunghezza come un intero (big-endian)
        self.socket.sendall(struct.pack('>I', length))

        # Invia la stringa codificata in UTF-8
        self.socket.sendall(encoded_string)

        print("Invio nome effettuato")

    def read(self):
        """
        Reads the current state from the server and updates the local state.
        """
        board, turn = StreamUtils.read_state(self.socket)
        self.current_state.set_board(board)
        self.current_state.set_turn(turn)

    def close(self):
        """
        Closes the connection to the server.
        """
        self.socket.close()


# Example Configuration class for port definitions
class Configuration:
    white_port = 5800
    black_port = 5801
