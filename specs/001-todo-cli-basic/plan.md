# Implementation Plan: Todo CLI Basic

**Branch**: `001-todo-cli-basic` | **Date**: 2026-01-16 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-todo-cli-basic/spec.md`

## Summary

Build a CLI-based task manager with 5 core operations (Add, Delete, Update, View, Mark Complete) using Python 3.13+ with in-memory storage. Technical approach: Separate TaskManager class (business logic) from CLI loop (I/O layer) with comprehensive type hints and error handling.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: Python standard library only (typing, dataclasses, enum)
**Storage**: In-memory (Python dict/list data structures)
**Testing**: pytest (Python standard)
**Target Platform**: Cross-platform CLI (Linux, macOS, Windows)
**Project Type**: Single CLI application
**Performance Goals**: Response time < 2 seconds for view operations with up to 1000 tasks
**Constraints**: No external dependencies, no persistence, CLI-only interface
**Scale/Scope**: Single-user, single-session, up to 1000 tasks in memory

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Pre-Phase 0 Check

- ✅ **Mission-Driven Scope**: CLI-based task manager, no web/GUI/AI features
- ✅ **Technical Stack**: Python 3.13+, managed via uv, in-memory storage
- ✅ **Five Functional Requirements**: All 5 pillars (Add, Delete, Update, View, Mark Complete) covered in spec
- ✅ **Architectural Guardrails**: Plan includes TaskManager class (logic) and cli_loop (I/O) separation
- ✅ **Type Hints**: All functions will use typing module
- ✅ **SDD Workflow**: Following Spec → Plan → Tasks → Implementation

**Status**: ✅ PASSED - No violations

### Post-Phase 1 Check

- ✅ **Separation of Concerns**: TaskManager (services/) separate from CLI (cli/) confirmed in design
- ✅ **Type Hints**: data-model.md specifies type hints for all functions (Task, TaskManager, CLI functions)
- ✅ **Error Handling**: Custom exceptions (TaskError, TaskNotFoundError, InvalidTaskDataError) defined
- ✅ **Status Indicators**: CLI contract specifies [ ] and [X] formatting
- ✅ **Five Operations**: All 5 pillars implemented in TaskManager (add, delete, update, view, toggle)
- ✅ **In-Memory Only**: Dictionary storage confirmed, no persistence layer
- ✅ **Python stdlib Only**: No external dependencies beyond typing, dataclasses, enum, pytest (dev)

**Status**: ✅ PASSED - Design fully compliant with constitution

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-cli-basic/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   └── cli-interface.md # CLI command interface specification
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Single project structure (CLI application)
src/
├── models/
│   └── task.py          # Task data class with Status enum
├── services/
│   └── task_manager.py  # TaskManager class (business logic)
├── cli/
│   ├── __init__.py
│   ├── commands.py      # CLI command parsing and dispatch
│   └── formatter.py     # Output formatting ([ ] and [X] indicators)
└── __init__.py

tests/
├── unit/
│   ├── test_task_model.py
│   ├── test_task_manager.py
│   └── test_formatter.py
└── integration/
    └── test_cli_e2e.py  # End-to-end CLI tests

main.py                  # Entry point with CLI loop
pyproject.toml           # uv project configuration
README.md                # User documentation
```

**Structure Decision**: Single project structure selected because this is a standalone CLI application with no web frontend, backend API, or mobile components. The separation between `models/`, `services/`, and `cli/` directories enforces the constitutional requirement for separation of concerns (TaskManager logic vs CLI I/O).

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

*No violations - this section is not applicable*
