# CLI Interface Contract: Enhanced Todo CLI with Refined UI

**Feature**: todo-features
**Created**: 2026-01-16
**Updated**: 2026-01-17

## Menu System

### Main Menu

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

**Input**: Integer 1-8
**Error Output**: `Error: Invalid choice. Please enter a number between 1 and 8`

---

## Menu Option 1: Add Task

### Interactive Flow

```
--- Add New Task ---
Title: [user input - required]
Description (press Enter to skip): [user input - optional]
Priority (1=High, 2=Medium, 3=Low) [2]: [user input - 1/2/3 or Enter for default]
Category (press Enter to skip): [user input - optional]
Due Date (YYYY-MM-DD or YYYY-MM-DD HH:MM, press Enter to skip): [user input - optional]
Recurring (1=Daily, 2=Weekly, 3=Monthly, press Enter to skip): [user input - 1/2/3 or Enter]
----------------------------------------
Task added successfully! ID: [generated_id]
```

### Validation

| Field | Required | Valid Input | Error Message |
|-------|----------|-------------|---------------|
| Title | Yes | Non-empty string | `Error: Task title cannot be empty` |
| Description | No | Any string | N/A |
| Priority | No | 1, 2, 3, or empty | `Error: Invalid priority. Enter 1 (High), 2 (Medium), or 3 (Low)` |
| Category | No | Any string | N/A |
| Due Date | No | YYYY-MM-DD or YYYY-MM-DD HH:MM | `Error: Invalid date format. Use YYYY-MM-DD or YYYY-MM-DD HH:MM` |
| Recurring | No | 1, 2, 3, or empty | `Error: Invalid recurring. Enter 1 (Daily), 2 (Weekly), 3 (Monthly), or press Enter to skip` |

### Example Session

```
--- Add New Task ---
Title: Buy groceries
Description (press Enter to skip): Milk, bread, eggs
Priority (1=High, 2=Medium, 3=Low) [2]: 1
Category (press Enter to skip): Shopping
Due Date (YYYY-MM-DD or YYYY-MM-DD HH:MM, press Enter to skip): 2026-01-20
Recurring (1=Daily, 2=Weekly, 3=Monthly, press Enter to skip): 2
----------------------------------------
Task added successfully! ID: 1
```

---

## Menu Option 2: View All Tasks

### Output Format

```
========================================
              ALL TASKS
========================================
[1] [ ] [H] [Shopping] Buy groceries
     Due: 2026-01-20 | Recurring: Weekly
     Milk, bread, eggs
----------------------------------------
[2] [X] [M] [Work] Complete report
     Due: 2026-01-18 14:00
     Quarterly sales report
----------------------------------------
[3] [ ] [L] Call mom
----------------------------------------

Total: 3 task(s)
========================================
```

### Empty List Output

```
========================================
              ALL TASKS
========================================
Your task list is empty.
========================================
```

### Display Components

| Component | Format | Condition |
|-----------|--------|-----------|
| ID | `[n]` | Always |
| Status | `[ ]` or `[X]` | Always |
| Priority | `[H]`, `[M]`, `[L]` | Always |
| Category | `[CategoryName]` | If set |
| Title | Plain text | Always |
| Due line | `Due: YYYY-MM-DD HH:MM` | If date/time set |
| Recurring | `Recurring: Daily/Weekly/Monthly` | If recurring |
| Description | Indented text | If present |

---

## Menu Option 3: Update Task

### Interactive Flow

```
--- Update Task ---
Enter Task ID: [user input]

Current Task:
[1] [ ] [H] [Shopping] Buy groceries
     Due: 2026-01-20 | Recurring: Weekly
     Milk, bread, eggs

Select field to update:
1. Title
2. Description
3. Priority
4. Category
5. Due Date
6. Recurring
7. Back to Main Menu

Enter your choice (1-7): [user input]
```

### Field Update Prompts

| Field | Prompt | Validation |
|-------|--------|------------|
| Title | `New title: ` | Non-empty |
| Description | `New description: ` | Any string |
| Priority | `New priority (1=High, 2=Medium, 3=Low): ` | 1, 2, or 3 |
| Category | `New category: ` | Any string |
| Due Date | `New due date (YYYY-MM-DD or YYYY-MM-DD HH:MM): ` | Valid format |
| Recurring | `New recurring (1=Daily, 2=Weekly, 3=Monthly, 0=None): ` | 0, 1, 2, or 3 |

