import unittest

from hypothesis import given, strategies as hst

import onedigit

# class Model:
#     digit: int
#     max_value: int
#     max_cost: int
#     state: Dict[int, Combo]
#     logger: logging.Logger
#     def __init__(self, digit: int, max_value: int, max_cost: int, *, shallow: bool = False): ...


class Test_Model(unittest.TestCase):
    def check_model(self, model: onedigit.Model, digit: int):
        # Verify integrity of the object
        assert model is not None
        assert isinstance(model, onedigit.Model)

        # Verify integrity of the Model object
        assert isinstance(model.digit, int)
        assert model.digit == digit

        assert isinstance(model.state, dict)
        assert len(model.state) > 0

        # At least we should have a combination for the digit itself
        assert digit in model.state
        assert model.state[digit] is not None
        assert isinstance(model.state[digit], onedigit.Combo)
        assert model.state[digit].value == digit

    @given(digit=hst.integers(min_value=1, max_value=9))
    def test_model_creation_good(self, digit: int):
        # Good digit
        model1 = onedigit.Model(digit=digit, max_value=99, max_cost=4)
        self.check_model(model1, digit)

    @given(digit=hst.integers(min_value=10))
    def test_model_creation_bad(self, digit: int):
        # Bad digit
        with self.assertRaises(expected_exception=ValueError):
            model1 = onedigit.Model(digit=digit, max_value=99, max_cost=4)

    @given(digit=hst.integers(min_value=1, max_value=9))
    def test_model_copy_basic(self, digit: int):
        # Create a model with some combinations
        model1 = onedigit.Model(digit=digit, max_value=99, max_cost=4)
        # Get a copy and delete the original
        model2 = model1.copy()
        del model1

        # Verify integrity of the copy, after we have deleted the original
        self.check_model(model2, digit)
