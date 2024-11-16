import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


from AbstractClient import TablutClient
from TablutProject.State import State
import time
import random
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Client for Tablut")
    parser.add_argument(
        "-p",
        "--player",
        help="Player role (white or black)",
        required=True,
        choices=["white", "black"],
    )
    parser.add_argument(
        "-t",
        "--timeout",
        help="Timeout in seconds",
        required=True,
    )
    parser.add_argument(
        "-i",
        "--ip",
        help="IP address of the server",
        required=True,
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
