"""
MOB CHESS: Universe Control
Universe – the board: galaxies, solar systems, adjacency, and body placement.
"""

from __future__ import annotations
import random
from typing import List, Set, Optional

from .constants import (
    GALAXY_NAMES,
    SOLAR_SYSTEM_NAMES,
    GALAXY_BRIDGES,
    ALL_BODIES,
    CHAOS,
    ORDER,
    NEUTRAL,
    PLAYER,
    CHAOS_START_SYSTEMS,
    ORDER_START_SYSTEMS,
    CHAOS_PIECE_START,
    ORDER_PIECE_START,
    CONTROL_SYMBOLS,
    CONTROL_NAMES,
    GOD_CHAOS_NAME,
    GOD_ORDER_NAME,
    GOD_PIECE_HP,
    GOD_PIECE_POWER,
    TOTAL_SYSTEMS,
)
from .entities import Galaxy, GodPiece, SolarSystem


class Universe:
    """
    The multidimensional game board.
    Manages all galaxies, systems, adjacency graph, body placements,
    and God-piece positions.
    """

    def __init__(self, rng: random.Random) -> None:
        self._rng = rng
        self.galaxies: List[Galaxy] = []
        self.chaos_piece: Optional[GodPiece] = None
        self.order_piece: Optional[GodPiece] = None
        self._build()
        self._place_bodies()

    # ──────────────────────────────────────────────────────────────────
    # Construction
    # ──────────────────────────────────────────────────────────────────

    def _build(self) -> None:
        """Build all galaxies, solar systems, and set initial control."""
        for g_idx, g_name in enumerate(GALAXY_NAMES):
            systems = []
            for s_idx, s_name in enumerate(SOLAR_SYSTEM_NAMES[g_idx]):
                systems.append(
                    SolarSystem(galaxy_idx=g_idx, sys_idx=s_idx, name=s_name)
                )
            self.galaxies.append(Galaxy(idx=g_idx, name=g_name, systems=systems))

        # Set initial territory
        for (gi, si) in CHAOS_START_SYSTEMS:
            self.get_system(gi, si).controller = CHAOS
        for (gi, si) in ORDER_START_SYSTEMS:
            self.get_system(gi, si).controller = ORDER
        # Player starts at (0,0) — already NEUTRAL; game.py will flip it to PLAYER

        # Place God pieces
        self.chaos_piece = GodPiece(
            god_name=GOD_CHAOS_NAME,
            position=CHAOS_PIECE_START,
            hp=GOD_PIECE_HP,
            max_hp=GOD_PIECE_HP,
            power=GOD_PIECE_POWER,
            symbol="CHO",
        )
        self.order_piece = GodPiece(
            god_name=GOD_ORDER_NAME,
            position=ORDER_PIECE_START,
            hp=GOD_PIECE_HP,
            max_hp=GOD_PIECE_HP,
            power=GOD_PIECE_POWER,
            symbol="ORD",
        )
        self._sync_piece_locations()

    def _place_bodies(self) -> None:
        """
        Scatter bodies across the universe.
        One body per neutral system, up to the number of body types we have.
        """
        shuffled_bodies = list(ALL_BODIES)
        self._rng.shuffle(shuffled_bodies)
        body_iter = iter(shuffled_bodies)

        # Place one body in each neutral system (skip god-start systems)
        for galaxy in self.galaxies:
            for system in galaxy.systems:
                if system.controller == NEUTRAL:
                    body = next(body_iter, None)
                    if body:
                        system.bodies.append(dict(body))

    # ──────────────────────────────────────────────────────────────────
    # Accessors
    # ──────────────────────────────────────────────────────────────────

    def get_system(self, galaxy_idx: int, sys_idx: int) -> SolarSystem:
        return self.galaxies[galaxy_idx].systems[sys_idx]

    def system_by_name(self, name: str) -> Optional[SolarSystem]:
        for galaxy in self.galaxies:
            for system in galaxy.systems:
                if system.name.lower() == name.lower():
                    return system
        return None

    def all_systems(self) -> List[SolarSystem]:
        return [s for g in self.galaxies for s in g.systems]

    def controlled_count(self, controller: int) -> int:
        return sum(1 for s in self.all_systems() if s.controller == controller)

    # ──────────────────────────────────────────────────────────────────
    # Adjacency graph
    # ──────────────────────────────────────────────────────────────────

    def neighbors(self, galaxy_idx: int, sys_idx: int) -> List[tuple]:
        """
        Return list of (galaxy_idx, sys_idx) coords adjacent to given coord.
        Within a galaxy: linear chain (0↔1↔2↔3↔4).
        Between galaxies: defined GALAXY_BRIDGES.
        """
        adj: Set[tuple] = set()
        coord = (galaxy_idx, sys_idx)

        # Within-galaxy chain
        if sys_idx > 0:
            adj.add((galaxy_idx, sys_idx - 1))
        if sys_idx < len(SOLAR_SYSTEM_NAMES[galaxy_idx]) - 1:
            adj.add((galaxy_idx, sys_idx + 1))

        # Cross-galaxy wormhole bridges
        for (ga, sa, gb, sb) in GALAXY_BRIDGES:
            if (ga, sa) == coord:
                adj.add((gb, sb))
            elif (gb, sb) == coord:
                adj.add((ga, sa))

        return list(adj)

    def all_neighbors_of_piece(self, piece: GodPiece) -> List[tuple]:
        return self.neighbors(*piece.position)

    # ──────────────────────────────────────────────────────────────────
    # Piece management
    # ──────────────────────────────────────────────────────────────────

    def _sync_piece_locations(self) -> None:
        """Update has_piece flags on every system to match piece positions."""
        for s in self.all_systems():
            s.has_piece = None
        gi, si = self.chaos_piece.position
        self.get_system(gi, si).has_piece = "CHAOS"
        gi, si = self.order_piece.position
        self.get_system(gi, si).has_piece = "ORDER"

    def move_piece(self, piece: GodPiece, new_pos: tuple) -> None:
        piece.position = new_pos
        self._sync_piece_locations()

    def piece_for(self, god_key: str) -> GodPiece:
        return self.chaos_piece if god_key == "CHAOS" else self.order_piece

    # ──────────────────────────────────────────────────────────────────
    # Display
    # ──────────────────────────────────────────────────────────────────

    def render_map(self, player_pos: tuple) -> str:
        """Return a full ASCII map of the universe."""
        lines = []
        for galaxy in self.galaxies:
            lines.append(f"\n  ── {galaxy.name} {'─' * (40 - len(galaxy.name))}")
            for system in galaxy.systems:
                ctrl_sym = CONTROL_SYMBOLS[system.controller]
                # Annotate player position, piece presence, bodies
                tags = []
                if system.coord == player_pos:
                    tags.append("👑YOU")
                if system.has_piece == "CHAOS":
                    tags.append("⚡CHO")
                if system.has_piece == "ORDER":
                    tags.append("⚡ORD")
                if system.bodies:
                    tags.append(f"💀×{len(system.bodies)}")
                tag_str = "  " + "  ".join(tags) if tags else ""
                lines.append(
                    f"    [{ctrl_sym}] {system.name:<20} {tag_str}"
                )

        # Summary bar
        p_count = self.controlled_count(PLAYER)
        c_count = self.controlled_count(CHAOS)
        o_count = self.controlled_count(ORDER)
        n_count = self.controlled_count(NEUTRAL)
        lines.append(
            f"\n  Control: YOU={p_count}  CHAOS={c_count}"
            f"  ORDER={o_count}  Neutral={n_count}  "
            f"(Win at {TOTAL_SYSTEMS // 2 + 1})"
        )
        return "\n".join(lines)
