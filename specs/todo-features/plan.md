# Implementation Plan: Enhanced Todo CLI with Refined UI

**Branch**: `todo-features` | **Date**: 2026-01-17 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/todo-features/spec.md`

## Summary

Refactor the existing CLI-based Todo application to use a numeric menu system (1-8) with interactive prompts instead of command-line arguments. Add new features including Category field, Sort functionality, and maintain existing Recurring task support. The application transitions from text-based commands (`add`, `list`, `complete`) to a numbered menu interface with visual separation lines for improved usability.

**Key Changes from Previous Implementation**:
1. Replace text commands with numeric menu (1-8)
2. Replace command-line flags with interactive sequential prompts
3. Add Category field to Task model
4. Add Sort functionality (by due date, by priority)
5. Add visual separation lines (40-char `=` and `-`)
6. Update Filter to include Category filter
7. Maintain Recurring functionality with numeric input (1/2/3)

## Technical Context

**Language/Version**: Python 3.13+ (per constitution)
**Primary Dependencies**: Python standard library only (typing, dataclasses, enum, datetime, calendar)
**Storage**: In-Memory (Python dict/list data structures - clears on exit)
**Testing**: pytest, mypy (dev dependencies via uv)
**Target Platform**: CLI application (Linux/macOS/Windows via Python)
**Project Type**: Single project (extends existing structure)
**Performance Goals**: Instant response for all operations (< 100ms)
**Constraints**: No external dependencies, no database, no persistence
**Scale/Scope**: Single user, unlimited tasks (memory-limited)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Requirement | Status |
|------|-------------|--------|
| Language | Python 3.13+ | ✅ PASS |
| Dependencies | Standard library only | ✅ PASS |
| Storage | In-Memory only | ✅ PASS |
| Typing | Type hints mandatory | ✅ PASS |
| Architecture | Separation of concerns (TaskManager vs CLI) | ✅ PASS |
| Error Handling | Handle ValueError, TaskNotFoundError, InvalidTaskDataError | ✅ PASS |
| SDD Workflow | Docstrings reference task IDs | ✅ PASS |
| CLI UI | Numeric menu (1-8), separation lines | ✅ PASS (new requirement) |
| Validation | Date/Priority/Menu input validation | ✅ PASS (new requirement) |

**All gates passed. Proceeding with design.**

## Project Structure

### Documentation (this feature)

```text
specs/todo-features/
├── plan.md              # This file
├── spec.md              # Feature specification (updated)
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output (updated)
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── cli-interface.md # CLI menu contracts
├── checklists/
│   └── requirements.md  # Spec validation checklist
└── tasks.md             # Phase 2 output (/sp.tasks)
```

### Source Code (repository root)

```text
src/
├── __init__.py
├── models/
│   ├── __init__.py
│   └── task.py          # Task dataclass, Status, Priority, Recurrence enums
├── services/
│   ├── __init__.py
│   └── task_manager.py  # TaskManager class with CRUD + filter + sort operations
└── cli/
    ├── __init__.py
    ├── commands.py      # Menu handlers and interactive prompts (MAJOR REFACTOR)
    ├── formatter.py     # Output formatting with indicators and separation lines
    └── parser.py        # Input parsing and validation utilities

tests/
├── __init__.py
├── unit/
│   ├── __init__.py
│   ├── test_task_model.py
│   ├── test_task_manager.py
│   └── test_formatter.py
└── integration/
    ├── __init__.py
    └── test_cli_commands.py

