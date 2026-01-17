# Feature Specification: Enhanced Todo CLI with Refined UI

**Feature Branch**: `todo-features`
**Created**: 2026-01-16
**Updated**: 2026-01-17
**Status**: Draft
**Input**: User description: "Enhanced Todo CLI with numeric menu, interactive prompts, category, priority, recurring, date/time, filtering, and sorting"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Add Task with Interactive Prompts (Priority: P1)

As a user, I want to add tasks through a guided interactive flow with sequential prompts so that I can easily enter all task information without memorizing command syntax.

**Why this priority**: This is the foundation of the enhanced system. Without the ability to add tasks with all attributes, no other feature can be demonstrated. The interactive flow improves usability over command-line flags.

**Independent Test**: Select menu option 1, follow prompts to enter all attributes, and verify task is created correctly.

**Acceptance Scenarios**:

1. **Given** the main menu is displayed, **When** I select `1` (Add Task), **Then** I am prompted for Title first.

2. **Given** I am in the Add Task flow, **When** I enter a title and press Enter, **Then** I am prompted for Description with option to skip.

3. **Given** I am prompted for Priority, **When** I enter `1`, **Then** the task is set to High priority.

4. **Given** I am prompted for Priority, **When** I press Enter without input, **Then** the task defaults to Medium priority (2).

5. **Given** I am prompted for Category, **When** I enter "Work", **Then** the task is assigned to the Work category.

6. **Given** I am prompted for Category, **When** I press Enter without input, **Then** the task has no category.

7. **Given** I am prompted for Due Date, **When** I enter `2026-01-20`, **Then** the task has due date set.

8. **Given** I am prompted for Due Date, **When** I enter `2026-01-20 09:00`, **Then** the task has both due date and time set.

9. **Given** I am prompted for Recurring, **When** I enter `1`, **Then** the task is set to Daily recurring.

10. **Given** I am prompted for Recurring, **When** I enter `2`, **Then** the task is set to Weekly recurring.

11. **Given** I am prompted for Recurring, **When** I enter `3`, **Then** the task is set to Monthly recurring.

12. **Given** I am prompted for Recurring, **When** I press Enter without input, **Then** the task has no recurring (None).

13. **Given** I complete all prompts, **When** the task is created, **Then** I see "Task added successfully! ID: [id]" with separation lines.

14. **Given** I am prompted for Title, **When** I press Enter without input, **Then** I see "Error: Task title cannot be empty".

---

### User Story 2 - View All Tasks with Visual Indicators (Priority: P1)

As a user, I want to see all my tasks displayed with clear visual indicators for status, priority, category, due date/time, and recurring settings so that I can quickly understand my task list at a glance.

**Why this priority**: Viewing tasks is essential for any task manager. Combined with US1, this forms the MVP.

**Independent Test**: Add multiple tasks with different attributes, select menu option 2, and verify all information displays with correct formatting.

**Acceptance Scenarios**:

1. **Given** the main menu is displayed, **When** I select `2` (View All Tasks), **Then** all tasks are displayed with visual indicators.

2. **Given** tasks exist with various priorities, **When** I view tasks, **Then** each task shows `[H]`, `[M]`, or `[L]` indicator for High, Medium, or Low priority.

3. **Given** tasks exist with categories, **When** I view tasks, **Then** each task shows its category in brackets like `[Work]` or `[Personal]`.

4. **Given** tasks exist with due dates, **When** I view tasks, **Then** each task shows the due date in `YYYY-MM-DD` format and time in `HH:MM` format if set.

5. **Given** recurring tasks exist, **When** I view tasks, **Then** recurring tasks show indicator `(Daily)`, `(Weekly)`, or `(Monthly)`.

6. **Given** no tasks exist, **When** I view tasks, **Then** message "Your task list is empty" is displayed.

7. **Given** tasks exist, **When** I view tasks, **Then** the display uses separation lines and format:
   ```
   ----------------------------------------
   [ID] [Status] [Priority] [Category] Title
        Due: YYYY-MM-DD HH:MM | Recurring: type
        Description text
   ----------------------------------------
   ```

---

### User Story 3 - Numeric Menu on Startup (Priority: P1)

As a user, I want to see a numbered menu with all options when the app starts so that I can navigate by entering a number instead of typing commands.

**Why this priority**: Essential for user onboarding. The numeric menu is more intuitive than text commands.

