# Todo In-Memory Python Console App

**Phase I: Basic Level Functionality**

A command-line todo application that stores tasks in memory, built using Claude Code and Spec-Kit Plus following Spec-Driven Development (SDD) workflow.

## Overview

This project demonstrates the Agentic Dev Stack workflow:
1. Write spec → Generate plan → Break into tasks → Implement via Claude Code

## Features (Basic Level - 5 Pillars)

1. **Add Task** - Store a title (required) and description (optional)
2. **Delete Task** - Remove a task using its unique integer ID
3. **Update Task** - Modify the title or description of an existing task
4. **View Task List** - Display all tasks with IDs and status indicators
5. **Mark as Complete** - Toggle status between "Pending" and "Complete"

## Technology Stack

- **UV** - Python package manager
- **Python 3.13+** - Standard library only (typing, dataclasses, enum)
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
python main.py
```

### Available Commands

```
add <title> [description]        Add a new task
list                             View all tasks
complete <task_id>               Mark task as complete/pending (toggle)
update <task_id> <field> <value> Update task title or description
delete <task_id>                 Delete a task
help                             Show help message
quit                             Exit the application
```

### Examples

```bash
> add "Buy groceries"
✓ Task added: [1] Buy groceries

> add "Call dentist" "Schedule annual checkup"
✓ Task added: [2] Call dentist

> list
Your Tasks:

[1] [ ] Buy groceries
[2] [ ] Call dentist
    Schedule annual checkup

Total: 2 task(s)

> complete 1
✓ Task [1] marked as complete

> list
Your Tasks:

[1] [X] Buy groceries
[2] [ ] Call dentist
    Schedule annual checkup

Total: 2 task(s)

> update 2 title "Call dentist at 2pm"
✓ Task [2] updated

> delete 1
✓ Task [1] deleted

> quit
Goodbye!
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

- **src/models/task.py** - Task data model and exceptions
- **src/services/task_manager.py** - Business logic
- **src/cli/commands.py** - Command parsing and handlers
- **src/cli/formatter.py** - Output formatting
- **main.py** - Entry point and CLI loop

## Constitution Compliance

This project follows Spec-Driven Development (SDD) workflow:
- Specification: `specs/001-todo-cli-basic/spec.md`
- Implementation Plan: `specs/001-todo-cli-basic/plan.md`
- Tasks: `specs/001-todo-cli-basic/tasks.md`
