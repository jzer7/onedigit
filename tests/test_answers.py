import math
import unittest

from hypothesis import given, strategies as hst

import onedigit


class TestAnswers(unittest.TestCase):
    @given(
        digit=hst.integers(min_value=1, max_value=9),
        upper_value=hst.integers(min_value=10, max_value=50),
        steps=hst.integers(min_value=2, max_value=3),
    )

    def test_answers(self, digit: int, upper_value: int, steps: int) -> None:
        model = onedigit.Model(digit=digit, upper_value=upper_value)
        assert model is not None
        onedigit.advance(state=model, steps=steps)

        for combo in model.get_valid_combos():
            val, cost = combo.value, combo.cost
            expr_full, expr_simple = combo.expr_full, combo.expr_simple

            # Check cost is correct
            assert cost == expr_full.count(str(digit))

            # Ensure upper value was respected
            assert val <= upper_value
