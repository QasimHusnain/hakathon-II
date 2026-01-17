<!--
  SYNC IMPACT REPORT
  ==================
  Version Change: 2.0.0 → 2.2.0 (MINOR)

  Modified Sections:
  - III. Phase I Functional Requirements: Added Category field, Sort functionality, Recurring
  - III.A. Core Features: Updated Add Task (includes Recurring), View All (includes Recurring indicator),
    Update Task (includes Recurring), Toggle Completion (auto-recurring)
  - III.C. Interactive Add Task Flow: Added Recurring prompt
  - III.D. Task Attribute Defaults: Added Category and Recurring
  - IV. Architectural Guardrails: Added new CLI UI Consistency section
  - NEW: VI. CLI User Interface Standards (separation lines, prompts, numeric menu)
  - NEW: VII. Input Validation Rules (date formats, integer choices, recurring values)
  - Data Model: Added Category field, Recurring field, Recurrence enum

  Added Sections:
  - VI. CLI User Interface Standards
  - VII. Input Validation Rules
  - Recurrence enum in Data Model
  - Interactive Add Task Flow with Recurring

  Removed Sections:
  - None

  Templates Updated:
  - specs/todo-features/spec.md ✅ updated (Category, Sort, Recurring)
  - specs/todo-features/data-model.md ✅ updated (Category, Recurring)
  - specs/todo-features/plan.md ⚠ pending (update roadmap)
  - specs/todo-features/tasks.md ⚠ pending (regenerate tasks)

  Follow-up TODOs:
  - Update plan.md with numeric menu transition roadmap
  - Regenerate tasks.md with file-based granularity
-->

# Todo In-Memory Python Console App - Constitution

**Phase I: Enhanced Functionality with Refined CLI**

## Core Principles

### I. Mission-Driven Scope
**Mission**: Build a command-line todo application that stores tasks in memory using Claude Code and Spec-Kit Plus, following the Spec-Driven Development (SDD) workflow.

**Development Approach**: Use the Agentic Dev Stack workflow: Write spec → Generate plan → Break into tasks → Implement via Claude Code. No manual coding allowed.

**Constraint**: Implement ONLY Phase I features. Do not implement web interfaces, AI agents, or database persistence.

### II. Technical Stack (NON-NEGOTIABLE)
- **Language**: Python 3.13+
- **Tooling**: Managed via `uv`. No external database drivers allowed.
- **Data Persistence**: Strictly In-Memory. Data is held in Python data structures (Lists/Dictionaries) and will clear upon exit.
- **Typing**: Mandatory use of `typing` module (Type Hints) for all function signatures.
- **Date/Time**: Use Python `datetime` module from standard library.

### III. Phase I Functional Requirements

#### A. Core Features (8 Pillars)

1. **Add Task**: Create task via interactive sequential prompts:
   - Title (required, non-empty)
   - Description (optional, press Enter to skip)
   - Priority: 1=High, 2=Medium, 3=Low (default: 2)
   - Category (optional, e.g., Work, Personal, Shopping)
   - Due Date (optional, format: YYYY-MM-DD or YYYY-MM-DD HH:MM)
   - Recurring: 1=Daily, 2=Weekly, 3=Monthly (optional, press Enter for None)

2. **View All Tasks**: Display all tasks with:
   - Task ID
   - Status indicator: `[ ]` pending, `[X]` complete
   - Priority indicator: `[H]` High, `[M]` Medium, `[L]` Low
   - Category (if set)
   - Title
   - Due date/time (if set)
   - Recurring indicator: `(Daily)`, `(Weekly)`, `(Monthly)` (if set)
   - Description (if present)

3. **Update Task**: Modify any task attribute via interactive prompts:
   - Title
   - Description
   - Priority
   - Category
   - Due Date
   - Recurring

4. **Delete Task**: Remove a task using its unique integer ID.

5. **Toggle Task Completion**: Toggle status between "Pending" and "Complete."
   - For recurring tasks marked complete: Auto-create next occurrence with advanced due date

6. **Search / Filter Tasks**: View tasks filtered by:
   - Category (exact match)
   - Priority (1=High, 2=Medium, 3=Low)
   - Status (pending/complete)