**Independent Test**: Start the app and verify the numbered menu (1-8) is displayed with all options.

**Acceptance Scenarios**:

1. **Given** I launch the application, **When** the app starts, **Then** I see the header with separation lines and numbered menu 1-8.

2. **Given** the menu is displayed, **When** I enter `1`, **Then** I enter the Add Task flow.

3. **Given** the menu is displayed, **When** I enter `8`, **Then** the application exits.

4. **Given** I complete any operation, **When** the operation finishes, **Then** the main menu is displayed again.

5. **Given** the menu is displayed, **When** I enter `9` or any invalid number, **Then** I see "Error: Invalid choice. Please enter a number between 1 and 8".

6. **Given** the menu is displayed, **When** I enter `abc`, **Then** I see "Error: Invalid choice. Please enter a number between 1 and 8".

---

### User Story 4 - Update Task via Interactive Prompts (Priority: P2)

As a user, I want to update any attribute of an existing task through guided prompts so that I can easily modify task details.

**Why this priority**: Important for task management flexibility. Depends on US1 for tasks to exist.

**Independent Test**: Create a task, select menu option 3, follow prompts to update attributes, and verify changes persist.

**Acceptance Scenarios**:

1. **Given** the main menu is displayed, **When** I select `3` (Update Task), **Then** I am prompted to enter Task ID.

2. **Given** I entered a valid Task ID, **When** the task is found, **Then** I see the current task details and a submenu of fields to update.

3. **Given** the update submenu is displayed, **When** I select a field, **Then** I am prompted to enter the new value.

4. **Given** I am updating priority, **When** I enter `1`, `2`, or `3`, **Then** the priority is updated to High, Medium, or Low respectively.

5. **Given** I am updating category, **When** I enter a new category name, **Then** the category is updated.

6. **Given** I am updating recurring, **When** I enter `1`, `2`, or `3`, **Then** the recurring is set to Daily, Weekly, or Monthly.

7. **Given** I enter a non-existent Task ID, **When** the system searches, **Then** I see "Error: Task [ID] not found".

---

### User Story 5 - Delete Task (Priority: P2)

As a user, I want to delete tasks that are no longer needed so that I can keep my task list clean.

**Why this priority**: Standard CRUD operation. Important for task list maintenance.

**Independent Test**: Create a task, select menu option 4, enter the ID, and verify the task is removed.

**Acceptance Scenarios**:

1. **Given** the main menu is displayed, **When** I select `4` (Delete Task), **Then** I am prompted to enter Task ID.

2. **Given** a task with ID 1 exists, **When** I enter `1`, **Then** the task is removed and I see "Task [1] deleted successfully".

3. **Given** I enter `999`, **When** task 999 doesn't exist, **Then** I see "Error: Task [999] not found".

4. **Given** I am prompted for Task ID, **When** I enter `abc`, **Then** I see "Error: Task ID must be a number".

---

### User Story 6 - Toggle Task Completion with Auto-Recurring (Priority: P2)

As a user, I want to toggle task status between Pending and Complete, and for recurring tasks, I want the system to automatically create the next occurrence.

**Why this priority**: Core task management functionality. Recurring automation saves user effort.

**Independent Test**: Create a recurring task, select menu option 5, toggle it complete, and verify new task is auto-created.

**Acceptance Scenarios**:

1. **Given** the main menu is displayed, **When** I select `5` (Toggle Task Completion), **Then** I am prompted to enter Task ID.

2. **Given** a pending non-recurring task exists, **When** I toggle it, **Then** the status changes to Complete `[X]`.

3. **Given** a completed task exists, **When** I toggle it, **Then** the status changes to Pending `[ ]`.

4. **Given** a daily recurring task with due date 2026-01-16 is pending, **When** I mark it complete, **Then** the original shows Complete AND a new Pending task is created with due date 2026-01-17.

5. **Given** a weekly recurring task with due date 2026-01-16 is pending, **When** I mark it complete, **Then** a new Pending task is created with due date 2026-01-23.

6. **Given** a monthly recurring task with due date 2026-01-16 is pending, **When** I mark it complete, **Then** a new Pending task is created with due date 2026-02-16.

7. **Given** a recurring task creates a new occurrence, **When** the toggle completes, **Then** I see "New recurring task created: [new_id]".

8. **Given** a completed recurring task exists, **When** I toggle it back to pending, **Then** no new task is created (only toggles status).

---

