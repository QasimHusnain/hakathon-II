# Quickstart Guide: Todo CLI Basic

**Feature**: 001-todo-cli-basic
**Date**: 2026-01-16
**Target Audience**: Developers implementing this feature

## Overview

This quickstart guide provides a step-by-step walkthrough for implementing the Todo CLI Basic feature. Follow these steps in order to build a working CLI task manager.

## Prerequisites

- Python 3.13+ installed
- `uv` package manager installed
- Git repository initialized
- On branch: `001-todo-cli-basic`

## Implementation Steps

### Step 1: Project Setup

1. **Initialize uv project**:
```bash
uv init
```

2. **Create pyproject.toml**:
```toml
[project]
name = "todo-cli-basic"
version = "0.1.0"
description = "Simple CLI task manager"
requires-python = ">=3.13"
dependencies = []

[project.optional-dependencies]
dev = ["pytest>=8.0.0", "mypy>=1.8.0"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

3. **Create directory structure**:
```bash
mkdir -p src/models src/services src/cli tests/unit tests/integration
touch src/__init__.py src/cli/__init__.py
```

### Step 2: Implement Data Model

**File**: `src/models/task.py`

Refer to: `specs/001-todo-cli-basic/data-model.md`

Key components to implement:
1. `Status` enum (PENDING, COMPLETE)
2. `Task` dataclass with validation
3. Custom exceptions: `TaskError`, `TaskNotFoundError`, `InvalidTaskDataError`

**Testing**: Create `tests/unit/test_task_model.py`

### Step 3: Implement TaskManager

**File**: `src/services/task_manager.py`

Refer to: `specs/001-todo-cli-basic/data-model.md` (TaskManager section)

Methods to implement:
1. `__init__()` - Initialize tasks dict and next_id counter
2. `add_task(title, description)` - Create new task
3. `get_task(task_id)` - Retrieve task by ID
4. `get_all_tasks()` - List all tasks
5. `update_task(task_id, title, description)` - Modify task
6. `delete_task(task_id)` - Remove task
7. `toggle_complete(task_id)` - Toggle status

**Testing**: Create `tests/unit/test_task_manager.py`

### Step 4: Implement CLI Formatter

**File**: `src/cli/formatter.py`

Refer to: `specs/001-todo-cli-basic/contracts/cli-interface.md`

Functions to implement:
1. `format_task(task)` - Format single task with status indicator
2. `format_task_list(tasks)` - Format complete task list
3. `format_success(message)` - Format success messages
4. `format_error(message)` - Format error messages

Output format:
- `[ ]` for pending tasks
- `[X]` for completed tasks
- Task display: `[ID] [status] title` with optional description indented

**Testing**: Create `tests/unit/test_formatter.py`

### Step 5: Implement CLI Commands

**File**: `src/cli/commands.py`

Refer to: `specs/001-todo-cli-basic/contracts/cli-interface.md`

Command handlers to implement:
1. `handle_add(args, manager)` - Parse and execute add command
2. `handle_list(args, manager)` - Execute list command
3. `handle_complete(args, manager)` - Parse and execute complete command
4. `handle_update(args, manager)` - Parse and execute update command
5. `handle_delete(args, manager)` - Parse and execute delete command
6. `handle_help()` - Display help message
7. `parse_command(input_str)` - Parse user input into command and args

### Step 6: Implement Main CLI Loop

**File**: `main.py` (repository root)

```python
#!/usr/bin/env python3
"""
Todo CLI Basic - Main entry point

Satisfies: spec.md - FR-014 (CLI interface requirement)
"""

from src.services.task_manager import TaskManager
from src.cli.commands import parse_command, execute_command

def main():
    """Main CLI loop"""
    manager = TaskManager()
    print("Welcome to Todo CLI!")
    print("Type 'help' for available commands.\n")

    while True:
        try:
            user_input = input("> ").strip()
            if not user_input:
                continue

            command, args = parse_command(user_input)

            if command in ("quit", "exit"):
                print("Goodbye!")
                break

            result = execute_command(command, args, manager)
            print(result)

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
```

### Step 7: Write Tests

#### Unit Tests

**tests/unit/test_task_model.py**:
- Test Task creation with valid/invalid data
- Test Status enum values
- Test custom exceptions

**tests/unit/test_task_manager.py**:
- Test all CRUD operations
- Test error cases (non-existent IDs, invalid data)
- Test ID generation and uniqueness
- Test status toggling

**tests/unit/test_formatter.py**:
- Test task formatting with pending/complete status
- Test empty list formatting
- Test success/error message formatting

#### Integration Tests

**tests/integration/test_cli_e2e.py**:
- Test complete user workflows (add → list → complete → update → delete)
- Test error handling in CLI
- Test command parsing

### Step 8: Run Tests

```bash
# Install dev dependencies
uv pip install -e ".[dev]"

# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Type checking
mypy src/
```

### Step 9: Manual Testing

```bash
# Run the application
python main.py

# Try these commands:
> add "Buy groceries" "Get milk and eggs"
> add "Call dentist"
> list
> complete 1
> list
> update 2 description "Call at 2pm"
> list
> delete 1
> list
> quit
```

## Expected Behavior

### Adding Tasks
```text
> add "Buy groceries"
✓ Task added: [1] Buy groceries

> add "Call dentist" "Schedule annual checkup"
✓ Task added: [2] Call dentist
```

### Viewing Tasks
```text
> list
Your Tasks:

[1] [ ] Buy groceries
[2] [ ] Call dentist
    Schedule annual checkup

Total: 2 task(s)
```

### Completing Tasks
```text
> complete 1
✓ Task [1] marked as complete

> list
Your Tasks:

[1] [X] Buy groceries
[2] [ ] Call dentist
    Schedule annual checkup

Total: 2 task(s)
```

### Updating Tasks
```text
> update 2 title "Call dentist at 2pm"
✓ Task [2] updated
```

### Deleting Tasks
```text
> delete 1
✓ Task [1] deleted

> list
Your Tasks:

[2] [ ] Call dentist at 2pm
    Schedule annual checkup

Total: 1 task(s)
```

## Common Issues & Solutions

### Issue: Import errors
**Solution**: Ensure you're running from repository root and `src/` is in PYTHONPATH:
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python main.py
```

### Issue: Type checking fails
**Solution**: Install type stubs and ensure all functions have type hints:
```bash
uv pip install types-all
```

### Issue: Tests fail with "module not found"
**Solution**: Install package in editable mode:
```bash
uv pip install -e .
```

## Success Criteria Checklist

After implementation, verify:

- ✅ All 5 operations work (add, delete, update, view, mark complete)
- ✅ Task IDs are sequential and unique
- ✅ Status indicators `[ ]` and `[X]` display correctly
- ✅ Error messages are clear for invalid inputs
- ✅ Empty titles are rejected
- ✅ Non-existent task IDs show appropriate errors
- ✅ All functions have type hints
- ✅ All tests pass
- ✅ mypy type checking passes
- ✅ Data clears on application exit

## Next Steps

After completing implementation:

1. Run `/sp.tasks` to generate detailed task breakdown
2. Follow TDD workflow: Write tests → Implement → Refactor
3. Create git commit with reference to spec
4. Update documentation if needed

## References

- **Specification**: `specs/001-todo-cli-basic/spec.md`
- **Data Model**: `specs/001-todo-cli-basic/data-model.md`
- **CLI Contract**: `specs/001-todo-cli-basic/contracts/cli-interface.md`
- **Research**: `specs/001-todo-cli-basic/research.md`
- **Constitution**: `.specify/memory/constitution.md`

## Development Notes

### Type Hints Example
```python
from typing import Optional

def add_task(self, title: str, description: Optional[str] = None) -> Task:
    """
    Add a new task to the manager.

    Satisfies: tasks.md - TASK-001 (reference will be added after /sp.tasks)

    Args:
        title: Task title (non-empty string)
        description: Optional task description

    Returns:
        Created Task object

    Raises:
        InvalidTaskDataError: If title is empty or whitespace-only
    """
    # Implementation here
```

### Error Handling Pattern
```python
try:
    task = manager.get_task(task_id)
    # Do something with task
except TaskNotFoundError:
    return f"Error: Task [{task_id}] not found"
except InvalidTaskDataError as e:
    return f"Error: {str(e)}"
```

### Testing Pattern
```python
def test_add_task_with_valid_data():
    """Test adding task with valid title and description"""
    manager = TaskManager()
    task = manager.add_task("Test task", "Test description")

    assert task.id == 1
    assert task.title == "Test task"
    assert task.description == "Test description"
    assert task.status == Status.PENDING
```
