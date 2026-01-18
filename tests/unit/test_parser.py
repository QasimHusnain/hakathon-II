"""
Unit tests for CLI parser validation utilities.

Tests validation functions for priority, recurring, date, and menu input.

Satisfies: specs/todo-features/tasks.md - T087
"""

import pytest
from datetime import date, time

from src.cli.parser import (
    validate_priority_input,
    validate_recurring_input,
    validate_date_input,
    validate_menu_choice,
    parse_date,
    parse_time,
    advance_date,
)
from src.models.task import Priority, Recurrence


class TestValidatePriorityInput:
    """Test validate_priority_input function."""

    def test_valid_high_priority(self) -> None:
        """Test input '1' returns HIGH priority."""
        result = validate_priority_input("1")
        assert result == Priority.HIGH

    def test_valid_medium_priority(self) -> None:
        """Test input '2' returns MEDIUM priority."""
        result = validate_priority_input("2")
        assert result == Priority.MEDIUM

    def test_valid_low_priority(self) -> None:
        """Test input '3' returns LOW priority."""
        result = validate_priority_input("3")
        assert result == Priority.LOW

    def test_invalid_priority_zero(self) -> None:
        """Test input '0' returns None."""
        result = validate_priority_input("0")
        assert result is None

    def test_invalid_priority_four(self) -> None:
        """Test input '4' returns None."""
        result = validate_priority_input("4")
        assert result is None

    def test_invalid_priority_text(self) -> None:
        """Test non-numeric input returns None."""
        result = validate_priority_input("high")
        assert result is None

    def test_invalid_priority_empty(self) -> None:
        """Test empty input returns None."""
        result = validate_priority_input("")
        assert result is None


class TestValidateRecurringInput:
    """Test validate_recurring_input function."""

    def test_valid_none_recurrence(self) -> None:
        """Test input '0' returns NONE recurrence."""
        result = validate_recurring_input("0")
        assert result == Recurrence.NONE

    def test_valid_daily_recurrence(self) -> None:
        """Test input '1' returns DAILY recurrence."""
        result = validate_recurring_input("1")
        assert result == Recurrence.DAILY

    def test_valid_weekly_recurrence(self) -> None:
        """Test input '2' returns WEEKLY recurrence."""
        result = validate_recurring_input("2")
        assert result == Recurrence.WEEKLY

    def test_valid_monthly_recurrence(self) -> None:
        """Test input '3' returns MONTHLY recurrence."""
        result = validate_recurring_input("3")
        assert result == Recurrence.MONTHLY

    def test_invalid_recurrence_four(self) -> None:
        """Test input '4' returns None."""
        result = validate_recurring_input("4")
        assert result is None

    def test_invalid_recurrence_text(self) -> None:
        """Test non-numeric input returns None."""
        result = validate_recurring_input("daily")
        assert result is None


class TestValidateDateInput:
    """Test validate_date_input function."""

    def test_valid_date_only(self) -> None:
        """Test valid YYYY-MM-DD format."""
        result = validate_date_input("2026-01-20")
        assert result is not None
        assert result[0] == date(2026, 1, 20)
        assert result[1] is None

    def test_valid_date_with_time(self) -> None:
        """Test valid YYYY-MM-DD HH:MM format."""
        result = validate_date_input("2026-01-20 14:30")
        assert result is not None
        assert result[0] == date(2026, 1, 20)
        assert result[1] == time(14, 30)

    def test_invalid_date_format(self) -> None:
        """Test invalid date format returns None."""
        result = validate_date_input("01-20-2026")
        assert result is None

    def test_invalid_time_format(self) -> None:
        """Test invalid time format returns None."""
        result = validate_date_input("2026-01-20 2:30pm")
        assert result is None

    def test_empty_input(self) -> None:
        """Test empty input returns None."""
        result = validate_date_input("")
        assert result is None

    def test_whitespace_input(self) -> None:
        """Test whitespace input returns None."""
        result = validate_date_input("   ")
        assert result is None


class TestValidateMenuChoice:
    """Test validate_menu_choice function."""

    def test_valid_choice_in_range(self) -> None:
        """Test valid choice within range."""
        result = validate_menu_choice("5", 1, 8)
        assert result == 5

    def test_valid_choice_min_boundary(self) -> None:
        """Test minimum boundary value."""
        result = validate_menu_choice("1", 1, 8)
        assert result == 1

    def test_valid_choice_max_boundary(self) -> None:
        """Test maximum boundary value."""
        result = validate_menu_choice("8", 1, 8)
        assert result == 8

    def test_invalid_choice_below_min(self) -> None:
        """Test choice below minimum returns None."""
        result = validate_menu_choice("0", 1, 8)
        assert result is None

    def test_invalid_choice_above_max(self) -> None:
        """Test choice above maximum returns None."""
        result = validate_menu_choice("9", 1, 8)
        assert result is None

    def test_invalid_choice_non_numeric(self) -> None:
        """Test non-numeric input returns None."""
        result = validate_menu_choice("abc", 1, 8)
        assert result is None


class TestParseDate:
    """Test parse_date function."""

    def test_parse_valid_date(self) -> None:
        """Test parsing valid date string."""
        result = parse_date("2026-01-20")
        assert result == date(2026, 1, 20)

    def test_parse_invalid_date_raises_error(self) -> None:
        """Test invalid date format raises ValueError."""
        with pytest.raises(ValueError, match="Invalid date format"):
            parse_date("01-20-2026")


class TestParseTime:
    """Test parse_time function."""

    def test_parse_valid_time(self) -> None:
        """Test parsing valid time string."""
        result = parse_time("14:30")
        assert result == time(14, 30)

    def test_parse_invalid_time_raises_error(self) -> None:
        """Test invalid time format raises ValueError."""
        with pytest.raises(ValueError, match="Invalid time format"):
            parse_time("2:30pm")


class TestAdvanceDate:
    """Test advance_date function for recurring tasks."""

    def test_advance_daily(self) -> None:
        """Test daily recurrence advances by one day."""
        result = advance_date(date(2026, 1, 20), 1)
        assert result == date(2026, 1, 21)

    def test_advance_weekly(self) -> None:
        """Test weekly recurrence advances by one week."""
        result = advance_date(date(2026, 1, 20), 2)
        assert result == date(2026, 1, 27)

    def test_advance_monthly(self) -> None:
        """Test monthly recurrence advances by one month."""
        result = advance_date(date(2026, 1, 20), 3)
        assert result == date(2026, 2, 20)

    def test_advance_monthly_end_of_month(self) -> None:
        """Test monthly edge case: Jan 31 -> Feb 28."""
        result = advance_date(date(2026, 1, 31), 3)
        assert result == date(2026, 2, 28)

    def test_advance_monthly_december_to_january(self) -> None:
        """Test monthly year boundary: Dec -> Jan."""
        result = advance_date(date(2026, 12, 15), 3)
        assert result == date(2027, 1, 15)

    def test_advance_none_returns_same(self) -> None:
        """Test no recurrence returns same date."""
        original = date(2026, 1, 20)
        result = advance_date(original, 0)
        assert result == original