### User Story 7 - Search / Filter Tasks (Priority: P3)

As a user, I want to filter my task list by category, priority, or status so that I can focus on specific subsets of tasks.

**Why this priority**: Enhances usability for users with many tasks. Depends on US2 for task display.

**Independent Test**: Create tasks with various attributes, select menu option 6, apply filters, and verify correct subset shown.

**Acceptance Scenarios**:

1. **Given** the main menu is displayed, **When** I select `6` (Search / Filter Tasks), **Then** I see a filter submenu.

2. **Given** the filter submenu is displayed, **When** I select `1` (By Category), **Then** I am prompted to enter a category name.

3. **Given** I filter by category "Work", **When** tasks with category "Work" exist, **Then** only those tasks are displayed.

4. **Given** the filter submenu is displayed, **When** I select `2` (By Priority), **Then** I am prompted to enter priority (1/2/3).

5. **Given** I filter by priority `1` (High), **When** high priority tasks exist, **Then** only High priority tasks are displayed.

6. **Given** the filter submenu is displayed, **When** I select `3` (By Status), **Then** I am prompted to select Pending or Complete.

7. **Given** I filter by status "pending", **When** pending tasks exist, **Then** only pending tasks are displayed.

8. **Given** I apply a filter, **When** no tasks match, **Then** I see "No tasks match your filter criteria".

9. **Given** the filter submenu is displayed, **When** I select `4` (Back to Main Menu), **Then** I return to the main menu.

---

### User Story 8 - Sort Tasks (Priority: P3)

As a user, I want to sort my task list by due date or priority so that I can view tasks in a meaningful order.

**Why this priority**: Improves task organization. Lower priority as basic list view is sufficient for MVP.

**Independent Test**: Create tasks with different due dates and priorities, select menu option 7, apply sort, and verify correct order.

**Acceptance Scenarios**:

1. **Given** the main menu is displayed, **When** I select `7` (Sort Tasks), **Then** I see a sort submenu.

2. **Given** the sort submenu is displayed, **When** I select `1` (By Due Date), **Then** tasks are displayed sorted by due date ascending.

3. **Given** I sort by due date, **When** some tasks have no due date, **Then** tasks without due dates appear at the end.

4. **Given** the sort submenu is displayed, **When** I select `2` (By Priority), **Then** tasks are displayed sorted High → Medium → Low.

5. **Given** the sort submenu is displayed, **When** I select `3` (Back to Main Menu), **Then** I return to the main menu.

---

### User Story 9 - Exit Application (Priority: P1)

As a user, I want to exit the application cleanly when I'm done.

**Why this priority**: Basic application control - users must be able to exit.

**Independent Test**: Select menu option 8 and verify the application exits.

**Acceptance Scenarios**:

1. **Given** the main menu is displayed, **When** I select `8` (Exit), **Then** the application displays "Goodbye!" and exits.

---

### Edge Cases

