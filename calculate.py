#!/usr/bin/env python3
"""CLI to calculate number combinations with a single digit."""

from fire import Fire
import src.onedigit as onedigit
from json import JSONEncoder
from dataclasses import asdict


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

    combos = onedigit.simple.calculate(digit, upper, steps=steps)
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
            cc.append(asdict(c))
        jsenc = JSONEncoder()
        jstxt = jsenc.encode(cc)
        print(jstxt)






if __name__ == "__main__":
    f = Fire(calculate)
