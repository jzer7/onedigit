#!/usr/bin/env python3
"""CLI to calculate number combinations with a single digit."""

import datetime
import json
import logging
import logging.handlers

import fire

import onedigit

# Set loggers quickly, as they are used in multiple places
logging.basicConfig(level=logging.DEBUG)
__logger = logging.getLogger("cli")


def calculate(
    digit: int,
    *,
    max_value: int = 9999,
    max_cost: int = 2,
    max_steps: int = 5,
    full: bool = False,
    output_filename: str = "",
) -> bool:
    """
    Command line interface to calculate combinations using a given digit.

    Args:
        digit (int): the digit to use to generate combinations.
        max_value (int, optional): largest value for a combination to be shown in the output. Defaults to 9999.
        max_cost (int, optional): maximum cost a combination can have for it to be remembered. Defaults to 2.
        max_steps (int, optional): maximum number of generative rounds. Defaults to 5.
        full (bool, optional): display combinations using full expressions. Defaults to False.
        output_filename (str, optional): JSON file used to store the model upon completion. If not filename is provided, a random filename will be used. Empty by default.

    Returns:
        bool: True if calculation runs without issues.
    """
    __logger.debug(
        f"calculate(digit={type(digit).__name__}({digit}), "
        f"max_value={type(max_value).__name__}({max_value}), "
        f"max_steps={type(max_steps).__name__}({max_steps}), "
        f"max_cost={type(max_cost).__name__}({max_cost}), "
        f"output_filename={type(output_filename).__name__}({output_filename})"
    )

    # ------------------------------------------------------------
    # This is an entry level function. So handle for input
    # sanitation.
    try:
        digit = int(digit)
        max_value = int(max_value)
        max_cost = int(max_cost)
        max_steps = int(max_steps)
    except ValueError:
        __logger.error("digit, max_value, max_cost, and max_steps must be positive integer numbers")
        return False

    if not (1 <= digit <= 9):
        __logger.error("digit must be an integer number between 1 and 9")
        return False

    # ------------------------------------------------------------
    if not isinstance(output_filename, str):
        __logger.error("output_filename is not valid")
    if not output_filename:
        tz = datetime.UTC
        t = datetime.datetime.now(tz)
        output_filename = "model" + "." + t.strftime("%Y%m%d%H%M%S") + ".json"

    # ------------------------------------------------------------
    # Start calculation
    model = onedigit.calculate(
        digit=digit, max_value=max_value, max_cost=max_cost, max_steps=max_steps
    )

    # ------------------------------------------------------------
    # Get the combinations
    combos = []
    if not model:
        __logger.error("failure creating and running model")
        return False
    else:
        combos = sorted(model.state.values())

    # ------------------------------------------------------------
    # Take care of outputs
    if output_filename:
        # Represent model in JSON format
        model_dict = model.asdict()
        jsenc = json.JSONEncoder()
        jstxt = jsenc.encode(model_dict)

        # Write the whole model to a file
        with open(output_filename, mode="w", encoding="utf-8") as output_fp:
            output_fp.write(jstxt)

    # ------------------------------------------------------------
    # Output to terminal
    cc = []
    for c in combos:
        cc.append(c.asdict())
    for c in combos:
        if full:
            print(f"{c.value:>4} = {c.expr_full:<70}   [{c.cost:>3}]")
        else:
            print(f"{c.value:>4} = {c.expr_simple:<15}   [{c.cost:>3}]")

    return True


if __name__ == "__main__":
    # -----------------------------------------------------------
    # Configure logging
    # * The console will get messages INFO and higher, things
    #   we want the user to see right away.
    # * The log file will get messages DEBUG and higher,
    #   information for post execution analysis
    # -----------------------------------------------------------

    # Main logger : used only by other libraries
    logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

    # Logger for the CLI
    __logger.setLevel(logging.DEBUG)

    # create formatters
    __fileformatter = logging.Formatter(
        "%(asctime)s, %(name)s, %(levelname)s, %(message)s", datefmt="%Y-%m-%dT%H:%M:%S%z"
    )
    __consoleformatter = logging.Formatter("%(levelname)s - %(message)s")

    # create file handler which logs even debug messages
    fh = logging.handlers.RotatingFileHandler(
        filename="calculate.log", maxBytes=100000, backupCount=5, encoding="utf-8"
    )
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(__fileformatter)
    __logger.addHandler(fh)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    ch.setFormatter(__consoleformatter)
    __logger.addHandler(ch)

    fire = fire.Fire(calculate)
    exit(0 if fire else 1)
