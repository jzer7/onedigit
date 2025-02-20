"""Single digit combo."""

# Needed so classes can make self references to their type
from __future__ import annotations

import dataclasses
import logging
import math
from typing import Any, Dict, List


@dataclasses.dataclass
class Combo:
    """
    Represents an arithmetic combination using a single digit.

    Args:
        value (int): value of the expression after evaluation.
        cost (int): number of times the digit is used in the expression.
        expr_full (str): string representing the instruction.
        expr_simple (str): string representing a simplified expression
            of the last value(s) and operand that were used to generate
            this expression.
    """

    value: int
    cost: int = 0  # (set to 10**9 if empty)
    expr_full: str = ""  # (set to str(value) if empty)
    expr_simple: str = ""  # (set to str(value) if empty)

    def __post_init__(self):
        """Run after instantiation of a dataclass object."""
        if self.cost == 0:
            self.cost = 10**9
        if not self.expr_full:
            self.expr_full = str(self.value)
        if not self.expr_simple:
            self.expr_simple = str(self.value)

    def __repr__(self) -> str:
        """
        Provide a string representatoin of the Combo object.

        Returns:
            str: string representation of the Combo object
        """
        return f"Combo: {self.value} = {self.expr_simple}    [{self.cost}]"

    def __lt__(self, other: Combo) -> bool:
        """
        Compare the order of this combination against another.

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
        Create a dictionary representation of the Combo object.

        This is needed to serialize the object to JSON.
        It is also used during serialization of the Model object
        (see Model.asdict()).

        Returns:
            dict[str, Any]: dictionary with the dataclass fields.
        """
        return dataclasses.asdict(self)

    def unary_operation(self, op: str) -> Combo:
        """
        Apply an operation on a single number.

        This function can result in an invalid value, in which case the
        result is a Combo object that evaluates to zero.

        Operations produce a new Combo object.
        Operations do not modify the current object.

        Args:
            op (str): operation to run (!, sqrt).

        Raises:
            ValueError: when receiving an invalid operation

        Returns:
            Combo: a new Combo object.
        """

        # Only use parenthesis for cases it helps (if expression has spaces)
        value1_expr_full = self.expr_full
        if " " in value1_expr_full:
            value1_expr_full = "(" + value1_expr_full + ")"

        match op:
            case "!":
                if (self.value < 0) or (self.value > 20):
                    # FIXME: This is an opaque value. See how to clean this up.
                    # Prevent illogical or gigantic values in calculations
                    # Value: 20! is 2x10^18 ,  62-bits
                    #        21! is         ,  66-bits
                    #        24! is         ,  80-bits
                    #        30! is         , 108-bits
                    #        34! is         , 128-bits
                    return Combo(value=0)
                rc_val = math.factorial(self.value)
                rc_expr_full = value1_expr_full + "!"
                rc_expr_simple = str(rc_val) + "!"
            case "sqrt":
                if self.value < 0:
                    # Prevent irrational values
                    return Combo(value=0)
                rc_val = math.isqrt(self.value)
                if (rc_val * rc_val) != self.value:
                    # Only allow expressions that result in exact integer values
                    return Combo(value=0)
                rc_expr_full = "√(" + value1_expr_full + ")"
                rc_expr_simple = "√(" + str(self.value) + ")"
            case _:
                raise ValueError("bad operator:", op)

        return Combo(value=rc_val, cost=self.cost, expr_full=rc_expr_full, expr_simple=rc_expr_simple)

    def binary_operation(self, combo2: Combo, op: str) -> Combo:
        """
        Apply an operation with this combo and another one.

        This function can result in an invalid value, in which case the
        result is a Combo object that evaluates to zero.

        Operations produce a new Combo object.
        Operations do not modify the current object.

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

        # Only use parenthesis for cases it helps (if expression has spaces)
        value1_expr_full, value2_expr_full = self.expr_full, combo2.expr_full
        if " " in value1_expr_full:
            value1_expr_full = "(" + value1_expr_full + ")"
        if " " in value2_expr_full:
            value2_expr_full = "(" + value2_expr_full + ")"

        match op:
            case "+":
                rc_val = self.value + combo2.value
                rc_expr_full = f"{value1_expr_full} + {value2_expr_full}"
                rc_expr_simple = f"{self.value} + {combo2.value}"

            case "-":
                rc_val = self.value - combo2.value
                rc_expr_full = f"{value1_expr_full} - {value2_expr_full}"
                rc_expr_simple = f"{self.value} - {combo2.value}"

            case "*":
                rc_val = self.value * combo2.value
                rc_expr_full = f"{value1_expr_full} * {value2_expr_full}"
                rc_expr_simple = f"{self.value} * {combo2.value}"

            case "/":
                if self.value % combo2.value != 0:
                    return Combo(value=0)

                rc_val = self.value // combo2.value
                rc_expr_full = f"{value1_expr_full} / {value2_expr_full}"
                rc_expr_simple = f"{self.value} / {combo2.value}"

            case "^":
                # FIXME: This is an opaque value. See how to clean this up.
                # Prevent illogical or gigantic values in calculations
                # Value: 9^20 is 1.2x10^19,  64-bits
                #        9^40 is 1.4x10^38, 127-bits
                if self.value < 0 or combo2.value > 40:
                    return Combo(value=0)

                rc_val = self.value**combo2.value
                rc_expr_full = f"{value1_expr_full} ^ {value2_expr_full}"
                rc_expr_simple = f"{self.value} ^ {combo2.value}"

            case _:
                raise ValueError("bad operator:", op)

        return Combo(value=rc_val, cost=cost, expr_full=rc_expr_full, expr_simple=rc_expr_simple)


class Model:
    """Model the space for expressions using a single digit."""

    digit: int
    max_value: int = 0
    max_cost: int = 0
    state: Dict[int, Combo]
    logger: logging.Logger

    def __init__(self, digit):
        """
        Build a model for the game simulation.

        Args:
            digit (int): digit to use when creating expresions
        Raises:
            ValueError: if digit value is out of range [1,9]
        """

        self.logger = logging.getLogger("model")
        self.logger.setLevel(logging.INFO)
        self.logger.debug("Model.__init__()")

        if not isinstance(digit, int) or not (1 <= digit <= 9):
            raise ValueError("digit must be an integer between 1 and 9, inclusive.")
        self.digit = digit

        self.state = {}

    def seed(self, *, max_value: int = 0, max_cost: int = 0) -> None:
        """
        Args:
            max_value (int, optional): upper limit of values the model
                retains.
            max_cost (int, optional): maximum cost a combination can
                have, for the simulation to use it to generate other
                combinations.
        Raises:
            ValueError: if max value is too large (more than 1M).
        """
        if not isinstance(max_value, int) or not (1 <= max_value <= 1_000_000):
            raise ValueError("max value must be a positive number below 1M.")
        self.max_value = max_value

        if not isinstance(max_cost, int) or not (1 <= max_cost <= 30):
            raise ValueError("maximum cost must be a positive number below 30.")
        self.max_cost = max_cost

        # Set up the digit for the simulation
        self.state[self.digit] = Combo(value=self.digit, cost=1, expr_full=str(self.digit), expr_simple=str(self.digit))

        # Allow expressions for joint digits (say, 22, two 2s)
        if 1 <= self.digit <= 9:
            num, expr, cost = self.digit, str(self.digit), 1
            while (num <= self.max_value) and (cost <= self.max_cost):
                self.state[num] = Combo(value=num, cost=cost, expr_full=expr, expr_simple=expr)

                num, expr, cost = 10 * num + self.digit, expr + str(self.digit), cost + 1

    def copy(self) -> Model:
        """Create a new object with all information about this model.

        This function is used as a way to create a snapshot. When called
        a blank Model object is created, and data from the current object
        is copied over. At the end, there are no data structures shared
        between both objects.

        Returns:
            Model: a new Model object
        """
        new_model = Model(digit=self.digit)
        new_model.digit = self.digit
        new_model.max_value = self.max_value
        new_model.max_cost = self.max_cost
        new_model.state = self.state.copy()
        new_model.logger = self.logger
        return new_model

    def fromdict(self, input: dict):
        """Create a Model object from a dictionary.

        Functions to export an Model to a dictionary, and to create an
        object from a dictionary are used during object serialization. That
        functionality is used when taking snapshots of a Model simulation.

        Args:
            input (dict): dictionary representation of the object

        Raises:
            ValueError: _description_
        """
        for k in ["digit", "max_value", "max_cost", "state"]:
            if k not in input:
                raise ValueError(f"input dictionary is missing key {k}")

        new_model = Model(digit=0, max_value=0, max_cost=0, shallow=True)
        new_model.digit = input["digit"]
        new_model.max_value = input["max_value"]
        new_model.max_cost = input["max_cost"]
        new_model.state = input["state"]

    def __repr__(self) -> str:
        """
        Provide a string representatoin of the Model object.

        Returns:
            str: string representation of the Model object
        """
        return f"Model(digit={self.digit}, max_value={self.max_value}, max_cost={self.max_cost})"

    def state_update(self, candidate: Combo) -> bool:
        """
        Attempt addition of a single combination to the existing state.

        The combination will be checked against existing solutions, and
        it will be added if it is consider beneficial to the calculation.

        Args:
            candidate (Combo): combination to add

        Returns:
            bool: True if the update was valid.
        """

        self.logger.debug("Model.state_update()")

        if candidate.cost > self.max_cost:
            return False

        value, cost = candidate.value, candidate.cost

        # Are we keeping track of this value?
        if not (1 <= value <= self.max_value):
            return False

        # There was no improvement in cost
        if (value in self.state) and (self.state[value].cost <= cost):
            return False

        self.state[value] = candidate
        return True

    def state_merge(self, extra: Model) -> None:
        """
        Merge combinations from a separate Model into the current model.

        It picks the best combination for a given value based on cost of
        the full expression.

        Args:
            extra (Model): model with combinations to be added to this model
        """

        self.logger.debug("Model.state_merge()")

        for combo2 in extra.get_valid_combos():
            val2, cost2 = combo2.value, combo2.cost

            if (
                cost2 > self.max_cost
                or val2 < 1
                or val2 >= self.max_value
                or (val2 in self.state and self.state[val2].cost <= cost2)
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

        known = list(self.state.values())
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
        return list(self.state.values())

    def asdict(self) -> dict[str, Any]:
        """
        Create a dictionary representation of the Model object.

        Functions to export an Model to a dictionary, and to create an
        object from a dictionary are used during object serialization. That
        functionality is used when taking snapshots of a Model simulation.

        Returns:
            dict[str, Any]: dictionary with the dataclass fields.
        """
        state = []
        for num in sorted(self.state.keys()):
            state.append(self.state[num].asdict())

        obj = {"digit": self.digit, "max_cost": self.max_cost, "max_value": self.max_value, "combinations": state}
        return obj
