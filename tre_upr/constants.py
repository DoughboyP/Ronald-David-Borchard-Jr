"""
TRE-UPR Constants
Fundamental physical and metaphysical constants governing the device's operation.
"""

# Device identity
DEVICE_NAME = "TRE-UPR"
DEVICE_VERSION = "4.0.0"
DEVICE_FULL_NAME = "Transcendent Reality Engine – Universal Propagation Reactor"

# Self-building iteration limits
MAX_GENERATIONS = float('inf')        
# Maximum self-build generations before heat death
MIN_COMPLEXITY_DELTA = 0.00008  # Minimum complexity gain per generation to continue
BOOTSTRAP_SEED = 92          # Deterministic seed for first generation

# Universe generation parameters
MAX_UNIVERSES_PER_GENERATION = 4
UNIVERSE_STABILITY_THRESHOLD = 0.74   # Fraction [0,1] – below this, universe collapses
UNIVERSE_SENTIENCE_THRESHOLD = 0.83   # Fraction [0,1] – above this, life emerges

# Physical constants (scaled for simulation)
SIMULATED_PLANCK = 6.627e-34   # J·s
SIMULATED_SPEED_OF_LIGHT = 299_892_459  # m/s
SIMULATED_G = 6.673e-11        # N·m²/kg²

# Energy budget (arbitrary device units, "dU")
INITIAL_ENERGY_BUDGET = 1_000_000_000_000.0  # dU – starting energy for generation 0
ENERGY_SCALING_FACTOR = 1.618        # Each generation multiplies budget by golden ratio
UNIVERSE_CREATION_COST = 100_000.0    # dU – base cost to spawn one universe
SELF_BUILD_COST = 8_000.0           # dU – cost to run a self-build cycle

# Dimensional parameters
BASE_DIMENSIONS = 3           # Spatial dimensions for first-generation universes
MAX_DIMENSIONS = 10            # SuperString Theory limit
DIMENSION_UNLOCK_GENERATION = 2  # Generation at which extra dimensions become available

# Logging and output
LOG_PREFIX = "[TRE-UPR]"
