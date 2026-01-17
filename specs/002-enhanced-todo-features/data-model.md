# Data Model: Enhanced Todo CLI with Refined UI

**Feature**: 002-enhanced-todo-features
**Created**: 2026-01-16
**Updated**: 2026-01-17

## Entities

### Task

The core entity representing a todo item.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| id | int | Yes | Auto-generated | Unique sequential identifier |
| title | str | Yes | - | Task title (non-empty) |
| status | Status | Yes | PENDING | Completion state |
| priority | Priority | Yes | MEDIUM | Importance level (numeric input: 1/2/3) |
| category | Optional[str] | No | None | Task category (free text, e.g., Work, Personal) |
| description | Optional[str] | No | None | Additional details |
| due_date | Optional[date] | No | None | Target completion date |
| due_time | Optional[time] | No | None | Target completion time |
| recurring | Recurrence | Yes | NONE | Recurrence pattern (numeric input: 1/2/3) |
| created_at | datetime | Yes | Auto-generated | Creation timestamp |

**Validation Rules**:
- `id` must be positive integer
- `title` must be non-empty and not whitespace-only
- `priority` must be 1 (High), 2 (Medium), or 3 (Low)
- `category` is free-form text (no validation required)
- `due_date` format: YYYY-MM-DD or YYYY-MM-DD HH:MM
- `due_time` format: HH:MM (24-hour)
- `recurring` must be 1 (Daily), 2 (Weekly), 3 (Monthly), or empty (None)

**State Transitions**:
```
PENDING ←→ COMPLETE (via toggle_complete)
```

For recurring tasks when transitioning PENDING → COMPLETE:
- Original task becomes COMPLETE
- New task created with status PENDING
- New task has same title, description, priority, category, recurring
- New task has due_date advanced by recurrence interval

## Enumerations

### Status

Task completion state.

| Value | String | Indicator | Description |
|-------|--------|-----------|-------------|
| PENDING | "pending" | [ ] | Task not yet completed |
| COMPLETE | "complete" | [X] | Task finished |

### Priority

Task importance level.

| Value | Numeric | String | Indicator | Description |
|-------|---------|--------|-----------|-------------|
| HIGH | 1 | "high" | [H] | Urgent/important tasks |
| MEDIUM | 2 | "medium" | [M] | Normal priority (default) |
| LOW | 3 | "low" | [L] | Can wait, less urgent |

**User Input**: Enter 1 for High, 2 for Medium, 3 for Low. Press Enter for default (Medium).

### Recurrence

Task repetition pattern.

| Value | Numeric | String | Interval | Description |
|-------|---------|--------|----------|-------------|
| NONE | - | "none" | - | One-time task (default) |
| DAILY | 1 | "daily" | +1 day | Repeats every day |
| WEEKLY | 2 | "weekly" | +7 days | Repeats every week |
| MONTHLY | 3 | "monthly" | +1 month | Repeats every month |

**User Input**: Enter 1 for Daily, 2 for Weekly, 3 for Monthly. Press Enter for None.

**Monthly Edge Case**: When the current day exceeds days in next month (e.g., Jan 31 → Feb), use the last day of the target month.

## Relationships

```
TaskManager 1──────* Task
     │
     └── tasks: dict[int, Task]
     └── next_id: int
```

## Storage Structure

In-memory storage using Python dict:

```python
class TaskManager:
    tasks: dict[int, Task]  # id → Task mapping
    next_id: int            # Next available ID
```

**Operations**:
- Add: O(1) - dict insertion
- Get by ID: O(1) - dict lookup
- Get all: O(n) - values iteration
- Filter by category: O(n) - linear scan with string match
- Filter by priority: O(n) - linear scan
- Filter by status: O(n) - linear scan
- Sort by due_date: O(n log n) - sorted() with key
- Sort by priority: O(n log n) - sorted() with key
- Delete: O(1) - dict deletion
- Update: O(1) - dict lookup + field update

## Data Flow

### Add Task (Interactive Flow)
```
Display "--- Add New Task ---"
    ↓
Prompt "Title:" → Validate non-empty → Store
    ↓
Prompt "Description (press Enter to skip):" → Store or None
    ↓
Prompt "Priority (1=High, 2=Medium, 3=Low) [2]:" → Validate 1/2/3 or default → Store
    ↓
Prompt "Category (press Enter to skip):" → Store or None
    ↓
Prompt "Due Date (YYYY-MM-DD or YYYY-MM-DD HH:MM, press Enter to skip):" → Validate format → Store
    ↓
Prompt "Recurring (1=Daily, 2=Weekly, 3=Monthly, press Enter to skip):" → Validate 1/2/3 or None → Store
    ↓
Create Task → Assign next_id → Store in dict → Display success
```

### Complete Task (Recurring)
```
Prompt "Enter Task ID:" → Parse int → Get Task → Validate exists
    ↓
Toggle status (PENDING ↔ COMPLETE)
    ↓
If recurring and was PENDING:
    → Create new Task with:
        - Same title, description, priority, category, recurring
        - Advanced due_date
        - Status = PENDING
    → Store new Task
    → Display "New recurring task created: [new_id]"
    ↓
Return to main menu
```

### Filter Tasks
```
Display filter submenu (1-4)
    ↓
If 1 (Category): Prompt category → Filter tasks where task.category == input
If 2 (Priority): Prompt 1/2/3 → Filter tasks where task.priority == Priority(input)
If 3 (Status): Prompt pending/complete → Filter tasks where task.status == input
If 4: Return to main menu
    ↓
Display filtered tasks or "No tasks match your filter criteria"
```

### Sort Tasks
```
Display sort submenu (1-3)
    ↓
If 1 (Due Date): Sort tasks by due_date ascending, None values at end
If 2 (Priority): Sort tasks by priority value (1=High first, 3=Low last)
If 3: Return to main menu
    ↓
Display sorted tasks
```

## Task Display Format

```
----------------------------------------
[1] [ ] [H] [Work] Complete project report
     Due: 2026-01-20 17:00 | Recurring: Weekly
     Finish the quarterly report for management
----------------------------------------
[2] [X] [M] [Personal] Buy groceries
     Due: 2026-01-17
     Milk, bread, eggs
----------------------------------------
```

**Format Components**:
- `[ID]` - Task ID number
- `[ ]` or `[X]` - Status indicator (Pending/Complete)
- `[H]`, `[M]`, `[L]` - Priority indicator
- `[Category]` - Category label (only if set)
- Title - Task title
- Due line - Date/time and recurring info (only if set)
- Description line - Indented description (only if set)

## Migration from Previous Version

The existing Task dataclass needs extension for Category:

**Previous (002 v1)**:
```python
@dataclass
class Task:
    id: int
    title: str
    status: Status
    priority: Priority = Priority.MEDIUM
    description: Optional[str] = None
    due_date: Optional[date] = None
    due_time: Optional[time] = None
    recurring: Recurrence = Recurrence.NONE
    created_at: datetime = field(default_factory=datetime.now)
```

**Updated (002 v2 - with Category)**:
```python
@dataclass
class Task:
    id: int
    title: str
    status: Status
    priority: Priority = Priority.MEDIUM
    category: Optional[str] = None      # NEW FIELD
    description: Optional[str] = None
    due_date: Optional[date] = None
    due_time: Optional[time] = None
    recurring: Recurrence = Recurrence.NONE
    created_at: datetime = field(default_factory=datetime.now)
```

**Backward Compatibility**: New field has default, so existing code will continue to work.
