#!/usr/bin/env python3
"""CLI to calculate number combinations with a single digit."""

import logging
from json import JSONEncoder
from typing import Any

import fire

import onedigit

# Set loggers quickly, as they are used in multiple places
logging.basicConfig(level=logging.DEBUG)
__logger = logging.getLogger("cli")


def calculate(
    digit: int = 9,
    upper: int = 90,
    *,
    full: bool = False,
    steps: int = 10,
    output: str = "text",
):
    """
    Command line interface for the calculate function.

    Args:
        digit:  the digit to use to generate combinations
        upper:  upper limit is the last number that is calculated
        full:   display combinations using full expressions. Otherwise, it uses a simplified expression (default).
        steps:  maximum number of generative rounds
        output: format for the output (text, json).
    """

    combos = onedigit.calculate(digit, upper, steps=steps)
    output = output.lower()
    if output == "text":
        for c in combos:
            if full:
                print(f"{c.value:>4} = {c.expr:<70}   [{c.cost:>3}]")
            else:
                print(f"{c.value:>4} = {c.expr_simple:<15}   [{c.cost:>3}]")
    elif output == "json":
        cc = []
        for c in combos:
            cc.append(c.todict())
        jsenc = JSONEncoder()
        jstxt = jsenc.encode(cc)
        print(jstxt)


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
    __fileformatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    __consoleformatter = logging.Formatter("%(levelname)s - %(message)s")

    # create file handler which logs even debug messages
    fh = logging.FileHandler("calculate.log")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(__fileformatter)
    __logger.addHandler(fh)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    ch.setFormatter(__consoleformatter)
    __logger.addHandler(ch)

    fire = fire.Fire(calculate)
