"""Single digit combo."""

# Needed so classes can make self references to their type
from __future__ import annotations

import dataclasses
import logging
import math
from typing import Any, ClassVar, List


@dataclasses.dataclass
class Combo:
    """
    Represents an arithmetic combination.
    """

    value: int
    cost: int = -1
    expr_full: str = ""
    expr_simple: str = ""

    __INF: ClassVar[int] = 10**9

    def __post_init__(self):
        """Runs after instantiation of a dataclass object."""
        if self.cost == -1:
            self.cost = self.__INF

    def exists(self) -> bool:
        """
        Check if a solution exists to produce this value.
        """
        return self.cost < self.__INF

    def __repr__(self) -> str:
        return f"Combo: {self.value} = {self.expr_simple}    [{self.cost}]"

    def __lt__(self, other) -> int:
        """
        Compares 2 combos according to their value.
        This function is used by Python's sorting functions.
        """
        return self.value < other.value

    def todict(self) -> dict[str, Any]:
        """
        Creates a dictionary out of this dataclass object.
        This is needed to serialize the object to JSON.

        Returns:
            dict[str, Any]: dictionary with the dataclass fields.
        """
        return dataclasses.asdict(self)

    def unary_operation(self, op: str) -> Combo:
        """
        Apply an operation on a single number.

        Args:
            op (str): operation to run (!, sqrt).

        Raises:
            ValueError: when receiving an invalid operation

        Returns:
            Combo: a new Combo object.
        """

        match op:
            case "!":
                val = math.factorial(self.value)
                expr1 = f"({self.expr_full})!"
                expr2 = f"{self.value}!"
            case "sqrt":
                val = int(math.sqrt(self.value))
                if (val * val) != self.value:
                    return Combo(value=0, expr_full="", expr_simple="")
                expr1 = f"√({self.expr_full})"
                expr2 = f"√{self.value}"
            case _:
                raise ValueError("bad operator:", op)

        return Combo(value=val, cost=self.cost, expr_full=expr1, expr_simple=expr2)

    def binary_operation(self, combo2: Combo, op: str) -> Combo:
        """
        Apply an operation with this combo, and another one.

        Args:

        Raises:
            ValueError: when receiving an invalid operation

        Returns:
            Combo: a new Combo object.
        """

        cost = self.cost + combo2.cost

        match op:
            case "+":
                val = self.value + combo2.value
                expr1 = f"({self.expr_full}) + ({combo2.expr_full})"
                expr2 = f"{self.value} + {combo2.value}"

            case "-":
                val = self.value - combo2.value
                expr1 = f"({self.expr_full}) - ({combo2.expr_full})"
                expr2 = f"{self.value} - {combo2.value}"

            case "*":
                val = self.value * combo2.value
                expr1 = f"({self.expr_full}) * ({combo2.expr_full})"
                expr2 = f"{self.value} * {combo2.value}"

            case "/":
                if self.value % combo2.value != 0:
                    return Combo(value=0, expr_full="", expr_simple="")

                val = self.value // combo2.value
                expr1 = f"({self.expr_full}) / ({combo2.expr_full})"
                expr2 = f"{self.value} / {combo2.value}"

            case "^":
                if self.value <= 1 or combo2.value > 10:
                    return Combo(value=0, expr_full="", expr_simple="")

                val = self.value**combo2.value
                expr1 = f"({self.expr_full}) ^ ({combo2.expr_full})"
                expr2 = f"{self.value} ^ {combo2.value}"

            case _:
                raise ValueError("bad operator:", op)

        return Combo(value=val, cost=cost, expr_full=expr1, expr_simple=expr2)


