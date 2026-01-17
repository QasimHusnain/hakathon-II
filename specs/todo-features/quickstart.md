# Quickstart: Enhanced Todo CLI with Refined UI

**Feature**: todo-features
**Updated**: 2026-01-17

## Installation

```bash
# Clone repository
git clone <repo-url>
cd hakathon-todo

# Install with uv
uv sync

# Run application
uv run python main.py
```

## Quick Demo

### 1. Start the Application

```bash
$ uv run python main.py

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

### 2. Add Your First Task (Option 1)

```
Enter your choice (1-8): 1

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

### 3. Add Another Task

```
Enter your choice (1-8): 1

--- Add New Task ---
Title: Team meeting
Description (press Enter to skip): Weekly standup with the team
Priority (1=High, 2=Medium, 3=Low) [2]: 1
Category (press Enter to skip): Work
Due Date (YYYY-MM-DD or YYYY-MM-DD HH:MM, press Enter to skip): 2026-01-18 09:00
Recurring (1=Daily, 2=Weekly, 3=Monthly, press Enter to skip): 2
----------------------------------------
Task added successfully! ID: 2
```

### 4. View All Tasks (Option 2)

```
Enter your choice (1-8): 2

========================================
              ALL TASKS
========================================
[1] [ ] [H] [Shopping] Buy groceries
     Due: 2026-01-20 | Recurring: Weekly
     Milk, bread, eggs
----------------------------------------
[2] [ ] [H] [Work] Team meeting
     Due: 2026-01-18 09:00 | Recurring: Weekly
     Weekly standup with the team
----------------------------------------

Total: 2 task(s)
========================================
```

### 5. Complete a Recurring Task (Option 5)

```
Enter your choice (1-8): 5

--- Toggle Task Completion ---
Enter Task ID: 2

Task [2] marked as complete.
New recurring task created: [3]
```

### 6. Filter Tasks by Priority (Option 6)

```
Enter your choice (1-8): 6

--- Filter Tasks ---
1. By Category
2. By Priority
3. By Status
4. Back to Main Menu

Enter your choice (1-4): 2
Enter priority (1=High, 2=Medium, 3=Low): 1

========================================
         FILTERED TASKS
========================================
[1] [ ] [H] [Shopping] Buy groceries
     Due: 2026-01-20 | Recurring: Weekly
----------------------------------------
[3] [ ] [H] [Work] Team meeting
     Due: 2026-01-25 09:00 | Recurring: Weekly
----------------------------------------

Found: 2 task(s) matching filter
========================================
```

### 7. Sort Tasks by Due Date (Option 7)

```
Enter your choice (1-8): 7

--- Sort Tasks ---
1. By Due Date (ascending)
2. By Priority (High → Low)
3. Back to Main Menu

Enter your choice (1-3): 1

========================================
         SORTED TASKS
========================================
[1] [ ] [H] [Shopping] Buy groceries
     Due: 2026-01-20 | Recurring: Weekly
----------------------------------------
[3] [ ] [H] [Work] Team meeting
     Due: 2026-01-25 09:00 | Recurring: Weekly
----------------------------------------
[2] [X] [H] [Work] Team meeting
     (no due date)
----------------------------------------

Total: 3 task(s) (sorted by due date)
========================================
```

### 8. Update a Task (Option 3)

```
Enter your choice (1-8): 3

--- Update Task ---
Enter Task ID: 1

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

Enter your choice (1-7): 2
New description: Milk, bread, eggs, cheese, yogurt

Task [1] updated successfully.
```

### 9. Delete a Task (Option 4)

```
Enter your choice (1-8): 4

--- Delete Task ---
Enter Task ID: 2

Task to delete:
[2] [X] [H] [Work] Team meeting

Are you sure you want to delete this task? (y/n): y

Task [2] deleted successfully.
```

### 10. Exit (Option 8)

```
Enter your choice (1-8): 8

Goodbye!
```

## Menu Summary

| Option | Feature | Description |
|--------|---------|-------------|
| 1 | Add Task | Interactive prompts for new task |
| 2 | View All Tasks | Display all tasks with indicators |
| 3 | Update Task | Modify task attributes |
| 4 | Delete Task | Remove task by ID |
| 5 | Toggle Completion | Mark complete/pending |
| 6 | Filter Tasks | Filter by category, priority, status |
| 7 | Sort Tasks | Sort by due date or priority |
| 8 | Exit | Quit application |

## Task Attribute Input

| Attribute | Input Format | Example |
|-----------|--------------|---------|
| Title | Any text | `Buy groceries` |
| Description | Any text or Enter to skip | `Milk, bread, eggs` |
| Priority | 1 (High), 2 (Medium), 3 (Low) | `1` |
| Category | Any text or Enter to skip | `Shopping` |
| Due Date | YYYY-MM-DD or YYYY-MM-DD HH:MM | `2026-01-20 09:00` |
| Recurring | 1 (Daily), 2 (Weekly), 3 (Monthly) | `2` |

## Visual Indicators

| Indicator | Meaning |
|-----------|---------|
| `[ ]` | Pending task |
| `[X]` | Completed task |
| `[H]` | High priority |
| `[M]` | Medium priority |
| `[L]` | Low priority |
| `[Category]` | Task category |
| `(Daily)` | Daily recurring |
| `(Weekly)` | Weekly recurring |
| `(Monthly)` | Monthly recurring |

## Error Handling Examples

```
Enter your choice (1-8): 9
Error: Invalid choice. Please enter a number between 1 and 8

Title:
Error: Task title cannot be empty

Priority (1=High, 2=Medium, 3=Low) [2]: 5
Error: Invalid priority. Enter 1 (High), 2 (Medium), or 3 (Low)

Due Date (YYYY-MM-DD or YYYY-MM-DD HH:MM, press Enter to skip): 01-20-2026
Error: Invalid date format. Use YYYY-MM-DD or YYYY-MM-DD HH:MM

Enter Task ID: abc
Error: Task ID must be a number

Enter Task ID: 999
Error: Task [999] not found
```

## Notes

- All data is stored in memory and will be lost when the application exits
- Task IDs are sequential and never reused
- Recurring tasks automatically create the next occurrence when completed (from pending status only)
- 24-hour time format is used (e.g., 14:30 for 2:30 PM)
- Separation lines are 40 characters wide for consistent formatting
- Filter and Sort options include "Back to Main Menu" for easy navigation
