"""Functionality for easy access. It schedules the operations that calculate the combinations."""

import logging

from onedigit import model

__logger = logging.getLogger("simple")
__logger.setLevel(logging.INFO)


def calculate(digit: int, *, max_value: int = 9999, max_cost: int = 10, max_steps: int = 10) -> model.Model | None:
    """
    Run a simple calculation.

    Args:
        digit (int): digit to use
        max_number (int, optional): largest value to remember. Defaults to 9999.
        max_cost (int, optional): maximum cost a combination can have to be remembered. Defaults to 10.
        max_steps (int, optional): maximum number of steps (iterations) to run. Defaults to 10.

    Returns:
        model.Model: model object, or None if there is a failure.
    """
    __logger.debug(f"calculate(digit={digit}, max_value={max_value}, max_cost={max_cost}, max_steps={max_steps})")

    mymodel = get_model(digit=digit, max_value=max_value, max_cost=max_cost)
    if not mymodel:
        return None

    mymodel = advance(mymodel=mymodel, max_steps=max_steps)
    if not mymodel:
        return None

    return mymodel


def get_model(digit: int, *, max_value: int = 9999, max_cost: int = 2) -> model.Model | None:
    """
    Obtain an initial model.

    """
    __logger.debug(f"get_model(digit={digit}, max_value={max_value}, max_cost={max_cost})")
    # Build a blank model
    mymodel = model.Model(digit=digit)

    if not mymodel:
        __logger.error("unable to build a model")
        return None

    # Adjust parameters and add initial values (in case they do not exist there already)
    mymodel.seed(max_value=max_value, max_cost=max_cost)

    return mymodel


def advance(mymodel: model.Model, max_steps: int = 10) -> model.Model:
    """
    Perform iterations over a onedigit model.

    This function will stop earlier than the number of steps,
    if there is no change in state after an iteration.

    Args:
        mymodel (model.Model): model at the begining of the simulation.
        max_steps (int): maximum number of steps (iterations) to run. Defaults to 10.

    Returns:
        model.Model: reference to the updated model.
    """
    __logger.debug(f"simple.advance(mymodel={mymodel}, max_steps={max_steps})")

    # Run a few steps
    for step in range(1, max_steps + 1):
        updates = mymodel.simulate()
        if updates == 0:
            __logger.info(f"stopping early as state does not advance past {step} iterations.")
            break

    return mymodel
