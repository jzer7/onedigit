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

        Returns:
            bool: True if this is a valid combination
        """
        return self.cost < self.__INF

    def __repr__(self) -> str:
        """
        Provide a string representatoin of the Combo object.

        Returns:
            str: string representation of the Combo object
        """
        return f"Combo: {self.value} = {self.expr_simple}    [{self.cost}]"

    def __lt__(self, other: Combo) -> bool:
        """
        Compares this combination against another.

        This function is used by Python to sort containers
        with this type of objects.

        Args:
            other (Combo): combination object we are comparing with

        Returns:
            bool: True if this combination has a lower value compared to the 'other' combination.
        """
        assert isinstance(other, Combo)
        return self.value < other.value

    def asdict(self) -> dict[str, Any]:
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
        Apply an operation with this combo and another one.

        This function can result in an invalid value, in which case the
        result is a Combo object that evaluates to zero.

        Args:
            combo2 (Combo): second combination to use
            op (str): operation to perform between both combinations.
                Operations supported: addition(+), subtraction(-),
                multiplication(*), integer division(/), exponentiation(^)

        Raises:
            ValueError: when receiving an invalid operation

        Returns:
            Combo: the result of the operation, as a new Combo object.
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

    digit: int
    upper_value: int
    state: List[Combo]
    logger: logging.Logger

    def __init__(self, digit: int, upper_value: int = 100, empty: bool = False):
        """
        Build a model for the game simulation.

        Args:
            digit (int): digit to use when creating expresions
            upper_value (int, optional): upper limit of values the model
                retains. Defaults to 100.
            empty (bool, optional): leave object uninitialized. Useful
                when the plan is to copy values from a different object
                inside. (Look at Model.copy()). Defaults to False.
        Raises:
            ValueError: if digit value is out of range [1,9]
            ValueError: if upper value is too large (more than 10,000).
        """

        self.logger = logging.getLogger("model")
        self.logger.setLevel(logging.INFO)
        self.logger.debug("Model.__init__()")

        # In some cases, we need to skip the rest of the initialization.
        # For example if this is a shallow object that will be used to
        # receive a full copy of another object.
        if empty:
            return

        if not isinstance(digit, int) or not (1 <= digit <= 9):
            raise ValueError("digit must be an integer between 1 and 9, inclusive.")
        self.digit = digit

        if not isinstance(upper_value, int) or not (0 <= upper_value <= 10_000):
            raise ValueError("upper value must be a positive number below 10k.")
        self.upper_value = upper_value

        combos = [Combo(value=i) for i in range(upper_value + 1)]

        # Set up the digit for the simulation
        combos[digit].expr_full = combos[digit].expr_simple = str(digit)
        combos[digit].cost = 1

        # Allow an expression for `1`
        combos[1].expr_full = f"{digit}/{digit}"
        combos[1].expr_simple = str(1)
        combos[1].cost = 2

        # Allow expressions for joint digits (say, 22, two 2s)
        if 1 <= digit <= 9:
            num, expr, cost = digit, str(digit), 1
            while num <= upper_value:
                combos[num].expr_full = combos[num].expr_simple = expr
                combos[num].cost = cost

                num, expr, cost = 10 * num + digit, expr + str(digit), cost + 1

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
        new_model.digit = self.digit
        new_model.upper_value = self.upper_value
        new_model.state = self.state.copy()
        new_model.logger = self.logger
        return new_model

    def __repr__(self) -> str:
        """
        Provide a string representatoin of the Model object.

        Returns:
            str: string representation of the Model object
        """
        return f"Model(digit={self.digit}, upper_value={self.upper_value})"

    def state_update(self, candidate: Combo, *, max_cost: int = 20) -> bool:
        """
        Attempt addition of a single combination to the existing state.

        The combination will be checked against existing solutions, and
        it will be added if it is consider beneficial to the calculation.

        Args:
            candidate (Combo): combination to add
            max_cost (int, optional): highest cost for combination
                the model will accept. Defaults to 20.

        Returns:
            bool: True if the update was valid.
        """

        self.logger.debug("Model.state_update()")

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

        Args:
            extra (Model): model with combinations to be added to this model
            max_cost (int, optional): highest cost for combination
                the model will accept. Defaults to 20.
        """

        self.logger.debug("Model.state_merge()")

        for combo2 in extra.get_valid_combos():
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

    def get_valid_combos(self) -> List[Combo]:
        """
        Get valid combinations.

        Returns:
            List[Combo]: list of valid Combo objects
        """
        return [s for s in self.state if s.exists()]
