# Tasks: Todo CLI Basic

**Input**: Design documents from `/specs/001-todo-cli-basic/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are NOT included in this task list as they were not explicitly requested in the specification. The constitution requires testability, which is achieved through the independently testable user stories.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

Single project structure at repository root:
- Source: `src/models/`, `src/services/`, `src/cli/`
- Tests: `tests/unit/`, `tests/integration/`
- Entry: `main.py`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project directory structure (src/models/, src/services/, src/cli/, tests/unit/, tests/integration/)
- [ ] T002 Initialize uv project with pyproject.toml (Python 3.13+, dev dependencies: pytest, mypy)
- [ ] T003 [P] Create src/__init__.py and src/cli/__init__.py module files
- [ ] T004 [P] Create .gitignore for Python project (__pycache__, .pytest_cache, .mypy_cache, *.pyc)
- [ ] T005 [P] Create README.md with basic usage instructions

**Checkpoint**: Project structure ready for implementation

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core data model and exceptions that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T006 [P] Create Status enum (PENDING, COMPLETE) in src/models/task.py
- [ ] T007 [P] Create custom exception classes (TaskError, TaskNotFoundError, InvalidTaskDataError) in src/models/task.py
- [ ] T008 Create Task dataclass with validation in src/models/task.py (depends on T006, T007)
- [ ] T009 Create TaskManager class skeleton with __init__ in src/services/task_manager.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add and View Tasks (Priority: P1) 🎯 MVP

**Goal**: Users can add tasks with title and optional description, then view their complete task list with status indicators

**Independent Test**: Add one or more tasks via CLI and display the task list with clear formatting. Delivers immediate value as a basic task capture tool.

### Implementation for User Story 1

- [ ] T010 [P] [US1] Implement TaskManager.add_task(title, description) method in src/services/task_manager.py
- [ ] T011 [P] [US1] Implement TaskManager.get_all_tasks() method in src/services/task_manager.py
- [ ] T012 [P] [US1] Create format_task(task) function in src/cli/formatter.py
- [ ] T013 [P] [US1] Create format_task_list(tasks) function with [ ] status indicators in src/cli/formatter.py
- [ ] T014 [US1] Implement handle_add(args, manager) command handler in src/cli/commands.py
- [ ] T015 [US1] Implement handle_list(args, manager) command handler in src/cli/commands.py
- [ ] T016 [US1] Implement parse_command(input_str) function in src/cli/commands.py
- [ ] T017 [US1] Create main() CLI loop with TaskManager initialization in main.py
- [ ] T018 [US1] Add welcome message and help command to CLI loop in main.py
- [ ] T019 [US1] Add error handling for InvalidTaskDataError (empty title) in handle_add

**Checkpoint**: At this point, User Story 1 should be fully functional - users can add tasks and view their list

---

## Phase 4: User Story 2 - Mark Tasks Complete (Priority: P2)

**Goal**: Users can toggle task status between Pending and Complete, with visual indicator changes from [ ] to [X]

**Independent Test**: Add a task, mark it complete, and verify the status indicator changes from [ ] to [X] in the task list.

### Implementation for User Story 2

- [ ] T020 [US2] Implement TaskManager.get_task(task_id) method in src/services/task_manager.py
- [ ] T021 [US2] Implement TaskManager.toggle_complete(task_id) method in src/services/task_manager.py
- [ ] T022 [US2] Update format_task() to display [X] for complete status in src/cli/formatter.py
- [ ] T023 [US2] Implement handle_complete(args, manager) command handler in src/cli/commands.py
- [ ] T024 [US2] Add complete command to parse_command() in src/cli/commands.py
- [ ] T025 [US2] Add error handling for TaskNotFoundError in handle_complete
- [ ] T026 [US2] Add error handling for non-integer task IDs (ValueError) in handle_complete

**Checkpoint**: At this point, User Stories 1 AND 2 should both work - users can add, view, and mark tasks complete

---

## Phase 5: User Story 3 - Update Task Details (Priority: P3)

**Goal**: Users can modify the title or description of existing tasks to correct or enhance task information

**Independent Test**: Add a task, modify its title or description, and verify the changes are reflected in the task list.

### Implementation for User Story 3

- [ ] T027 [US3] Implement TaskManager.update_task(task_id, title, description) method in src/services/task_manager.py
- [ ] T028 [US3] Implement handle_update(args, manager) command handler in src/cli/commands.py
- [ ] T029 [US3] Add update command to parse_command() in src/cli/commands.py
- [ ] T030 [US3] Add validation for update field (must be 'title' or 'description') in handle_update
- [ ] T031 [US3] Add error handling for TaskNotFoundError in handle_update
- [ ] T032 [US3] Add error handling for invalid field names in handle_update
- [ ] T033 [US3] Add error handling for empty title updates (InvalidTaskDataError) in handle_update

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should work - users can add, view, complete, and update tasks

---

## Phase 6: User Story 4 - Delete Unwanted Tasks (Priority: P4)

**Goal**: Users can remove tasks that are no longer relevant or were added by mistake

**Independent Test**: Add a task, delete it by ID, and verify it no longer appears in the task list.

### Implementation for User Story 4

- [ ] T034 [US4] Implement TaskManager.delete_task(task_id) method in src/services/task_manager.py
- [ ] T035 [US4] Implement handle_delete(args, manager) command handler in src/cli/commands.py
- [ ] T036 [US4] Add delete command to parse_command() in src/cli/commands.py
- [ ] T037 [US4] Add error handling for TaskNotFoundError in handle_delete
- [ ] T038 [US4] Add error handling for non-integer task IDs (ValueError) in handle_delete

**Checkpoint**: All 4 user stories should now be independently functional - full CRUD operations available

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and ensure code quality

- [ ] T039 [P] Implement handle_help() to display all available commands in src/cli/commands.py
- [ ] T040 [P] Implement format_success(message) helper in src/cli/formatter.py
- [ ] T041 [P] Implement format_error(message) helper in src/cli/formatter.py
- [ ] T042 Add help command to parse_command() in src/cli/commands.py
- [ ] T043 Add quit/exit command handling to main CLI loop in main.py
- [ ] T044 [P] Add type hints validation with mypy - run 'mypy src/' and fix any type errors
- [ ] T045 [P] Add docstrings with task ID references to all functions per constitution requirement
- [ ] T046 Update README.md with complete usage examples for all commands
- [ ] T047 Manual testing: Run through quickstart.md validation scenarios
- [ ] T048 Edge case handling: Test empty list display message in format_task_list()
- [ ] T049 Edge case handling: Test very long descriptions (100+ chars) formatting
- [ ] T050 Edge case handling: Test whitespace-only title rejection

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (US1 → US2 → US3 → US4)
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Independent (uses get_task and toggle, doesn't depend on US1)
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Independent (uses get_task and update, doesn't depend on US1 or US2)
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Independent (uses delete only, doesn't depend on other stories)

**Note**: While user stories are technically independent, US1 provides the most value and should be completed first as the MVP foundation.

### Within Each User Story

- **US1 Flow**: TaskManager methods (T010, T011) → Formatter (T012, T013) → Commands (T014-T016) → Main loop (T017, T018) → Error handling (T019)
- **US2 Flow**: TaskManager methods (T020, T021) → Formatter update (T022) → Commands (T023, T024) → Error handling (T025, T026)
- **US3 Flow**: TaskManager method (T027) → Command (T028, T029) → Validation & error handling (T030-T033)
- **US4 Flow**: TaskManager method (T034) → Command (T035, T036) → Error handling (T037, T038)

### Parallel Opportunities

**Setup Phase**:
- T003, T004, T005 can all run in parallel

**Foundational Phase**:
- T006, T007 can run in parallel
- T008 depends on both T006 and T007
- T009 depends on T008

**User Story 1**:
- T010, T011 can run in parallel (different TaskManager methods)
- T012, T013 can run in parallel (different formatter functions)
- T014, T015, T016 must be sequential (T016 parses commands, T014/T015 handle them)

**User Story 2**:
- T020, T021 can run in parallel

**Between User Stories**:
- Once Foundational is complete, all 4 user stories (US1, US2, US3, US4) can be worked on in parallel by different developers

**Polish Phase**:
- T039, T040, T041, T044, T045, T046 can all run in parallel

---

## Parallel Example: User Story 1

```bash
# After Foundational Phase completes, launch these in parallel:

