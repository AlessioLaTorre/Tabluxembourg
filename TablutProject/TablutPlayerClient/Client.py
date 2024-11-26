import sys
import os
import numpy as np
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

parent_folder = os.path.abspath(os.getcwd())
#print('parent_folder: '+parent_folder)
statesValuesPath = os.path.join(parent_folder, 'TABLUT','Tabluxembourg','TablutProject','statesValues.json')
#print('states       : '+statesValuesPath)


from AbstractClient import TablutClient
from TablutProject.State import State
import time
import random
import argparse
from TablutProject.Utils.Utils import StreamUtils

class TablutPlayerClient(TablutClient):

    def play(self):

        while True:
            self.read()
            # ho aggiunto 'moves per leggibilità
            print(f"Current state:\n{self.current_state} moves")

            #print(f"Turn: {self.current_state.turn}")

            if self.player == "WHITE":
                if self.current_state.turn == "WHITE":
                    action_to_send = self.choose_action()

                    print(f"Ammissible action: {action_to_send}")
                    self.write(action_to_send)
                    print(f"messaggio inviato")


                    ##DA CAMBIARE
                    if action_to_send.win(self.current_state):
                        self.aggiorna_file(True)

                elif self.current_state.Turn.BLACK == self.current_state.get_turn():
                    print("Waiting for opponent move ... ")
                    break
                elif self.current_state.Turn.BLACKWIN == self.current_state.get_turn():
                    self.aggiorna_file(False)
                    print("YOU LOSE")
                    break
                elif self.current_state.Turn.WHITEWIN == self.current_state.get_turn():
                    self.aggiorna_file(True)
                    print("YOU WIN")
                    break
                elif self.current_state.Turn.DRAW == self.current_state.get_turn():
                    print("DRAW")
                    break

            else: # se siamo i neri
                if self.current_state.turn == "BLACK": #se è il turno dei neri
                    action_to_send = self.choose_action()
                    print(f"Ammissible action: {action_to_send}")
                    self.write(action_to_send)

                    if action_to_send.win(self.current_state):
                        self.aggiorna_file(True)

                elif self.current_state.Turn.WHITE == self.current_state.get_turn():
                    print("Waiting for opponent move ... ")
                    break
                elif self.current_state.Turn.BLACKWIN == self.current_state.get_turn():
                    self.aggiorna_file(True)
                    print("YOU WIN")
                    break
                elif self.current_state.Turn.WHITEWIN == self.current_state.get_turn():
                    self.aggiorna_file(False)
                    print("YOU LOSE")
                    break
                elif self.current_state.Turn.DRAW == self.current_state.get_turn():
                    print("DRAW")



    def choose_action(self):
        ammissible_actions = self.current_state.ammissible_actions()
        r = np.arange(len(ammissible_actions))
        np.random.shuffle(r)
        '''
        Essendo la selezione random metto un contatore per far si che quando arrivo all'ultima
        azione venga presa obbligatoriamente per avere un'azione da inviare'''
        count = 0
        isLast = False
        for i in r:
            count += 1
            if count == len(ammissible_actions) - 1:
                isLast = True
            action = ammissible_actions[i]
            print(f"Ammissible action: {action}")
            if action.is_good_enough(self.current_state, self.list_of_state_reached, isLast):
                return action



    def aggiorna_file(self, win: bool):
        with open(statesValuesPath, 'r') as f:
            dati = json.load(f)
        if win:
            if self.player == "WHITE":
                for st in self.list_of_state_reached:
                    dati[st] = dati.get(st, 0) + 1

                with open(statesValuesPath, 'w') as f:
                    json.dump(dati, f, indent=4)
            else: # se siamo i neri e abbiamo vinto
                for st in self.list_of_state_reached:
                    dati[st] = dati.get(st, 0) - 1

                with open(statesValuesPath, 'w') as f:
                    json.dump(dati, f, indent=4)
        else:
            if self.player == "WHITE":
                for st in self.list_of_state_reached:
                    dati[st] = dati.get(st, 0) - 1

                with open(statesValuesPath, 'w') as f:
                    json.dump(dati, f, indent=4)
            else: # se siamo i neri e abbiamo perso
                for st in self.list_of_state_reached:
                    dati[st] = dati.get(st, 0) + 1

                with open(statesValuesPath, 'w') as f:
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
        default="localhost",
    )

    args = parser.parse_args()

    example = TablutPlayerClient(args.player, "Tabluxemburg", int(args.timeout), args.ip)
    example.declare_name()

    example.play()
