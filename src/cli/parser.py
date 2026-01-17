"""
Parser utilities for Enhanced Todo CLI.

Provides functions for parsing command arguments, dates, times,
and handling recurring task date advancement.

Satisfies: specs/todo-features/tasks.md - T003, T007, T008, T009
"""

from datetime import datetime, date, time, timedelta
from typing import Optional, Tuple, Dict, Any, List, Union
import calendar
import shlex

from src.models.task import Priority, Recurrence


def parse_date(date_str: str) -> date:
    """
    Parse a date string in YYYY-MM-DD format.

    Args:
        date_str: Date string in YYYY-MM-DD format

    Returns:
        date object

    Raises:
        ValueError: If date format is invalid

    Satisfies: specs/todo-features/tasks.md - T007
    """
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD")


def parse_time(time_str: str) -> time:
    """
    Parse a time string in HH:MM format.

    Args:
        time_str: Time string in HH:MM format

    Returns:
        time object

    Raises:
        ValueError: If time format is invalid

    Satisfies: specs/todo-features/tasks.md - T008
    """
    try:
        return datetime.strptime(time_str, "%H:%M").time()
    except ValueError:
        raise ValueError("Invalid time format. Use HH:MM")


def advance_date(current_date: date, recurrence: int) -> date:
    """
    Calculate the next occurrence date based on recurrence type.

    Handles monthly edge cases (e.g., Jan 31 -> Feb 28).

    Args:
        current_date: The current due date
        recurrence: Recurrence type (0=None, 1=Daily, 2=Weekly, 3=Monthly)

    Returns:
        Next occurrence date

    Satisfies: specs/todo-features/tasks.md - T009, T033
    """
    if recurrence == 1:  # DAILY
        return current_date + timedelta(days=1)
    elif recurrence == 2:  # WEEKLY
        return current_date + timedelta(weeks=1)
    elif recurrence == 3:  # MONTHLY
        # Handle month advancement with edge cases
        year = current_date.year
        month = current_date.month + 1
        day = current_date.day

        if month > 12:
            month = 1
            year += 1

        # Handle edge case: day doesn't exist in target month
        # e.g., Jan 31 -> Feb 28 (or 29 in leap year)
        max_day = calendar.monthrange(year, month)[1]
        day = min(day, max_day)

        return date(year, month, day)
    else:
        # No recurrence, return same date
        return current_date


def parse_add_options(args: List[str]) -> Dict[str, Any]:
    """
    Parse add command options from argument list.

    Extracts -d, -p, --date, --time, -r flags from the argument list.

    Args:
        args: List of argument strings (title and options)

    Returns:
        Dictionary with parsed options:
            - title: str
            - description: Optional[str]
            - priority: Optional[str]
            - due_date: Optional[str]
            - due_time: Optional[str]
            - recurring: Optional[str]

    Satisfies: specs/todo-features/tasks.md - T011
    """
    result: Dict[str, Any] = {
        "title": None,
        "description": None,
        "priority": None,
        "due_date": None,
        "due_time": None,
        "recurring": None,
    }

    if not args:
        return result

    i = 0
    title_parts = []

    while i < len(args):
        arg = args[i]

        if arg in ("-d", "--desc"):
            if i + 1 < len(args):
                result["description"] = args[i + 1]
                i += 2
            else:
                i += 1
        elif arg in ("-p", "--priority"):
            if i + 1 < len(args):
                result["priority"] = args[i + 1]
                i += 2
            else:
                i += 1
        elif arg == "--date":
            if i + 1 < len(args):
                result["due_date"] = args[i + 1]
                i += 2
            else:
                i += 1
        elif arg == "--time":
            if i + 1 < len(args):
                result["due_time"] = args[i + 1]
                i += 2
            else:
                i += 1
        elif arg in ("-r", "--recurring"):
            if i + 1 < len(args):
                result["recurring"] = args[i + 1]
                i += 2
            else:
                i += 1
        else:
            # Part of the title
            title_parts.append(arg)
            i += 1

    if title_parts:
        result["title"] = " ".join(title_parts)

    return result


