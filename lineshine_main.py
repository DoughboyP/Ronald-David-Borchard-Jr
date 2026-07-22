"""
Lineshine Entry Point
Run this script to launch the Lineshine world-creation engine with Ra's Eye.

Usage
-----
    python3 lineshine_main.py                              # interactive mode (default)
    python3 lineshine_main.py --seed 42                   # custom random seed
    python3 lineshine_main.py --log-level DEBUG           # verbose logging
    python3 lineshine_main.py --save-file worlds.json     # auto-save/load worlds
"""

import argparse
import logging
import sys

from lineshine import LineshineComputer


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="lineshine_main.py",
        description=(
            "Lineshine – World-Creation Engine  |  "
            "Shenzhen, China  |  Ra's Eye: INSTALLED"
        ),
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=2025,
        help="Master random seed for reproducibility (default: 2025).",
    )
    parser.add_argument(
        "--log-level",
        default="WARNING",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging verbosity (default: WARNING).",
    )
    parser.add_argument(
        "--save-file",
        default=None,
        metavar="FILE",
        help=(
            "JSON file for world persistence. "
            "Worlds are loaded from this file on boot and saved to it on shutdown."
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
        level=getattr(logging, args.log_level.upper(), logging.WARNING),
        stream=sys.stdout,
    )

    computer = LineshineComputer(seed=args.seed, save_file=args.save_file)
    computer.boot()

    try:
        computer.run_interactive()
    except KeyboardInterrupt:
        print()
        computer.shutdown()
        sys.exit(0)


if __name__ == "__main__":
    main()
