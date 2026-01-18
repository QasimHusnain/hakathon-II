"""
Integration tests for CLI command handlers.

Tests the interaction between CLI handlers and TaskManager service.

Satisfies: specs/todo-features/tasks.md - T089, T090, T091
"""

import pytest
from io import StringIO
from unittest.mock import patch
from datetime import date

from src.services.task_manager import TaskManager
from src.models.task import Status, Priority, Recurrence
from src.cli.commands import (
    handle_add_task,
    handle_view_tasks,
    handle_filter_menu,
    handle_sort_menu,
    handle_delete_task,
    handle_toggle_complete,
    handle_update_task,
)


class TestAddTaskIntegration:
    """
    Integration tests for Add Task flow.

    Satisfies: specs/todo-features/tasks.md - T089
    """

    def test_add_task_with_all_fields(self) -> None:
        """Test adding task with all fields via CLI handler."""
        manager = TaskManager()

        # Simulate user input: title, description, priority, category, due date, recurring
        inputs = [
            "Buy groceries",       # title
            "Get milk and eggs",   # description
            "1",                   # priority (High)
            "Shopping",            # category
            "2026-01-20 14:30",   # due date with time
            "2",                   # recurring (Weekly)
        ]

        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                handle_add_task(manager)
                output = mock_stdout.getvalue()

        # Verify task was created
        assert len(manager.tasks) == 1
        task = manager.get_task(1)
        assert task.title == "Buy groceries"
        assert task.description == "Get milk and eggs"
        assert task.priority == Priority.HIGH
        assert task.category == "Shopping"
        assert task.due_date == date(2026, 1, 20)
        assert task.recurring == Recurrence.WEEKLY

        # Verify success message
        assert "Task added successfully!" in output
        assert "ID: 1" in output

    def test_add_task_with_minimal_fields(self) -> None:
        """Test adding task with only required title."""
        manager = TaskManager()

        # Simulate user input: title only, skip optional fields
        inputs = [
            "Simple task",  # title
            "",            # description (skip)
            "",            # priority (default)
            "",            # category (skip)
            "",            # due date (skip)
            "",            # recurring (skip)
        ]

        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new_callable=StringIO):
                handle_add_task(manager)

        # Verify task was created with defaults
        assert len(manager.tasks) == 1
        task = manager.get_task(1)
        assert task.title == "Simple task"
        assert task.description is None
        assert task.priority == Priority.MEDIUM
        assert task.category is None
        assert task.due_date is None
        assert task.recurring == Recurrence.NONE

    def test_add_task_empty_title_retries(self) -> None:
        """Test that empty title is rejected and user can retry."""
        manager = TaskManager()

        # Simulate: empty title, then valid title, then skip rest
        inputs = [
            "",            # empty title (rejected)
            "Valid title", # valid title
            "",            # description (skip)
            "",            # priority (default)
            "",            # category (skip)
            "",            # due date (skip)
            "",            # recurring (skip)
        ]

        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                handle_add_task(manager)
                output = mock_stdout.getvalue()

        # Verify error was shown and task was eventually created
        assert "Error: Task title cannot be empty" in output
        assert len(manager.tasks) == 1
        assert manager.get_task(1).title == "Valid title"


class TestFilterMenuIntegration:
    """
    Integration tests for Filter submenu.

    Satisfies: specs/todo-features/tasks.md - T090
    """

    def test_filter_by_category(self) -> None:
        """Test filtering tasks by category."""
        manager = TaskManager()
        manager.add_task("Work task 1", category="Work")
        manager.add_task("Personal task", category="Personal")
        manager.add_task("Work task 2", category="Work")

        # Simulate: choose category filter, enter "Work", then back
        inputs = ["1", "Work"]

        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                handle_filter_menu(manager)
                output = mock_stdout.getvalue()

        # Verify filtered output
        assert "FILTERED TASKS" in output
        assert "Work task 1" in output
        assert "Work task 2" in output
        assert "Personal task" not in output
        assert "Found: 2 task(s) matching filter" in output

    def test_filter_by_priority(self) -> None:
        """Test filtering tasks by priority."""
        manager = TaskManager()
        manager.add_task("High priority task", priority=Priority.HIGH)
        manager.add_task("Low priority task", priority=Priority.LOW)
        manager.add_task("Another high task", priority=Priority.HIGH)

        # Simulate: choose priority filter, enter "1" (High)
        inputs = ["2", "1"]

        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                handle_filter_menu(manager)
                output = mock_stdout.getvalue()

        # Verify filtered output
        assert "High priority task" in output
        assert "Another high task" in output
        assert "Low priority task" not in output
        assert "Found: 2 task(s) matching filter" in output

    def test_filter_by_status_pending(self) -> None:
        """Test filtering tasks by pending status."""
        manager = TaskManager()
        manager.add_task("Pending task")
        manager.add_task("Complete task")
        manager.toggle_complete(2)  # Mark second task complete

        # Simulate: choose status filter, then "Pending"
        inputs = ["3", "1"]

        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                handle_filter_menu(manager)
                output = mock_stdout.getvalue()

        # Verify only pending task shown
        assert "Pending task" in output
        assert "Found: 1 task(s) matching filter" in output

    def test_filter_no_matches(self) -> None:
        """Test filtering when no tasks match."""
        manager = TaskManager()
        manager.add_task("Work task", category="Work")

        # Simulate: filter by category "Personal" (no matches)
        inputs = ["1", "Personal"]

        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                handle_filter_menu(manager)
                output = mock_stdout.getvalue()

        assert "No tasks match your filter criteria." in output


