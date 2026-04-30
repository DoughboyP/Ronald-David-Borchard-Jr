"""
El Capitan – Supercomputer
Top-level orchestrator for the El Capitan world-simulation engine.

El Capitan is modelled after the Lawrence Livermore National Laboratory
supercomputer of the same name.  This Python module lets it simulate
multiple Earth-like worlds using a triple-processing architecture.
"""

from __future__ import annotations

import logging
import random
import sys
from typing import List, Optional

from .constants import (
    COMPUTER_FULL_NAME,
    COMPUTER_LOCATION,
    COMPUTER_NAME,
    COMPUTER_VERSION,
    DEFAULT_NUM_WORLDS,
    DEFAULT_SEED,
    DEFAULT_SIMULATION_TICKS,
    LINE_WIDTH,
    LOG_PREFIX,
    WORLD_NAME_POOL,
)
from .models import World
from .processor import TripleProcessor

logger = logging.getLogger(__name__)


_BANNER = r"""
  _____ _    ____    _    ____  ___ _____  _    _   _
 | ____| |  / ___|  / \  |  _ \|_ _|_   _|/ \  | \ | |
 |  _| | | | |     / _ \ | |_) || |  | | / _ \ |  \| |
 | |___| |_| |___ / ___ \|  __/ | |  | |/ ___ \| |\  |
 |_____|_____\____/_/   \_\_|  |___| |_/_/   \_\_| \_|

  {full_name}
  Location : {location}
  Mission  : Simulate Earth-like worlds using triple-processing architecture
"""


class ElCapitan:
    """
    El Capitan supercomputer – world simulation engine.

    Lifecycle
    ---------
    1. Call ``boot()`` to initialise the engine and spawn worlds.
    2. Call ``run_auto()`` for a full hands-off simulation, or
       ``run_interactive()`` to step through ticks manually.
    3. Call ``shutdown()`` (or let ``run_*`` finish) for a final report.

    Parameters
    ----------
    num_worlds:
        Number of parallel Earth-like worlds to simulate.
    ticks:
        Total simulation ticks to run.
    seed:
        Master random seed for reproducibility.
    log_level:
        Python logging level (e.g. ``logging.INFO``).
    """

    def __init__(
        self,
        num_worlds: int = DEFAULT_NUM_WORLDS,
        ticks: int = DEFAULT_SIMULATION_TICKS,
        seed: int = DEFAULT_SEED,
        log_level: int = logging.WARNING,
    ) -> None:
        self._num_worlds = num_worlds
        self._ticks = ticks
        self._seed = seed
        self._log_level = log_level

        self._worlds: List[World] = []
        self._processor: Optional[TripleProcessor] = None
        self._booted = False

        logging.basicConfig(
            format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
            level=log_level,
            stream=sys.stdout,
        )

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def boot(self) -> None:
        """Initialise the engine, spawn worlds, and print the boot banner."""
        print(_BANNER.format(
            full_name=COMPUTER_FULL_NAME,
            location=COMPUTER_LOCATION,
        ))
        print(f"{LOG_PREFIX} Booting {COMPUTER_NAME} v{COMPUTER_VERSION}...")
        print(f"{LOG_PREFIX} Seed          : {self._seed}")
        print(f"{LOG_PREFIX} Worlds        : {self._num_worlds}")
        print(f"{LOG_PREFIX} Ticks         : {self._ticks}")

        rng = random.Random(self._seed)
        names = rng.sample(WORLD_NAME_POOL, min(self._num_worlds, len(WORLD_NAME_POOL)))
        # If more worlds than names, fall back to generated names
        while len(names) < self._num_worlds:
            names.append(f"World-{len(names) + 1}")

        self._worlds = [World.create(name, rng) for name in names]
        self._processor = TripleProcessor(seed=self._seed)
        self._booted = True

        print(f"{LOG_PREFIX} ✅ {COMPUTER_NAME} online.\n")
        for w in self._worlds:
            print(f"  ✦ Spawned {w.status_line()}")
        print()

    def shutdown(self) -> None:
        """Print final report and shut down the engine."""
        print(f"\n{'═' * LINE_WIDTH}")
        print(f"{LOG_PREFIX} {COMPUTER_NAME} shutdown sequence initiated")
        print(f"{'═' * LINE_WIDTH}")

        # Final world states
        print(f"\n  {'World':<20} {'Age':>6}  {'Pop':>10}  {'Sapient':<8}  {'Habitable'}")
        print(f"  {'─'*20}  {'─'*6}  {'─'*10}  {'─'*8}  {'─'*9}")
        for w in self._worlds:
            pop_str = f"{w.total_population():,}"
            sapient = "YES 🧠" if w.has_sapient_life() else "NO"
            hab = "YES" if w.is_habitable else "NO"
            print(f"  {w.name:<20} {w.age_ticks:>6}t  {pop_str:>10}  {sapient:<8}  {hab}")

        # Processor performance
        if self._processor:
            print(f"\n  ── Triple-Processor Performance ──")
            print(self._processor.performance_report())

        print(f"\n{LOG_PREFIX} 🛑 {COMPUTER_NAME} powered down.\n")

    # ------------------------------------------------------------------
    # Operation modes
    # ------------------------------------------------------------------

    def run_auto(self) -> None:
        """Run all ticks automatically and then shut down."""
        self._require_boot()
        print(f"{LOG_PREFIX} AUTO mode – running {self._ticks} ticks...\n")

        for tick in range(self._ticks):
            metrics = self._processor.run_tick(self._worlds)
            if tick % max(1, self._ticks // 10) == 0 or tick == self._ticks - 1:
                self._print_tick_summary(tick, metrics)

        self.shutdown()

    def run_interactive(self) -> None:
        """Step through ticks one at a time with user prompts."""
        self._require_boot()
        print(
            f"{LOG_PREFIX} INTERACTIVE mode – press ENTER to advance each tick, "
            f"'q' to quit.\n"
        )

        for tick in range(self._ticks):
            try:
                cmd = input(
                    f"{LOG_PREFIX} [Tick {tick}/{self._ticks}] "
                    "Press ENTER to continue, 'q' to quit: "
                ).strip().lower()
            except EOFError:
                break

            if cmd in ("q", "quit"):
                break

            metrics = self._processor.run_tick(self._worlds)
            self._print_tick_summary(tick, metrics)

        self.shutdown()

    def run_single_tick(self) -> bool:
        """
        Advance the simulation by exactly one tick.

        Returns True while there are remaining ticks, False when done.
        """
        self._require_boot()
        if self._processor.tick_count >= self._ticks:
            return False
        self._processor.run_tick(self._worlds)
        return self._processor.tick_count < self._ticks

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------

    @property
    def worlds(self) -> List[World]:
        """The list of simulated worlds (read-only view)."""
        return list(self._worlds)

    @property
    def is_booted(self) -> bool:
        return self._booted

    @property
    def current_tick(self) -> int:
        return self._processor.tick_count if self._processor else 0

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _require_boot(self) -> None:
        if not self._booted:
            raise RuntimeError(
                f"{COMPUTER_NAME} must be booted before operation. Call .boot() first."
            )

    def _print_tick_summary(self, tick: int, metrics) -> None:
        habitable = sum(1 for w in self._worlds if w.is_habitable)
        total_pop = sum(w.total_population() for w in self._worlds)
        sapient_worlds = sum(1 for w in self._worlds if w.has_sapient_life())

        print(
            f"  t={tick:>4d} | habitable={habitable}/{len(self._worlds)} | "
            f"pop={total_pop:>10,} | sapient_worlds={sapient_worlds} | "
            f"{metrics.summary()}"
        )