7. **Sort Tasks**: Order tasks by:
   - Due Date (ascending, tasks without dates at end)
   - Priority (High → Medium → Low)

8. **Exit**: Quit the application with confirmation.

#### B. Numeric Menu System

The application MUST present a numbered menu on startup:

```
========================================
         TODO TASK MANAGER
========================================

1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Toggle Task Completion
6. Search / Filter Tasks
7. Sort Tasks
8. Exit

========================================
Enter your choice (1-8):
```

#### C. Interactive Add Task Flow

When user selects "1. Add Task", the system MUST prompt sequentially:

```
--- Add New Task ---
Title: [user input]
Description (press Enter to skip): [user input]
Priority (1=High, 2=Medium, 3=Low) [2]: [user input]
Category (press Enter to skip): [user input]
Due Date (YYYY-MM-DD or YYYY-MM-DD HH:MM, press Enter to skip): [user input]
Recurring (1=Daily, 2=Weekly, 3=Monthly, press Enter to skip): [user input]
----------------------------------------
Task added successfully! ID: [generated_id]
```

#### D. Task Attribute Defaults

| Attribute   | Required | Default Value |
|-------------|----------|---------------|
| Title       | Yes      | -             |
| Description | No       | None          |
| Priority    | No       | Medium (2)    |
| Category    | No       | None          |
| Due Date    | No       | None          |
| Recurring   | No       | None          |
| Status      | Auto     | Pending       |

### IV. Architectural Guardrails

- **Clean CLI**: Output must be formatted for readability with clear indicators and separation lines.
- **Numeric Menu**: Use numbered options (1-8) instead of text commands.
- **Feature Menu**: Show numbered menu on startup and after each operation.
- **Separation of Concerns**: Keep the `TaskManager` class (logic) separate from the `cli_loop` (IO).
- **Error Handling**: Must handle:
  - `ValueError` for non-integer ID inputs
  - `TaskNotFoundError` for missing IDs
  - `InvalidTaskDataError` for validation failures
  - Invalid date/time formats
  - Invalid priority values (not 1, 2, or 3)
  - Invalid menu choices (not 1-8)

### V. SDD Workflow Rule
**Reference Mandatory**: Every function generated by Claude Code must include a docstring comment referencing the speckit.tasks ID it satisfies.

### VI. CLI User Interface Standards

#### A. Separation Lines
- Use `========================================` (40 chars) for major section headers
- Use `----------------------------------------` (40 chars) for subsection dividers
- Use `---` for inline separators within outputs

#### B. Standard Prompt Formats
- Menu choice: `Enter your choice (1-8): `
- Task ID input: `Enter Task ID: `
- Confirmation: `Are you sure? (y/n): `
- Field input: `[FieldName]: ` or `[FieldName] (default): `

#### C. Success/Error Messages
- Success: Prefix with `✓` or clear success text
- Error: Prefix with `Error:` followed by helpful message
- Info: No prefix, just clear text

#### D. Task Display Format
```
[ID] [Status] [Priority] [Category] Title
     Due: YYYY-MM-DD HH:MM
     Description text (if present)
```

### VII. Input Validation Rules

#### A. Date Formats (MUST validate)
- Date only: `YYYY-MM-DD` (e.g., 2026-01-20)
- Date with time: `YYYY-MM-DD HH:MM` (e.g., 2026-01-20 09:00)
- Invalid format: Show `Error: Invalid date format. Use YYYY-MM-DD or YYYY-MM-DD HH:MM`

#### B. Priority Values (MUST validate)
- Valid: 1 (High), 2 (Medium), 3 (Low)
- Invalid: Show `Error: Invalid priority. Enter 1 (High), 2 (Medium), or 3 (Low)`
- Empty input: Default to 2 (Medium)

#### C. Menu Choices (MUST validate)
- Valid: Integers 1-8
- Invalid: Show `Error: Invalid choice. Please enter a number between 1 and 8`

#### D. Task ID (MUST validate)
- Valid: Positive integer matching existing task
- Non-integer: Show `Error: Task ID must be a number`
- Not found: Show `Error: Task [ID] not found`

#### E. Empty/Whitespace Title (MUST reject)
- Show `Error: Task title cannot be empty`

## Code Quality Standards

