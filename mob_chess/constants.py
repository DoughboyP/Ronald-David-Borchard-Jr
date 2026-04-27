"""
MOB CHESS: Universe Control
Constants – the laws of the cosmic game.
"""

GAME_TITLE = "MOB CHESS: UNIVERSE CONTROL"
VERSION = "1.0.0"

# ──────────────────────────────────────────────
# Universe layout
# 4 galaxies × 5 solar systems = 20 total systems
# ──────────────────────────────────────────────
GALAXY_NAMES = [
    "Milky Hustle",
    "Andromeda Prime",
    "Dark Matter Bloc",
    "Nebula Federation",
]

SOLAR_SYSTEM_NAMES = [
    ["Alpha Block", "Sigma Gate", "Nova Crown", "Dark Matter Pt", "Eclipse Prime"],
    ["Beta Throne", "Delta Rise", "Omega Keep", "Void Gate", "Star Forge"],
    ["Shadow Den", "Phantom Reach", "Midnight Sun", "Cosmic Trap", "Black Hole Bloc"],
    ["Nebula One", "Spirit Realm", "Cloud Nine", "Thunder Dome", "Final Frontier"],
]

# Wormhole bridges between galaxies: (gal_a, sys_a, gal_b, sys_b)
GALAXY_BRIDGES = [
    (0, 4, 1, 0),   # Eclipse Prime  ↔ Beta Throne
    (1, 4, 2, 0),   # Star Forge     ↔ Shadow Den
    (2, 4, 3, 0),   # Black Hole Bloc↔ Nebula One
    (0, 2, 3, 4),   # Nova Crown     ↔ Final Frontier  (secret wormhole)
]

# ──────────────────────────────────────────────
# Control states
# ──────────────────────────────────────────────
NEUTRAL = 0
PLAYER  = 1
CHAOS   = 2   # God of Chaos
ORDER   = 3   # God of Order

CONTROL_SYMBOLS = {
    NEUTRAL: " · ",
    PLAYER:  "YOU",
    CHAOS:   "CHO",
    ORDER:   "ORD",
}

CONTROL_NAMES = {
    NEUTRAL: "Neutral",
    PLAYER:  "Your Turf",
    CHAOS:   "Chaos",
    ORDER:   "Order",
}

# ──────────────────────────────────────────────
# Starting positions / territory
# ──────────────────────────────────────────────
PLAYER_START = (0, 0)          # (galaxy, system)

CHAOS_START_SYSTEMS = [        # Andromeda Prime – systems 0-4
    (1, 0), (1, 1), (1, 2), (1, 3), (1, 4),
]
CHAOS_PIECE_START = (1, 2)     # Omega Keep

ORDER_START_SYSTEMS = [        # Nebula Federation – systems 0-4
    (3, 0), (3, 1), (3, 2), (3, 3), (3, 4),
]
ORDER_PIECE_START = (3, 2)     # Cloud Nine

# ──────────────────────────────────────────────
# Player stats
# ──────────────────────────────────────────────
PLAYER_START_HP    = 100
PLAYER_START_POWER = 15
PLAYER_START_CRED  = 0

# ──────────────────────────────────────────────
# God stats
# ──────────────────────────────────────────────
GOD_CHAOS_NAME = "THE ARCHITECT OF CHAOS"
GOD_ORDER_NAME = "THE SOVEREIGN OF ORDER"

GOD_PIECE_HP    = 40
GOD_PIECE_POWER = 22

# ──────────────────────────────────────────────
# Bodies – collectible souls worn for power
# Each entry: name, power bonus, hp bonus, ability key, flavour
# ──────────────────────────────────────────────
ALL_BODIES = [
    {
        "name": "Shadow Walker",
        "power": 5,  "hp": 5,
        "ability": "dodge",
        "desc": "Ghost-moves through the dark. +30% dodge chance.",
    },
    {
        "name": "The Brute",
        "power": 15, "hp": 10,
        "ability": "crush",
        "desc": "Pure mass. Hits harder than a dying star.",
    },
    {
        "name": "Oracle Prime",
        "power": 3,  "hp": 5,
        "ability": "foresee",
        "desc": "Sees the future. Preview God moves each turn.",
    },
    {
        "name": "Ghost Rider",
        "power": 8,  "hp": 0,
        "ability": "dash",
        "desc": "Moves like smoke. Travel 2 systems per Move action.",
    },
    {
        "name": "Iron Titan",
        "power": 5,  "hp": 50,
        "ability": "endure",
        "desc": "Built like a planet. +50 max HP.",
    },
    {
        "name": "Time Bender",
        "power": 10, "hp": 10,
        "ability": "rewind",
        "desc": "Turns back the clock. ONCE: undo a bad combat roll.",
    },
    {
        "name": "Void King",
        "power": 20, "hp": 20,
        "ability": "void",
        "desc": "Commands the nothing. ONCE: nullify a God action.",
    },
    {
        "name": "Star Crusher",
        "power": 12, "hp": 15,
        "ability": "supernova",
        "desc": "Goes supernova. ONCE: weaken all enemy systems in galaxy.",
    },
    {
        "name": "Soul Collector",
        "power": 6,  "hp": 8,
        "ability": "drain",
        "desc": "Feeds on pain. Drain 10 HP from enemies on combat win.",
    },
    {
        "name": "Cosmic Pawn",
        "power": 4,  "hp": 12,
        "ability": "shield",
        "desc": "Shields the demigod. ONCE: absorb a lethal hit.",
    },
    {
        "name": "Galaxy Reaper",
        "power": 18, "hp": 10,
        "ability": "reap",
        "desc": "Claims without a fight. ONCE: auto-claim any neutral system.",
    },
    {
        "name": "Dimensional Lord",
        "power": 15, "hp": 25,
        "ability": "warp",
        "desc": "Bends dimensions. ONCE: warp to any system in the universe.",
    },
]

MAX_BODIES_WORN = 7   # lucky number – max bodies you can carry at once

# ──────────────────────────────────────────────
# Win / lose conditions
# ──────────────────────────────────────────────
TOTAL_SYSTEMS = 20        # 4 galaxies × 5 systems
WIN_SYSTEMS   = 11        # >50% → you run the universe
GOD_WIN_SYSTEMS = 16      # a God controls ≥16 → universe is lost

# ──────────────────────────────────────────────
# Combat
# ──────────────────────────────────────────────
ATTACKER_ROLL_MAX  = 20
DEFENDER_ROLL_MAX  = 15
DEFENDER_BONUS     = 5    # home-turf advantage
NEUTRAL_CLAIM_COST = 20   # HP cost to claim a neutral system (no combat)
CRED_PER_HUSTLE    = 5    # cred per controlled system when you hustle

# ──────────────────────────────────────────────
# Display
# ──────────────────────────────────────────────
LINE_WIDTH = 72
