"""Functionality for easy access. It schedules the operations that calculate the combinations."""

import logging
from typing import List

from onedigit import model

__logger = logging.getLogger("simple")
__logger.setLevel(logging.INFO)


def calculate(digit: int, upper_value: int = 20, *, steps: int = 10) -> List[model.Combo]:
    """
    Run a simple calculation.

    Args:
        digit (int): digit to use
        max_number (int, optional): largest value to remember. Defaults to 20.
        steps (int, optional): maximum number of steps (iterations) to run. Defaults to 10.

    Returns:
        List[model.Combo]: combinations generated.
    """

    __logger.debug(f"calculate(digit={digit},upper_value={upper_value},steps={steps})")

    state = model.Model(digit=digit, upper_value=upper_value)

    return advance(state=state, steps=steps).get_valid_combos()


def advance(state: model.Model, steps: int = 10) -> model.Model:
    """
    Perform iterations over a onedigit model.

    This function will stop earlier than the number of steps,
    if there is no change in state after an iteration.

    Args:
        digit (int): digit to use
        steps (int, optional): maximum number of steps (iterations) to run. Defaults to 10.

    Returns:
        model.Model: reference to the updated model.
    """

    __logger.debug(f"simple.advance(state={state}, steps={steps})")

    # Run a few steps
    for step in range(1, steps + 1):
        updates = state.simulate()
        if updates == 0:
            __logger.info(f"stopping early as state does not advance past {step} iterations.")
            break

    return state
