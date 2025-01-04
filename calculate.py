#!/usr/bin/env python3
"""A CLI to calculate number combinations with a single digit."""

import sys
import src.onedigit as onedigit
from json import JSONEncoder
from dataclasses import asdict


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



def main():
    digit, max_number, steps = 3, 50, 10

    if len(sys.argv) >= 2:
        try:
            digit = int(sys.argv[1])
        except ValueError:
            print(f"Argument is the digit used. You used '{sys.argv[1]}'.")
            exit(-1)
        max_number = max(max_number, 10 * digit + 10)

    if len(sys.argv) == 3:
        try:
            max_number = int(sys.argv[2])
        except ValueError:
            print(f"Argument is the digit used. You used '{sys.argv[2]}'.")
            exit(-1)

    calculate(digit, max_number, steps=steps)
if __name__ == "__main__":
    main()
