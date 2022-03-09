""" Define API versions."""
from configparser import LegacyInterpolation
from enum import Enum

class Version(Enum):
    LEGACY = 0
    V1 = 1