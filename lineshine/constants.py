"""
Lineshine – Constants
Configuration constants for the Lineshine world-creation engine.
"""

# ──────────────────────────────────────────────
# Identity
# ──────────────────────────────────────────────
COMPUTER_NAME = "Lineshine"
COMPUTER_LOCATION = "Shenzhen, China"
COMPUTER_VERSION = "1.0.0"
COMPUTER_FULL_NAME = f"{COMPUTER_NAME} World-Creation Engine v{COMPUTER_VERSION}"
COMPUTER_OWNER = "Ronald David Borchard Jr"

LOG_PREFIX = "[LINESHINE]"
EYE_PREFIX = "[RA'S-EYE]"

# ──────────────────────────────────────────────
# Ra's Eye parameters
# ──────────────────────────────────────────────
RAS_EYE_POWER_LEVELS = ["Awakening", "Scanning", "Perceiving", "Omniscient"]
RAS_EYE_DIVINE_INSIGHTS = [
    "All worlds are threads in a single tapestry.",
    "Creation is the highest form of dominion.",
    "The eye that sees all governs all.",
    "Each world holds a fragment of the infinite.",
    "Light precedes every world into existence.",
    "To name a world is to breathe life into it.",
    "Unlimited creation flows from a single will.",
    "Every void yields to the architect's intent.",
    "The cosmos expands because the creator wills it.",
    "Order emerges wherever Ra's light touches.",
]

# ──────────────────────────────────────────────
# World defaults
# ──────────────────────────────────────────────
WORLD_TYPES = [
    "Terrestrial", "Ocean", "Arid", "Frozen",
    "Volcanic", "Jungle", "Crystalline", "Nebular",
]

WORLD_NAME_POOL = [
    "Aurum", "Borchard Prime", "Caelum", "Dawnspire",
    "Etherion", "Ferraxis", "Goldenveil", "Heliodor",
    "Ironsong", "Jadehaven", "Kemethra", "Luxara",
    "Meridius", "Novalis", "Osirian", "Pyracor",
    "Quazara", "Radiantis", "Solareth", "Terramund",
    "Umbralis", "Verdaxis", "Wyrmoor", "Xanathis",
    "Yorindel", "Zenithia",
]

AGE_STAGES = ["Newborn", "Young", "Mature", "Ancient", "Primordial"]

MIN_WORLD_RADIUS_KM = 4_000
MAX_WORLD_RADIUS_KM = 9_000

INITIAL_POPULATION_MIN = 0
INITIAL_POPULATION_MAX = 1_000

# ──────────────────────────────────────────────
# Simulation
# ──────────────────────────────────────────────
DEFAULT_TICKS_PER_WORLD = 10
POPULATION_GROWTH_RATE = 0.08
WORLD_STABILITY_DECAY = 0.005

# ──────────────────────────────────────────────
# Display
# ──────────────────────────────────────────────
LINE_WIDTH = 80
