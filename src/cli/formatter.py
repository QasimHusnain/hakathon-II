"""
Output formatting for Todo CLI Enhanced.

Satisfies: specs/001-todo-cli-basic/tasks.md - T012, T013, T040, T041
Satisfies: specs/002-enhanced-todo-features/tasks.md - T013, T014, T015, T016, T019, T020, T021, T022, T023, T050
"""

from datetime import date, time
from typing import Optional
from src.models.task import Task, Status, Priority, Recurrence

# Separation line constants (T013, T014)
SEPARATOR_MAJOR = "=" * 40
SEPARATOR_MINOR = "-" * 40


def format_priority(priority: Priority) -> str:
    """
    Format priority as indicator [H], [M], [L].

    Args:
        priority: Priority enum value

    Returns:
        Formatted priority indicator

    Satisfies: specs/002-enhanced-todo-features/tasks.md - T019
    """
    indicators = {
        Priority.HIGH: "[H]",
        Priority.MEDIUM: "[M]",
        Priority.LOW: "[L]"
    }
    return indicators.get(priority, "[M]")


def format_due_info(
    due_date: Optional[date],
    due_time: Optional[time],
    recurring: Recurrence
) -> str:
    """
    Format due date, time, and recurring info.

    Args:
        due_date: Optional due date
        due_time: Optional due time
        recurring: Recurrence type

    Returns:
        Formatted due info string or empty string if no info

    Satisfies: specs/002-enhanced-todo-features/tasks.md - T020, T023
    """
    parts = []

    if due_date:
        date_str = due_date.strftime("%Y-%m-%d")
        if due_time:
            time_str = due_time.strftime("%H:%M")
            parts.append(f"Due: {date_str} {time_str}")
        else:
            parts.append(f"Due: {date_str}")
    elif due_time:
        time_str = due_time.strftime("%H:%M")
        parts.append(f"Due: {time_str}")

    if recurring != Recurrence.NONE:
        recurrence_names = {1: "Daily", 2: "Weekly", 3: "Monthly"}
        parts.append(f"Recurring: {recurrence_names.get(recurring.value, 'None')}")

    return " | ".join(parts)


def format_task(task: Task) -> str:
    """
    Format a single task with status, priority, category, and due info indicators.

    Args:
        task: Task object to format

    Returns:
        Formatted string with all indicators and task details

    Satisfies: specs/001-todo-cli-basic/tasks.md - T012
    Satisfies: specs/002-enhanced-todo-features/tasks.md - T015, T016, T021, T023
    """
    # Status indicator: [ ] for pending, [X] for complete
    status_indicator = "[X]" if task.status == Status.COMPLETE else "[ ]"

    # Priority indicator: [H], [M], [L]
    priority_indicator = format_priority(task.priority)

    # Category indicator: [Category] if set (T015)
    category_indicator = f" [{task.category}]" if task.category else ""

    # Format: [ID] [status] [priority] [category] title
    result = f"[{task.id}] {status_indicator} {priority_indicator}{category_indicator} {task.title}"

    # Add due info line if any due info exists (T023)
    due_info = format_due_info(task.due_date, task.due_time, task.recurring)
    if due_info:
        result += f"\n     {due_info}"

    # Add description on new line if present
    if task.description:
        result += f"\n     {task.description}"

    return result


def format_task_list(tasks: list[Task], is_filtered: bool = False) -> str:
    """
    Format complete task list with all enhanced indicators.

    Args:
        tasks: List of Task objects to format
        is_filtered: Whether the list is a filtered result

    Returns:
        Formatted string with all tasks or appropriate empty message

    Satisfies: specs/001-todo-cli-basic/tasks.md - T013
    Satisfies: specs/002-enhanced-todo-features/tasks.md - T022, T050
    """
    if not tasks:
        if is_filtered:
            return "No tasks match your filter criteria."
        return "Your task list is empty. Use 'add' to create a task."

    result = "Your Tasks:\n\n"

    for task in tasks:
        result += format_task(task) + "\n"

    result += f"\nTotal: {len(tasks)} task(s)"

    return result


def format_success(message: str) -> str:
    """
    Format success message with checkmark.

    Args:
        message: Success message text

    Returns:
        Formatted success message

    Satisfies: specs/001-todo-cli-basic/tasks.md - T040
    """
    return f"✓ {message}"


def format_error(message: str) -> str:
    """
    Format error message.

    Args:
        message: Error message text

    Returns:
        Formatted error message

    Satisfies: specs/001-todo-cli-basic/tasks.md - T041
    """
    return f"Error: {message}"
