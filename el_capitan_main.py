"""
El Capitan Entry Point
Run this script to launch the El Capitan world-simulation engine.

Usage
-----
    python3 el_capitan_main.py                          # interactive mode
    python3 el_capitan_main.py --auto                   # run all ticks automatically
    python3 el_capitan_main.py --auto --worlds 5 --ticks 100
    python3 el_capitan_main.py --auto --seed 42 --log-level DEBUG
"""

import argparse
import logging
import sys

from el_capitan import ElCapitan


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="el_capitan_main.py",
        description=(
            "El Capitan – World Simulation Engine  |  "
            "Lawrence Livermore National Laboratory, Livermore, CA"
        ),
    )
    parser.add_argument(
        "--auto",
        action="store_true",
        help="Run all ticks automatically without pausing (default: interactive).",
    )
    parser.add_argument(
        "--worlds",
        type=int,
        default=3,
        metavar="N",
        help="Number of Earth-like worlds to simulate (default: 3).",
    )
    parser.add_argument(
        "--ticks",
        type=int,
        default=50,
        metavar="T",
        help="Total simulation ticks to run (default: 50).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=2024,
        help="Master random seed for reproducibility (default: 2024).",
    )
    parser.add_argument(
        "--log-level",
        default="WARNING",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging verbosity (default: WARNING).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    log_level = getattr(logging, args.log_level.upper(), logging.WARNING)

    engine = ElCapitan(
        num_worlds=args.worlds,
        ticks=args.ticks,
        seed=args.seed,
        log_level=log_level,
    )
    engine.boot()

    try:
        if args.auto:
            engine.run_auto()
        else:
            engine.run_interactive()
    except KeyboardInterrupt:
        print("\n")
        engine.shutdown()
        sys.exit(0)


if __name__ == "__main__":
    main()