# TaskManager methods (can be done simultaneously):
Task T010: "Implement TaskManager.add_task(title, description) method"
Task T011: "Implement TaskManager.get_all_tasks() method"

# Formatter functions (can be done simultaneously):
Task T012: "Create format_task(task) function"
Task T013: "Create format_task_list(tasks) function"

# After methods and formatters are done, implement commands sequentially
```

---

## Parallel Example: All User Stories (Multi-Developer Team)

```bash
# After Foundational Phase (Phase 2) completes:

Developer A: Phase 3 (User Story 1) - Add and View Tasks
Developer B: Phase 4 (User Story 2) - Mark Tasks Complete
Developer C: Phase 5 (User Story 3) - Update Task Details
Developer D: Phase 6 (User Story 4) - Delete Tasks

# Each developer implements their story independently
# Stories integrate naturally through shared TaskManager and formatter
```

---

## Implementation Strategy

### MVP First (User Story 1 Only) - Recommended Approach

1. Complete Phase 1: Setup (T001-T005)
2. Complete Phase 2: Foundational (T006-T009) - CRITICAL
3. Complete Phase 3: User Story 1 (T010-T019)
4. **STOP and VALIDATE**: Test User Story 1 independently
   - Can add tasks with title and description
   - Can view task list with [ ] indicators
   - Empty title is rejected
   - Empty list shows appropriate message
5. Demo/deploy if ready - you have a working task capture tool!

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → **Deploy/Demo MVP!** ✅
3. Add User Story 2 → Test independently → Deploy/Demo (now with completion tracking)
4. Add User Story 3 → Test independently → Deploy/Demo (now with editing)
5. Add User Story 4 → Test independently → Deploy/Demo (now with deletion)
6. Add Polish → Final release
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers (after Foundational Phase completes):

1. Team completes Setup (Phase 1) + Foundational (Phase 2) together
2. Once Foundational is done, split work:
   - **Developer A**: User Story 1 (T010-T019) - Priority 1
   - **Developer B**: User Story 2 (T020-T026) - Priority 2
   - **Developer C**: User Story 3 (T027-T033) - Priority 3
   - **Developer D**: User Story 4 (T034-T038) - Priority 4
3. Stories complete independently and integrate naturally
4. Team reconvenes for Polish (Phase 7)

---

## Task Summary

- **Total Tasks**: 50
- **Setup**: 5 tasks (T001-T005)
- **Foundational**: 4 tasks (T006-T009)
- **User Story 1 (P1)**: 10 tasks (T010-T019) - MVP
- **User Story 2 (P2)**: 7 tasks (T020-T026)
- **User Story 3 (P3)**: 7 tasks (T027-T033)
- **User Story 4 (P4)**: 5 tasks (T034-T038)
- **Polish**: 12 tasks (T039-T050)

**Parallel Opportunities**: 15 tasks marked [P] can run in parallel with other tasks in their phase

**MVP Scope** (Recommended first delivery): Phase 1 + Phase 2 + Phase 3 = 19 tasks

**Independent Stories**: All 4 user stories are independently testable after Foundational phase

---

## Notes

- **[P] tasks**: Different files, no dependencies - can run in parallel
- **[Story] label**: Maps task to specific user story for traceability
- **Constitution compliance**: All tasks include type hints, docstrings with task IDs, and error handling
- **Each user story independently testable**: Can validate US1 without US2/US3/US4, etc.
- **No tests included**: Tests not explicitly requested in specification; testability achieved through independent user stories
- **Type hints mandatory**: Task T044 validates all type hints with mypy
- **Task ID references**: Task T045 adds docstrings referencing task IDs per constitution
- **Error handling**: ValueError for non-integer IDs, TaskNotFoundError for missing IDs, InvalidTaskDataError for validation failures
- **Separation of concerns**: Models (task.py), Services (task_manager.py), CLI (commands.py, formatter.py) clearly separated
- **Commit after each task or logical group**: Enables incremental progress tracking
- **Stop at checkpoints**: Validate each story independently before proceeding
