from hypothesis import given, strategies as hst
import unittest

import onedigit

# class Model:
#     digit: int
#     upper_value: int
#     state: List[Combo]
#     logger: logging.Logger
#     def __init__(self, digit: int, upper_value: int = 100, empty: bool = False): ...


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
    def test_model_creation_good(self, digit):

        # Good digit
        model = onedigit.Model(digit=digit, max_value=99, max_cost=4)
        self.check_model(model, digit)

    @given(digit=hst.integers(min_value=10))
    def test_model_creation_bad(self, digit):
        # Bad digit
        with self.assertRaises(expected_exception=ValueError):
            model = onedigit.Model(digit=digit, max_value=99, max_cost=4)

    @given(digit=hst.integers(min_value=1, max_value=9))
    def test_model_copy(self, digit):
        # Create a copy and delete the original
        model1 = onedigit.Model(digit=digit, max_value=99, max_cost=4)
        model2 = model1.copy()
        del model1

        # Verify integrity of the copy
        self.check_model(model2, digit)