class TestSortMenuIntegration:
    """
    Integration tests for Sort submenu.

    Satisfies: specs/todo-features/tasks.md - T091
    """

    def test_sort_by_due_date(self) -> None:
        """Test sorting tasks by due date."""
        manager = TaskManager()
        manager.add_task("Later task", due_date=date(2026, 3, 1))
        manager.add_task("Earlier task", due_date=date(2026, 1, 1))
        manager.add_task("Middle task", due_date=date(2026, 2, 1))

        # Simulate: choose sort by due date
        inputs = ["1"]

        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                handle_sort_menu(manager)
                output = mock_stdout.getvalue()

        # Verify sorted output - Earlier should appear before Later
        assert "SORTED TASKS" in output
        earlier_pos = output.find("Earlier task")
        middle_pos = output.find("Middle task")
        later_pos = output.find("Later task")
        assert earlier_pos < middle_pos < later_pos
        assert "sorted by due date" in output

    def test_sort_by_priority(self) -> None:
        """Test sorting tasks by priority."""
        manager = TaskManager()
        manager.add_task("Low task", priority=Priority.LOW)
        manager.add_task("High task", priority=Priority.HIGH)
        manager.add_task("Medium task", priority=Priority.MEDIUM)

        # Simulate: choose sort by priority
        inputs = ["2"]

        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                handle_sort_menu(manager)
                output = mock_stdout.getvalue()

        # Verify sorted output - High should appear before Low
        high_pos = output.find("High task")
        medium_pos = output.find("Medium task")
        low_pos = output.find("Low task")
        assert high_pos < medium_pos < low_pos
        assert "sorted by priority" in output

    def test_sort_empty_list(self) -> None:
        """Test sorting when no tasks exist."""
        manager = TaskManager()

        # Simulate: choose sort by due date on empty list
        inputs = ["1"]

        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                handle_sort_menu(manager)
                output = mock_stdout.getvalue()

        assert "Your task list is empty." in output


class TestDeleteTaskIntegration:
    """Integration tests for Delete Task flow."""

    def test_delete_task_with_confirmation(self) -> None:
        """Test deleting task with 'y' confirmation."""
        manager = TaskManager()
        manager.add_task("Task to delete")

        # Simulate: enter task ID, confirm with 'y'
        inputs = ["1", "y"]

        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                handle_delete_task(manager)
                output = mock_stdout.getvalue()

        # Verify task was deleted
        assert len(manager.tasks) == 0
        assert "deleted successfully" in output

    def test_delete_task_cancelled(self) -> None:
        """Test cancelling task deletion with 'n'."""
        manager = TaskManager()
        manager.add_task("Task to keep")

        # Simulate: enter task ID, cancel with 'n'
        inputs = ["1", "n"]

        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                handle_delete_task(manager)
                output = mock_stdout.getvalue()

        # Verify task was NOT deleted
        assert len(manager.tasks) == 1
        assert "Delete cancelled" in output


class TestToggleCompleteIntegration:
    """Integration tests for Toggle Complete flow."""

    def test_toggle_pending_to_complete(self) -> None:
        """Test toggling task from pending to complete."""
        manager = TaskManager()
        manager.add_task("Test task")

        inputs = ["1"]

        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                handle_toggle_complete(manager)
                output = mock_stdout.getvalue()

        assert manager.get_task(1).status == Status.COMPLETE
        assert "marked as complete" in output

    def test_toggle_recurring_creates_new_task(self) -> None:
        """Test toggling recurring task creates new occurrence."""
        manager = TaskManager()
        manager.add_task(
            "Recurring task",
            due_date=date(2026, 1, 20),
            recurring=Recurrence.WEEKLY
        )

        inputs = ["1"]

        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                handle_toggle_complete(manager)
                output = mock_stdout.getvalue()

        # Verify new recurring task was created
        assert len(manager.tasks) == 2
        assert "New recurring task created" in output
        assert "[2]" in output


class TestUpdateTaskIntegration:
    """Integration tests for Update Task flow."""

    def test_update_task_title(self) -> None:
        """Test updating task title through CLI."""
        manager = TaskManager()
        manager.add_task("Original title")

        # Simulate: enter task ID, choose title (1), enter new title, back (7)
        inputs = ["1", "1", "Updated title"]

        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                handle_update_task(manager)
                output = mock_stdout.getvalue()

        assert manager.get_task(1).title == "Updated title"
        assert "updated successfully" in output

    def test_update_nonexistent_task(self) -> None:
        """Test updating task that doesn't exist."""
        manager = TaskManager()

        inputs = ["99"]

        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                handle_update_task(manager)
                output = mock_stdout.getvalue()

        assert "Task [99] not found" in output
