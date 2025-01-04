"""Functionality for easy access. It schedules the operations that calculate the combinations."""

from typing import List
from . import model


def calculate(digit: int, max_number: int = 20, *, steps: int = 10) -> List[model.Combo]:
    """
    Runs the most frequent calculation.
    """

    # Prepare
    state = model.setup_simulation(digit, space=max_number)

    # Run a few steps
    for step in range(1, steps + 1):
        state, updates = model.simulate(state)
        if updates == 0:
            break

    return model.state_prune(state)
