# Research & Design Decisions: Todo CLI Basic

**Feature**: 001-todo-cli-basic
**Date**: 2026-01-16
**Phase**: 0 - Outline & Research

## Overview

This document captures research findings and design decisions for the Todo CLI Basic feature. All technical choices align with the constitution's requirements for Python 3.13+, in-memory storage, and CLI-only interface.

## Research Areas

### 1. Python Data Structure for Task Storage

**Decision**: Use dictionary with integer keys for task storage

**Rationale**:
- Provides O(1) lookup by task ID (required for update, delete, mark complete operations)
- Dictionary keys naturally enforce unique IDs
- Easy to iterate for displaying all tasks
- No external dependencies needed (Python standard library)

**Alternatives considered**:
- **List-based storage**: Rejected because lookup by ID would require O(n) iteration
- **dataclass with __post_init__ registry**: Rejected as over-engineered for this simple use case
- **OrderedDict**: Not needed since Python 3.7+ dicts maintain insertion order

**Implementation approach**:
```python
tasks: dict[int, Task] = {}
next_id: int = 1
```

### 2. CLI Command Parsing Pattern

**Decision**: Simple command-word pattern matching with argparse-like manual parsing

**Rationale**:
- Meets constitution requirement for "simple command-action-parameters pattern"
- No external dependencies (avoiding argparse complexity for this basic use case)
- Direct control over error messages for better UX
- Easy to test individual command handlers

**Alternatives considered**:
- **argparse module**: Rejected because it's designed for UNIX-style arguments (--flags), not interactive commands
- **cmd module**: Rejected as unnecessary abstraction for 5 commands
- **click/typer libraries**: Rejected due to external dependency constraint

**Command format**:
```text
add <title> [description]
list
update <id> <title|description> <new_value>
delete <id>
complete <id>
quit
```

### 3. Status Representation

**Decision**: Use Python Enum for status with two states

**Rationale**:
- Type-safe representation prevents invalid status values
- Built-in to Python standard library (enum module)
- Clear intent in code (Status.PENDING vs string "Pending")
- Easy to extend if future phases need additional states

**Alternatives considered**:
- **Boolean (is_complete)**: Rejected because less readable and harder to extend
- **String literals**: Rejected due to lack of type safety and potential typos
- **Integer codes**: Rejected as less readable than enum names

**Implementation**:
```python
from enum import Enum

class Status(Enum):
    PENDING = "pending"
    COMPLETE = "complete"
```

### 4. Task Model Structure

**Decision**: Use @dataclass for Task with frozen=False

**Rationale**:
- Auto-generates __init__, __repr__, __eq__ methods
- Built-in to Python standard library (dataclasses module)
- Clear declaration of fields with type hints
- Mutable (frozen=False) to support update operations
- Satisfies constitution requirement for type hints

**Alternatives considered**:
- **NamedTuple**: Rejected because tasks must be mutable for updates
- **Regular class with __init__**: Rejected as more boilerplate than dataclass
- **TypedDict**: Rejected because it's for dictionaries, not objects

**Implementation**:
```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class Task:
    id: int
    title: str
    status: Status
    description: Optional[str] = None
```

### 5. Error Handling Strategy

**Decision**: Custom exception classes with try-except in CLI layer

**Rationale**:
- Separates business logic exceptions from CLI presentation
- TaskManager can raise domain-specific errors
- CLI layer catches and formats error messages for user
- Satisfies constitution requirement for ValueError/KeyError handling

**Exception hierarchy**:
```python
class TaskError(Exception):
    """Base exception for task operations"""
    pass

class TaskNotFoundError(TaskError):
    """Raised when task ID doesn't exist"""
    pass

class InvalidTaskDataError(TaskError):
    """Raised for validation errors (empty title, etc.)"""
    pass
```

**Alternatives considered**:
- **Return None on error**: Rejected as less explicit than exceptions
- **Return tuples (success, error)**: Rejected as non-Pythonic
- **Use built-in exceptions only**: Rejected because custom exceptions provide better context

### 6. CLI Output Formatting

**Decision**: Dedicated formatter module with template strings

**Rationale**:
- Separates presentation logic from business logic
- Easy to modify output format without touching TaskManager
- Testable independently
- Supports constitution requirement for "[ ]" and "[X]" indicators

**Format specification**:
```text
[ID] [status] Title
    Description (if present)

Example:
[1] [ ] Buy groceries
    Get milk and eggs
[2] [X] Call dentist
```

**Alternatives considered**:
- **Inline formatting in commands**: Rejected due to code duplication
- **Rich/prettytable library**: Rejected due to external dependency constraint
- **JSON output**: Rejected as not user-friendly for CLI

### 7. Testing Strategy

**Decision**: pytest with unit tests for each module and integration tests for CLI

**Rationale**:
- pytest is Python standard for testing
- Constitution requires "all core functionality must be testable"
- Unit tests cover TaskManager, Task model, formatter independently
- Integration tests verify end-to-end CLI flows

**Test coverage areas**:
- Task model: validation, field access
- TaskManager: all 5 operations, error cases, edge cases
- Formatter: status indicators, empty list, long descriptions
- CLI integration: command parsing, error messages, user flows

**Alternatives considered**:
- **unittest module**: Rejected because pytest has better fixtures and assertions
- **Manual testing only**: Rejected due to constitution testing requirements
- **Property-based testing (hypothesis)**: Deferred to future phases

### 8. ID Generation Strategy

**Decision**: Sequential counter starting from 1, never reused

**Rationale**:
- Matches spec assumption: "Task IDs will not be reused after deletion"
- Simple to implement with single integer counter
- Predictable for users (IDs always increase)
- No collision risk in single-session in-memory app

**Implementation**:
```python
class TaskManager:
    def __init__(self):
        self.tasks: dict[int, Task] = {}
        self.next_id: int = 1

    def add_task(self, title: str, description: Optional[str] = None) -> Task:
        task = Task(id=self.next_id, title=title, status=Status.PENDING, description=description)
        self.tasks[self.next_id] = task
        self.next_id += 1
        return task
```

**Alternatives considered**:
- **UUID**: Rejected as overkill for single-user, single-session app
- **Reuse IDs after deletion**: Rejected per spec assumptions
- **Hash-based IDs**: Rejected as less user-friendly than sequential integers

## Best Practices Applied

### Python 3.13+ Features
- Type hints on all functions (constitution requirement)
- dataclasses for Task model
- Enum for Status
- Optional type for nullable description

### Separation of Concerns
- **Models layer** (`task.py`): Data structures only
- **Services layer** (`task_manager.py`): Business logic only
- **CLI layer** (`commands.py`, `formatter.py`): I/O and presentation only

### Error Handling
- Validate inputs at TaskManager boundary
- Raise custom exceptions for domain errors
- CLI layer catches and formats for user display
- Constitution-required: ValueError, KeyError/IndexError handling

### Code Quality
- Type hints enable mypy static analysis
- Docstrings will reference task IDs per constitution
- Single responsibility per module
- No external dependencies (Python stdlib only)

## Open Questions

*None - all technical decisions resolved based on constitution and spec requirements*

## References

- Constitution: `.specify/memory/constitution.md`
- Feature Spec: `specs/001-todo-cli-basic/spec.md`
- Python Dataclasses: https://docs.python.org/3/library/dataclasses.html
- Python Enum: https://docs.python.org/3/library/enum.html
- Python Type Hints: https://docs.python.org/3/library/typing.html
