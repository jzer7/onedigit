"""Functionality for easy access. It schedules the operations that calculate the combinations."""

import logging
from typing import List

from onedigit import model

__logger = logging.getLogger("simple")
__logger.setLevel(logging.INFO)


def calculate(digit: int, *, max_value: int = 9999, max_cost: int = 10, max_steps: int = 10) -> List[model.Combo]:
    """
    Run a simple calculation.

    Args:
        digit (int): digit to use
        max_number (int, optional): largest value to remember. Defaults to 9999.
        max_cost (int, optional): maximum cost a combination can have to be remembered. Defaults to 10.
        max_steps (int, optional): maximum number of steps (iterations) to run. Defaults to 10.

    Returns:
        List[model.Combo]: combinations generated.
    """

    __logger.debug(f"calculate(digit={digit},max_value={max_value},max_cost={max_cost},max_steps={max_steps})")

    state = model.Model(digit=digit, max_value=max_value, max_cost=max_cost)

    return advance(state=state, max_steps=max_steps).get_valid_combos()


def advance(state: model.Model, max_steps: int = 10) -> model.Model:
    """
    Perform iterations over a onedigit model.

    This function will stop earlier than the number of steps,
    if there is no change in state after an iteration.

    Args:
        state (model.Model): initial state for the simulation.
        max_steps (int): maximum number of steps (iterations) to run. Defaults to 10.

    Returns:
        model.Model: reference to the updated model.
    """

    __logger.debug(f"simple.advance(state={state}, max_steps={max_steps})")

    # Run a few steps
    for step in range(1, max_steps + 1):
        updates = state.simulate()
        if updates == 0:
            __logger.info(f"stopping early as state does not advance past {step} iterations.")
            break

    return state
