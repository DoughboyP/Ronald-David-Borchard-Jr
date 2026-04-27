"""
MOB CHESS: Universe Control
AI – the two Gods make their moves each turn.

Each God follows a simple priority:
  1. If piece is adjacent to a non-controlled system → move there and claim it.
  2. If piece is adjacent to player → attack (if player is weak or God is strong).
  3. Otherwise → move toward the nearest unclaimed system.
"""

from __future__ import annotations
import random
from typing import List, Optional, Tuple

from .constants import (
    CHAOS,
    ORDER,
    PLAYER,
    NEUTRAL,
    GOD_CHAOS_NAME,
    GOD_ORDER_NAME,
)
from .entities import GodPiece
from .universe import Universe


class GodAI:
    """
    Drives one God's piece each turn.
    Returns a list of log messages describing what the God did.
    """

    def __init__(self, god_key: str, rng: random.Random) -> None:
        assert god_key in ("CHAOS", "ORDER")
        self.god_key  = god_key
        self.ctrl_val = CHAOS if god_key == "CHAOS" else ORDER
        self.name     = GOD_CHAOS_NAME if god_key == "CHAOS" else GOD_ORDER_NAME
        self._rng     = rng

    # ──────────────────────────────────────────────────────────────────
    # Public: take a turn
    # ──────────────────────────────────────────────────────────────────

    def take_turn(
        self,
        universe: Universe,
        player_pos: tuple,
        player_power: int,
        piece: GodPiece,
    ) -> Tuple[List[str], int]:
        """
        Execute one God turn.
        Returns (messages, damage_dealt_to_player).
        damage_dealt_to_player is 0 unless the God attacks the player directly.
        """
        messages: List[str] = []
        damage_to_player = 0

        if not piece.is_alive:
            messages.append(
                f"  💤 {self.name}'s avatar is dormant — regenerating..."
            )
            piece.heal_full()
            return messages, 0

        neighbors = universe.neighbors(*piece.position)

        # ── Priority 1: attack player if adjacent and advantaged ──────
        if player_pos in neighbors:
            if piece.power >= player_power or self._rng.random() < 0.35:
                dmg = self._rng.randint(8, 18)
                messages.append(
                    f"  ⚡ {self.name} STRIKES at {self._system_name(universe, player_pos)}! "
                    f"Deals {dmg} damage to you!"
                )
                return messages, dmg

        # ── Priority 2: claim an adjacent non-owned system ────────────
        claimable = [
            n for n in neighbors
            if universe.get_system(*n).controller != self.ctrl_val
            and universe.get_system(*n).controller != self._enemy_ctrl()
        ]
        if claimable:
            target = self._rng.choice(claimable)
            universe.move_piece(piece, target)
            universe.get_system(*target).controller = self.ctrl_val
            messages.append(
                f"  ⚡ {self.name} moves to {self._system_name(universe, target)} "
                f"and CLAIMS it."
            )
            return messages, 0

        # ── Priority 3: claim enemy (player) adjacent system ─────────
        enemy_adj = [
            n for n in neighbors
            if universe.get_system(*n).controller == PLAYER
        ]
        if enemy_adj and self._rng.random() < 0.5:
            target = self._rng.choice(enemy_adj)
            universe.move_piece(piece, target)
            universe.get_system(*target).controller = self.ctrl_val
            messages.append(
                f"  ⚡ {self.name} INVADES {self._system_name(universe, target)} "
                f"and takes it from you!"
            )
            return messages, 0

        # ── Priority 4: move toward nearest unclaimed system ──────────
        goal = self._find_nearest_unclaimed(universe, piece.position)
        if goal:
            step = self._step_toward(universe, piece.position, goal)
            if step:
                universe.move_piece(piece, step)
                messages.append(
                    f"  ⚡ {self.name} pushes toward {self._system_name(universe, goal)}."
                )
                return messages, 0

        # ── Fallback: random move ─────────────────────────────────────
        if neighbors:
            step = self._rng.choice(neighbors)
            universe.move_piece(piece, step)
            messages.append(
                f"  ⚡ {self.name} patrols to {self._system_name(universe, step)}."
            )

        return messages, 0

    # ──────────────────────────────────────────────────────────────────
    # Internal helpers
    # ──────────────────────────────────────────────────────────────────

    def _enemy_ctrl(self) -> int:
        return ORDER if self.ctrl_val == CHAOS else CHAOS

    def _system_name(self, universe: Universe, coord: tuple) -> str:
        return universe.get_system(*coord).name

    def _find_nearest_unclaimed(
        self, universe: Universe, start: tuple
    ) -> Optional[tuple]:
        """BFS to find the nearest system not owned by this God."""
        visited = {start}
        queue   = [start]
        while queue:
            current = queue.pop(0)
            if universe.get_system(*current).controller != self.ctrl_val:
                if current != start:
                    return current
            for nb in universe.neighbors(*current):
                if nb not in visited:
                    visited.add(nb)
                    queue.append(nb)
        return None

    def _step_toward(
        self, universe: Universe, start: tuple, goal: tuple
    ) -> Optional[tuple]:
        """
        Return the neighbour of *start* that is closest (BFS distance) to *goal*.
        """
        neighbors = universe.neighbors(*start)
        if not neighbors:
            return None

        def bfs_dist(a: tuple, b: tuple) -> int:
            visited = {a}
            queue   = [(a, 0)]
            while queue:
                node, dist = queue.pop(0)
                if node == b:
                    return dist
                for nb in universe.neighbors(*node):
                    if nb not in visited:
                        visited.add(nb)
                        queue.append((nb, dist + 1))
            return 9999

        return min(neighbors, key=lambda n: bfs_dist(n, goal))
