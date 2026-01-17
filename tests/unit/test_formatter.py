"""
Unit tests for CLI formatter functions.

Tests task formatting, list formatting, and message formatting.
"""

from src.cli.formatter import format_task, format_task_list, format_success, format_error
from src.models.task import Task, Status


class TestFormatTask:
    """Test format_task function."""

    def test_format_pending_task_without_description(self) -> None:
        """Test formatting pending task without description."""
        task = Task(id=1, title="Test task", status=Status.PENDING)
        result = format_task(task)

        assert "[1]" in result
        assert "[ ]" in result
        assert "Test task" in result
        assert "\n" not in result  # No description line

    def test_format_complete_task(self) -> None:
        """Test formatting complete task shows [X]."""
        task = Task(id=1, title="Test task", status=Status.COMPLETE)
        result = format_task(task)

        assert "[X]" in result
        assert "[ ]" not in result

    def test_format_task_with_description(self) -> None:
        """Test formatting task with description."""
        task = Task(
            id=1,
            title="Test task",
            status=Status.PENDING,
            description="Test description"
        )
        result = format_task(task)

        assert "Test task" in result
        assert "Test description" in result
        assert "    " in result  # Indentation for description


class TestFormatTaskList:
    """Test format_task_list function."""

    def test_format_empty_list(self) -> None:
        """Test formatting empty task list."""
        result = format_task_list([])

        assert "empty" in result.lower()
        assert "add" in result.lower()

    def test_format_list_with_single_task(self) -> None:
        """Test formatting list with one task."""
        tasks = [Task(id=1, title="Test task", status=Status.PENDING)]
        result = format_task_list(tasks)

        assert "Your Tasks:" in result
        assert "[1]" in result
        assert "Total: 1 task(s)" in result

    def test_format_list_with_multiple_tasks(self) -> None:
        """Test formatting list with multiple tasks."""
        tasks = [
            Task(id=1, title="Task 1", status=Status.PENDING),
            Task(id=2, title="Task 2", status=Status.COMPLETE),
            Task(id=3, title="Task 3", status=Status.PENDING)
        ]
        result = format_task_list(tasks)

        assert "Task 1" in result
        assert "Task 2" in result
        assert "Task 3" in result
        assert "Total: 3 task(s)" in result


class TestFormatMessages:
    """Test message formatting functions."""

    def test_format_success(self) -> None:
        """Test formatting success message."""
        result = format_success("Task added")

        assert "✓" in result
        assert "Task added" in result

    def test_format_error(self) -> None:
        """Test formatting error message."""
        result = format_error("Task not found")

        assert "Error:" in result
        assert "Task not found" in result
