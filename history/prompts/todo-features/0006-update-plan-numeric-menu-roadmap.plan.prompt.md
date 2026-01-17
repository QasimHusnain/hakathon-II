---
id: 0006
title: Update Plan Numeric Menu Roadmap
stage: plan
date: 2026-01-17
surface: agent
model: claude-opus-4-5-20251101
feature: todo-features
branch: todo-features
user: user
command: /sp.plan
labels: ["plan-update", "numeric-menu", "transition-roadmap", "cli-refactor"]
links:
  spec: specs/todo-features/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/todo-features/plan.md
  - specs/todo-features/contracts/cli-interface.md
  - specs/todo-features/quickstart.md
tests:
  - null
---

## Prompt

Update sp.plan: Outline the high-level roadmap for transitioning the current state to the full 8-feature menu. This includes:
- Transition from text commands to numeric menu (1-8)
- Interactive prompts instead of command-line flags
- Category field addition
- Sort functionality
- Visual separation lines
- Recurring functionality with numeric input

## Response snapshot

Updated plan.md with comprehensive transition roadmap:

**Technical Context**:
- Python 3.13+, standard library only
- In-memory storage
- pytest/mypy for testing

**Constitution Check**: All 9 gates passed

**Design Decisions**:
1. Transition from text commands to numeric menu
2. Interactive prompt flow for Add Task
3. Category field as free-form text
4. Sort by due date (ascending, nulls last) and priority (H→M→L)
5. Separation lines (40 chars)
6. Validation per constitution rules

**Transition Roadmap** (5 Phases):
- Phase 1: Model Updates (Category field)
- Phase 2: Service Layer (filter/sort methods)
- Phase 3: CLI Refactoring (menus, prompts, formatters)
- Phase 4: Main Loop (menu selection loop)
- Phase 5: Testing Updates

**Files Requiring Changes**:
- src/models/task.py - Add category
- src/services/task_manager.py - Add filter/sort
- src/cli/commands.py - Major refactor to menu handlers
- src/cli/formatter.py - Separation lines
- main.py - Major refactor to menu loop
- All test files updated

**Updated Artifacts**:
- contracts/cli-interface.md - Full menu system contract
- quickstart.md - Updated with menu-based demo

## Outcome

- ✅ Impact: Plan updated with clear transition roadmap from text commands to numeric menu
- 🧪 Tests: N/A (documentation only)
- 📁 Files: 3 files updated (plan.md, cli-interface.md, quickstart.md)
- 🔁 Next prompts: Generate tasks.md via /sp.tasks with file-based granularity
- 🧠 Reflection: Plan provides clear phased approach minimizing risk of breaking changes

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed with task generation organized by file
