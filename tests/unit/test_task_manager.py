"""
Unit tests for TaskManager service.

Tests all CRUD operations and error handling.
"""

import pytest
from src.services.task_manager import TaskManager
from src.models.task import Status, TaskNotFoundError, InvalidTaskDataError


class TestTaskManager:
    """Test TaskManager class."""

    def test_initialization(self) -> None:
        """Test TaskManager initializes with empty storage."""
        manager = TaskManager()
        assert manager.tasks == {}
        assert manager.next_id == 1

    def test_add_task_with_title_only(self) -> None:
        """Test adding task with title only."""
        manager = TaskManager()
        task = manager.add_task("Test task")

        assert task.id == 1
        assert task.title == "Test task"
        assert task.status == Status.PENDING
        assert task.description is None
        assert len(manager.tasks) == 1

    def test_add_task_with_description(self) -> None:
        """Test adding task with title and description."""
        manager = TaskManager()
        task = manager.add_task("Test task", "Test description")

        assert task.description == "Test description"

    def test_add_task_increments_id(self) -> None:
        """Test that IDs increment sequentially."""
        manager = TaskManager()
        task1 = manager.add_task("Task 1")
        task2 = manager.add_task("Task 2")

        assert task1.id == 1
        assert task2.id == 2
        assert manager.next_id == 3

    def test_add_task_with_empty_title_raises_error(self) -> None:
        """Test adding task with empty title raises error."""
        manager = TaskManager()

        with pytest.raises(InvalidTaskDataError):
            manager.add_task("")

    def test_get_all_tasks_empty(self) -> None:
        """Test getting all tasks when list is empty."""
        manager = TaskManager()
        tasks = manager.get_all_tasks()

        assert tasks == []

    def test_get_all_tasks_with_multiple_tasks(self) -> None:
        """Test getting all tasks returns all added tasks."""
        manager = TaskManager()
        manager.add_task("Task 1")
        manager.add_task("Task 2")
        manager.add_task("Task 3")

        tasks = manager.get_all_tasks()
        assert len(tasks) == 3

    def test_get_task_by_id(self) -> None:
        """Test retrieving task by ID."""
        manager = TaskManager()
        added_task = manager.add_task("Test task")

        retrieved_task = manager.get_task(1)
        assert retrieved_task.id == added_task.id
        assert retrieved_task.title == added_task.title

    def test_get_task_with_invalid_id_raises_error(self) -> None:
        """Test getting non-existent task raises TaskNotFoundError."""
        manager = TaskManager()

        with pytest.raises(TaskNotFoundError, match="Task \\[99\\] not found"):
            manager.get_task(99)

    def test_toggle_complete_pending_to_complete(self) -> None:
        """Test toggling task from pending to complete."""
        manager = TaskManager()
        task = manager.add_task("Test task")

        assert task.status == Status.PENDING

        toggled_task, new_task = manager.toggle_complete(1)
        assert toggled_task.status == Status.COMPLETE
        assert new_task is None  # No recurring task created

    def test_toggle_complete_complete_to_pending(self) -> None:
        """Test toggling task from complete back to pending."""
        manager = TaskManager()
        manager.add_task("Test task")
        manager.toggle_complete(1)  # Make complete

        toggled_task, new_task = manager.toggle_complete(1)  # Toggle back
        assert toggled_task.status == Status.PENDING
        assert new_task is None  # Never creates recurring on toggle back

    def test_toggle_complete_invalid_id_raises_error(self) -> None:
        """Test toggling non-existent task raises error."""
        manager = TaskManager()

        with pytest.raises(TaskNotFoundError):
            manager.toggle_complete(99)

    def test_update_task_title(self) -> None:
        """Test updating task title."""
        manager = TaskManager()
        manager.add_task("Old title")

        updated_task = manager.update_task(1, title="New title")
        assert updated_task.title == "New title"

    def test_update_task_description(self) -> None:
        """Test updating task description."""
        manager = TaskManager()
        manager.add_task("Task")

        updated_task = manager.update_task(1, description="New description")
        assert updated_task.description == "New description"

    def test_update_task_both_fields(self) -> None:
        """Test updating both title and description."""
        manager = TaskManager()
        manager.add_task("Old title", "Old description")

        updated_task = manager.update_task(
            1,
            title="New title",
            description="New description"
        )
        assert updated_task.title == "New title"
        assert updated_task.description == "New description"

    def test_update_task_with_empty_title_raises_error(self) -> None:
        """Test updating with empty title raises error."""
        manager = TaskManager()
        manager.add_task("Original title")

        with pytest.raises(InvalidTaskDataError):
            manager.update_task(1, title="")

    def test_update_task_invalid_id_raises_error(self) -> None:
        """Test updating non-existent task raises error."""
        manager = TaskManager()

        with pytest.raises(TaskNotFoundError):
            manager.update_task(99, title="New title")

    def test_delete_task(self) -> None:
        """Test deleting a task."""
        manager = TaskManager()
        manager.add_task("Task 1")
        manager.add_task("Task 2")

        assert len(manager.tasks) == 2

        manager.delete_task(1)
        assert len(manager.tasks) == 1
        assert 1 not in manager.tasks
        assert 2 in manager.tasks

    def test_delete_task_invalid_id_raises_error(self) -> None:
        """Test deleting non-existent task raises error."""
        manager = TaskManager()

        with pytest.raises(TaskNotFoundError, match="Task \\[99\\] not found"):
            manager.delete_task(99)

    def test_delete_task_does_not_reuse_id(self) -> None:
        """Test that deleting task doesn't reuse ID."""
        manager = TaskManager()
        manager.add_task("Task 1")
        manager.delete_task(1)

        new_task = manager.add_task("Task 2")
        assert new_task.id == 2  # ID 1 not reused
