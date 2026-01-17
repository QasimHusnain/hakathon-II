# Research: Enhanced Todo CLI

**Feature**: todo-features
**Date**: 2026-01-16
**Status**: Complete

## Overview

This document captures research findings and design decisions for the Enhanced Todo CLI feature. All technical constraints are defined by the constitution, so no external research was required.

## Decision Log

### 1. Date/Time Parsing

**Decision**: Use `datetime.strptime` with strict format validation

**Rationale**:
- Standard library only (constitution constraint)
- Clear error messages for invalid formats
- Consistent parsing across all date/time inputs

**Alternatives Considered**:
- `dateutil.parser` - Rejected: external dependency
- Manual string parsing - Rejected: error-prone, reinventing the wheel

**Implementation**:
```python
from datetime import datetime, date, time

def parse_date(date_str: str) -> date:
    return datetime.strptime(date_str, "%Y-%m-%d").date()

def parse_time(time_str: str) -> time:
    return datetime.strptime(time_str, "%H:%M").time()
```

### 2. Monthly Recurrence Edge Case

**Decision**: Use `calendar.monthrange` to handle month-end dates

**Rationale**:
- Jan 31 + 1 month should become Feb 28/29, not error
- Standard library `calendar` module provides days-in-month calculation
- Consistent with user expectations

**Alternatives Considered**:
- Error on invalid dates - Rejected: poor UX
- `dateutil.relativedelta` - Rejected: external dependency

**Implementation**:
```python
from calendar import monthrange
from datetime import date, timedelta

def advance_by_month(d: date) -> date:
    year = d.year + (d.month // 12)
    month = (d.month % 12) + 1
    max_day = monthrange(year, month)[1]
    day = min(d.day, max_day)
    return date(year, month, day)
```

### 3. Argument Parsing for Add Command

**Decision**: Use `shlex.split` + manual flag parsing

**Rationale**:
- Already using `shlex` in existing codebase
- Handles quoted strings properly
- Simple to extend for new flags
- No additional dependencies

**Alternatives Considered**:
- `argparse` subparsers - Rejected: overkill for simple CLI, verbose error messages
- `click` library - Rejected: external dependency
- Custom tokenizer - Rejected: reinventing the wheel

**Flag Mapping**:
| Flag | Long Form | Value |
|------|-----------|-------|
| `-d` | `--desc` | Description text |
| `-p` | `--priority` | high/medium/low |
| `-r` | `--recurring` | daily/weekly/monthly |
| | `--date` | YYYY-MM-DD |
| | `--time` | HH:MM |

### 4. Filter Implementation

**Decision**: Separate filter methods in TaskManager, combined in CLI

**Rationale**:
- Single responsibility: each filter method does one thing
- Composable: CLI can combine filters if needed later
- Testable: each filter can be unit tested independently

**Methods**:
- `get_tasks_by_status(status: Status) -> list[Task]`
- `get_tasks_by_priority(priority: Priority) -> list[Task]`
- `get_tasks_due_today() -> list[Task]`
- `get_tasks_overdue() -> list[Task]`

### 5. Display Format

**Decision**: Multi-line format with clear visual indicators

**Rationale**:
- Matches existing `001-todo-cli-basic` style
- Easy to scan for priority/status at a glance
- Description on separate line avoids line wrapping issues

**Format**:
```
[ID] [Status] [Priority] Title
     Due: YYYY-MM-DD HH:MM | Recurring: type
     Description text here
```

**Indicators**:
- Status: `[ ]` pending, `[X]` complete
- Priority: `[H]` high, `[M]` medium, `[L]` low
- Recurring: `(Daily)`, `(Weekly)`, `(Monthly)`

### 6. Error Message Strategy

**Decision**: User-friendly messages with correct format hints

**Rationale**:
- Help users fix mistakes quickly
- Consistent format across all error types
- Include valid options when applicable

**Examples**:
- Invalid date: `Error: Invalid date format. Use YYYY-MM-DD (e.g., 2026-01-16)`
- Invalid priority: `Error: Invalid priority. Use: high, medium, low`
- Task not found: `Error: Task [5] not found`

## No Unknowns

All technical decisions are resolved by:
1. Constitution constraints (Python 3.13+, standard library only, in-memory)
2. Existing codebase patterns from `001-todo-cli-basic`
3. Standard software engineering practices

## References

- Python `datetime` module: https://docs.python.org/3/library/datetime.html
- Python `calendar` module: https://docs.python.org/3/library/calendar.html
- Python `shlex` module: https://docs.python.org/3/library/shlex.html