def parse_list_filters(args: List[str]) -> Dict[str, Any]:
    """
    Parse list command filter options.

    Extracts --pending, --complete, --priority, --today, --overdue flags.

    Args:
        args: List of argument strings

    Returns:
        Dictionary with parsed filters:
            - status: Optional[str] ('pending' or 'complete')
            - priority: Optional[str] ('high', 'medium', 'low')
            - today: bool
            - overdue: bool

    Satisfies: specs/todo-features/tasks.md - T048
    """
    result: Dict[str, Any] = {
        "status": None,
        "priority": None,
        "today": False,
        "overdue": False,
    }

    i = 0
    while i < len(args):
        arg = args[i]

        if arg == "--pending":
            result["status"] = "pending"
            i += 1
        elif arg == "--complete":
            result["status"] = "complete"
            i += 1
        elif arg == "--priority":
            if i + 1 < len(args):
                result["priority"] = args[i + 1]
                i += 2
            else:
                i += 1
        elif arg == "--today":
            result["today"] = True
            i += 1
        elif arg == "--overdue":
            result["overdue"] = True
            i += 1
        else:
            i += 1

    return result


def validate_priority_input(value: str) -> Optional[Priority]:
    """
    Validate and convert priority input (1=High, 2=Medium, 3=Low).

    Args:
        value: User input string

    Returns:
        Priority enum if valid, None if invalid

    Satisfies: specs/todo-features/tasks.md - T017
    """
    try:
        num = int(value)
        if num == 1:
            return Priority.HIGH
        elif num == 2:
            return Priority.MEDIUM
        elif num == 3:
            return Priority.LOW
    except ValueError:
        pass
    return None


def validate_recurring_input(value: str) -> Optional[Recurrence]:
    """
    Validate and convert recurring input (1=Daily, 2=Weekly, 3=Monthly).

    Args:
        value: User input string

    Returns:
        Recurrence enum if valid, None if invalid

    Satisfies: specs/todo-features/tasks.md - T018
    """
    try:
        num = int(value)
        if num == 1:
            return Recurrence.DAILY
        elif num == 2:
            return Recurrence.WEEKLY
        elif num == 3:
            return Recurrence.MONTHLY
        elif num == 0:
            return Recurrence.NONE
    except ValueError:
        pass
    return None


def validate_date_input(value: str) -> Optional[Tuple[date, Optional[time]]]:
    """
    Validate and parse date input (YYYY-MM-DD or YYYY-MM-DD HH:MM).

    Args:
        value: User input string

    Returns:
        Tuple of (date, time or None) if valid, None if invalid

    Satisfies: specs/todo-features/tasks.md - T019
    """
    value = value.strip()
    if not value:
        return None

    # Try YYYY-MM-DD HH:MM format first
    if " " in value:
        parts = value.split(" ", 1)
        try:
            parsed_date = datetime.strptime(parts[0], "%Y-%m-%d").date()
            parsed_time = datetime.strptime(parts[1], "%H:%M").time()
            return (parsed_date, parsed_time)
        except ValueError:
            return None
    else:
        # Try YYYY-MM-DD format
        try:
            parsed_date = datetime.strptime(value, "%Y-%m-%d").date()
            return (parsed_date, None)
        except ValueError:
            return None


def validate_menu_choice(value: str, min_val: int, max_val: int) -> Optional[int]:
    """
    Validate menu choice input within a range.

    Args:
        value: User input string
        min_val: Minimum valid value (inclusive)
        max_val: Maximum valid value (inclusive)

    Returns:
        Integer if valid, None if invalid

    Satisfies: specs/todo-features/tasks.md - T020
    """
    try:
        num = int(value)
        if min_val <= num <= max_val:
            return num
    except ValueError:
        pass
    return None
