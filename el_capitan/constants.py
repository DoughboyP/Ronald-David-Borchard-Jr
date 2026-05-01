"""
El Capitan – Constants
Configuration constants for the El Capitan supercomputer world-simulation engine.
"""

# ──────────────────────────────────────────────
# Identity
# ──────────────────────────────────────────────
COMPUTER_NAME = "El Capitan"
COMPUTER_LOCATION = "Lawrence Livermore National Laboratory, Livermore, CA"
COMPUTER_VERSION = "1.0.0"
COMPUTER_FULL_NAME = f"{COMPUTER_NAME} World Simulation Engine v{COMPUTER_VERSION}"

LOG_PREFIX = "[EL-CAP]"

# ──────────────────────────────────────────────
# Simulation defaults
# ──────────────────────────────────────────────
DEFAULT_NUM_WORLDS = 4
DEFAULT_SIMULATION_TICKS = 1000
DEFAULT_SEED = 1992

# ──────────────────────────────────────────────
# World parameters
# ──────────────────────────────────────────────
WORLD_NAME_POOL = [
    "Aetheria", "Borchard Prime", "Cascadia", "Dawnworld", "Ronnie's hells", "Hollywood",
    "Elysium", "Feronia", "Gaia-2", "Horizon", "Ironreach",
    "Jadestone", "Kairos", "Luminos", "Meridian", "Novaterra",
]

MIN_WORLD_RADIUS_KM = 5_000
MAX_WORLD_RADIUS_KM = 8_000

# ──────────────────────────────────────────────
# Environment (Tier 1) parameters
# ──────────────────────────────────────────────
CLIMATE_TYPES = ["Tropical", "Arid", "Temperate", "Continental", "Polar"]
TERRAIN_TYPES = ["Plains", "Mountains", "Forest", "Desert", "Tundra", "Ocean", "Wetlands"]

TEMP_MIN_C = -60.0
TEMP_MAX_C = 60.0
TEMP_CHANGE_RATE = 0.5        # °C per tick (max delta)
PRECIPITATION_MAX_MM = 500.0  # mm per tick
WIND_SPEED_MAX_KMH = 120.0

# ──────────────────────────────────────────────
# Resource (Tier 2) parameters
# ──────────────────────────────────────────────
INITIAL_WATER_UNITS = 10_000.0
INITIAL_MINERAL_UNITS = 5_000.0
INITIAL_ENERGY_UNITS = 8_000.0
INITIAL_FOOD_UNITS = 6_000.0

RESOURCE_REGEN_RATE = 0.02    # fraction of max regenerated per tick
RESOURCE_DEPLETION_RATE = 0.01  # baseline consumption per entity per tick

# ──────────────────────────────────────────────
# Ecology (Tier 3) parameters
# ──────────────────────────────────────────────
ENTITY_TYPES = ["Flora", "Fauna", "Aquatic", "Avian", "Sapient"]

INITIAL_ENTITY_COUNT = 20
MAX_ENTITIES_PER_WORLD = 200
ENTITY_BIRTH_RATE = 0.05      # probability per existing entity per tick
ENTITY_DEATH_RATE = 0.02      # baseline mortality per tick
SAPIENCE_EMERGENCE_MIN_POPULATION = 100  # minimum total world population before sapience can emerge

# ──────────────────────────────────────────────
# Triple-processor threading
# ──────────────────────────────────────────────
TIER1_THREAD_NAME = "Tier-1-Environment"
TIER2_THREAD_NAME = "Tier-2-Resources"
TIER3_THREAD_NAME = "Tier-3-Ecology"

PROCESSOR_TIMEOUT_SECONDS = 30

# ──────────────────────────────────────────────
# Logging / display
# ──────────────────────────────────────────────
LINE_WIDTH = 80
