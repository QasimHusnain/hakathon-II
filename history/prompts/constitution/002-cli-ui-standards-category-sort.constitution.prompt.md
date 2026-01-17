---
id: 002
title: CLI UI Standards Category Sort
stage: constitution
date: 2026-01-17
surface: agent
model: claude-opus-4-5-20251101
feature: none
branch: todo-features
user: user
command: /sp.constitution
labels: ["cli-ui", "validation", "category", "sort", "numeric-menu"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - CLAUDE.md
tests:
  - null
---

## Prompt

Role: Expert Python Developer / CLI Architect. Context: We are refining the Todo App. You must strictly follow the Speckit Plus workflow for all changes. Do not modify source code until the documentation phase is complete.

Reference Features (from Terminal Session): Align the application to support the following CLI menu:

View All Tasks
Update Task
Delete Task
Toggle Task Completion
Search / Filter Tasks (by Category, Priority, or Status)
Sort Tasks (by Due Date or Priority)
Exit

Specific "Add Task" Flow Requirements: Ensure the input sequence matches: Title → Description → Priority (1-3) → Category → Due Date (YYYY-MM-DD or YYYY-MM-DD HH:MM).

Required Workflow Steps (In Order):
1. Update sp.constitution: Add rules for CLI UI consistency (e.g., use of separation lines, standard prompt formats). Define validation rules for input (e.g., date formats, integer choices).
2. Update sp.spec: Detail the functional specifications for the Search/Filter and Sort logic. Define the data schema requirements in models.py to support these features.
3. Update sp.plan: Outline the high-level roadmap for transitioning the current state to the full 7-feature menu.
4. Update sp.tasks: Generate a granular task list. Break tasks down by file: services/ (logic), storage.py (persistence), and main.py (CLI loop).
5. Implementation: Once I approve the tasks, begin implementing the changes. Ensure the terminal output uses clear separation lines as seen in the reference image.

## Response snapshot

Updated constitution from v2.0.0 to v2.1.0 (MINOR bump) with the following changes:

**Added Sections:**
- VI. CLI User Interface Standards (separation lines, standard prompts, success/error formats)
- VII. Input Validation Rules (date formats, priority values, menu choices, task ID, empty title)

**Modified Sections:**
- III.A. Core Features: Expanded from 7 to 8 Pillars, added Category field, Sort functionality
- III.B. Numeric Menu System: Added 1-8 numbered menu structure
- III.C. Interactive Add Task Flow: Sequential prompts (Title → Description → Priority → Category → Due Date)
- III.D. Task Attribute Defaults: Added Category field
- Data Model: Added category field to Task dataclass, updated Priority enum to use integer values

**Updated Files:**
- `.specify/memory/constitution.md` - Full constitution update with sync impact report
- `CLAUDE.md` - Updated Phase I Features to 8 Pillars, added CLI Menu System section

## Outcome

- ✅ Impact: Constitution updated to v2.1.0 with CLI UI standards and validation rules
- 🧪 Tests: N/A (documentation only)
- 📁 Files: 2 files modified (.specify/memory/constitution.md, CLAUDE.md)
- 🔁 Next prompts: Update spec.md, plan.md, tasks.md per workflow steps 2-4
- 🧠 Reflection: MINOR version bump appropriate - added new sections without breaking existing governance

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed with spec update to add Category and Sort specifications
