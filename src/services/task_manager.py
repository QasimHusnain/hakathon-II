"""
TaskManager service for managing tasks.

Satisfies: specs/001-todo-cli-basic/tasks.md - T009, and later tasks for methods
Satisfies: specs/todo-features/tasks.md - T010, T012, T030-T036, T037-T043, T044-T047
"""

from datetime import date, time
from typing import Optional, Tuple
from src.models.task import Task, Status, Priority, Recurrence, TaskNotFoundError, InvalidTaskDataError
from src.cli.parser import advance_date


class TaskManager:
    """
    Manages the collection of tasks and provides CRUD operations.

    Supports enhanced Task fields: priority, due_date, due_time, recurring, created_at.

    Satisfies: specs/001-todo-cli-basic/tasks.md - T009
    Satisfies: specs/todo-features/tasks.md - T010
    """

    def __init__(self) -> None:
        """
        Initialize TaskManager with empty task storage.

        Storage handles all Task fields including enhanced attributes.

        Satisfies: specs/001-todo-cli-basic/tasks.md - T009
        Satisfies: specs/todo-features/tasks.md - T010
        """
        self.tasks: dict[int, Task] = {}
        self.next_id: int = 1

    def add_task(
        self,
        title: str,
        description: Optional[str] = None,
        priority: Priority = Priority.MEDIUM,
        category: Optional[str] = None,
        due_date: Optional[date] = None,
        due_time: Optional[time] = None,
        recurring: Recurrence = Recurrence.NONE
    ) -> Task:
        """
        Add a new task to the manager with enhanced attributes.

        Args:
            title: Task title (non-empty string)
            description: Optional task description
            priority: Task priority level (defaults to MEDIUM)
            category: Optional task category
            due_date: Optional due date
            due_time: Optional due time
            recurring: Recurrence type (defaults to NONE)

        Returns:
            Created Task object

        Raises:
            InvalidTaskDataError: If title is empty or whitespace-only

        Satisfies: specs/001-todo-cli-basic/tasks.md - T010
        Satisfies: specs/todo-features/tasks.md - T011, T012
        """
        # Validation happens in Task.__post_init__
        task = Task(
            id=self.next_id,
            title=title,
            status=Status.PENDING,
            priority=priority,
            category=category,
            description=description,
            due_date=due_date,
            due_time=due_time,
            recurring=recurring
        )
        self.tasks[self.next_id] = task
        self.next_id += 1
        return task

    def get_all_tasks(self) -> list[Task]:
        """
        Retrieve all tasks in the system.

        Returns:
            List of all Task objects (may be empty)

        Satisfies: specs/001-todo-cli-basic/tasks.md - T011
        """
        return list(self.tasks.values())

    def get_task(self, task_id: int) -> Task:
        """
        Retrieve a task by its ID.

        Args:
            task_id: The task's unique identifier

        Returns:
            Task object if found

        Raises:
            TaskNotFoundError: If task_id doesn't exist

        Satisfies: specs/001-todo-cli-basic/tasks.md - T020
        """
        if task_id not in self.tasks:
            raise TaskNotFoundError(f"Task [{task_id}] not found")
        return self.tasks[task_id]

    def toggle_complete(self, task_id: int) -> Tuple[Task, Optional[Task]]:
        """
        Toggle task status between PENDING and COMPLETE.

        For recurring tasks being marked complete, automatically creates
        the next occurrence with advanced due date.

        Args:
            task_id: The task's unique identifier

        Returns:
            Tuple of (toggled_task, new_recurring_task_or_none)
            new_recurring_task is only set when completing a recurring pending task

        Raises:
            TaskNotFoundError: If task_id doesn't exist

        Satisfies: specs/001-todo-cli-basic/tasks.md - T021
        Satisfies: specs/todo-features/tasks.md - T030, T031, T032, T034, T036
        """
        task = self.get_task(task_id)
        new_task: Optional[Task] = None

        # Toggle status
        if task.status == Status.PENDING:
            task.status = Status.COMPLETE

            # Check if recurring and create next occurrence (T030, T031, T036)
            if task.recurring != Recurrence.NONE and task.due_date:
                # Calculate next due date using advance_date (T032)
                next_due_date = advance_date(task.due_date, task.recurring.value)

                # Create next occurrence
                new_task = self.add_task(
                    title=task.title,
                    description=task.description,
                    priority=task.priority,
                    category=task.category,
                    due_date=next_due_date,
                    due_time=task.due_time,
                    recurring=task.recurring
                )
        else:
            # Toggling complete→pending does NOT create new recurring task (T036)
            task.status = Status.PENDING

        return (task, new_task)

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[Priority] = None,
        category: Optional[str] = None,
        due_date: Optional[date] = None,
        due_time: Optional[time] = None,
        recurring: Optional[Recurrence] = None
    ) -> Task:
        """
        Update any attribute of an existing task.

        Args:
            task_id: The task's unique identifier
            title: New title if updating
            description: New description if updating
            priority: New priority if updating
            category: New category if updating
            due_date: New due date if updating
            due_time: New due time if updating
            recurring: New recurrence type if updating

        Returns:
            Updated Task object

        Raises:
            TaskNotFoundError: If task_id doesn't exist
            InvalidTaskDataError: If new title is empty/whitespace

        Satisfies: specs/001-todo-cli-basic/tasks.md - T027
        Satisfies: specs/todo-features/tasks.md - T012, T037, T038, T039, T040
        """
        task = self.get_task(task_id)

        if title is not None:
            # Validate title is not empty/whitespace
            if not title or not title.strip():
                raise InvalidTaskDataError("Task title cannot be empty or whitespace-only")
            task.title = title

        if description is not None:
            task.description = description

        if priority is not None:
            task.priority = priority

        if category is not None:
            task.category = category

        if due_date is not None:
            task.due_date = due_date

        if due_time is not None:
            task.due_time = due_time

        if recurring is not None:
            task.recurring = recurring

        return task

    def delete_task(self, task_id: int) -> None:
        """
        Remove a task from the system.

        Args:
            task_id: The task's unique identifier

        Raises:
            TaskNotFoundError: If task_id doesn't exist

        Satisfies: specs/001-todo-cli-basic/tasks.md - T034
        """
        if task_id not in self.tasks:
            raise TaskNotFoundError(f"Task [{task_id}] not found")
        del self.tasks[task_id]

    def get_tasks_by_status(self, status: Status) -> list[Task]:
        """
        Filter tasks by completion status.

        Args:
            status: Status enum value to filter by

        Returns:
            List of tasks matching the status

        Satisfies: specs/todo-features/tasks.md - T044
        """
        return [task for task in self.tasks.values() if task.status == status]

    def get_tasks_by_priority(self, priority: Priority) -> list[Task]:
        """
        Filter tasks by priority level.

        Args:
            priority: Priority enum value to filter by

        Returns:
            List of tasks matching the priority

        Satisfies: specs/todo-features/tasks.md - T045
        """
        return [task for task in self.tasks.values() if task.priority == priority]

    def get_tasks_due_today(self) -> list[Task]:
        """
        Get all tasks due today.

        Returns:
            List of tasks with due_date equal to today

        Satisfies: specs/todo-features/tasks.md - T046
        """
        from datetime import date as date_type
        today = date_type.today()
        return [task for task in self.tasks.values() if task.due_date == today]

    def get_tasks_overdue(self) -> list[Task]:
        """
        Get all tasks that are overdue (past due date and still pending).

        Returns:
            List of overdue tasks (pending with due_date before today)

        Satisfies: specs/todo-features/tasks.md - T047
        """
        from datetime import date as date_type
        today = date_type.today()
        return [
            task for task in self.tasks.values()
            if task.due_date and task.due_date < today and task.status == Status.PENDING
        ]

    def get_tasks_by_category(self, category: str) -> list[Task]:
        """
        Filter tasks by category (case-insensitive).

        Args:
            category: Category string to filter by

        Returns:
            List of tasks matching the category

        Satisfies: specs/todo-features/tasks.md - T008
        """
        category_lower = category.lower()
        return [
            task for task in self.tasks.values()
            if task.category and task.category.lower() == category_lower
        ]

    def get_tasks_sorted_by_date(self) -> list[Task]:
        """
        Get all tasks sorted by due date (ascending, nulls last).

        Returns:
            List of tasks sorted by due_date

        Satisfies: specs/todo-features/tasks.md - T009
        """
        tasks_with_date = [t for t in self.tasks.values() if t.due_date is not None]
        tasks_without_date = [t for t in self.tasks.values() if t.due_date is None]

        # Sort tasks with dates ascending
        tasks_with_date.sort(key=lambda t: (t.due_date, t.due_time or time(23, 59)))

        return tasks_with_date + tasks_without_date

    def get_tasks_sorted_by_priority(self) -> list[Task]:
        """
        Get all tasks sorted by priority (High -> Medium -> Low).

        Returns:
            List of tasks sorted by priority

        Satisfies: specs/todo-features/tasks.md - T010
        """
        return sorted(self.tasks.values(), key=lambda t: t.priority.value)
