"""
TRE-UPR Device
Top-level orchestrator that boots the device, manages the self-building
engine, and exposes the interactive console interface.
"""

import sys
from typing import Optional

from .constants import (
    DEVICE_FULL_NAME,
    DEVICE_NAME,
    DEVICE_VERSION,
    LOG_PREFIX,
    MAX_GENERATIONS,
)
from .engine import SelfBuildingEngine


_BANNER = r"""
 _____ ____  _____       _   _ ____  ____
|_   _|  _ \| ____|     | | | |  _ \|  _ \
  | | | |_) |  _| ______| | | | |_) | |_) |
  | | |  _ <| |__|______| |_| |  __/|  _ <
  |_| |_| \_|_____|      \___/|_|   |_| \_\

  Transcendent Reality Engine – Universal Propagation Reactor
  Version {version}  ·  All realities simulated within are fictional.
"""


class TREUPRDevice:
    """
    The TRE-UPR device.

    It boots from a cold state, spins up its self-building engine, and
    iteratively creates, simulates, and expands universes across multiple
    generations – each one more complex than the last.
    """

    def __init__(self, seed: Optional[int] = None) -> None:
        from .constants import BOOTSTRAP_SEED
        self._seed = seed if seed is not None else BOOTSTRAP_SEED
        self._engine: Optional[SelfBuildingEngine] = None
        self._booted = False

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def boot(self) -> None:
        """Power on the TRE-UPR device."""
        print(_BANNER.format(version=DEVICE_VERSION))
        print(f"{LOG_PREFIX} Booting {DEVICE_FULL_NAME}...")
        print(f"{LOG_PREFIX} Seed: {self._seed}")
        self._engine = SelfBuildingEngine(seed=self._seed)
        self._booted = True
        print(f"{LOG_PREFIX} ✅ Device online. Ready to generate universes.\n")

    def shutdown(self) -> None:
        """Power off the device gracefully."""
        print(f"\n{LOG_PREFIX} Initiating shutdown sequence...")
        if self._engine:
            completed = len(self._engine.reports)
            total_universes = sum(
                len(r.universes) for r in self._engine.reports
            )
            sentient = sum(
                r.sentient_count for r in self._engine.reports
            )
            print(f"{LOG_PREFIX} Generations completed : {completed}")
            print(f"{LOG_PREFIX} Total universes created: {total_universes}")
            print(f"{LOG_PREFIX} Universes with sentience: {sentient}")
        print(f"{LOG_PREFIX} 🛑 TRE-UPR powered down.\n")

    # ------------------------------------------------------------------
    # Operation modes
    # ------------------------------------------------------------------

    def run_auto(self) -> None:
        """Run all generations automatically until natural sip."""
        self._require_boot()
        print(f"{LOG_PREFIX} AUTO mode – running all generations...\n")
        self._engine.run_all()
        self.shutdown()

    def run_interactive(self) -> None:
        """Step through generations interactively."""
        self._require_boot()
        print(f"{LOG_PREFIX} INTERACTIVE mode – press ENTER to advance each generation.")
        print(f"{LOG_PREFIX} Type 'q' or 'quit' to shut down.\n")

        while self._engine.generation < MAX_GENERATIONS:
            cmd = input(
                f"{LOG_PREFIX} [Generation {self._engine.generation}] "
                f"Press ENTER to run, or 'q' to quit: "
            ).strip().lower()

            if cmd in ("q", "quit"):
                break

            report, should_continue = self._engine.run_generation()
            print(report.summary())

            if not should_continue:
                print(f"{LOG_PREFIX} Engine reports natural halt.")
                break

        self.shutdown()

    def run_single_generation(self) -> bool:
        """Run exactly one generation. Returns True if device can continue."""
        self._require_boot()
        report, should_continue = self._engine.run_generation()
        print(report.summary())
        return should_continue

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _require_boot(self) -> None:
        if not self._booted:
            raise RuntimeError(
                f"{DEVICE_NAME} must be booted before operation. Call .boot() first."
            )

    @property
    def is_booted(self) -> bool:
        return self._booted

    @property
    def current_generation(self) -> int:
        return self._engine.generation if self._engine else 0
