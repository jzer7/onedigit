"""Package to calculate combinations to form a number out of a algebraic operations using a single digit."""

from onedigit.info import (  # noqa: F401
    __author__,
    __maintainer__,
    __email__,
    __license__,
    __version__,
    __url__,
    __bugtrack_url__,
)
from onedigit.logger import main_logger
from onedigit.model import Combo, Model
from onedigit.simple import advance, calculate, get_model
from onedigit.cli import main

__all__ = ["Combo", "Model", "advance", "calculate", "get_model", "main_logger", "main"]
