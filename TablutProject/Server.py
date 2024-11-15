import socket
import json
import logging
import threading
from datetime import datetime, timedelta

# Configurazione di logging
logging.basicConfig(filename="system_log.txt", level=logging.DEBUG, format="%(asctime)s - %(message)s")
logger = logging.getLogger()

# Costanti per configurazione
WHITE_PORT = 5800
BLACK_PORT = 5801
CONNECTION_TIMEOUT = 300  # in secondi
MOVE_TIMEOUT = 60  # Tempo massimo per una mossa


class Server:
    def __init__(self, move_time=60, cache_size=-1, errors=0, repeated=0, game_type=4, enable_gui=True):
        self.time = move_time
        self.cache_size = cache_size
        self.errors_allowed = errors
        self.repeated = repeated
        self.game_type = game_type
        self.enable_gui = enable_gui

        self.state = None  # Stato del gioco
        self.white_socket = None
        self.black_socket = None
        self.white_name = "WP"
        self.black_name = "BP"
        self.white_errors = 0
        self.black_errors = 0
        self.endgame = False

    def start_server(self):
        logger.info("Avvio del server...")
        self.state = self.initialize_game_state()

        # Configurazione delle connessioni
        self.white_socket = self.accept_connection(WHITE_PORT, "White")
        self.white_name = self.read_name(self.white_socket, "White")

        self.black_socket = self.accept_connection(BLACK_PORT, "Black")
        self.black_name = self.read_name(self.black_socket, "Black")

        # Invio stato iniziale ai giocatori
        self.send_state(self.white_socket)
        self.send_state(self.black_socket)

        # Ciclo principale del gioco
        self.game_loop()

    def accept_connection(self, port, player):
        logger.info(f"In attesa della connessione del giocatore {player} sulla porta {port}...")
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("", port))
        server_socket.listen(1)

        server_socket.settimeout(CONNECTION_TIMEOUT)
        try:
            client_socket, addr = server_socket.accept()
            logger.info(f"Connessione accettata per il giocatore {player} da {addr}")
            return client_socket
        except socket.timeout:
            logger.error(f"Timeout per il giocatore {player}.")
            exit(1)

    def read_name(self, client_socket, player):
        logger.info(f"Lettura del nome del giocatore {player}...")
        try:
            data = client_socket.recv(1024).decode()
            player_name = json.loads(data)
            logger.info(f"Nome ricevuto per il giocatore {player}: {player_name}")
            return player_name
        except Exception as e:
            logger.error(f"Errore durante la lettura del nome del giocatore {player}: {e}")
            exit(1)

    def send_state(self, client_socket):
        try:
            state_json = json.dumps(self.state)
            client_socket.sendall(state_json.encode())
        except Exception as e:
            logger.error(f"Errore nell'invio dello stato del gioco: {e}")
            exit(1)

    def game_loop(self):
        start_time = datetime.now()
        while not self.endgame:
            if (datetime.now() - start_time).seconds > 3600 * 10:  # Limite di 10 ore
                logger.warning("Timeout della partita.")
                self.state["turn"] = "DRAW"
                self.endgame = True
                break

            # Ciclo delle mosse dei giocatori
            current_turn = self.state["turn"]
            logger.info(f"Turno del giocatore {current_turn}...")
            client_socket = self.white_socket if current_turn == "WHITE" else self.black_socket
            action = self.receive_action(client_socket)

            try:
                self.state = self.process_move(action)
                self.send_state(self.white_socket)
                self.send_state(self.black_socket)
            except Exception as e:
                logger.error(f"Errore durante la gestione della mossa del giocatore {current_turn}: {e}")
                if current_turn == "WHITE":
                    self.white_errors += 1
                    if self.white_errors > self.errors_allowed:
                        logger.info("Troppi errori per il giocatore White, Black vince!")
                        self.state["turn"] = "BLACKWIN"
                        self.endgame = True
                else:
                    self.black_errors += 1
                    if self.black_errors > self.errors_allowed:
                        logger.info("Troppi errori per il giocatore Black, White vince!")
                        self.state["turn"] = "WHITEWIN"
                        self.endgame = True

    def receive_action(self, client_socket):
        logger.info("Ricezione della mossa dal client...")
        client_socket.settimeout(MOVE_TIMEOUT)
        try:
            data = client_socket.recv(1024).decode()
            action = json.loads(data)
            logger.info(f"Mossa ricevuta: {action}")
            return action
        except socket.timeout:
            logger.error("Timeout durante la ricezione della mossa.")
            exit(1)
        except Exception as e:
            logger.error(f"Errore nella ricezione della mossa: {e}")
            exit(1)

    def process_move(self, action):
        # Processa la mossa (placeholder, implementare la logica del gioco)
        logger.info(f"Processo la mossa: {action}")
        #TODO
        return self.state

    def initialize_game_state(self):
        # Inizializza lo stato del gioco (placeholder, implementare la logica
        #TODO
        return {"turn": "WHITE"}


if __name__ == "__main__":
    server = Server()
    server.start_server()
