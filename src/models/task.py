"""
Task model and related types for Todo CLI Enhanced.

Satisfies: specs/001-todo-cli-basic/tasks.md - T006, T007, T008
Satisfies: specs/002-enhanced-todo-features/tasks.md - T002, T004, T005, T006
"""

from dataclasses import dataclass, field
from datetime import datetime, date, time
from enum import Enum
from typing import Optional
import calendar


class Status(Enum):
    """
    Task completion status.

    Satisfies: specs/001-todo-cli-basic/tasks.md - T006
    """
    PENDING = "pending"
    COMPLETE = "complete"


class Priority(Enum):
    """
    Task priority level with integer values for numeric menu input.

    Satisfies: specs/002-enhanced-todo-features/tasks.md - T004, T005
    """
    HIGH = 1
    MEDIUM = 2
    LOW = 3


class Recurrence(Enum):
    """
    Task recurrence type with integer values for numeric menu input.

    Satisfies: specs/002-enhanced-todo-features/tasks.md - T005, T006
    """
    NONE = 0
    DAILY = 1
    WEEKLY = 2
    MONTHLY = 3


class TaskError(Exception):
    """
    Base exception for all task-related errors.

    Satisfies: specs/001-todo-cli-basic/tasks.md - T007
    """
    pass


class TaskNotFoundError(TaskError):
    """
    Raised when attempting to operate on non-existent task ID.

    Satisfies: specs/001-todo-cli-basic/tasks.md - T007
    """
    pass


class InvalidTaskDataError(TaskError):
    """
    Raised when task data fails validation.

    Satisfies: specs/001-todo-cli-basic/tasks.md - T007
    """
    pass


@dataclass
class Task:
    """
    Represents a single to-do item with enhanced attributes.

    Attributes:
        id: Unique identifier (positive integer)
        title: Task title (non-empty string)
        status: Completion status (Status enum)
        priority: Task priority level (Priority enum)
        category: Optional task category
        description: Optional task description
        due_date: Optional due date
        due_time: Optional due time
        recurring: Recurrence type (Recurrence enum)
        created_at: Timestamp when task was created

    Satisfies: specs/001-todo-cli-basic/tasks.md - T008
    Satisfies: specs/002-enhanced-todo-features/tasks.md - T004, T006
    """
    id: int
    title: str
    status: Status
    priority: Priority = Priority.MEDIUM
    category: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[date] = None
    due_time: Optional[time] = None
    recurring: Recurrence = Recurrence.NONE
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        """
        Validate task data after initialization.

        Raises:
            ValueError: If task ID is not positive
            InvalidTaskDataError: If title is empty or whitespace-only
        """
        if self.id <= 0:
            raise ValueError("Task ID must be positive integer")
        if not self.title or not self.title.strip():
            raise InvalidTaskDataError("Task title cannot be empty or whitespace-only")
