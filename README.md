# Todo In-Memory Python Console App

**Phase I: Enhanced Functionality**

A command-line todo application that stores tasks in memory, built using Claude Code and Spec-Kit Plus following Spec-Driven Development (SDD) workflow.

## Overview

This project demonstrates the Agentic Dev Stack workflow:
1. Write spec → Generate plan → Break into tasks → Implement via Claude Code

## Features (8 Pillars)

1. **Add Task** - Interactive prompts for Title, Description, Priority, Category, Due Date, and Recurring
2. **View All Tasks** - Display all tasks with ID, status, priority, category indicators
3. **Update Task** - Modify any task attribute via interactive submenu
4. **Delete Task** - Remove task by unique integer ID with confirmation
5. **Toggle Task Completion** - Switch between Pending and Complete status
6. **Search / Filter Tasks** - Filter by Category, Priority, or Status
7. **Sort Tasks** - Order by Due Date or Priority
8. **Exit** - Quit application

## Technology Stack

- **UV** - Python package manager
- **Python 3.13+** - Standard library only (typing, dataclasses, enum, datetime)
- **Claude Code** - AI-assisted development
- **Spec-Kit Plus** - Spec-driven development framework
- **In-Memory Storage** - Data clears on exit (no database)

## Installation

Requires Python 3.13+ and uv package manager.

```bash
# Install dependencies
uv pip install -e ".[dev]"
```

## Usage

```bash
# Run the application
uv run python main.py
```

### Main Menu

```
========================================
         TODO TASK MANAGER
========================================

1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Toggle Task Completion
6. Search / Filter Tasks
7. Sort Tasks
8. Exit

========================================
Enter your choice (1-8):
```

### Task Fields

| Field | Required | Description |
|-------|----------|-------------|
| Title | Yes | Task name (cannot be empty) |
| Description | No | Additional details |
| Priority | No | High (1), Medium (2), Low (3) - Default: Medium |
| Category | No | Custom category for grouping |
| Due Date | No | Format: YYYY-MM-DD or YYYY-MM-DD HH:MM |
| Recurring | No | Daily (1), Weekly (2), Monthly (3) |

### Examples

**Adding a Task:**
```
Enter your choice (1-8): 1

--- Add New Task ---
Title: Buy groceries
Description (press Enter to skip): Weekly shopping
Priority (1=High, 2=Medium, 3=Low) [2]: 1
Category (press Enter to skip): Shopping
Due Date (YYYY-MM-DD or YYYY-MM-DD HH:MM, press Enter to skip): 2025-01-20
Recurring (1=Daily, 2=Weekly, 3=Monthly, press Enter to skip): 2
----------------------------------------
Task added successfully! ID: 1
```

**Viewing All Tasks:**
```
Enter your choice (1-8): 2

========================================
              ALL TASKS
========================================
[1] [ ] [H] [Shopping] Buy groceries
     Due: 2025-01-20 | Recurring: Weekly
     Weekly shopping
----------------------------------------

Total: 1 task(s)
========================================
```

**Filtering Tasks:**
```
Enter your choice (1-8): 6

--- Filter Tasks ---
1. By Category
2. By Priority
3. By Status
4. Back to Main Menu

Enter your choice (1-4): 2
Enter priority (1=High, 2=Medium, 3=Low): 1

========================================
         FILTERED TASKS
========================================
[1] [ ] [H] [Shopping] Buy groceries
     Due: 2025-01-20 | Recurring: Weekly
----------------------------------------

Found: 1 task(s) matching filter
========================================
```

**Sorting Tasks:**
```
Enter your choice (1-8): 7

--- Sort Tasks ---
1. By Due Date (ascending)
2. By Priority (High → Low)
3. Back to Main Menu

Enter your choice (1-3): 2
```

**Toggling Completion:**
```
Enter your choice (1-8): 5

--- Toggle Task Completion ---
Enter Task ID: 1

Task [1] marked as complete.
```

**Deleting a Task:**
```
Enter your choice (1-8): 4

--- Delete Task ---
Enter Task ID: 1

Task to delete:
[1] [X] [H] [Shopping] Buy groceries
     Due: 2025-01-20 | Recurring: Weekly
     Weekly shopping

Are you sure you want to delete this task? (y/n): y

Task [1] deleted successfully.
```

## Development

Run tests:
```bash
pytest
```

Type checking:
```bash
mypy src/
```

## Architecture

- **src/models/task.py** - Task data model with Priority, Status, Recurrence enums
- **src/services/task_manager.py** - Business logic for CRUD and filtering/sorting
- **src/cli/commands.py** - Menu handlers and interactive prompts
- **src/cli/formatter.py** - Output formatting with separators
- **src/cli/parser.py** - Input validation utilities
- **main.py** - Entry point and main menu loop

## Constitution Compliance

This project follows Spec-Driven Development (SDD) workflow:
- Specification: `specs/todo-features/spec.md`
- Implementation Plan: `specs/todo-features/plan.md`
- Tasks: `specs/todo-features/tasks.md`
