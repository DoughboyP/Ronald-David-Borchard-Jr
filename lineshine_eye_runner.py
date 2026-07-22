"""
Python eye-control runner for launching supercomputer-style simulations.

This script provides a simple eye-input command loop and uses the existing
El Capitan simulation engine as the execution backend.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator, Optional

from el_capitan import ElCapitan


@dataclass
class SimulationConfig:
    worlds: int
    ticks: int
    seed: int


class EyeInputSource:
    def next_event(self) -> Optional[str]:
        raise NotImplementedError


class ConsoleEyeInputSource(EyeInputSource):
    def next_event(self) -> Optional[str]:
        raw = input("Eye event [LEFT/RIGHT/UP/DOWN/CENTER/BLINK/QUIT]: ").strip().upper()
        if not raw:
            return None
        return raw


class ScriptedEyeInputSource(EyeInputSource):
    def __init__(self, events: Iterable[str]) -> None:
        self._events: Iterator[str] = iter(events)

    def next_event(self) -> Optional[str]:
        return next(self._events, "QUIT")


class LineShineEyeRunner:
    def __init__(self, config: SimulationConfig, input_source: EyeInputSource) -> None:
        self.config = config
        self.input_source = input_source
        self._armed_to_run = False

    def run(self) -> None:
        print("\nLineShine Eye Runner (Python)")
        print("Control simulation settings with eye events.")
        self._print_status()

        while True:
            event = self.input_source.next_event()
            if event is None:
                continue

            if event in {"QUIT", "Q", "EXIT"}:
                print("Stopping eye-control session.")
                return

            handled = self._handle_event(event)
            if not handled:
                print(f"Unknown event: {event}")

    def _handle_event(self, event: str) -> bool:
        if event == "LEFT":
            self.config.worlds = max(1, self.config.worlds - 1)
            self._armed_to_run = False
            self._print_status()
            return True
        if event == "RIGHT":
            self.config.worlds = min(20, self.config.worlds + 1)
            self._armed_to_run = False
            self._print_status()
            return True
        if event == "UP":
            self.config.ticks = min(5000, self.config.ticks + 10)
            self._armed_to_run = False
            self._print_status()
            return True
        if event == "DOWN":
            self.config.ticks = max(10, self.config.ticks - 10)
            self._armed_to_run = False
            self._print_status()
            return True
        if event == "CENTER":
            self._armed_to_run = False
            self._print_status()
            return True
        if event == "BLINK":
            if self._armed_to_run:
                self._armed_to_run = False
                self._launch_simulation()
            else:
                self._armed_to_run = True
                print("Run armed. Blink again to start simulation.")
            return True
        return False

    def _print_status(self) -> None:
        print(
            f"Config -> worlds={self.config.worlds}, "
            f"ticks={self.config.ticks}, seed={self.config.seed}"
        )

    def _launch_simulation(self) -> None:
        print("Launching simulation backend...")
        engine = ElCapitan(
            num_worlds=self.config.worlds,
            ticks=self.config.ticks,
            seed=self.config.seed,
        )
        engine.boot()
        engine.run_auto()
        print("Simulation complete. Eye control is active again.")


def _load_script_events(path: Path) -> list[str]:
    events: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        event = line.strip().upper()
        if event and not event.startswith("#"):
            events.append(event)
    return events


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Use eye-input events to control and launch LineShine-style "
            "supercomputer simulations from Python."
        )
    )
    parser.add_argument("--worlds", type=int, default=3, help="Initial world count.")
    parser.add_argument("--ticks", type=int, default=50, help="Initial simulation ticks.")
    parser.add_argument("--seed", type=int, default=2024, help="Simulation random seed.")
    parser.add_argument(
        "--script",
        type=Path,
        help="Optional file with one eye event per line for non-interactive runs.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = SimulationConfig(
        worlds=max(1, args.worlds),
        ticks=max(10, args.ticks),
        seed=args.seed,
    )

    if args.script:
        events = _load_script_events(args.script)
        input_source: EyeInputSource = ScriptedEyeInputSource(events)
    else:
        input_source = ConsoleEyeInputSource()

    runner = LineShineEyeRunner(config=config, input_source=input_source)
    runner.run()


if __name__ == "__main__":
    main()
