"""
Python eye-control runner for launching supercomputer-style simulations.

This script provides a simple eye-input command loop and uses the existing
El Capitan simulation engine as the execution backend.
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator, Optional
from urllib import error, request

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
        raw = input("Eye event [LEFT/RIGHT/UP/DOWN/CENTER/BLINK/QUIT]: ").strip()
        if not raw:
            return None
        return raw


class ScriptedEyeInputSource(EyeInputSource):
    def __init__(self, events: Iterable[str]) -> None:
        self._events: Iterator[str] = iter(events)

    def next_event(self) -> Optional[str]:
        return next(self._events, "QUIT")


class ClaudeEventInterpreter:
    _KNOWN_EVENTS = {"LEFT", "RIGHT", "UP", "DOWN", "CENTER", "BLINK", "QUIT"}

    def __init__(self, enabled: bool, model: str, api_key_env: str) -> None:
        self.enabled = enabled
        self.model = model
        self.api_key = os.getenv(api_key_env, "")

    def to_event(self, raw_event: str) -> Optional[str]:
        text = raw_event.strip()
        if not text:
            return None

        simple = text.upper()
        if simple in self._KNOWN_EVENTS:
            return simple

        if self.enabled and self.api_key:
            interpreted = self._query_claude(text)
            if interpreted in self._KNOWN_EVENTS:
                return interpreted

        return self._fallback_event(text)

    def _query_claude(self, text: str) -> Optional[str]:
        payload = {
            "model": self.model,
            "max_tokens": 20,
            "temperature": 0,
            "system": (
                "Map the user's eye-tracking phrase to one token only: "
                "LEFT, RIGHT, UP, DOWN, CENTER, BLINK, or QUIT. "
                "Return only the token."
            ),
            "messages": [{"role": "user", "content": text}],
        }
        body = json.dumps(payload).encode("utf-8")
        req = request.Request(
            "https://api.anthropic.com/v1/messages",
            data=body,
            method="POST",
            headers={
                "content-type": "application/json",
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
            },
        )
        try:
            with request.urlopen(req, timeout=8) as resp:  # noqa: S310
                data = json.loads(resp.read().decode("utf-8"))
        except (error.URLError, TimeoutError, OSError, ValueError):
            return None

        content = data.get("content", [])
        if not content:
            return None
        text_out = str(content[0].get("text", "")).strip().upper()
        return text_out

    def _fallback_event(self, text: str) -> Optional[str]:
        t = text.lower()
        if "left" in t:
            return "LEFT"
        if "right" in t:
            return "RIGHT"
        if "up" in t or "increase" in t or "more" in t:
            return "UP"
        if "down" in t or "decrease" in t or "less" in t:
            return "DOWN"
        if "center" in t or "status" in t:
            return "CENTER"
        if "blink" in t or "start" in t or "run" in t:
            return "BLINK"
        if "quit" in t or "stop" in t or "exit" in t:
            return "QUIT"
        return None


class LineShineEyeRunner:
    def __init__(
        self,
        config: SimulationConfig,
        input_source: EyeInputSource,
        event_interpreter: ClaudeEventInterpreter,
    ) -> None:
        self.config = config
        self.input_source = input_source
        self.event_interpreter = event_interpreter
        self._armed_to_run = False

    def run(self) -> None:
        print("\nLineShine Eye Runner (Python)")
        print("Control simulation settings with eye events.")
        self._print_status()

        while True:
            raw_event = self.input_source.next_event()
            if raw_event is None:
                continue
            event = self.event_interpreter.to_event(raw_event)
            if event is None:
                print(f"Unknown event: {raw_event}")
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
    parser.add_argument(
        "--use-claude",
        action="store_true",
        help="Use Claude API to interpret free-form eye phrases into control commands.",
    )
    parser.add_argument(
        "--claude-model",
        default="claude-sonnet-4.6",
        help="Claude model name for event interpretation.",
    )
    parser.add_argument(
        "--anthropic-api-key-env",
        default="ANTHROPIC_API_KEY",
        help="Environment variable containing your Anthropic API key.",
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

    event_interpreter = ClaudeEventInterpreter(
        enabled=args.use_claude,
        model=args.claude_model,
        api_key_env=args.anthropic_api_key_env,
    )
    runner = LineShineEyeRunner(
        config=config,
        input_source=input_source,
        event_interpreter=event_interpreter,
    )
    runner.run()


if __name__ == "__main__":
    main()
