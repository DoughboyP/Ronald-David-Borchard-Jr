"""
El Capitan – Tier 1: Environment Processor
Simulates weather patterns, climate shifts, tectonic events, and terrain changes
for each world. Runs in its own thread as part of the triple-processing architecture.
"""

from __future__ import annotations

import logging
import random
from typing import List

from .constants import (
    LOG_PREFIX,
    PRECIPITATION_MAX_MM,
    TEMP_CHANGE_RATE,
    TEMP_MAX_C,
    TEMP_MIN_C,
    TERRAIN_TYPES,
    WIND_SPEED_MAX_KMH,
)
from .models import World

logger = logging.getLogger(__name__)


class EnvironmentProcessor:
    """
    Tier-1 processor: environment simulation.

    Responsibilities:
    - Weather dynamics (temperature, precipitation, wind)
    - Climate drift over long time-scales
    - Tectonic activity and sea-level changes
    - Terrain transformation events
    """

    def __init__(self, rng: random.Random) -> None:
        self._rng = rng

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def process(self, worlds: List[World]) -> None:
        """
        Run one environment tick across all worlds.
        Called by the TripleProcessor from Tier-1 thread.
        """
        for world in worlds:
            if not world.is_habitable:
                continue
            self._update_weather(world)
            self._update_climate_drift(world)
            self._process_tectonic_events(world)
            self._check_habitability(world)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _update_weather(self, world: World) -> None:
        """Stochastic weather update – temperature, precipitation, wind."""
        env = world.environment
        rng = self._rng

        # Temperature random walk clamped to world limits
        delta_t = rng.uniform(-TEMP_CHANGE_RATE, TEMP_CHANGE_RATE)
        env.temperature_c = max(TEMP_MIN_C, min(TEMP_MAX_C, env.temperature_c + delta_t))

        # Precipitation is anti-correlated with recent temperature rise
        precip_scale = max(0.0, 1.0 - (env.temperature_c / TEMP_MAX_C) * 0.5)
        env.precipitation_mm = rng.uniform(0.0, PRECIPITATION_MAX_MM * precip_scale)

        # Wind speed random walk
        wind_delta = rng.uniform(-5.0, 5.0)
        env.wind_speed_kmh = max(0.0, min(WIND_SPEED_MAX_KMH, env.wind_speed_kmh + wind_delta))

        # Humidity tracks precipitation
        env.humidity_pct = min(100.0, env.humidity_pct * 0.9 + env.precipitation_mm * 0.02)

    def _update_climate_drift(self, world: World) -> None:
        """Slowly shift climate zone based on accumulated temperature."""
        env = world.environment
        tick = world.age_ticks

        if tick > 0 and tick % 20 == 0:
            # Every 20 ticks consider a climate zone transition
            if env.temperature_c > 30 and env.climate not in ("Tropical", "Arid"):
                env.climate = "Tropical" if env.humidity_pct > 50 else "Arid"
                msg = f"Climate shift → {env.climate}"
                env.event_log.append(msg)
                world.log(msg)
                logger.debug("%s %s: %s", LOG_PREFIX, world.name, msg)
            elif env.temperature_c < -10 and env.climate != "Polar":
                env.climate = "Polar"
                msg = "Climate shift → Polar"
                env.event_log.append(msg)
                world.log(msg)
                logger.debug("%s %s: %s", LOG_PREFIX, world.name, msg)

    def _process_tectonic_events(self, world: World) -> None:
        """Random volcanic / earthquake events driven by tectonic activity level."""
        env = world.environment
        rng = self._rng

        # Tectonic activity fluctuates gradually
        env.tectonic_activity = max(
            0.0,
            min(1.0, env.tectonic_activity + rng.uniform(-0.05, 0.05)),
        )

        # Rare major event (earthquake / eruption)
        if rng.random() < env.tectonic_activity * 0.03:
            sea_delta = rng.uniform(-2.0, 2.0)
            env.sea_level_m += sea_delta
            # Major eruptions can inject aerosols, cooling temperature
            cooling = rng.uniform(0.0, 3.0)
            env.temperature_c -= cooling
            event = (
                f"Tectonic event! Sea level Δ{sea_delta:+.1f}m, "
                f"temp cooling -{cooling:.1f}°C"
            )
            env.event_log.append(event)
            world.log(event)
            logger.info("%s %s: %s", LOG_PREFIX, world.name, event)

        # Terrain can shift near plate boundaries
        if rng.random() < env.tectonic_activity * 0.01:
            new_terrain = rng.choice(TERRAIN_TYPES)
            if new_terrain != env.terrain:
                event = f"Terrain shift: {env.terrain} → {new_terrain}"
                env.terrain = new_terrain
                env.event_log.append(event)
                world.log(event)
                logger.info("%s %s: %s", LOG_PREFIX, world.name, event)

    def _check_habitability(self, world: World) -> None:
        """Mark a world uninhabitable if conditions become extreme."""
        env = world.environment
        if env.temperature_c <= TEMP_MIN_C + 2 or env.temperature_c >= TEMP_MAX_C - 2:
            if world.is_habitable:
                world.is_habitable = False
                msg = "World conditions critical – marked UNINHABITABLE"
                world.log(msg)
                logger.warning("%s %s: %s", LOG_PREFIX, world.name, msg)
