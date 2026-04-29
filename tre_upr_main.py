"""
TRE-UPR Entry Point
Run this script to start the Transcendent Reality Engine – Universal Propagation Reactor.

Usage:
    python tre_upr_main.py           # interactive mode (step through generations
    python tre_upr_main.py --seed 7  # set a custom random seed
"""

import argparse
import sys

from tre_upr import TREUPRDevice


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="tre_upr_main.py",
        description="TRE-UPR: Transcendent Reality Engine – Universal Propagation Reactor",
    )
    parser.add_argument(
        "--auto",
        action="store_true",
        help="Run all generations automatically without pausing.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Integer seed for the random universe generator (default: 92).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    device = TREUPRDevice(seed=args.seed)
    device.boot()

    try:
        if args.auto:
            device.run_auto()
        else:
            device.run_interactive()
    except KeyboardInterrupt:
        print("\n")
        device.shutdown()
        sys.exit(0)


if __name__ == "__main__":
    main()
