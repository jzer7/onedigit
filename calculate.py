#!/usr/bin/env python3
"""CLI to calculate number combinations with a single digit."""

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
    max_cost: int = 12,
    max_steps: int = 10,
    full: bool = False,
    output: str = "text",
) -> bool:
    """
    Command line interface to calculate combinations using a given digit.

    Args:
        digit (int): the digit to use to generate combinations.
        max_value (int, optional): largest value for a combination to be shown in the output. Defaults to 9999.
        max_cost (int, optional): maximum cost a combination can have for it to be remembered. Defaults to 12.
        max_steps (int, optional): maximum number of generative rounds. Defaults to 10.
        full (bool, optional): display combinations using full expressios. Defaults to False.
        output (str, optional): format for the output (text/json). Defaults to "text".

    Returns:
        bool: True if calculation runs without issues.
    """

    __logger.debug(
        f"calculate(digit={type(digit).__name__}({digit}), max_value={type(max_value).__name__}({max_value}), max_steps={type(max_steps).__name__}({max_steps}), max_cost={type(max_cost).__name__}({max_cost}), output={type(output).__name__}({output}))"
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

    if isinstance(output, str):
        output = output.lower()
    else:
        output = ""
    if output not in ["text", "json"]:
        __logger.error("output must be 'text' or 'json'")
        return False

    # ------------------------------------------------------------
    combos = onedigit.calculate(digit=digit, max_value=max_value, max_cost=max_cost, max_steps=max_steps)
    if output == "text":
        for c in combos:
            if full:
                print(f"{c.value:>4} = {c.expr_full:<70}   [{c.cost:>3}]")
            else:
                print(f"{c.value:>4} = {c.expr_simple:<15}   [{c.cost:>3}]")
    elif output == "json":
        cc = []
        for c in combos:
            cc.append(c.asdict())
        jsenc = json.JSONEncoder()
        jstxt = jsenc.encode(cc)
        print(jstxt)

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
