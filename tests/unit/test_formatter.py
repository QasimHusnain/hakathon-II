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

    def test_format_task_with_category(self) -> None:
        """
        Test formatting task with category shows category indicator.

        Satisfies: specs/todo-features/tasks.md - T088
        """
        task = Task(
            id=1,
            title="Test task",
            status=Status.PENDING,
            category="Work"
        )
        result = format_task(task)

        assert "[Work]" in result

    def test_format_task_without_category(self) -> None:
        """
        Test formatting task without category omits category indicator.

        Satisfies: specs/todo-features/tasks.md - T088
        """
        task = Task(
            id=1,
            title="Test task",
            status=Status.PENDING
        )
        result = format_task(task)

        # Should not have category brackets (other than status indicator)
        lines = result.split("\n")
        first_line = lines[0]
        # Check that no category indicator appears after the title area
        assert "[ ]" in first_line or "[X]" in first_line  # Status exists
        assert first_line.count("[") <= 3  # ID, status, maybe priority

    def test_format_task_with_priority(self) -> None:
        """
        Test formatting task with priority shows priority indicator.

        Satisfies: specs/todo-features/tasks.md - T088
        """
        from src.models.task import Priority
        task = Task(
            id=1,
            title="Test task",
            status=Status.PENDING,
            priority=Priority.HIGH
        )
        result = format_task(task)

        assert "[H]" in result

    def test_format_task_with_due_date(self) -> None:
        """
        Test formatting task with due date shows date info.

        Satisfies: specs/todo-features/tasks.md - T088
        """
        from datetime import date
        task = Task(
            id=1,
            title="Test task",
            status=Status.PENDING,
            due_date=date(2026, 1, 20)
        )
        result = format_task(task)

        assert "2026-01-20" in result

    def test_format_task_with_all_enhanced_fields(self) -> None:
        """
        Test formatting task with all enhanced fields.

        Satisfies: specs/todo-features/tasks.md - T088
        """
        from datetime import date, time
        from src.models.task import Priority, Recurrence
        task = Task(
            id=1,
            title="Complete project",
            status=Status.PENDING,
            priority=Priority.HIGH,
            category="Work",
            description="Finish the todo app",
            due_date=date(2026, 1, 20),
            due_time=time(14, 30),
            recurring=Recurrence.WEEKLY
        )
        result = format_task(task)

        assert "[1]" in result
        assert "[ ]" in result
        assert "[H]" in result
        assert "[Work]" in result
        assert "Complete project" in result
        assert "2026-01-20" in result
        assert "14:30" in result
        assert "Weekly" in result or "weekly" in result.lower()
        assert "Finish the todo app" in result


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
