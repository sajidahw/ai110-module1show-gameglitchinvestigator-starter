import pytest
from logic_utils import check_guess, parse_guess


def test_exact_match_returns_win():  # FIX: Refactor import and updated assertion for tuple return value
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert message == "🎉 Correct!"


def test_guess_too_high_returns_correct_outcome_and_hint():  # FIX: Refactor import and updated assertion for tuple return value
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert message == "📉 Go LOWER!"


def test_guess_too_low_returns_correct_outcome_and_hint():  # FIX: Refactor import and updated assertion for tuple return value
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert message == "📈 Go HIGHER!"


def test_negative_input_is_rejected():  # FIX: added to verify parse_guess rejects negatives — previously accepted as valid guesses
    ok, value, err = parse_guess("-5")
    assert not ok
    assert value is None
    assert err is not None


def test_out_of_range_input_is_rejected():  # FIX: added low/high params to parse_guess and updated test to check for out-of-range input
    ok, value, err = parse_guess("9999", low=1, high=100)
    assert not ok
    assert value is None
    assert err is not None


def test_decimal_input_is_truncated_to_int():  # FIX: added to document that decimals are silently truncated (3.9 → 3) rather than rejected or warned about
    # "3.9" is silently truncated to 3 via int(float(raw)) — documents known truncation behavior
    ok, value, err = parse_guess("3.9")
    assert ok
    assert value == 3
    assert err is None
