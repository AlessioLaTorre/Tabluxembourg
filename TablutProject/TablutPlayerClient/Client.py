import sys
import os
import numpy as np
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


from AbstractClient import TablutClient
from TablutProject.State import State
import time
import random
import argparse
from TablutProject.Utils.Utils import StreamUtils

class TablutPlayerClient(TablutClient):
    list_of_state_reached: list

    def play(self):

        while True:
            board, turn = StreamUtils.read_state(self.socket)
            self.current_state.set_board(board)
            self.current_state.set_turn(turn)

            print(f"Current state: {self.current_state}")

            print(f"Turn: {self.current_state.turn}")

            if self.player == "WHITE":
                if self.current_state.turn == "W":
                    ammisible_actions = self.current_state.ammisible_actions("W")
                    r = np.arange(len(ammisible_actions))
                    np.random.shuffle(r)
                    for i in r:
                        action = ammisible_actions[i]
                        if action.is_good_enough(self.player, self.current_state, self.list_of_state_reached):
                            StreamUtils.send_action(self.socket, action)
                            break
                    ...
                elif self.current_state.turn.BLACK == self.current_state.get_turn():
                    print("Waiting for opponent move ... ")
                    break
                elif self.current_state.turn.BLACKWIN == self.current_state.get_turn():
                    self.aggiorna_file(False)
                    print("YOU LOSE")
                    break
                elif self.current_state.turn.WHITEWIN == self.current_state.get_turn():
                    self.aggiorna_file(True)
                    print("YOU WIN")
                    break
                elif self.current_state.turn.DRAW == self.current_state.get_turn():
                    print("DRAW")
                    break

            else:
                if self.current_state.turn == "B":
                    ...
                elif self.current_state.turn.WHITE == self.current_state.get_turn():
                    print("Waiting for opponent move ... ")
                elif self.current_state.turn.BLACKWIN == self.current_state.get_turn():
                    self.aggiorna_file(True)
                    print("YOU WIN")
                    break
                elif self.current_state.turn.WHITEWIN == self.current_state.get_turn():
                    self.aggiorna_file(False)
                    print("YOU LOSE")
                    break
                elif self.current_state.turn.DRAW == self.current_state.get_turn():
                    print("DRAW")


def aggiorna_file(self, win):
    with open('data.json', 'r') as f:
        dati = json.load(f)
    if win:
        if self.player == "WHITE":
            for st in self.list_of_state_reached:
                dati[st] = dati.get(st, 0) + 1

            with open('data.json', 'w') as f:
                json.dump(dati, f, indent=4)
        else:
            for st in self.list_of_state_reached:
                dati[st] = dati.get(st, 0) - 1

            with open('data.json', 'w') as f:
                json.dump(dati, f, indent=4)
    else:
        if self.player == "WHITE":
            for st in self.list_of_state_reached:
                dati[st] = dati.get(st, 0) - 1

            with open('data.json', 'w') as f:
                json.dump(dati, f, indent=4)
        else:
            for st in self.list_of_state_reached:
                dati[st] = dati.get(st, 0) + 1

            with open('data.json', 'w') as f:
                json.dump(dati, f, indent=4)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Client for Tablut")
    parser.add_argument(
        "-p",
        "--player",
        help="Player role (white or black)",
        required=True,
        choices=["white", "black"],
        default="white"
    )
    parser.add_argument(
        "-t",
        "--timeout",
        help="Timeout in seconds",
        required=True,
        default=60,
    )
    parser.add_argument(
        "-i",
        "--ip",
        help="IP address of the server",
        required=True,
        default="127.0.0.1",
    )

    args = parser.parse_args()

    example = TablutClient(args.player, "Tabluxemburg", int(args.timeout), args.ip)
    example.declare_name()

    while True:
        # Legge lo stato attuale
        example.read()
        print(example.current_state)

        # Pensa a una mossa
        action = State.Pawn.from_string(input("Inserisci la mossa: "))

        # Aggiorna lo stato
        example.current_state.apply_move(action)

        # Invia la mossa al server
        example.write(action)

        time.sleep(1)