### Success/Error Output

```
Task [ID] updated successfully.
```

```
Error: Task [ID] not found
Error: Task ID must be a number
```

---

## Menu Option 4: Delete Task

### Interactive Flow

```
--- Delete Task ---
Enter Task ID: [user input]

Task to delete:
[1] [ ] [H] [Shopping] Buy groceries

Are you sure you want to delete this task? (y/n): [user input]
```

### Output

```
Task [1] deleted successfully.
```

```
Delete cancelled.
```

```
Error: Task [ID] not found
Error: Task ID must be a number
```

---

## Menu Option 5: Toggle Task Completion

### Interactive Flow

```
--- Toggle Task Completion ---
Enter Task ID: [user input]
```

### Output (Non-Recurring)

```
Task [1] marked as complete.
```
or
```
Task [1] marked as pending.
```

### Output (Recurring, was pending)

```
Task [1] marked as complete.
New recurring task created: [2]
```

### Error Output

```
Error: Task [ID] not found
Error: Task ID must be a number
```

---

## Menu Option 6: Search / Filter Tasks

### Submenu

```
--- Filter Tasks ---
1. By Category
2. By Priority
3. By Status
4. Back to Main Menu

Enter your choice (1-4):
```

### Option 1: By Category

```
Enter category to filter: [user input]
```

### Option 2: By Priority

```
Enter priority (1=High, 2=Medium, 3=Low): [user input]
```

### Option 3: By Status

```
Select status:
1. Pending
2. Complete

Enter your choice (1-2): [user input]
```

### Filtered Results

```
========================================
         FILTERED TASKS
========================================
[1] [ ] [H] [Shopping] Buy groceries
     Due: 2026-01-20 | Recurring: Weekly
----------------------------------------

Found: 1 task(s) matching filter
========================================
```

### No Results

```
No tasks match your filter criteria.
```

---

## Menu Option 7: Sort Tasks

### Submenu

```
--- Sort Tasks ---
1. By Due Date (ascending)
2. By Priority (High → Low)
3. Back to Main Menu

Enter your choice (1-3):
```

### Sorted Output

```
========================================
         SORTED TASKS
========================================
[3] [ ] [H] [Work] Urgent meeting
     Due: 2026-01-18 09:00
----------------------------------------
[1] [ ] [H] [Shopping] Buy groceries
     Due: 2026-01-20
----------------------------------------
[2] [ ] [M] Call mom
----------------------------------------

Total: 3 task(s) (sorted by due date)
========================================
```

### Sort Order Notes

**By Due Date**:
- Tasks with dates sorted ascending (earliest first)
- Tasks without dates appear at the end

**By Priority**:
- High priority (1) first
- Medium priority (2) second
- Low priority (3) last

---

## Menu Option 8: Exit

### Output

```
Goodbye!
```

---

## Separation Lines

| Type | Characters | Usage |
|------|------------|-------|
| Major header | `========================================` (40 chars) | Menu headers, section boundaries |
| Subsection | `----------------------------------------` (40 chars) | Between tasks, within sections |
| Inline | `---` | Small dividers |

---

## Error Messages Reference

| Error | Message |
|-------|---------|
| Invalid menu choice | `Error: Invalid choice. Please enter a number between 1 and 8` |
| Invalid submenu choice | `Error: Invalid choice.` |
| Empty title | `Error: Task title cannot be empty` |
| Invalid priority | `Error: Invalid priority. Enter 1 (High), 2 (Medium), or 3 (Low)` |
| Invalid date format | `Error: Invalid date format. Use YYYY-MM-DD or YYYY-MM-DD HH:MM` |
| Invalid recurring | `Error: Invalid recurring. Enter 1 (Daily), 2 (Weekly), 3 (Monthly), or press Enter to skip` |
| Invalid task ID | `Error: Task ID must be a number` |
| Task not found | `Error: Task [ID] not found` |
