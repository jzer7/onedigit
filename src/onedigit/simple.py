"""Functionality for easy access. It schedules the operations that calculate the combinations."""

import logging
from typing import List

from onedigit import model

__LOGGER = logging.getLogger("simple")
__LOGGER.setLevel(logging.INFO)


def calculate(digit: int, max_number: int = 20, *, steps: int = 10) -> List[model.Combo]:
    """
    Runs the most frequent calculation.
    """

    # Prepare
    current = model.Model(digit, space=max_number)

    # Run a few steps
    for step in range(1, steps + 1):
        updates = current.simulate()
        if updates == 0:
            break

    return current.state_prune()
