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
