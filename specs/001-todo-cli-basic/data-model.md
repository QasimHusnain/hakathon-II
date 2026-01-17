# Data Model: Todo CLI Basic

**Feature**: 001-todo-cli-basic
**Date**: 2026-01-16
**Phase**: 1 - Design & Contracts

## Overview

This document defines the data model for the Todo CLI Basic application. The model is implementation-focused, specifying Python classes, types, and relationships that will be used in the codebase.

## Entity: Task

### Description
Represents a single to-do item with a unique identifier, title, optional description, and completion status.

### Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| id | int | Yes | Auto-assigned | Unique identifier, sequential starting from 1 |
| title | str | Yes | None | Task title, non-empty, non-whitespace |
| status | Status (Enum) | Yes | Status.PENDING | Current completion status |
| description | Optional[str] | No | None | Optional task description |

### Validation Rules

1. **id**:
   - Must be positive integer > 0
   - Auto-assigned by TaskManager, not user-provided
   - Sequential, never reused after deletion

2. **title**:
   - Must be non-empty string
   - Must contain at least one non-whitespace character
   - Validation error if empty or whitespace-only

3. **status**:
   - Must be one of: Status.PENDING or Status.COMPLETE
   - Defaults to Status.PENDING on creation
   - Can toggle between states

4. **description**:
   - Optional, can be None
   - If provided, can be any string (including empty)
   - Can be updated after task creation

### State Transitions

```text
[Create Task]
    ↓
Status.PENDING ←→ Status.COMPLETE
    (toggle)
```

**Allowed transitions**:
- PENDING → COMPLETE (mark task as done)
- COMPLETE → PENDING (unmark task)
- No other status values exist in Phase I

### Python Implementation

```python
from dataclasses import dataclass
from typing import Optional
from enum import Enum

class Status(Enum):
    """Task completion status"""
    PENDING = "pending"
    COMPLETE = "complete"

@dataclass
class Task:
    """
    Represents a single to-do item.

    Attributes:
        id: Unique identifier (positive integer)
        title: Task title (non-empty string)
        status: Completion status (Status enum)
        description: Optional task description
    """
    id: int
    title: str
    status: Status
    description: Optional[str] = None

    def __post_init__(self):
        """Validate task data after initialization"""
        if not self.title or not self.title.strip():
            raise ValueError("Task title cannot be empty or whitespace-only")
        if self.id <= 0:
            raise ValueError("Task ID must be positive integer")
```

## Entity: TaskManager

### Description
Manages the collection of tasks and provides operations for CRUD (Create, Read, Update, Delete) functionality. This is the business logic layer, separated from CLI I/O.

### Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| tasks | dict[int, Task] | Yes | {} | Storage for all tasks, keyed by ID |
| next_id | int | Yes | 1 | Counter for generating sequential IDs |

### Operations

#### 1. add_task(title: str, description: Optional[str] = None) -> Task

**Purpose**: Create a new task with auto-assigned ID

**Inputs**:
- `title` (str): Task title, required, non-empty
- `description` (Optional[str]): Optional task description

**Outputs**:
- Returns: Created Task object with assigned ID

**Validation**:
- Raises `InvalidTaskDataError` if title is empty or whitespace-only

**Side effects**:
- Increments `next_id` counter
- Adds task to `tasks` dictionary

#### 2. get_task(task_id: int) -> Task

**Purpose**: Retrieve a task by its ID

**Inputs**:
- `task_id` (int): The task's unique identifier

**Outputs**:
- Returns: Task object if found

**Validation**:
- Raises `TaskNotFoundError` if task_id doesn't exist

#### 3. get_all_tasks() -> list[Task]

**Purpose**: Retrieve all tasks in the system

**Inputs**: None

**Outputs**:
- Returns: List of all Task objects (may be empty)

**Notes**:
- Returns tasks in insertion order (dict maintains order in Python 3.7+)

