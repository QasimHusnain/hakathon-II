# Tasks: Enhanced Todo CLI with Refined UI

**Input**: Design documents from `/specs/todo-features/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/cli-interface.md, quickstart.md

**Tests**: Tests included for validation of new functionality
**Organization**: Tasks organized by user story with clear file paths for implementation

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project structure** per plan.md
- Source: `src/models/`, `src/services/`, `src/cli/`
- Tests: `tests/unit/`, `tests/integration/`
- Entry: `main.py`

---

## Phase 1: Setup

**Purpose**: Prepare for CLI refactoring to numeric menu system

- [X] T001 Verify Python 3.13+ and uv installation
- [X] T002 [P] Create backup of existing src/cli/commands.py before refactor
- [X] T003 [P] Create backup of existing main.py before refactor

---

## Phase 2: Foundational (Model & Service Updates)

**Purpose**: Core data model and service layer changes that ALL user stories depend on

**⚠️ CRITICAL**: Complete before any CLI refactoring

### Model Updates

- [X] T004 [P] Add `category: Optional[str] = None` field to Task dataclass in src/models/task.py
- [X] T005 [P] Verify Priority enum values are integers (HIGH=1, MEDIUM=2, LOW=3) in src/models/task.py
- [X] T006 [P] Verify Recurrence enum has NONE=0, DAILY=1, WEEKLY=2, MONTHLY=3 in src/models/task.py
- [X] T007 Update `__init__.py` exports in src/models/__init__.py if needed

### Service Layer Updates

- [X] T008 Add `get_tasks_by_category(category: str) -> list[Task]` method in src/services/task_manager.py
- [X] T009 Add `get_tasks_sorted_by_date() -> list[Task]` method (nulls last) in src/services/task_manager.py
- [X] T010 Add `get_tasks_sorted_by_priority() -> list[Task]` method (H→M→L) in src/services/task_manager.py
- [X] T011 Update `add_task()` to accept category parameter in src/services/task_manager.py
- [X] T012 Update `update_task()` to handle category field in src/services/task_manager.py

### Formatter Updates (Shared by all display)

- [X] T013 [P] Add `SEPARATOR_MAJOR = "=" * 40` constant in src/cli/formatter.py
- [X] T014 [P] Add `SEPARATOR_MINOR = "-" * 40` constant in src/cli/formatter.py
- [X] T015 Update `format_task()` to include category indicator `[Category]` in src/cli/formatter.py
- [X] T016 Update `format_task()` to use separation lines per constitution in src/cli/formatter.py

### Validation Utilities

- [X] T017 [P] Add `validate_priority_input(value: str) -> Optional[Priority]` in src/cli/parser.py
- [X] T018 [P] Add `validate_recurring_input(value: str) -> Optional[Recurrence]` in src/cli/parser.py
- [X] T019 [P] Add `validate_date_input(value: str) -> Optional[tuple[date, time]]` in src/cli/parser.py
- [X] T020 [P] Add `validate_menu_choice(value: str, min_val: int, max_val: int) -> Optional[int]` in src/cli/parser.py

**Checkpoint**: Foundation ready - CLI refactoring can now begin

---

## Phase 3: User Story 3 - Numeric Menu on Startup (Priority: P1) 🎯 MVP Foundation

**Goal**: Display numbered menu (1-8) on startup instead of text commands

**Independent Test**: Run `python main.py`, see numbered menu, enter invalid choice, see error

### Implementation for US3

- [X] T021 [US3] Create `display_main_menu()` function with header and 8 options in src/cli/commands.py
- [X] T022 [US3] Add menu header with `========` separation lines per constitution in src/cli/commands.py
- [X] T023 [US3] Create `get_menu_choice() -> int` with validation 1-8 in src/cli/commands.py
- [X] T024 [US3] Implement menu choice error handling with helpful message in src/cli/commands.py
- [X] T025 [US3] Create `main_menu_loop()` function skeleton in main.py
- [X] T026 [US3] Wire menu choice to stub handlers (print "Not implemented yet") in main.py
- [X] T027 [US3] Update main.py entry point to call main_menu_loop() instead of old cli_loop()

**Checkpoint**: Menu displays on startup, accepts 1-8, shows error for invalid input

---

## Phase 4: User Story 9 - Exit Application (Priority: P1)

**Goal**: Clean exit when user selects option 8

**Independent Test**: Select 8 from menu, see "Goodbye!", app exits

### Implementation for US9

- [X] T028 [US9] Implement `handle_exit()` function that prints "Goodbye!" in src/cli/commands.py
- [X] T029 [US9] Wire menu option 8 to handle_exit() and return from loop in main.py

**Checkpoint**: Menu option 8 exits cleanly

---

## Phase 5: User Story 1 - Add Task with Interactive Prompts (Priority: P1) 🎯 MVP

**Goal**: Interactive sequential prompts for task creation (Title → Description → Priority → Category → Due Date → Recurring)

**Independent Test**: Select 1, enter all fields, see "Task added successfully! ID: 1"

### Implementation for US1

- [X] T030 [US1] Create `handle_add_task(manager: TaskManager)` function skeleton in src/cli/commands.py
- [X] T031 [US1] Implement title prompt with empty validation ("Error: Task title cannot be empty") in src/cli/commands.py
- [X] T032 [US1] Implement description prompt (Enter to skip) in src/cli/commands.py
- [X] T033 [US1] Implement priority prompt (1=High, 2=Medium, 3=Low) [2] default in src/cli/commands.py
- [X] T034 [US1] Implement category prompt (Enter to skip) in src/cli/commands.py
- [X] T035 [US1] Implement due date prompt with YYYY-MM-DD or YYYY-MM-DD HH:MM validation in src/cli/commands.py
- [X] T036 [US1] Implement recurring prompt (1=Daily, 2=Weekly, 3=Monthly or Enter) in src/cli/commands.py
- [X] T037 [US1] Call TaskManager.add_task() with collected values in src/cli/commands.py
- [X] T038 [US1] Display success message with task ID and `---` separation lines in src/cli/commands.py
- [X] T039 [US1] Wire menu option 1 to handle_add_task(manager) in main.py

**Checkpoint**: Can add tasks via interactive prompts, all validation works

---

## Phase 6: User Story 2 - View All Tasks (Priority: P1)

**Goal**: Display all tasks with visual indicators for status, priority, category, due date, recurring

**Independent Test**: Add tasks, select 2, see formatted list with indicators and separation lines

### Implementation for US2

- [X] T040 [US2] Create `handle_view_tasks(manager: TaskManager)` function in src/cli/commands.py
- [X] T041 [US2] Add header "ALL TASKS" with `========` separation lines in src/cli/commands.py
- [X] T042 [US2] Call TaskManager.get_all_tasks() and format each with format_task() in src/cli/commands.py
- [X] T043 [US2] Handle empty list case with "Your task list is empty." message in src/cli/commands.py
- [X] T044 [US2] Display "Total: N task(s)" at bottom in src/cli/commands.py
- [X] T045 [US2] Wire menu option 2 to handle_view_tasks(manager) in main.py

**Checkpoint**: All tasks display with correct formatting and indicators

---

## Phase 7: User Story 4 - Update Task (Priority: P2)

**Goal**: Interactive prompts to update any task attribute via submenu

**Independent Test**: Add task, select 3, enter ID, select field, enter new value, verify change

### Implementation for US4

- [X] T046 [US4] Create `handle_update_task(manager: TaskManager)` function in src/cli/commands.py
- [X] T047 [US4] Prompt for task ID with validation ("Error: Task ID must be a number") in src/cli/commands.py
- [X] T048 [US4] Lookup task and display current details or "Task [ID] not found" in src/cli/commands.py
- [X] T049 [US4] Create update field submenu (1-7: Title, Description, Priority, Category, Due Date, Recurring, Back) in src/cli/commands.py
- [X] T050 [US4] Implement update handler for each field with appropriate validation in src/cli/commands.py
- [X] T051 [US4] Add "Back to Main Menu" option (7) in src/cli/commands.py
- [X] T052 [US4] Display "Task [ID] updated successfully." after update in src/cli/commands.py
- [X] T053 [US4] Wire menu option 3 to handle_update_task(manager) in main.py

**Checkpoint**: Can update any task field via interactive submenu

---

## Phase 8: User Story 5 - Delete Task (Priority: P2)

**Goal**: Delete task by ID with confirmation

**Independent Test**: Add task, select 4, enter ID, confirm, verify task removed

### Implementation for US5

- [X] T054 [US5] Create `handle_delete_task(manager: TaskManager)` function in src/cli/commands.py
- [X] T055 [US5] Prompt for task ID with validation in src/cli/commands.py
- [X] T056 [US5] Lookup task and display "Task to delete:" details or error in src/cli/commands.py
- [X] T057 [US5] Add confirmation prompt "Are you sure you want to delete this task? (y/n):" in src/cli/commands.py
- [X] T058 [US5] Call TaskManager.delete_task() on 'y' confirmation in src/cli/commands.py
- [X] T059 [US5] Display "Task [ID] deleted successfully." or "Delete cancelled." in src/cli/commands.py
- [X] T060 [US5] Wire menu option 4 to handle_delete_task(manager) in main.py

**Checkpoint**: Can delete tasks with confirmation

---

## Phase 9: User Story 6 - Toggle Task Completion (Priority: P2)

**Goal**: Toggle status between Pending/Complete, auto-create next for recurring

**Independent Test**: Add recurring task, select 5, toggle complete, see new recurring task created

### Implementation for US6

- [X] T061 [US6] Create `handle_toggle_complete(manager: TaskManager)` function in src/cli/commands.py
- [X] T062 [US6] Prompt for task ID with validation in src/cli/commands.py
- [X] T063 [US6] Call TaskManager.toggle_complete() and capture result in src/cli/commands.py
- [X] T064 [US6] If recurring and was pending, display "New recurring task created: [new_id]" in src/cli/commands.py
- [X] T065 [US6] Display "Task [ID] marked as complete/pending." message in src/cli/commands.py
- [X] T066 [US6] Wire menu option 5 to handle_toggle_complete(manager) in main.py

**Checkpoint**: Toggle works, recurring tasks create next occurrence

---

## Phase 10: User Story 7 - Search / Filter Tasks (Priority: P3)

**Goal**: Filter submenu to view tasks by category, priority, or status

**Independent Test**: Add tasks with different attributes, select 6, filter by each criterion

### Implementation for US7

- [X] T067 [US7] Create `handle_filter_menu(manager: TaskManager)` function in src/cli/commands.py
- [X] T068 [US7] Display filter submenu with `--- Filter Tasks ---` header and options 1-4 in src/cli/commands.py
- [X] T069 [US7] Implement filter by category (option 1): prompt category, call get_tasks_by_category() in src/cli/commands.py
- [X] T070 [US7] Implement filter by priority (option 2): prompt 1/2/3, filter by Priority enum in src/cli/commands.py
- [X] T071 [US7] Implement filter by status (option 3): submenu 1=Pending, 2=Complete in src/cli/commands.py
- [X] T072 [US7] Add "Back to Main Menu" (option 4) in src/cli/commands.py
- [X] T073 [US7] Display filtered results with header or "No tasks match your filter criteria." in src/cli/commands.py
- [X] T074 [US7] Wire menu option 6 to handle_filter_menu(manager) in main.py

**Checkpoint**: All filter options work correctly

---

## Phase 11: User Story 8 - Sort Tasks (Priority: P3)

**Goal**: Sort submenu to order tasks by due date or priority

**Independent Test**: Add tasks with different dates/priorities, select 7, sort by each criterion

### Implementation for US8

- [X] T075 [US8] Create `handle_sort_menu(manager: TaskManager)` function in src/cli/commands.py
- [X] T076 [US8] Display sort submenu with `--- Sort Tasks ---` header and options 1-3 in src/cli/commands.py
- [X] T077 [US8] Implement sort by due date (option 1): call get_tasks_sorted_by_date() in src/cli/commands.py
- [X] T078 [US8] Implement sort by priority (option 2): call get_tasks_sorted_by_priority() in src/cli/commands.py
- [X] T079 [US8] Add "Back to Main Menu" (option 3) in src/cli/commands.py
- [X] T080 [US8] Display sorted results with header "(sorted by due date/priority)" in src/cli/commands.py
- [X] T081 [US8] Wire menu option 7 to handle_sort_menu(manager) in main.py

**Checkpoint**: All sort options work correctly

---

## Phase 12: Testing Updates

**Purpose**: Update tests for new functionality

### Unit Tests

- [X] T082 [P] Add unit tests for category field in tests/unit/test_task_model.py
- [X] T083 [P] Add unit tests for Priority integer values in tests/unit/test_task_model.py
- [X] T084 [P] Add unit tests for get_tasks_by_category() in tests/unit/test_task_manager.py
- [X] T085 [P] Add unit tests for get_tasks_sorted_by_date() in tests/unit/test_task_manager.py
- [X] T086 [P] Add unit tests for get_tasks_sorted_by_priority() in tests/unit/test_task_manager.py
- [X] T087 [P] Add unit tests for validation utilities in tests/unit/test_parser.py
- [X] T088 [P] Add unit tests for format_task() with category in tests/unit/test_formatter.py

### Integration Tests

- [X] T089 Add integration test for Add Task flow in tests/integration/test_cli_commands.py
- [X] T090 Add integration test for Filter submenu in tests/integration/test_cli_commands.py
- [X] T091 Add integration test for Sort submenu in tests/integration/test_cli_commands.py

**Checkpoint**: All tests pass (112 tests passing)

---

## Phase 13: Polish & Cross-Cutting Concerns

**Purpose**: Final cleanup and validation

- [X] T092 Run mypy type checking on all modified files
- [X] T093 Run quickstart.md validation - verify all menu examples work
- [X] T094 Update docstrings with task ID references in all modified files
- [X] T095 Remove backup files (T002, T003) if refactor successful (no backup files exist)

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Setup) ──────────────────┐
                                  ▼
Phase 2 (Foundational) ───────────┤ BLOCKS ALL BELOW
                                  ▼
Phase 3 (US3-Menu) ───────────────┤ Foundation for all stories
                 │                ▼
                 ├──► Phase 4 (US9-Exit)
                 │
                 ├──► Phase 5 (US1-Add) ──┬──► Phase 6 (US2-View)
                 │                        │
                 ├──► Phase 7 (US4-Update)│
                 ├──► Phase 8 (US5-Delete)│
                 ├──► Phase 9 (US6-Toggle)│
                 │                        │
                 ├──► Phase 10 (US7-Filter)
                 └──► Phase 11 (US8-Sort)
                                          │
                                          ▼
                            Phase 12 (Testing)
                                          │
                                          ▼
                            Phase 13 (Polish)
```