- What happens when a monthly recurring task has due date Jan 31 and next month has fewer days? (Use last day of month)
- What happens when user enters date in wrong format (e.g., 01-16-2026)? (Show error: "Invalid date format. Use YYYY-MM-DD or YYYY-MM-DD HH:MM")
- What happens when due time is set without due date? (Allow it - time without date is valid)
- What happens when filtering/sorting returns no results? (Show "No tasks match your filter criteria")
- What happens when marking a completed recurring task as pending? (Toggle status only, don't create new task)
- What happens when user enters invalid priority number like 4? (Show error: "Invalid priority. Enter 1 (High), 2 (Medium), or 3 (Low)")
- What happens when user enters invalid recurring number like 5? (Show error: "Invalid recurring. Enter 1 (Daily), 2 (Weekly), 3 (Monthly), or press Enter to skip")

## Requirements *(mandatory)*

### Functional Requirements

#### Menu System
- **FR-001**: System MUST display a numbered main menu (1-8) on startup
- **FR-002**: System MUST redisplay the main menu after each operation completes
- **FR-003**: System MUST validate menu choices are integers between 1-8
- **FR-004**: System MUST use separation lines (40 chars of `=` or `-`) for visual clarity

#### Task Creation (Interactive Flow)
- **FR-005**: System MUST prompt for attributes in order: Title → Description → Priority → Category → Due Date → Recurring
- **FR-006**: System MUST require a non-empty title
- **FR-007**: System MUST allow optional description (Enter to skip)
- **FR-008**: System MUST accept priority as 1 (High), 2 (Medium), 3 (Low) with default 2
- **FR-009**: System MUST allow optional category (free text, Enter to skip)
- **FR-010**: System MUST accept due date in YYYY-MM-DD or YYYY-MM-DD HH:MM format
- **FR-011**: System MUST accept recurring as 1 (Daily), 2 (Weekly), 3 (Monthly), Enter for None
- **FR-012**: System MUST auto-generate unique sequential integer IDs for tasks

#### Task Display
- **FR-013**: System MUST display status indicator: `[ ]` for Pending, `[X]` for Complete
- **FR-014**: System MUST display priority indicator: `[H]` High, `[M]` Medium, `[L]` Low
- **FR-015**: System MUST display category in brackets when set (e.g., `[Work]`)
- **FR-016**: System MUST display due date and time when set
- **FR-017**: System MUST display recurring indicator when set: `(Daily)`, `(Weekly)`, `(Monthly)`
- **FR-018**: System MUST display description on a separate indented line when present

#### Task Operations
- **FR-019**: System MUST allow toggling task status between Pending and Complete
- **FR-020**: System MUST auto-create next occurrence when recurring task is marked Complete (from Pending only)
- **FR-021**: System MUST advance due date by appropriate interval (1 day / 7 days / 1 month) for recurring tasks
- **FR-022**: System MUST allow updating any single task attribute via submenu
- **FR-023**: System MUST allow deleting tasks by ID

#### Filtering
- **FR-024**: System MUST support filtering by category (exact match)
- **FR-025**: System MUST support filtering by priority (1/2/3 input)
- **FR-026**: System MUST support filtering by status (pending/complete)
- **FR-027**: System MUST display filter submenu with options 1-4

#### Sorting
- **FR-028**: System MUST support sorting by due date (ascending, nulls last)
- **FR-029**: System MUST support sorting by priority (High → Medium → Low)
- **FR-030**: System MUST display sort submenu with options 1-3

#### Data Validation
- **FR-031**: System MUST reject empty or whitespace-only titles
- **FR-032**: System MUST validate date format as YYYY-MM-DD or YYYY-MM-DD HH:MM
- **FR-033**: System MUST validate priority values (1, 2, or 3 only)
- **FR-034**: System MUST validate recurring values (1, 2, 3, or empty only)
- **FR-035**: System MUST validate menu choices with helpful error messages
- **FR-036**: System MUST handle non-existent task IDs with clear error messages

### Key Entities

- **Task**: Represents a todo item with:
  - id (unique integer)
  - title (required string)
  - description (optional string)
  - status (Pending/Complete)
  - priority (High=1/Medium=2/Low=3)
  - category (optional string)
  - due_date (optional date)
  - due_time (optional time)
  - recurring (None/Daily=1/Weekly=2/Monthly=3)
  - created_at (timestamp)

- **Status**: Enumeration of task completion states (Pending, Complete)

- **Priority**: Enumeration of task importance levels (High=1, Medium=2, Low=3)

- **Recurrence**: Enumeration of recurring patterns (None, Daily=1, Weekly=2, Monthly=3)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can add a task with all attributes through guided prompts in under 30 seconds
- **SC-002**: Task list displays all task information clearly with visual indicators and separation lines
- **SC-003**: Users can navigate all features using only number keys (1-8) without typing commands
- **SC-004**: Users can identify task priority, status, and category at a glance using visual indicators
- **SC-005**: Recurring tasks automatically create next occurrence 100% of the time when marked complete
- **SC-006**: All filter options return accurate results with zero false positives/negatives
- **SC-007**: Sort by due date places tasks in correct chronological order with dateless tasks at end
- **SC-008**: Sort by priority places tasks in correct order (High → Medium → Low)
- **SC-009**: Invalid inputs produce helpful error messages that guide users to correct input
- **SC-010**: All submenus include a "Back to Main Menu" option for easy navigation
- **SC-011**: Date calculations for monthly recurring tasks handle month-end edge cases correctly

## Assumptions

- In-memory storage only - all data is lost when application exits
- Single user environment - no concurrent access considerations
- Command-line interface only - no graphical UI
- Python standard library datetime module handles all date/time operations
- 24-hour time format for consistency and unambiguous input
- Tasks are displayed in ID order by default (creation order)
- No timezone handling - all times are local
- Category is free-form text (not predefined list)
- Separation lines are 40 characters wide using `=` or `-`
