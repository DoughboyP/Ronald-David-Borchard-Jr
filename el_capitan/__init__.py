"""
El Capitan – World Simulation Engine

A Python module that simulates multiple Earth-like worlds using a triple-processing
architecture modelled after the El Capitan supercomputer at Lawrence Livermore
National Laboratory, Livermore, CA.

Architecture overview
---------------------
  Tier 1 (EnvironmentProcessor) – weather, climate, terrain
  Tier 2 (ResourceProcessor)    – resource management and dynamics
  Tier 3 (EcologyProcessor)     – ecological and entity interactions

All three tiers run concurrently in dedicated threads each simulation tick via
the TripleProcessor orchestrator.

Quick start
-----------
>>> from el_capitan import ElCapitan
>>> ec = ElCapitan(num_worlds=3, ticks=20)
>>> ec.boot()
>>> ec.run_auto()
"""

from .supercomputer import ElCapitan
from .models import World, Environment, Resources, Entity
from .processor import TripleProcessor, TickMetrics
from .tier1_environment import EnvironmentProcessor
from .tier2_resources import ResourceProcessor
from .tier3_ecology import EcologyProcessor
from .constants import (
    COMPUTER_NAME,
    COMPUTER_VERSION,
    COMPUTER_FULL_NAME,
    COMPUTER_LOCATION,
    SAPIENCE_EMERGENCE_MIN_POPULATION,
)

__all__ = [
    # Main interface
    "ElCapitan",
    # Data models
    "World",
    "Environment",
    "Resources",
    "Entity",
    # Processing architecture
    "TripleProcessor",
    "TickMetrics",
    "EnvironmentProcessor",
    "ResourceProcessor",
    "EcologyProcessor",
    # Metadata
    "COMPUTER_NAME",
    "COMPUTER_VERSION",
    "COMPUTER_FULL_NAME",
    "COMPUTER_LOCATION",
    "SAPIENCE_EMERGENCE_MIN_POPULATION",
]