### Parallel Opportunities

**Foundational Phase** (after T003):
```bash
# Models in parallel:
T004, T005, T006

# Formatters in parallel:
T013, T014

# Validators in parallel:
T017, T018, T019, T020
```

**After US3 Complete**:
```bash
# These user stories can run in parallel with different developers:
US1 (Add) || US9 (Exit)
US4 (Update) || US5 (Delete) || US6 (Toggle)
US7 (Filter) || US8 (Sort)
```

**Testing Phase**:
```bash
# All unit tests in parallel:
T082, T083, T084, T085, T086, T087, T088
```

---

## File Change Summary

| File | Tasks | Change Type |
|------|-------|-------------|
| src/models/task.py | T004-T006 | Modify (add category) |
| src/models/__init__.py | T007 | Modify (exports) |
| src/services/task_manager.py | T008-T012 | Modify (filter/sort/category) |
| src/cli/formatter.py | T013-T016 | Modify (separators, category) |
| src/cli/parser.py | T017-T020 | Modify (validators) |
| src/cli/commands.py | T021-T081 | **Major Refactor** (menu handlers) |
| main.py | T025-T027, T029, T039, T045, T053, T060, T066, T074, T081 | **Major Refactor** (menu loop) |
| tests/unit/*.py | T082-T088 | Modify (new tests) |
| tests/integration/*.py | T089-T091 | Modify (new tests) |

---

## Implementation Strategy

### MVP First (Phases 1-6)

1. **Phase 1**: Setup (3 tasks)
2. **Phase 2**: Foundational (17 tasks)
3. **Phase 3**: US3 - Menu (7 tasks)
4. **Phase 4**: US9 - Exit (2 tasks)
5. **Phase 5**: US1 - Add Task (10 tasks)
6. **Phase 6**: US2 - View Tasks (6 tasks)
7. **STOP and VALIDATE**: Basic app works - menu + add + view + exit

**MVP = 45 tasks**

### Incremental Delivery

1. **MVP**: Menu + Exit + Add + View = Working task manager
2. **CRUD Complete**: Add US4-US6 = Full task management
3. **Enhanced**: Add US7-US8 = Filter and Sort
4. **Quality**: Testing and Polish

---

## Summary

| Metric | Count |
|--------|-------|
| **Total Tasks** | 95 |
| **Completed Tasks** | 95 ✅ |
| Setup Tasks | 3 |
| Foundational Tasks | 17 |
| User Story Tasks | 64 |
| Testing Tasks | 10 |
| Polish Tasks | 4 |
| **MVP Tasks** | 45 |
| Files Modified | 9 |
| Major Refactors | 2 (commands.py, main.py) |
| **Test Count** | 112 passing |

| Phase | Story | Tasks | Status |
|-------|-------|-------|--------|
| 1 | Setup | 3 | ✅ Complete |
| 2 | Foundational | 17 | ✅ Complete |
| 3 | US3 (Menu) | 7 | ✅ Complete |
| 4 | US9 (Exit) | 2 | ✅ Complete |
| 5 | US1 (Add) | 10 | ✅ Complete |
| 6 | US2 (View) | 6 | ✅ Complete |
| 7 | US4 (Update) | 8 | ✅ Complete |
| 8 | US5 (Delete) | 7 | ✅ Complete |
| 9 | US6 (Toggle) | 6 | ✅ Complete |
| 10 | US7 (Filter) | 8 | ✅ Complete |
| 11 | US8 (Sort) | 7 | ✅ Complete |
| 12 | Testing | 10 | ✅ Complete |
| 13 | Polish | 4 | ✅ Complete |
