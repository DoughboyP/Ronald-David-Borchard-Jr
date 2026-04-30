"""
El Capitan – Triple Processor
Orchestrates the three-tier parallel processing architecture:

  Tier 1  – EnvironmentProcessor  (weather, climate, terrain)
  Tier 2  – ResourceProcessor     (resource management and dynamics)
  Tier 3  – EcologyProcessor      (ecological and entity interactions)

All three tiers run concurrently in dedicated threads each simulation tick,
then barrier-synchronise before the next tick begins.
"""

from __future__ import annotations

import logging
import random
import threading
import time
from typing import List, Optional

from .constants import (
    LOG_PREFIX,
    PROCESSOR_TIMEOUT_SECONDS,
    TIER1_THREAD_NAME,
    TIER2_THREAD_NAME,
    TIER3_THREAD_NAME,
)
from .models import World
from .tier1_environment import EnvironmentProcessor
from .tier2_resources import ResourceProcessor
from .tier3_ecology import EcologyProcessor

logger = logging.getLogger(__name__)


class TickMetrics:
    """Performance and state metrics recorded for a single simulation tick."""

    def __init__(self, tick: int) -> None:
        self.tick = tick
        self.tier_durations: dict = {}
        self.errors: List[str] = []

    def record_tier(self, tier: str, duration_s: float) -> None:
        self.tier_durations[tier] = duration_s

    def total_duration(self) -> float:
        return sum(self.tier_durations.values())

    def summary(self) -> str:
        parts = [f"Tick {self.tick:>4d} |"]
        for tier, dur in sorted(self.tier_durations.items()):
            parts.append(f" {tier}: {dur*1000:.1f}ms")
        parts.append(f" | total: {self.total_duration()*1000:.1f}ms")
        if self.errors:
            parts.append(f" | ERRORS: {len(self.errors)}")
        return "".join(parts)


class TripleProcessor:
    """
    Triple-processing architecture for the El Capitan engine.

    Each call to ``run_tick()`` launches three threads – one per tier –
    processes all worlds in parallel, then waits for all threads to finish
    before returning control to the caller.

    Thread safety:
        Each world's Environment, Resources, and Entities are modified by
        exactly one tier per tick.  The three tiers touch non-overlapping
        attributes, so no intra-tick locking is required.  Inter-tick
        state is safely handed off because all threads join before the
        next tick starts.
    """

    def __init__(self, seed: int) -> None:
        # Each tier gets its own RNG stream derived from the master seed
        master = random.Random(seed)
        self._tier1 = EnvironmentProcessor(rng=random.Random(master.randint(0, 2**31)))
        self._tier2 = ResourceProcessor(rng=random.Random(master.randint(0, 2**31)))
        self._tier3 = EcologyProcessor(rng=random.Random(master.randint(0, 2**31)))

        self._tick_count = 0
        self._metrics: List[TickMetrics] = []
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    @property
    def tick_count(self) -> int:
        return self._tick_count

    @property
    def metrics(self) -> List[TickMetrics]:
        return list(self._metrics)

    def run_tick(self, worlds: List[World]) -> TickMetrics:
        """
        Execute one simulation tick across all three tiers in parallel.

        Returns the TickMetrics for this tick.
        """
        m = TickMetrics(self._tick_count)
        errors: List[Optional[Exception]] = [None, None, None]

        def _run_tier(idx: int, name: str, processor_fn) -> None:
            t0 = time.perf_counter()
            try:
                processor_fn(worlds)
            except Exception as exc:  # noqa: BLE001
                errors[idx] = exc
                logger.exception("%s Tier %d (%s) raised: %s", LOG_PREFIX, idx + 1, name, exc)
            finally:
                m.record_tier(name, time.perf_counter() - t0)

        threads = [
            threading.Thread(
                target=_run_tier,
                args=(0, TIER1_THREAD_NAME, self._tier1.process),
                name=TIER1_THREAD_NAME,
                daemon=True,
            ),
            threading.Thread(
                target=_run_tier,
                args=(1, TIER2_THREAD_NAME, self._tier2.process),
                name=TIER2_THREAD_NAME,
                daemon=True,
            ),
            threading.Thread(
                target=_run_tier,
                args=(2, TIER3_THREAD_NAME, self._tier3.process),
                name=TIER3_THREAD_NAME,
                daemon=True,
            ),
        ]

        for t in threads:
            t.start()

        for t in threads:
            t.join(timeout=PROCESSOR_TIMEOUT_SECONDS)
            if t.is_alive():
                msg = f"Thread {t.name} timed out after {PROCESSOR_TIMEOUT_SECONDS}s"
                m.errors.append(msg)
                logger.error("%s %s", LOG_PREFIX, msg)

        # Surface any in-thread exceptions as log entries
        for exc in errors:
            if exc is not None:
                m.errors.append(str(exc))

        # Advance world age counters (serial – safe after all threads joined)
        for world in worlds:
            world.age_ticks += 1

        logger.debug("%s %s", LOG_PREFIX, m.summary())

        with self._lock:
            self._metrics.append(m)
            self._tick_count += 1

        return m

    def average_tick_ms(self) -> float:
        """Average wall-clock duration of a single tick in milliseconds."""
        if not self._metrics:
            return 0.0
        return sum(m.total_duration() for m in self._metrics) / len(self._metrics) * 1000

    def performance_report(self) -> str:
        """Return a human-readable performance summary."""
        total_ticks = len(self._metrics)
        if not total_ticks:
            return "No ticks recorded."
        avg_ms = self.average_tick_ms()
        error_count = sum(len(m.errors) for m in self._metrics)
        lines = [
            f"  Ticks completed   : {total_ticks}",
            f"  Avg tick duration : {avg_ms:.2f} ms",
            f"  Total errors      : {error_count}",
        ]
        return "\n".join(lines)
