from hypothesis import given, strategies as st
from car_insurance_premium_parser import normalize_registration, total_claim_amount, driver_age


@given(st.text() | st.none())
def test_normalize_registration_no_crash(s):
    """
    Feed arbitrary text (including None) into normalize_registration.
    The function must either return a string or raise ValueError.
    It must NEVER raise any other exception (e.g. AttributeError, TypeError).
    """
    try:
        result = normalize_registration(s)
        # If it succeeds the result should be a non-empty string of uppercase chars
        assert isinstance(result, str)
        assert len(result) > 0
    except ValueError:
        pass  # Expected for None or blank / whitespace-only inputs


@given(st.text() | st.none())
def test_total_claim_amount_no_crash(s):
    """
    Feed arbitrary text (including None) into total_claim_amount.
    The function must either return an integer or raise ValueError.
    It must NEVER raise any other exception (e.g. AttributeError, TypeError).
    """
    try:
        result = total_claim_amount(s)
        assert isinstance(result, int)
    except ValueError:
        pass  # Expected for None, blank input, or non-numeric tokens


@given(st.text() | st.none())
def test_driver_age_no_crash(s):
    """
    Feed arbitrary text (including None) into driver_age.
    The function must either return an integer or raise ValueError.
    It must NEVER raise any other exception (e.g. AttributeError, TypeError,
    IndexError).
    """
    try:
        result = driver_age(s)
        assert isinstance(result, int)
    except ValueError:
        pass  # Expected for None, missing '/', wrong number of parts, non-numeric year