main.py                  # Entry point with numeric menu loop (MAJOR REFACTOR)
```

**Structure Decision**: Single project structure - CLI application with clear separation between models, services, and CLI layers. Extends existing structure from previous implementation.

## Design Decisions

### 1. Transition from Text Commands to Numeric Menu

**Current State**: Text commands like `add "title" -p high --date 2026-01-20`
**Target State**: Numeric menu selection (1-8) with interactive prompts

**Approach**:
- Replace `parse_command()` logic with `display_menu()` and `get_menu_choice()`
- Replace command handlers with interactive prompt flows
- Reuse existing TaskManager methods (no changes to service layer logic)

### 2. Interactive Prompt Flow

For Add Task (menu option 1):
1. Display `--- Add New Task ---`
2. Prompt each field sequentially with validation
3. Create task after all inputs collected
4. Display success message with separation lines

**Benefits**: Easier for users, no command syntax to memorize

### 3. Category Field Addition

- Add `category: Optional[str]` to Task dataclass
- Free-form text, no predefined categories
- Display in brackets `[Category]` when viewing tasks
- Filter by exact match in Filter submenu

### 4. Sort Implementation

Two sort options:
1. **By Due Date**: `sorted(tasks, key=lambda t: (t.due_date is None, t.due_date))`
   - Tasks with dates first (ascending), then tasks without dates
2. **By Priority**: `sorted(tasks, key=lambda t: t.priority.value)`
   - HIGH (1) first, then MEDIUM (2), then LOW (3)

### 5. Visual Separation Lines

Per constitution VI.A:
- Major headers: `========================================` (40 chars)
- Subsection dividers: `----------------------------------------` (40 chars)
- Inline separators: `---`

### 6. Validation Rules

Per constitution VII:
- Date: `YYYY-MM-DD` or `YYYY-MM-DD HH:MM` (regex + strptime)
- Priority: `1`, `2`, `3` (or empty for default)
- Recurring: `1`, `2`, `3` (or empty for none)
- Menu choice: `1`-`8` (integer validation)
- Task ID: Positive integer, must exist

## Complexity Tracking

> No violations detected. All design choices align with constitution constraints.

| Check | Result |
|-------|--------|
| External dependencies | None added |
| Database usage | None (in-memory only) |
| Web interface | None (CLI only) |
| Separation of concerns | Maintained |
| New complexity | Minimal - mostly UI refactoring |

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| Breaking existing TaskManager API | Medium | Keep service layer interface stable; changes only in CLI layer |
| User confusion with new UI | Low | Clear prompts with format hints (e.g., "[2]" for defaults) |
| Input validation edge cases | Low | Comprehensive validation with helpful error messages |
| Monthly date edge cases | Medium | Use calendar.monthrange for month-end handling |

## Transition Roadmap

### Phase 1: Model Updates
1. Add `category` field to Task dataclass
2. Update Priority enum to use integer values if not already
3. Update TaskManager to handle category in CRUD operations

### Phase 2: Service Layer Updates
1. Add `get_tasks_by_category(category: str)` method
2. Add `get_tasks_sorted_by_date()` method
3. Add `get_tasks_sorted_by_priority()` method
4. Update existing filter methods if needed

### Phase 3: CLI Layer Refactoring (MAJOR)
1. Create `display_main_menu()` function with header and options
2. Create `get_menu_choice()` with validation
3. Refactor `handle_add()` to use interactive prompts
4. Create `handle_filter_menu()` submenu
5. Create `handle_sort_menu()` submenu
6. Update `handle_update()` to use interactive prompts
7. Add separation lines to all output functions

### Phase 4: Main Loop Refactoring
1. Replace command parsing loop with menu selection loop
2. Display menu after each operation
3. Handle exit gracefully

### Phase 5: Testing Updates
1. Update unit tests for new Category field
2. Add tests for sort functionality
3. Update integration tests for new CLI flow

## Next Steps

1. **Phase 0**: Research complete - no unknowns (constitution resolves all)
2. **Phase 1**: Data model and contracts already defined
3. **Phase 2**: Generate tasks.md via `/sp.tasks` with file-based granularity
4. **Implementation**: After user approval of tasks

## Files Requiring Changes

| File | Change Type | Description |
|------|-------------|-------------|
| `src/models/task.py` | Modify | Add category field |
| `src/services/task_manager.py` | Modify | Add category filter, sort methods |
| `src/cli/commands.py` | Major Refactor | Replace command handlers with menu + prompts |
| `src/cli/formatter.py` | Modify | Add separation lines, update task display |
| `src/cli/parser.py` | Modify | Update validation utilities |
| `main.py` | Major Refactor | Replace command loop with menu loop |
| `tests/unit/test_task_model.py` | Modify | Add category tests |
| `tests/unit/test_task_manager.py` | Modify | Add filter/sort tests |
| `tests/integration/test_cli_commands.py` | Modify | Update for menu-based flow |
