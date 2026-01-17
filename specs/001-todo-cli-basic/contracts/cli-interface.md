# CLI Interface Contract: Todo CLI Basic

**Feature**: 001-todo-cli-basic
**Date**: 2026-01-16
**Version**: 1.0.0

## Overview

This document specifies the command-line interface contract for the Todo CLI Basic application. It defines the exact commands users can enter, their parameters, expected outputs, and error messages.

## Command Format

All commands follow the pattern:
```text
<command> [arguments...]
```

Commands are case-insensitive. Arguments are space-separated.

## Commands

### 1. add - Add New Task

**Syntax**:
```text
add <title> [description]
```

**Parameters**:
- `title` (required): Task title as string. If contains spaces, must be quoted.
- `description` (optional): Task description as string. If contains spaces, must be quoted.

**Examples**:
```text
add "Buy groceries"
add "Call dentist" "Schedule annual checkup"
add Exercise
```

**Success Output**:
```text
✓ Task added: [<ID>] <title>
```

**Example**:
```text
✓ Task added: [1] Buy groceries
```

**Error Cases**:

| Condition | Error Message |
|-----------|---------------|
| No title provided | `Error: Task title is required. Usage: add <title> [description]` |
| Empty/whitespace title | `Error: Task title cannot be empty` |

### 2. list - View All Tasks

**Syntax**:
```text
list
```

**Parameters**: None

**Success Output (with tasks)**:
```text
Your Tasks:

[<ID>] [<status>] <title>
    <description>

[<ID>] [<status>] <title>
    <description>

Total: <count> task(s)
```

**Status Indicators**:
- `[ ]` for pending tasks
- `[X]` for completed tasks

**Example**:
```text
Your Tasks:

[1] [ ] Buy groceries
    Get milk and eggs
[2] [X] Call dentist
[3] [ ] Exercise

Total: 3 task(s)
```

**Success Output (no tasks)**:
```text
Your task list is empty. Use 'add' to create a task.
```

**Error Cases**: None (list always succeeds)

### 3. complete - Toggle Task Status

**Syntax**:
```text
complete <task_id>
```

**Parameters**:
- `task_id` (required): Integer ID of the task

**Examples**:
```text
complete 1
complete 42
```

**Success Output (marking as complete)**:
```text
✓ Task [<ID>] marked as complete
```

**Success Output (unmarking - toggle back)**:
```text
✓ Task [<ID>] marked as pending
```

**Error Cases**:

| Condition | Error Message |
|-----------|---------------|
| No ID provided | `Error: Task ID is required. Usage: complete <task_id>` |
| Non-integer ID | `Error: Task ID must be a number` |
| Task not found | `Error: Task [<ID>] not found` |

### 4. update - Modify Task Details

**Syntax**:
```text
update <task_id> title <new_title>
update <task_id> description <new_description>
```

**Parameters**:
- `task_id` (required): Integer ID of the task
- `field` (required): Either "title" or "description"
- `value` (required): New value for the field

**Examples**:
```text
update 1 title "Buy groceries and cook dinner"
update 2 description "Call at 2pm"
update 3 title Exercise
```

**Success Output**:
```text
✓ Task [<ID>] updated
```

**Error Cases**:

| Condition | Error Message |
|-----------|---------------|
| No ID provided | `Error: Task ID is required. Usage: update <task_id> <field> <value>` |
| Non-integer ID | `Error: Task ID must be a number` |
| Invalid field | `Error: Field must be 'title' or 'description'` |
| No value provided | `Error: New value is required` |
| Empty/whitespace title | `Error: Task title cannot be empty` |
| Task not found | `Error: Task [<ID>] not found` |

### 5. delete - Remove Task

**Syntax**:
```text
delete <task_id>
```

**Parameters**:
- `task_id` (required): Integer ID of the task

**Examples**:
```text
delete 1
delete 42
```

**Success Output**:
```text
✓ Task [<ID>] deleted
```

**Error Cases**:

| Condition | Error Message |
|-----------|---------------|
| No ID provided | `Error: Task ID is required. Usage: delete <task_id>` |
| Non-integer ID | `Error: Task ID must be a number` |
| Task not found | `Error: Task [<ID>] not found` |

### 6. help - Show Help Information

**Syntax**:
```text
help
```

**Parameters**: None

**Output**:
```text
Todo CLI - Available Commands:

  add <title> [description]        Add a new task
  list                             View all tasks
  complete <task_id>               Mark task as complete/pending (toggle)
  update <task_id> <field> <value> Update task title or description
  delete <task_id>                 Delete a task
  help                             Show this help message
  quit                             Exit the application

Examples:
  add "Buy groceries"
  list
  complete 1
  update 1 title "New title"
  delete 2
```

### 7. quit - Exit Application

**Syntax**:
```text
quit
exit
```

**Parameters**: None

**Output**:
```text
Goodbye!
```

**Side Effects**: Application terminates, all data is lost

## Input Handling

### Quoted Strings
Arguments containing spaces must be quoted:
```text
add "This is a title with spaces" "This is a description"
```

### Case Sensitivity
- Commands are case-insensitive: `ADD`, `add`, `Add` all work
- Arguments (titles, descriptions) are case-sensitive and preserved as entered

### Whitespace
- Leading/trailing whitespace in commands is ignored
- Whitespace within quoted arguments is preserved
- Multiple spaces between command and arguments are collapsed

### Special Characters
All printable characters are allowed in titles and descriptions, including:
- Punctuation: `.,!?;:'"-`
- Numbers: `0-9`
- Special: `@#$%&*()[]{}/<>`

## Error Handling

### General Error Format
```text
Error: <specific error message>
```

### Unknown Command
```text
Error: Unknown command '<command>'. Type 'help' for available commands.
```

### Invalid Arguments
Each command specifies its own error messages (see individual commands above).

## Application Flow

### Startup
```text
Welcome to Todo CLI!
Type 'help' for available commands.

>
```

### Prompt
```text
>
```

The `>` symbol indicates the application is ready for input.

### Command Execution
```text
> add "Buy milk"
✓ Task added: [1] Buy milk

> list
Your Tasks:

[1] [ ] Buy milk

Total: 1 task(s)

>
```

### Exit
```text
> quit
Goodbye!
```

## Contract Guarantees

1. **Idempotency**:
   - `list` can be called multiple times with same result
   - `complete` toggles, not idempotent by design

2. **Atomicity**:
   - Each command either succeeds completely or fails completely
   - No partial updates (e.g., if validation fails, nothing changes)

3. **Consistency**:
   - Task IDs are always unique and sequential
   - Status indicators always match internal state
   - Error messages are consistent and predictable

4. **Validation Order**:
   1. Check command exists
   2. Check required parameters present
   3. Check parameter types (e.g., ID is integer)
   4. Check business rules (e.g., task exists, title non-empty)

5. **Error Recovery**:
   - Errors do not crash the application
   - After error, prompt returns for next command
   - Invalid commands do not modify state

## Testing Contract

Each command should be tested for:
- ✅ Valid input with expected output
- ✅ Missing required parameters
- ✅ Invalid parameter types
- ✅ Boundary conditions (non-existent IDs, empty values)
- ✅ Edge cases (very long titles, special characters)

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-16 | Initial CLI interface specification |

## References

- Feature Spec: `specs/001-todo-cli-basic/spec.md`
- Data Model: `specs/001-todo-cli-basic/data-model.md`
- Research: `specs/001-todo-cli-basic/research.md`
