---
id: 0005
title: Update Spec Category Sort Menu
stage: spec
date: 2026-01-17
surface: agent
model: claude-opus-4-5-20251101
feature: todo-features
branch: todo-features
user: user
command: /sp.specify
labels: ["spec-update", "category", "sort", "numeric-menu", "interactive-prompts"]
links:
  spec: specs/todo-features/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/todo-features/spec.md
  - specs/todo-features/data-model.md
  - specs/todo-features/checklists/requirements.md
tests:
  - null
---

## Prompt

Role: Expert Python Developer / CLI Architect. Context: We are refining the Todo App. You must strictly follow the Speckit Plus workflow for all changes. Do not modify source code until the documentation phase is complete.

Reference Features (from Terminal Session): Align the application to support the following CLI menu:
- View All Tasks
- Update Task
- Delete Task
- Toggle Task Completion
- Search / Filter Tasks (by Category, Priority, or Status)
- Sort Tasks (by Due Date or Priority)
- Exit

Specific "Add Task" Flow Requirements: Ensure the input sequence matches: Title → Description → Priority (1-3) → Category → Due Date (YYYY-MM-DD or YYYY-MM-DD HH:MM).

User clarification: Do not remove recurring requirements. Must add recurring, so that the user can mention daily, weekly, or monthly but keep optional. There would be options: user selects 1 for daily, 2 for weekly, and so on.

## Response snapshot

Updated spec.md to align with Constitution v2.1.0 with the following changes:

**User Stories (9 total)**:
- US1: Add Task with Interactive Prompts (P1)
- US2: View All Tasks with Visual Indicators (P1)
- US3: Numeric Menu on Startup (P1)
- US4: Update Task via Interactive Prompts (P2)
- US5: Delete Task (P2)
- US6: Toggle Task Completion with Auto-Recurring (P2)
- US7: Search / Filter Tasks (P3)
- US8: Sort Tasks (P3) - NEW
- US9: Exit Application (P1)

**Key Changes**:
1. Added Category field to Task model
2. Added Sort functionality (by due date or priority)
3. Changed to numeric menu system (1-8)
4. Changed to interactive Add Task flow with sequential prompts
5. Updated Priority/Recurring to numeric input (1/2/3)
6. Added separation lines for visual clarity
7. Kept Recurring functionality with numeric input (1=Daily, 2=Weekly, 3=Monthly)

**Updated Files**:
- spec.md: 9 User Stories, 36 Functional Requirements, 11 Success Criteria
- data-model.md: Added category field, updated data flows
- checklists/requirements.md: Updated validation summary

## Outcome

- ✅ Impact: Specification updated to align with Constitution v2.1.0
- 🧪 Tests: N/A (documentation only)
- 📁 Files: 3 files modified (spec.md, data-model.md, checklists/requirements.md)
- 🔁 Next prompts: Update plan.md with roadmap, then tasks.md with granular file-based tasks
- 🧠 Reflection: User clarification about recurring was important - kept all recurring logic with new numeric input style

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed with plan update to define transition roadmap
