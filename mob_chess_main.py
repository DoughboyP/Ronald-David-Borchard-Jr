"""
MOB CHESS: Universe Control – Entry Point

Two Gods play a multidimensional chess match with the entire universe as
the board. You are a Demigod rising in the cracks between their moves.
Collect bodies, wear them, and run the whole universe on mob pimp shit.

Usage:
    python mob_chess_main.py
    python mob_chess_main.py --seed 42
"""

import argparse
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="mob_chess_main.py",
        description="MOB CHESS: Universe Control",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for a reproducible universe (default: random).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    from mob_chess import MobChessGame
    game = MobChessGame(seed=args.seed)

    try:
        game.run()
    except KeyboardInterrupt:
        print("\n\n  Peace out.\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
