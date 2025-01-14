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
    @given(digit=hst.integers(min_value=1, max_value=9))
    def test_model_creation_good(self, digit):
        # Good digit
        model = onedigit.Model(digit=digit)
        assert model.digit == digit

    @given(digit=hst.integers(min_value=10))
    def test_model_creation_bad(self, digit):
        # Bad digit
        with self.assertRaises(expected_exception=ValueError):
            model = onedigit.Model(digit=digit)

    @given(source=hst.integers())
    def test_model_copy(self, source):
        pass
