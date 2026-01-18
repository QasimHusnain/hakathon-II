"""
Unit tests for Task model.

Tests the Task dataclass, Status enum, and custom exceptions.
"""

import pytest
from src.models.task import Task, Status, InvalidTaskDataError


class TestStatus:
    """Test Status enum."""

    def test_status_pending(self) -> None:
        """Test PENDING status value."""
        assert Status.PENDING.value == "pending"

    def test_status_complete(self) -> None:
        """Test COMPLETE status value."""
        assert Status.COMPLETE.value == "complete"


class TestTask:
    """Test Task dataclass."""

    def test_task_creation_with_valid_data(self) -> None:
        """Test creating task with valid title."""
        task = Task(id=1, title="Test task", status=Status.PENDING)
        assert task.id == 1
        assert task.title == "Test task"
        assert task.status == Status.PENDING
        assert task.description is None

    def test_task_creation_with_description(self) -> None:
        """Test creating task with description."""
        task = Task(
            id=1,
            title="Test task",
            status=Status.PENDING,
            description="Test description"
        )
        assert task.description == "Test description"

    def test_task_creation_with_empty_title_raises_error(self) -> None:
        """Test that empty title raises InvalidTaskDataError."""
        with pytest.raises(InvalidTaskDataError, match="title cannot be empty"):
            Task(id=1, title="", status=Status.PENDING)

    def test_task_creation_with_whitespace_title_raises_error(self) -> None:
        """Test that whitespace-only title raises InvalidTaskDataError."""
        with pytest.raises(InvalidTaskDataError, match="title cannot be empty"):
            Task(id=1, title="   ", status=Status.PENDING)

    def test_task_creation_with_invalid_id_raises_error(self) -> None:
        """Test that non-positive ID raises ValueError."""
        with pytest.raises(ValueError, match="Task ID must be positive"):
            Task(id=0, title="Test", status=Status.PENDING)

        with pytest.raises(ValueError, match="Task ID must be positive"):
            Task(id=-1, title="Test", status=Status.PENDING)


class TestPriority:
    """
    Test Priority enum.

    Satisfies: specs/todo-features/tasks.md - T083
    """

    def test_priority_high_value(self) -> None:
        """Test HIGH priority has integer value 1."""
        from src.models.task import Priority
        assert Priority.HIGH.value == 1

    def test_priority_medium_value(self) -> None:
        """Test MEDIUM priority has integer value 2."""
        from src.models.task import Priority
        assert Priority.MEDIUM.value == 2

    def test_priority_low_value(self) -> None:
        """Test LOW priority has integer value 3."""
        from src.models.task import Priority
        assert Priority.LOW.value == 3

    def test_priority_ordering(self) -> None:
        """Test priority values support correct ordering (HIGH < MEDIUM < LOW)."""
        from src.models.task import Priority
        assert Priority.HIGH.value < Priority.MEDIUM.value < Priority.LOW.value


class TestRecurrence:
    """
    Test Recurrence enum.

    Satisfies: specs/todo-features/tasks.md - T083
    """

    def test_recurrence_none_value(self) -> None:
        """Test NONE recurrence has integer value 0."""
        from src.models.task import Recurrence
        assert Recurrence.NONE.value == 0

    def test_recurrence_daily_value(self) -> None:
        """Test DAILY recurrence has integer value 1."""
        from src.models.task import Recurrence
        assert Recurrence.DAILY.value == 1

    def test_recurrence_weekly_value(self) -> None:
        """Test WEEKLY recurrence has integer value 2."""
        from src.models.task import Recurrence
        assert Recurrence.WEEKLY.value == 2

    def test_recurrence_monthly_value(self) -> None:
        """Test MONTHLY recurrence has integer value 3."""
        from src.models.task import Recurrence
        assert Recurrence.MONTHLY.value == 3


class TestTaskWithCategory:
    """
    Test Task dataclass with category field.

    Satisfies: specs/todo-features/tasks.md - T082
    """

    def test_task_creation_with_category(self) -> None:
        """Test creating task with category."""
        from src.models.task import Priority
        task = Task(
            id=1,
            title="Test task",
            status=Status.PENDING,
            category="Work"
        )
        assert task.category == "Work"

    def test_task_default_category_is_none(self) -> None:
        """Test that default category is None."""
        task = Task(id=1, title="Test task", status=Status.PENDING)
        assert task.category is None

    def test_task_with_all_fields(self) -> None:
        """Test creating task with all enhanced fields."""
        from src.models.task import Priority, Recurrence
        from datetime import date, time
        task = Task(
            id=1,
            title="Full task",
            status=Status.PENDING,
            priority=Priority.HIGH,
            category="Project",
            description="Detailed description",
            due_date=date(2026, 1, 20),
            due_time=time(14, 30),
            recurring=Recurrence.WEEKLY
        )
        assert task.priority == Priority.HIGH
        assert task.category == "Project"
        assert task.description == "Detailed description"
        assert task.due_date == date(2026, 1, 20)
        assert task.due_time == time(14, 30)
        assert task.recurring == Recurrence.WEEKLY
