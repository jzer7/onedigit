"""Single digit combo."""

from dataclasses import dataclass
from typing import List
import math

INF = 10**9


@dataclass
class Combo:
    value: int
    cost: int
    expr: str = ""
    expr_simple: str = ""

    def exists(self) -> bool:
        """Check if a solution exists to produce this value."""
        return self.cost < INF

    def __repr__(self) -> str:
        return f"Combo: {self.value} = {self.expr_simple}    [{self.cost}]"

    def __lt__(self, other) -> int:
        return self.value < other.value


def setup_simulation(seed: int, space: int = 100) -> List:
    """Build space for a simulation"""

    combos = [Combo(value=i, cost=INF) for i in range(space + 1)]

    # Set up the seed digit
    combos[seed].expr = combos[seed].expr_simple = str(seed)
    combos[seed].cost = 1

    # Allow an expression for `1`
    combos[1].expr = f"{seed}/{seed}"
    combos[1].expr_simple = str(1)
    combos[1].cost = 2

    return combos


def combo_unary_operation(combo1: Combo, op: str) -> Combo:
    """Apply an operation on a single number."""
    cost = combo1.cost

    if op == "!":
        val = math.factorial(combo1.value)
        expr1 = f"({combo1.expr})!"
        expr2 = f"{combo1.value}!"
    else:
        raise Exception("bad operator:", op)

    return Combo(value=val, cost=cost, expr=expr1, expr_simple=expr2)


def combo_binary_operation(combo1: Combo, combo2: Combo, op: str) -> Combo:
    """Apply an operation on a pair of numbers."""

    cost = combo1.cost + combo2.cost

    match op:
        case "+":
            val = combo1.value + combo2.value
            expr1 = f"({combo1.expr}) + ({combo2.expr})"
            expr2 = f"{combo1.value} + {combo2.value}"

        case "-":
            val = combo1.value - combo2.value
            expr1 = f"({combo1.expr}) - ({combo2.expr})"
            expr2 = f"{combo1.value} - {combo2.value}"

        case "*":
            val = combo1.value * combo2.value
            expr1 = f"({combo1.expr}) * ({combo2.expr})"
            expr2 = f"{combo1.value} * {combo2.value}"

        case "/":
            if combo1.value % combo2.value != 0:
                return Combo(value=0, expr="", expr_simple="", cost=INF)

            val = combo1.value // combo2.value
            expr1 = f"({combo1.expr}) / ({combo2.expr})"
            expr2 = f"{combo1.value} / {combo2.value}"

        case "^":
            if combo1.value <= 1 or combo2.value > 10:
                return Combo(value=0, expr="", expr_simple="", cost=INF)

            val = combo1.value**combo2.value
            expr1 = f"({combo1.expr}) ^ ({combo2.expr})"
            expr2 = f"{combo1.value} ^ {combo2.value}"

        case _:
            raise Exception("bad operator:", op)

    return Combo(value=val, cost=cost, expr=expr1, expr_simple=expr2)


def state_update(state: List[Combo], candidate: Combo, *, max_cost: int = 20) -> bool:
    """Add a new combination to existing state. True if the update was valid."""

    if candidate.cost > max_cost:
        return False

    value, cost = candidate.value, candidate.cost

    if not (1 < value < len(state)):
        return False

    if state[value].exists() and state[value].cost <= cost:
        return False

    state[value] = candidate
    return True


def state_merge(state: List[Combo], extra: List[Combo], *, max_cost: int = 20):
    """Add new combinations to existing state."""

    for combo2 in extra:
        val2, cost2 = combo2.value, combo2.cost

        if cost2 > max_cost or val2 < 1 or val2 >= len(state) or state[val2].exists() and state[val2].cost <= cost2:
            continue
        else:
            state[val2] = combo2


def simulate(state: List = []) -> List[Combo]:
    """Take 1 round of simulation"""

    known = [s for s in state if s.exists()]
    new_combos = state.copy()

    updates = 0
    for combo1 in known:
        # Unary operations
        for op in ["!"]:
            updates += state_update(new_combos, combo_unary_operation(combo1, op=op))

        for combo2 in known:
            # Order is well defined:
            #   + and * are commutative
            #   / and - do not make sense if combo1 < combo2
            for op in ["+", "-", "*", "/"]:
                if combo1.value >= combo2.value:
                    updates += state_update(new_combos, combo_binary_operation(combo1, combo2, op))

            # Order is important:
            #   ^
            for op in "^":
                updates += state_update(new_combos, combo_binary_operation(combo1, combo2, op))

    print(f"[INFO] There were {updates} in this simulation step.")

    state_merge(state, new_combos)

    return state


def state_prune(state: List[Combo]) -> List[Combo]:
    """Remove combinations without a solution."""
    return [s for s in state if s.exists()]


def demo():
    steps = 10

    # Prepare
    state = setup_simulation(3, space=200)

    # Run a few steps
    for step in range(1, steps + 1):
        state = simulate(state)

    for c in state_prune(state):
        print(f"{c.value:>4} = {c.expr:<25}   [{c.cost}]")


if __name__ == "__main__":
    demo()
