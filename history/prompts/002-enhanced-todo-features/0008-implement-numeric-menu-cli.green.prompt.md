---
id: 0008
title: Implement Numeric Menu CLI
stage: green
date: 2026-01-17
surface: agent
model: claude-opus-4-5-20251101
feature: 002-enhanced-todo-features
branch: 002-enhanced-todo-features
user: user
command: /sp.implement
labels: ["implementation", "numeric-menu", "cli-refactor", "interactive-prompts"]
links:
  spec: specs/002-enhanced-todo-features/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - src/models/task.py
  - src/services/task_manager.py
  - src/cli/commands.py
  - src/cli/formatter.py
  - src/cli/parser.py
  - main.py
  - specs/002-enhanced-todo-features/tasks.md
tests:
  - null
---

## Prompt

/sp.implement - Execute the implementation plan by processing and executing all tasks defined in tasks.md for the 002-enhanced-todo-features feature. This includes transitioning from text-based commands to a numeric menu system (1-8), implementing interactive prompts for task creation, adding category field, sort functionality, and visual separation lines.

## Response snapshot

Successfully implemented all 81 tasks across 11 phases:

**Phase 1 (Setup)**: Created backups of commands.py and main.py

**Phase 2 (Foundational)**:
- Updated Priority enum to use integers (HIGH=1, MEDIUM=2, LOW=3)
- Updated Recurrence enum to use integers (NONE=0, DAILY=1, WEEKLY=2, MONTHLY=3)
- Added `category: Optional[str] = None` field to Task dataclass
- Added `get_tasks_by_category()`, `get_tasks_sorted_by_date()`, `get_tasks_sorted_by_priority()` methods
- Added SEPARATOR_MAJOR and SEPARATOR_MINOR constants for visual consistency
- Added validation utilities for priority, recurring, date, and menu choice inputs

**Phase 3-11 (User Stories)**:
- Implemented numeric menu display (options 1-8)
- Implemented all 8 menu handlers: Add Task, View All, Update, Delete, Toggle Complete, Filter, Sort, Exit
- Interactive prompts for Add Task: Title -> Description -> Priority -> Category -> Due Date -> Recurring
- Filter submenu: By Category, Priority, Status
- Sort submenu: By Due Date (ascending), By Priority (High->Low)

All syntax checks passed. All module imports verified.

## Outcome

- ✅ Impact: Complete CLI refactor from text commands to numeric menu system with all 9 user stories implemented
- 🧪 Tests: Syntax validation passed; integration testing pending
- 📁 Files: 6 source files modified, 1 spec file updated with task completion markers
- 🔁 Next prompts: Run application manually to verify functionality, then add unit/integration tests
- 🧠 Reflection: Phased approach enabled systematic implementation; foundational changes (enums, model) were critical prerequisites

## Evaluation notes (flywheel)

- Failure modes observed: None - all implementations successful
- Graders run and results (PASS/FAIL): Syntax check PASS, Import check PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Run manual testing to verify menu interactions work correctly