#### 4. update_task(task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Task

**Purpose**: Update title and/or description of existing task

**Inputs**:
- `task_id` (int): The task's unique identifier
- `title` (Optional[str]): New title if updating
- `description` (Optional[str]): New description if updating

**Outputs**:
- Returns: Updated Task object

**Validation**:
- Raises `TaskNotFoundError` if task_id doesn't exist
- Raises `InvalidTaskDataError` if new title is empty/whitespace
- At least one of title or description must be provided

**Notes**:
- Passing None for a field means "don't update this field"
- To clear description, need explicit empty string ""

#### 5. delete_task(task_id: int) -> None

**Purpose**: Remove a task from the system

**Inputs**:
- `task_id` (int): The task's unique identifier

**Outputs**:
- Returns: None

**Validation**:
- Raises `TaskNotFoundError` if task_id doesn't exist

**Side effects**:
- Removes task from `tasks` dictionary
- Does NOT decrement `next_id` counter (IDs never reused)

#### 6. toggle_complete(task_id: int) -> Task

**Purpose**: Toggle task status between PENDING and COMPLETE

**Inputs**:
- `task_id` (int): The task's unique identifier

**Outputs**:
- Returns: Updated Task object with new status

**Validation**:
- Raises `TaskNotFoundError` if task_id doesn't exist

**Side effects**:
- Modifies task.status in-place

## Custom Exceptions

### TaskError (Base)
```python
class TaskError(Exception):
    """Base exception for all task-related errors"""
    pass
```

### TaskNotFoundError
```python
class TaskNotFoundError(TaskError):
    """Raised when attempting to operate on non-existent task ID"""
    pass
```

**When raised**:
- get_task() with invalid ID
- update_task() with invalid ID
- delete_task() with invalid ID
- toggle_complete() with invalid ID

### InvalidTaskDataError
```python
class InvalidTaskDataError(TaskError):
    """Raised when task data fails validation"""
    pass
```

**When raised**:
- add_task() with empty/whitespace title
- update_task() with empty/whitespace title
- Task.__post_init__() validation failure

## Relationships

```text
TaskManager (1) ──── manages ──── (0..*) Task
    │
    ├── tasks: dict[int, Task]
    └── next_id: int (counter)

Task
    ├── id: int (unique)
    ├── title: str (required)
    ├── status: Status (enum)
    └── description: Optional[str]

Status (Enum)
    ├── PENDING
    └── COMPLETE
```

## Storage Strategy

**In-Memory Dictionary**:
- `TaskManager.tasks` is a `dict[int, Task]`
- Key: Task ID (int)
- Value: Task object
- O(1) lookup, insert, delete operations
- All data lost on application exit (per constitution)

**Why dictionary over list**:
- Direct access by ID without iteration
- Natural enforcement of unique IDs
- Efficient for all CRUD operations
- Maintains insertion order (Python 3.7+)

## Data Lifecycle

1. **Creation**: User adds task → TaskManager assigns ID → Task stored in dict
2. **Read**: User views tasks → TaskManager returns all tasks or single task
3. **Update**: User modifies task → TaskManager updates fields in existing Task object
4. **Status Toggle**: User marks complete → TaskManager toggles Status enum value
5. **Deletion**: User deletes task → TaskManager removes from dict (ID never reused)
6. **Session End**: Application exits → All in-memory data cleared (no persistence)

## Invariants

1. All task IDs in `tasks` dict are unique and positive
2. `next_id` always > max(task IDs in tasks dict)
3. All tasks have non-empty, non-whitespace titles
4. All tasks have valid Status enum value
5. Task IDs are sequential and never reused
6. No null/None Tasks in tasks dict (values are always Task objects)

## References

- Feature Spec: `specs/001-todo-cli-basic/spec.md`
- Research Decisions: `specs/001-todo-cli-basic/research.md`
- Constitution: `.specify/memory/constitution.md`
