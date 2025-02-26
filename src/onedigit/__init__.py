"""Evaluate expressions that use a single digit from 1 to 9, and basic arithmetic operations."""

from onedigit.info import (  # noqa: F401 I001
    __author__,
    __maintainer__,
    __email__,
    __license__,
    __version__,
    __url__,
    __bugtrack_url__,
)
from onedigit.logger import get_logger
from onedigit.model import Combo, Model
from onedigit.simple import advance, calculate, get_model
from onedigit.cli import main

__all__ = ["Combo", "Model", "advance", "calculate", "get_model", "get_logger", "main"]
