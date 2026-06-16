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


def test_negative_input_is_rejected():
    ok, value, err = parse_guess("-5")
    assert not ok
    assert value is None
    assert err is not None


def test_out_of_range_input_is_rejected():
    ok, value, err = parse_guess("9999", low=1, high=100)
    assert not ok
    assert value is None
    assert err is not None
