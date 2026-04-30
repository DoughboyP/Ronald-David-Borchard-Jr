"""
TRE-UPR Serpent Entity
======================

The Serpent is a sophisticated agent that navigates through the TRE-UPR world
simulation, weaving through universes on three simultaneous layers of meaning.

──────────────────────────────────────────────────────────────────────────────
MULTI-LAYERED DESIGN (ENTENDRES)
──────────────────────────────────────────────────────────────────────────────

  Layer 1 — Physical (the literal serpent)
    A serpent moves through dimensional space, sensing heat and light, choosing
    paths based on the terrain it perceives, and leaving a glittering trail of
    scales behind it wherever it goes.

  Layer 2 — Code (the serpent in the machine)
    The Serpent "slides through programming" by reading and writing simulation
    parameters — entropy rates, quantum coupling, dark energy density.  When it
    passes through a universe it is, in effect, running a live patch on the
    physics engine; the universe never knows it has been touched.

  Layer 3 — Symbolic (the eternal archetype)
    Across every culture the serpent carries the same bundle of meanings:
    transformation (shed skin / new generation), forbidden knowledge (it alone
    knows the truth of the tree), duality (healer and destroyer, ouroboros
    devouring its own tail), and the hidden path that only the wise can follow.
    Every action the Serpent takes inside the simulation carries an echo of
    these meanings.

──────────────────────────────────────────────────────────────────────────────
TRIPLE PROCESSING TIERS
──────────────────────────────────────────────────────────────────────────────

  Tier 1 — Environmental sensing & response
    The Serpent reads the universe's stability, complexity, and energy budget
    each tick, then adjusts its heading so it moves *toward* the richest zone.
    (Physically: heat-seeking. Code: parameter reading. Symbolically: the
    serpent always finds the garden.)

  Tier 2 — Resource interaction & manipulation
    As the Serpent crosses a universe it gently modulates the physics profile —
    nudging quantum coupling upward (amplifying possibility), slightly cooling
    entropy (preserving order), or shedding a fragment of its own stored energy
    into the universe's budget.
    (Physically: energy exchange. Code: live parameter patch. Symbolically: the
    gift of fire / forbidden fruit.)

  Tier 3 — Ecological impact & entity relationships
    The Serpent's passage leaves a permanent *trace* in the universe's event
    log.  Accumulated traces act as a catalyst: each trace slightly elevates the
    universe's sentience threshold, meaning that worlds visited by the Serpent
    are more likely to birth conscious life.
    (Physically: environmental enrichment. Code: threshold modification.
    Symbolically: the serpent that grants wisdom.)

──────────────────────────────────────────────────────────────────────────────
MEMORY & LEARNING
──────────────────────────────────────────────────────────────────────────────

  The Serpent remembers every universe it has visited, the state it found each
  universe in, and the outcomes of its interventions.  Over time it develops
  *preferences* — it is drawn more strongly toward universe types that responded
  well to its touch.  This is implemented as a simple reinforcement vector that
  biases future movement decisions.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Dict, List, Optional, Tuple

if TYPE_CHECKING:
    from .universe import Universe


# ──────────────────────────────────────────────────────────────────────────────
# Constants local to the Serpent
# ──────────────────────────────────────────────────────────────────────────────

# How much energy the Serpent donates to a universe on each visit (dU)
SERPENT_ENERGY_GIFT = 5_000.0

# Maximum nudge applied to quantum_coupling per tick (Layer 2)
SERPENT_COUPLING_NUDGE = 0.015

# Maximum cooling applied to entropy_rate per tick (Layer 2)
SERPENT_ENTROPY_COOLING = 0.003

# Fraction of the sentience threshold lowered by each trace left (Layer 3)
SERPENT_TRACE_SENTIENCE_BOOST = 0.002

# How quickly the Serpent's preference vector converges (learning rate)
SERPENT_LEARNING_RATE = 0.1

# Maximum energy the Serpent can carry before it must shed some
SERPENT_MAX_ENERGY = 500_000.0

# Starting energy the Serpent is born with
SERPENT_INITIAL_ENERGY = 50_000.0

# Symbols drawn from world serpent mythology (used in trace messages)
_SERPENT_SYMBOLS: List[str] = [
    "⟳",   # ouroboros — eternal cycle
    "𓆙",   # Egyptian Wadjet — divine protection
    "🐍",   # the literal serpent — the creature itself
    "∞",   # infinity — the unending path
    "⚕",   # Rod of Asclepius — healing / knowledge
    "◈",   # the diamond scale — precision
    "≋",   # water waves — flow, adaptation
    "✦",   # star — hidden light
]

# Dual-meaning phrases woven into every trace the Serpent leaves.
# Each phrase works on two levels simultaneously:
#   literal (what the serpent physically does) / symbolic (what it means).
_DUAL_MEANINGS: List[str] = [
    "Coils tighten; the code breathes in",
    "A scale falls; a parameter shifts",
    "The path is memorised; the map is rewritten",
    "Old skin dissolves; new constants take hold",
    "Venom or medicine — the dose decides",
    "The tongue reads the air; the state vector updates",
    "Deeper roots; higher branches",
    "The mouth that speaks also listens",
    "Transformation is the only constant",
    "What was hidden is now the seed",
    "The garden is not lost — it is moved",
    "Dark energy yields to the patient coil",
    "The cycle eats its tail; the loop closes cleanly",
    "Wisdom is entropy reversed",
    "Every shedding is a version release",
]


# ──────────────────────────────────────────────────────────────────────────────
# SerpentMemory — one remembered visit
# ──────────────────────────────────────────────────────────────────────────────

@dataclass
class SerpentMemory:
    """
    A single memory of a universe visit.

    The Serpent uses these memories to update its preference vector and to
    avoid revisiting universes that have already collapsed.
    """
    universe_id: str
    tick_visited: int
    stability_at_visit: float
    complexity_at_visit: float
    energy_gifted: float
    coupling_nudge: float
    entropy_cooled: float
    outcome_complexity_delta: float = 0.0  # filled in retrospectively

    def summary(self) -> str:
        """One-line summary for the event log."""
        return (
            f"visited universe {self.universe_id} at tick {self.tick_visited} "
            f"[stab={self.stability_at_visit:.3f} cplx={self.complexity_at_visit:.3f}] "
            f"— gifted {self.energy_gifted:.0f} dU, "
            f"nudged coupling +{self.coupling_nudge:.4f}, "
            f"cooled entropy -{self.entropy_cooled:.4f}"
        )


# ──────────────────────────────────────────────────────────────────────────────
# Serpent — the primary entity
# ──────────────────────────────────────────────────────────────────────────────

class Serpent:
    """
    The Serpent — an adaptive, multi-layered entity that navigates the TRE-UPR
    world simulation.

    Instantiate once per engine run; call ``visit(universe)`` each simulation
    tick for each universe the Serpent should interact with.  The Serpent
    decides autonomously whether to engage deeply or to pass through lightly,
    based on its accumulated memory and preference vector.

    Three entendres are always active simultaneously:

    * **Physical** — the Serpent moves, senses, and leaves a trail of scales.
    * **Code** — it reads and patches live simulation parameters.
    * **Symbolic** — every action echoes a myth older than writing.

    Parameters
    ----------
    name:
        Identity of the Serpent.  Defaults to ``"Ouroboros"`` — the self-
        devouring world-serpent of Norse, Egyptian, and Greek cosmology.
    seed:
        Random seed for reproducible behaviour.
    """

    def __init__(
        self,
        name: str = "Ouroboros",
        seed: Optional[int] = None,
    ) -> None:
        self.name = name
        self._rng = random.Random(seed)

        # ── Physical state ────────────────────────────────────────────────
        # Position is a normalised coordinate in [0, 1]^3 universe-space.
        # The Serpent moves in 3-D regardless of the target universe's
        # actual dimensionality (higher dimensions are projected).
        self._position: Tuple[float, float, float] = (
            self._rng.random(),
            self._rng.random(),
            self._rng.random(),
        )
        self._heading: Tuple[float, float, float] = self._random_unit_vector()

        # ── Energy & vitality ─────────────────────────────────────────────
        self._energy: float = SERPENT_INITIAL_ENERGY
        self._age_ticks: int = 0

        # ── Memory & learning ─────────────────────────────────────────────
        # memories: universe_id → list of visit records
        self._memories: Dict[str, List[SerpentMemory]] = {}

        # preference_vector: 3-component vector used to bias movement toward
        # "rewarding" universe states.  Components are:
        #   [0] = preference for high stability
        #   [1] = preference for high complexity
        #   [2] = preference for high energy
        self._preference: List[float] = [0.5, 0.5, 0.5]

        # Trail of symbolic scales left across the simulation
        self._trail: List[str] = []

        # Universes visited this generation (reset per generation)
        self._visited_this_gen: set = set()

    # ──────────────────────────────────────────────────────────────────────
    # Public API
    # ──────────────────────────────────────────────────────────────────────

    @property
    def age_ticks(self) -> int:
        """Number of simulation ticks the Serpent has lived."""
        return self._age_ticks

    @property
    def energy(self) -> float:
        """Current energy reserve of the Serpent."""
        return self._energy

    @property
    def trail(self) -> List[str]:
        """Read-only view of the symbolic trail left by the Serpent."""
        return list(self._trail)

    @property
    def position(self) -> Tuple[float, float, float]:
        """Current normalised position in universe-space."""
        return self._position

    def reset_generation(self) -> None:
        """
        Called at the start of each new engine generation.

        Clears the per-generation visit set so the Serpent can revisit
        universe types it encountered before.  Long-term memories are kept.

        *Symbolically*: the Serpent sheds its skin — old constraints fall
        away, but the wisdom gained (memories) is retained.
        """
        self._visited_this_gen = set()
        self._trail.append(
            f"[{self.name}] Shed skin. New generation begins. "
            f"Preferences: stab={self._preference[0]:.3f} "
            f"cplx={self._preference[1]:.3f} "
            f"energy={self._preference[2]:.3f}"
        )

    def visit(self, universe: "Universe") -> List[str]:
        """
        The Serpent visits a universe for one simulation tick.

        This is the main entry point and executes all three tiers:

        Tier 1 — Sense the universe; decide how deeply to engage.
        Tier 2 — Interact with resources and modify physics parameters.
        Tier 3 — Leave a trace; update the sentience landscape.

        Returns a list of event strings suitable for appending to
        ``universe.events``.

        Parameters
        ----------
        universe:
            The :class:`~tre_upr.universe.Universe` to visit.

        Returns
        -------
        list[str]
            Event messages generated during the visit.
        """
        events: List[str] = []
        self._age_ticks += 1

        if not universe.is_alive:
            # Even collapsed universes leave an impression on the Serpent.
            # Symbolically: the serpent knows death intimately — it swallows
            # the old world so that a new one can be born.
            self._trail.append(
                f"[{self.name}] {_pick_symbol(self._rng)} "
                f"Crossed the ruins of {universe.name}."
            )
            return events

        # ── Tier 1: Environmental sensing & pathfinding ────────────────────
        attraction = self._compute_attraction(universe)
        self._move_toward(attraction)

        engagement_depth = self._decide_engagement(universe)
        # engagement_depth in [0, 1] — 0 = pass-through, 1 = deep interaction

        # ── Tier 2: Resource interaction & physics manipulation ────────────
        energy_gifted = 0.0
        coupling_nudge = 0.0
        entropy_cooled = 0.0

        if engagement_depth > 0.0 and universe.physics is not None:
            energy_gifted, coupling_nudge, entropy_cooled = self._interact(
                universe, engagement_depth
            )
            if energy_gifted:
                events.append(
                    f"[tick {universe.age_ticks}] {_pick_symbol(self._rng)} "
                    f"{self.name} gifted {energy_gifted:.0f} dU to {universe.name}. "
                    f"(The serpent shares the fruit of the tree.)"
                )
            if coupling_nudge:
                events.append(
                    f"[tick {universe.age_ticks}] {_pick_symbol(self._rng)} "
                    f"{self.name} amplified quantum coupling in {universe.name} "
                    f"by +{coupling_nudge:.4f}. "
                    f"(Every possibility becomes more possible.)"
                )
            if entropy_cooled:
                events.append(
                    f"[tick {universe.age_ticks}] {_pick_symbol(self._rng)} "
                    f"{self.name} cooled entropy in {universe.name} "
                    f"by -{entropy_cooled:.4f}. "
                    f"(Order stretches a little further into the dark.)"
                )

        # ── Tier 3: Ecological impact & trace deposit ──────────────────────
        if engagement_depth > 0.2:
            trace_msg = self._leave_trace(universe)
            universe.events.append(trace_msg)
            events.append(trace_msg)
            # Each trace subtly lowers the sentience emergence threshold,
            # making consciousness more likely in worlds the Serpent has walked.
            universe.serpent_trace_count += 1

        # ── Memory update ──────────────────────────────────────────────────
        mem = SerpentMemory(
            universe_id=universe.id,
            tick_visited=universe.age_ticks,
            stability_at_visit=universe.stability,
            complexity_at_visit=universe.complexity,
            energy_gifted=energy_gifted,
            coupling_nudge=coupling_nudge,
            entropy_cooled=entropy_cooled,
        )
        self._memories.setdefault(universe.id, []).append(mem)
        self._visited_this_gen.add(universe.id)

        # ── Learning: update preference vector ────────────────────────────
        self._learn(universe)

        # ── Replenish energy from the universe (a small draw) ─────────────
        if self._energy < SERPENT_MAX_ENERGY and universe.energy > 0:
            draw = min(universe.energy * 0.0005, SERPENT_MAX_ENERGY - self._energy)
            universe.energy -= draw
            self._energy += draw

        return events

    def status_line(self) -> str:
        """One-line status string for reporting."""
        sym = _pick_symbol(self._rng)
        return (
            f"{sym} {self.name}  |  age={self._age_ticks} ticks  |  "
            f"energy={self._energy:.1f} dU  |  "
            f"memories={sum(len(v) for v in self._memories.values())}  |  "
            f"trail_len={len(self._trail)}  |  "
            f"pos=({self._position[0]:.3f}, {self._position[1]:.3f}, {self._position[2]:.3f})  |  "
            f"pref=[{self._preference[0]:.2f}, {self._preference[1]:.2f}, {self._preference[2]:.2f}]"
        )

    # ──────────────────────────────────────────────────────────────────────
    # Tier 1 helpers — sensing & movement
    # ──────────────────────────────────────────────────────────────────────

    def _compute_attraction(
        self, universe: "Universe"
    ) -> Tuple[float, float, float]:
        """
        Compute a 3-D attraction vector toward the given universe.

        The attraction is a weighted sum of:
        - universe stability  (weighted by preference[0])
        - universe complexity (weighted by preference[1])
        - universe energy     (weighted by preference[2])

        Symbolically: the serpent is drawn toward warmth, life, and potential.
        Physically: gradient ascent toward the richest region of phase space.
        In code: reading simulation state variables to steer.
        """
        norm_energy = min(universe.energy / 1e8, 1.0)
        score = (
            self._preference[0] * universe.stability
            + self._preference[1] * (universe.complexity / 10.0)
            + self._preference[2] * norm_energy
        )
        # Map score into a unit-vector biased toward the universe "centre"
        # (represented as the midpoint (0.5, 0.5, 0.5) of normalised space).
        cx, cy, cz = 0.5, 0.5, 0.5
        dx = cx - self._position[0]
        dy = cy - self._position[1]
        dz = cz - self._position[2]
        length = math.sqrt(dx * dx + dy * dy + dz * dz) or 1.0
        scale = score * 0.6 + self._rng.uniform(0.0, 0.4)
        return (dx / length * scale, dy / length * scale, dz / length * scale)

    def _move_toward(self, attraction: Tuple[float, float, float]) -> None:
        """
        Update position by blending current heading with the attraction vector.

        The Serpent does not teleport; it slides smoothly — its heading is
        interpolated between the old heading and the new target, preserving
        momentum.  This is the physical layer: sinuous, purposeful movement.
        """
        ax, ay, az = attraction
        hx, hy, hz = self._heading

        # Blend heading 70 % old, 30 % attraction
        new_hx = hx * 0.7 + ax * 0.3
        new_hy = hy * 0.7 + ay * 0.3
        new_hz = hz * 0.7 + az * 0.3

        # Normalise
        length = math.sqrt(new_hx**2 + new_hy**2 + new_hz**2) or 1.0
        self._heading = (new_hx / length, new_hy / length, new_hz / length)

        step = 0.05
        px = (self._position[0] + self._heading[0] * step) % 1.0
        py = (self._position[1] + self._heading[1] * step) % 1.0
        pz = (self._position[2] + self._heading[2] * step) % 1.0
        self._position = (px, py, pz)

    def _decide_engagement(self, universe: "Universe") -> float:
        """
        Return an engagement depth in [0, 1].

        High depth means the Serpent pours significant effort into modifying
        this universe; low depth means it merely passes through.

        Decision factors:
        - Universes with high complexity *and* high stability are most
          attractive (the Serpent nurtures thriving worlds).
        - Universes already visited this generation get a reduced score
          (the Serpent does not circle endlessly — it moves on).
        - Universes about to collapse get emergency engagement (the Serpent
          tries to stabilise dying worlds).
        """
        from .constants import UNIVERSE_STABILITY_THRESHOLD

        already_visited = universe.id in self._visited_this_gen
        near_collapse = universe.stability < UNIVERSE_STABILITY_THRESHOLD + 0.05

        if near_collapse:
            # Emergency intervention — full engagement regardless
            return 0.9

        base = (universe.stability * 0.4 + (universe.complexity / 10.0) * 0.6)
        if already_visited:
            base *= 0.25  # strong discouragement from re-visiting
        return min(base, 1.0)

    # ──────────────────────────────────────────────────────────────────────
    # Tier 2 helpers — resource interaction & physics manipulation
    # ──────────────────────────────────────────────────────────────────────

    def _interact(
        self,
        universe: "Universe",
        depth: float,
    ) -> Tuple[float, float, float]:
        """
        Interact with ``universe`` at the given engagement depth.

        Modifies:
        - ``universe.energy``              (energy gift from the Serpent)
        - ``universe.physics.quantum_coupling`` (amplified by coupling nudge)
        - ``universe.physics.entropy_rate``    (cooled by entropy cooling)

        Returns (energy_gifted, coupling_nudge, entropy_cooled).

        *Code layer*: these are live writes to the physics simulation.
        *Symbolic layer*: the serpent breathes life into the universe, tightens
        the laws of nature, and holds back the tide of chaos.
        """
        p = universe.physics

        # Energy gift — scaled by depth and the Serpent's own reserves
        max_gift = min(self._energy * 0.05, SERPENT_ENERGY_GIFT * depth)
        energy_gifted = max_gift * depth if self._energy > max_gift else 0.0
        if energy_gifted:
            universe.energy += energy_gifted
            self._energy -= energy_gifted

        # Quantum coupling nudge — amplifies complexity growth
        coupling_nudge = SERPENT_COUPLING_NUDGE * depth
        old_coupling = p.quantum_coupling
        p.quantum_coupling = min(1.0, p.quantum_coupling + coupling_nudge)
        actual_nudge = p.quantum_coupling - old_coupling

        # Entropy cooling — slows energy dissipation (preserves the universe)
        entropy_cooled = SERPENT_ENTROPY_COOLING * depth
        old_entropy = p.entropy_rate
        p.entropy_rate = max(0.001, p.entropy_rate - entropy_cooled)
        actual_cooling = old_entropy - p.entropy_rate

        return energy_gifted, actual_nudge, actual_cooling

    # ──────────────────────────────────────────────────────────────────────
    # Tier 3 helpers — ecological impact & traces
    # ──────────────────────────────────────────────────────────────────────

    def _leave_trace(self, universe: "Universe") -> str:
        """
        Deposit a symbolic trace in the universe's event log.

        The trace is both a literal annotation in the simulation record and a
        symbolic artefact: each scale the Serpent leaves behind carries a piece
        of knowledge that nudges the universe toward sentience.

        The trace message is deliberately written with two readings:
        - Surface: physical description of the Serpent's passage.
        - Symbolic: a fragment of mythological meaning.
        """
        sym = _pick_symbol(self._rng)
        scale_idx = len(self._trail)
        dual_meaning = _DUAL_MEANINGS[scale_idx % len(_DUAL_MEANINGS)]
        msg = (
            f"[tick {universe.age_ticks}] {sym} {self.name} passed through "
            f"{universe.name} leaving scale #{scale_idx + 1}. "
            f"[{dual_meaning}]"
        )
        self._trail.append(msg)
        return msg

    # ──────────────────────────────────────────────────────────────────────
    # Learning helper
    # ──────────────────────────────────────────────────────────────────────

    def _learn(self, universe: "Universe") -> None:
        """
        Update the preference vector based on the universe's current state.

        This is a simple online reinforcement step: if the universe we just
        visited has high stability, we increase our preference for stability;
        if it has high complexity, we increase our preference for complexity;
        etc.  Over many visits the preference vector converges toward the
        universe type that the Serpent has found most rewarding to visit.

        *Symbolically*: the Serpent accumulates wisdom — it remembers which
        gardens are worth returning to.
        """
        lr = SERPENT_LEARNING_RATE
        norm_energy = min(universe.energy / 1e8, 1.0)

        self._preference[0] = (
            self._preference[0] * (1 - lr) + universe.stability * lr
        )
        self._preference[1] = (
            self._preference[1] * (1 - lr) + (universe.complexity / 10.0) * lr
        )
        self._preference[2] = (
            self._preference[2] * (1 - lr) + norm_energy * lr
        )

    # ──────────────────────────────────────────────────────────────────────
    # Utility
    # ──────────────────────────────────────────────────────────────────────

    def _random_unit_vector(self) -> Tuple[float, float, float]:
        """Return a random unit vector in 3-D space."""
        x = self._rng.gauss(0, 1)
        y = self._rng.gauss(0, 1)
        z = self._rng.gauss(0, 1)
        length = math.sqrt(x * x + y * y + z * z) or 1.0
        return (x / length, y / length, z / length)

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"Serpent(name={self.name!r}, age={self._age_ticks}, "
            f"energy={self._energy:.1f})"
        )


# ──────────────────────────────────────────────────────────────────────────────
# Module-level helpers
# ──────────────────────────────────────────────────────────────────────────────

def _pick_symbol(rng: random.Random) -> str:
    """Choose a random serpent symbol from the mythology set."""
    return rng.choice(_SERPENT_SYMBOLS)