class Model:
    """
    A onedigit simulation.
    """

    seed: int
    space: int
    state: List[Combo]
    logger: logging.Logger

    def __init__(self, seed: int, space: int = 100, empty: bool = False):
        """
        Build space for a simulation.

        Args:
            seed (int): digit to use when creating expresions
            space (int, optional): upper limit of values the simulation
                retains. Defaults to 100.
            empty (bool, optional): leave object uninitialized. Useful
                when the plan is to copy values from a different object
                inside. Defaults to False.
        """
        if not empty:
            self.prepare(seed=seed, space=space)

    def prepare(self, seed: int, space: int):
        self.logger = logging.getLogger("model")
        self.logger.setLevel(logging.INFO)

        self.logger.debug("Model.prepare()")
        if not (1 <= seed <= 9):
            raise ValueError("seed must be an integer between 1 and 9, inclusive.")
        self.seed = seed
        if not (0 <= space <= 10_000):
            raise ValueError("space must be a positive number below 10k.")
        self.space = space

        combos = [Combo(value=i) for i in range(space + 1)]

        # Set up the seed digit
        combos[seed].expr_full = combos[seed].expr_simple = str(seed)
        combos[seed].cost = 1

        # Allow an expression for `1`
        combos[1].expr_full = f"{seed}/{seed}"
        combos[1].expr_simple = str(1)
        combos[1].cost = 2

        # Allow expressions for joint digits (say, 22, two 2s)
        if 1 <= seed <= 9:
            num, expr, cost = seed, str(seed), 1
            while num <= space:
                combos[num].expr_full = combos[num].expr_simple = expr
                combos[num].cost = cost

                num, expr, cost = 10 * num + seed, expr + str(seed), cost + 1

        self.state = combos

    def copy(self) -> Model:
        """Create a new object with all information about this model.

        This function is used as a way to create a snapshot. When called
        a blank Model object is created, and data from the current object
        is copied over. At the end, there are no data structures shared
        between both objects.

        Returns:
            Model: a new Model object
        """
        new_model = Model(0, 0, empty=True)
        new_model.seed = self.seed
        new_model.space = self.space
        new_model.state = self.state.copy()
        new_model.logger = self.logger
        return new_model

    def state_update(self, candidate: Combo, *, max_cost: int = 20) -> bool:
        """
        Attempt addition of a single combination to the existing state.


        Returns:
            bool: True if the update was valid.
        """

        self.logger.debug("state_update")


        if candidate.cost > max_cost:
            return False

        value, cost = candidate.value, candidate.cost

        # Are we keeping track of this value?
        if not (1 < value < len(self.state)):
            return False

        # There was no improvement in cost
        if self.state[value].exists() and self.state[value].cost <= cost:
            return False

        self.state[value] = candidate
        return True

    def state_merge(self, extra: Model, *, max_cost: int = 20) -> None:
        """
        Merges combinations from a separate Model into the current model.

        It picks the best combination for a given value based on cost of
        the full expression.

        """

        for combo2 in extra.get_combos():
            val2, cost2 = combo2.value, combo2.cost

            if (
                cost2 > max_cost
                or val2 < 1
                or val2 >= len(self.state)
                or self.state[val2].exists()
                and self.state[val2].cost <= cost2
            ):
                continue
            else:
                self.state[val2] = combo2

    def simulate(self) -> int:
        """
        Run one round of the simulation.

        The function takes all existing combinations, and applies
        operations that generate new values, and stores them in a
        separate object. Once all initial values are processed, we
        merge combinations from the new object. That prevents recursive
        loops, and let us determine liveness.

        Returns:
            int: number of values that were updated
        """

        known = [s for s in self.state if s.exists()]
        known.sort(key=lambda c: c.value)
        new_combos = self.copy()

        updates = 0
        for combo1 in known:
            # Unary operations
            #   !:    factorial
            #   sqrt: square root
            for op in ["!", "sqrt"]:
                updates += new_combos.state_update(combo1.unary_operation(op=op))

            for combo2 in known:
                # We only run cases where combo1 >= combo2
                #   + and * are commutative
                #   / and - are not commutative, but problem deals with
                #           positive integers, so it does not make sense
                #           to run cases where combo1 < combo2
                for op in ["+", "-", "*", "/"]:
                    if combo1.value >= combo2.value:
                        updates += new_combos.state_update(combo1.binary_operation(combo2, op))

                # We need to run both cases (combo1 > combo2, and combo2 > combo1)
                #   ^
                for op in "^":
                    updates += new_combos.state_update(combo1.binary_operation(combo2, op))

        self.state_merge(new_combos)

        return updates

    def get_combos(self) -> List[Combo]:
        """
        Get valid combinations.

        Returns:
            List[Combo]: list of valid Combo objects
        """
        return [s for s in self.state if s.exists()]