### Testing Requirements
- All core functionality must be testable
- Error paths must have explicit test cases
- Type hints enable static analysis via mypy
- Date/time edge cases must be tested
- Validation edge cases must be tested

### Error Handling
- User input validation for all CLI prompts
- Graceful degradation for invalid operations
- Clear error messages to stdout/stderr
- Date/time format validation with helpful messages
- Priority/menu choice validation with valid options shown

### Code Organization
- Single responsibility principle for classes and functions
- Type hints on all function signatures
- Docstrings with task ID references
- Enums for Priority, Status, Recurrence, and Category

## Data Model

### Task Entity
```python
@dataclass
class Task:
    id: int                          # Unique identifier
    title: str                       # Required, non-empty
    status: Status                   # PENDING | COMPLETE
    priority: Priority               # HIGH | MEDIUM | LOW
    category: Optional[str]          # Optional category label
    description: Optional[str]       # Optional details
    due_date: Optional[date]         # Optional due date
    due_time: Optional[time]         # Optional due time
    recurring: Recurrence            # NONE | DAILY | WEEKLY | MONTHLY
    created_at: datetime             # Auto-set on creation
```

### Enumerations
```python
class Status(Enum):
    PENDING = "pending"
    COMPLETE = "complete"

class Priority(Enum):
    HIGH = 1       # Display as [H]
    MEDIUM = 2     # Display as [M]
    LOW = 3        # Display as [L]

class Recurrence(Enum):
    NONE = 0       # One-time task (default)
    DAILY = 1      # Display as (Daily)
    WEEKLY = 2     # Display as (Weekly)
    MONTHLY = 3    # Display as (Monthly)
```

## CLI Menu Structure

| # | Menu Item | Description |
|---|-----------|-------------|
| 1 | Add Task | Interactive prompts for new task |
| 2 | View All Tasks | Display all tasks with indicators |
| 3 | Update Task | Modify task attributes |
| 4 | Delete Task | Remove task by ID |
| 5 | Toggle Task Completion | Change pending ↔ complete |
| 6 | Search / Filter Tasks | Filter by category, priority, status |
| 7 | Sort Tasks | Order by due date or priority |
| 8 | Exit | Quit application |

### Filter Submenu (Option 6)
```
--- Filter Tasks ---
1. By Category
2. By Priority
3. By Status
4. Back to Main Menu
Enter your choice (1-4):
```

### Sort Submenu (Option 7)
```
--- Sort Tasks ---
1. By Due Date (ascending)
2. By Priority (High → Low)
3. Back to Main Menu
Enter your choice (1-3):
```

## Development Workflow

### SDD Process
1. **Spec First**: Define requirements in `specs/<feature>/spec.md`
2. **Plan Next**: Architecture decisions in `specs/<feature>/plan.md`
3. **Tasks Then**: Testable tasks in `specs/<feature>/tasks.md`
4. **Implement Last**: Code with task ID references in docstrings

### Prompt History Records (PHR)
- Every user interaction must generate a PHR
- PHRs stored in `history/prompts/` with appropriate routing
- Constitution changes go to `history/prompts/constitution/`

### Architecture Decision Records (ADR)
- Suggest ADRs for architecturally significant decisions
- Wait for user consent before creating
- Store in `history/adr/`

## Deliverables

### Repository Structure
- Constitution file (`.specify/memory/constitution.md`)
- Specs history folder containing all specification files (`specs/`)
- `/src` folder with Python source code
- `README.md` with setup instructions
- `CLAUDE.md` with Claude Code instructions

### Working Console Application
- Numeric menu displayed on startup (1-8)
- Interactive Add Task flow with sequential prompts
- Viewing all tasks with visual indicators
- Filtering tasks by category, priority, status
- Sorting tasks by due date or priority
- Updating any task attribute
- Deleting tasks by ID
- Toggling task completion status
- Clean separation lines and consistent formatting

## Governance

- This constitution supersedes all other development practices
- All code must comply with the 8 functional requirements
- No features beyond Phase I scope
- All changes must reference SDD artifacts (spec/plan/tasks)
- PHR creation is mandatory after every user interaction

**Version**: 2.2.0 | **Ratified**: 2026-01-16 | **Last Amended**: 2026-01-17
