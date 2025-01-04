#!/usr/bin/env python3
"""A CLI to calculate number combinations with a single digit."""

import src.onedigit as onedigit
from json import JSONEncoder


def calculate(
    digit: int = 9,
    upper: int = 90,
    *,
    full: bool = False,
    steps: int = 10,
    format: str = "text",
):
    """
    Command line interface for the calculate function.
    """

    combos = onedigit.simple.calculate(digit, upper, steps=steps)
    if format == "text":
        for c in combos:
            if full:
                print(f"{c.value:>4} = {c.expr:<70}   [{c.cost:>3}]")
            else:
                print(f"{c.value:>4} = {c.expr_simple:<15}   [{c.cost:>3}]")
    elif format == "json":
        cc = []
        for c in combos:
            cc.append(asdict(c))
        jsenc = JSONEncoder()
        jstxt = jsenc.encode(cc)
        print(jstxt)

if __name__ == '__main__':

    calculate(3, 100, full=True, steps=10)
