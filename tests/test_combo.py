import math

from hypothesis import given, strategies as hst

import onedigit

# value: int
# cost: int = -1
# expr: str = ""
# expr_simple: str = ""


@given(value1=hst.integers())
def test_combo_positional(value1):
    combo1 = onedigit.Combo(value1)

    assert combo1.value == value1


@given(value1=hst.integers(), value2=hst.integers())
def test_combo_addition(value1, value2):
    combo1 = onedigit.Combo(value1)
    combo2 = onedigit.Combo(value2)

    combo3 = combo1.binary_operation(combo2, "+")
    combo4 = combo2.binary_operation(combo1, "+")

    assert combo3.value == combo4.value
    assert combo3.value == (value1 + value2)


@given(value1=hst.integers(), value2=hst.integers())
def test_combo_multiplication(value1, value2):
    combo1 = onedigit.Combo(value1)
    combo2 = onedigit.Combo(value2)

    combo3 = combo1.binary_operation(combo2, "*")
    combo4 = combo2.binary_operation(combo1, "*")

    assert combo3.value == combo4.value
    assert combo3.value == (value1 * value2)


@given(value1=hst.integers())
def test_combo_sqrt(value1):
    combo1 = onedigit.Combo(value1)

    combo2 = combo1.unary_operation("sqrt")

    assert (combo2.value * combo2.value) == value1


# Protect against gigantic values crashing the
# tester. 50! is over 3x10^64
@given(value1=hst.integers(max_value=50))
def test_combo_factorial(value1):
    combo1 = onedigit.Combo(value1)

    combo2 = combo1.unary_operation("!")

    # The class needs to guard against bad input
    if (value1 < 0) or (value1 > 11):
        assert combo2.value == 0
        return

    assert combo2.value == math.factorial(value1)
