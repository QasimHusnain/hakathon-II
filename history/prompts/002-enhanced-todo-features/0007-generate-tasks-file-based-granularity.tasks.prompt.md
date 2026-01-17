---
id: 0007
title: Generate Tasks File Based Granularity
stage: tasks
date: 2026-01-17
surface: agent
model: claude-opus-4-5-20251101
feature: 002-enhanced-todo-features
branch: 002-enhanced-todo-features
user: user
command: /sp.tasks
labels: ["tasks", "file-based", "granular", "numeric-menu", "refactor"]
links:
  spec: specs/002-enhanced-todo-features/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-enhanced-todo-features/tasks.md
tests:
  - null
---

## Prompt

Update sp.tasks: Generate a granular task list. Break tasks down by file: services/ (logic), storage.py (persistence), and main.py (CLI loop). Organize tasks by user story with clear file paths for implementation.

## Response snapshot

Generated comprehensive tasks.md with 95 tasks across 13 phases:

**Task Summary**:
- Total Tasks: 95
- Setup Tasks: 3
- Foundational Tasks: 17
- User Story Tasks: 64
- Testing Tasks: 10
- Polish Tasks: 4
- MVP Tasks: 45

**Phases**:
1. Setup (3 tasks) - Backup existing files
2. Foundational (17 tasks) - Model, service, formatter, validator updates
3. US3 Menu (7 tasks) - Numeric menu display and selection
4. US9 Exit (2 tasks) - Clean application exit
5. US1 Add (10 tasks) - Interactive add task prompts
6. US2 View (6 tasks) - Display all tasks with indicators
7. US4 Update (8 tasks) - Update task submenu
8. US5 Delete (7 tasks) - Delete with confirmation
9. US6 Toggle (6 tasks) - Toggle completion with auto-recurring
10. US7 Filter (8 tasks) - Filter submenu by category/priority/status
11. US8 Sort (7 tasks) - Sort submenu by date/priority
12. Testing (10 tasks) - Unit and integration tests
13. Polish (4 tasks) - Type checking, validation, cleanup

**Key Files**:
- src/cli/commands.py: 61 tasks (major refactor)
- main.py: 10 tasks (major refactor)
- src/services/task_manager.py: 5 tasks
- src/cli/formatter.py: 4 tasks
- src/cli/parser.py: 4 tasks
- src/models/task.py: 3 tasks

**MVP Strategy**: Phases 1-6 = 45 tasks for working menu + add + view + exit

## Outcome

- ✅ Impact: Comprehensive task list with file-based organization ready for implementation
- 🧪 Tests: Tests included in Phase 12 (10 tasks)
- 📁 Files: 1 file created (tasks.md)
- 🔁 Next prompts: User approval, then /sp.implement to begin implementation
- 🧠 Reflection: Tasks organized by user story enable incremental delivery; MVP is 45 tasks

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Await user approval then begin implementation
