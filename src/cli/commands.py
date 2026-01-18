"""
CLI menu handlers for Todo CLI Enhanced.

Provides numeric menu-based interaction with interactive prompts.

Satisfies: specs/todo-features/tasks.md - T021-T081
"""

from typing import Optional
from src.services.task_manager import TaskManager
from src.models.task import InvalidTaskDataError, TaskNotFoundError, Status, Priority, Recurrence
from src.cli.formatter import (
    format_task, format_task_list, SEPARATOR_MAJOR, SEPARATOR_MINOR
)
from src.cli.parser import (
    validate_priority_input, validate_recurring_input,
    validate_date_input, validate_menu_choice
)


def display_main_menu() -> None:
    """
    Display the main menu with 8 options.

    Satisfies: specs/todo-features/tasks.md - T021, T022
    """
    print()
    print(SEPARATOR_MAJOR)
    print("         TODO TASK MANAGER")
    print(SEPARATOR_MAJOR)
    print()
    print("1. Add Task")
    print("2. View All Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Toggle Task Completion")
    print("6. Search / Filter Tasks")
    print("7. Sort Tasks")
    print("8. Exit")
    print()
    print(SEPARATOR_MAJOR)


def get_menu_choice() -> Optional[int]:
    """
    Get and validate menu choice from user (1-8).

    Returns:
        Valid integer 1-8, or None if invalid

    Satisfies: specs/todo-features/tasks.md - T023, T024
    """
    try:
        user_input = input("Enter your choice (1-8): ").strip()
        choice = validate_menu_choice(user_input, 1, 8)
        if choice is None:
            print("Error: Invalid choice. Please enter a number between 1 and 8")
        return choice
    except EOFError:
        return 8  # Exit on EOF


def handle_exit() -> None:
    """
    Handle exit option - print goodbye message.

    Satisfies: specs/todo-features/tasks.md - T028
    """
    print()
    print("Goodbye!")


def handle_add_task(manager: TaskManager) -> None:
    """
    Handle Add Task option with interactive prompts.

    Prompts: Title -> Description -> Priority -> Category -> Due Date -> Recurring

    Satisfies: specs/todo-features/tasks.md - T030-T038
    """
    print()
    print(f"--- Add New Task ---")

    # T031: Title prompt with validation
    while True:
        title = input("Title: ").strip()
        if title:
            break
        print("Error: Task title cannot be empty")

    # T032: Description prompt (optional)
    description_input = input("Description (press Enter to skip): ").strip()
    description: str | None = description_input if description_input else None

    # T033: Priority prompt with default
    priority = Priority.MEDIUM
    while True:
        priority_input = input("Priority (1=High, 2=Medium, 3=Low) [2]: ").strip()
        if not priority_input:
            break  # Use default
        validated = validate_priority_input(priority_input)
        if validated:
            priority = validated
            break
        print("Error: Invalid priority. Enter 1 (High), 2 (Medium), or 3 (Low)")

    # T034: Category prompt (optional)
    category_input = input("Category (press Enter to skip): ").strip()
    category: str | None = category_input if category_input else None

    # T035: Due date prompt with validation
    due_date = None
    due_time = None
    while True:
        date_input = input("Due Date (YYYY-MM-DD or YYYY-MM-DD HH:MM, press Enter to skip): ").strip()
        if not date_input:
            break
        result = validate_date_input(date_input)
        if result:
            due_date, due_time = result
            break
        print("Error: Invalid date format. Use YYYY-MM-DD or YYYY-MM-DD HH:MM")

    # T036: Recurring prompt (optional)
    recurring = Recurrence.NONE
    while True:
        recurring_input = input("Recurring (1=Daily, 2=Weekly, 3=Monthly, press Enter to skip): ").strip()
        if not recurring_input:
            break
        validated_recurring = validate_recurring_input(recurring_input)
        if validated_recurring:
            recurring = validated_recurring
            break
        print("Error: Invalid recurring. Enter 1 (Daily), 2 (Weekly), 3 (Monthly), or press Enter to skip")

    # T037: Create task
    try:
        task = manager.add_task(
            title=title,
            description=description,
            priority=priority,
            category=category,
            due_date=due_date,
            due_time=due_time,
            recurring=recurring
        )
        # T038: Success message with separation line
        print(SEPARATOR_MINOR)
        print(f"Task added successfully! ID: {task.id}")
    except InvalidTaskDataError as e:
        print(f"Error: {e}")


def handle_view_tasks(manager: TaskManager) -> None:
    """
    Handle View All Tasks option.

    Satisfies: specs/todo-features/tasks.md - T040-T044
    """
    print()
    print(SEPARATOR_MAJOR)
    print("              ALL TASKS")
    print(SEPARATOR_MAJOR)

    tasks = manager.get_all_tasks()

    if not tasks:
        # T043: Empty list message
        print("Your task list is empty.")
    else:
        # T042: Format and display each task
        for task in tasks:
            print(format_task(task))
            print(SEPARATOR_MINOR)

        # T044: Total count
        print()
        print(f"Total: {len(tasks)} task(s)")

    print(SEPARATOR_MAJOR)


def handle_update_task(manager: TaskManager) -> None:
    """
    Handle Update Task option with interactive submenu.

    Satisfies: specs/todo-features/tasks.md - T046-T052
    """
    print()
    print(f"--- Update Task ---")

    # T047: Prompt for task ID
    task_id_input = input("Enter Task ID: ").strip()
    task_id = validate_menu_choice(task_id_input, 1, 999999)
    if task_id is None:
        print("Error: Task ID must be a number")
        return

    # T048: Lookup task
    try:
        task = manager.get_task(task_id)
    except TaskNotFoundError:
        print(f"Error: Task [{task_id}] not found")
        return

    print()
    print("Current Task:")
    print(format_task(task))
    print()

    # T049: Update field submenu
    while True:
        print("Select field to update:")
        print("1. Title")
        print("2. Description")
        print("3. Priority")
        print("4. Category")
        print("5. Due Date")
        print("6. Recurring")
        print("7. Back to Main Menu")
        print()

        choice_input = input("Enter your choice (1-7): ").strip()
        choice = validate_menu_choice(choice_input, 1, 7)

        if choice is None:
            print("Error: Invalid choice.")
            continue

        # T051: Back to main menu
        if choice == 7:
            break

        # T050: Handle each field update
        try:
            if choice == 1:  # Title
                new_title = input("New title: ").strip()
                if not new_title:
                    print("Error: Task title cannot be empty")
                    continue
                manager.update_task(task_id, title=new_title)

            elif choice == 2:  # Description
                new_desc = input("New description: ").strip()
                manager.update_task(task_id, description=new_desc if new_desc else None)

            elif choice == 3:  # Priority
                while True:
                    priority_input = input("New priority (1=High, 2=Medium, 3=Low): ").strip()
                    validated = validate_priority_input(priority_input)
                    if validated:
                        manager.update_task(task_id, priority=validated)
                        break
                    print("Error: Invalid priority. Enter 1 (High), 2 (Medium), or 3 (Low)")

            elif choice == 4:  # Category
                new_category = input("New category: ").strip()
                manager.update_task(task_id, category=new_category if new_category else None)

            elif choice == 5:  # Due Date
                while True:
                    date_input = input("New due date (YYYY-MM-DD or YYYY-MM-DD HH:MM): ").strip()
                    if not date_input:
                        break
                    result = validate_date_input(date_input)
                    if result:
                        manager.update_task(task_id, due_date=result[0], due_time=result[1])
                        break
                    print("Error: Invalid date format. Use YYYY-MM-DD or YYYY-MM-DD HH:MM")

            elif choice == 6:  # Recurring
                while True:
                    recurring_input = input("New recurring (1=Daily, 2=Weekly, 3=Monthly, 0=None): ").strip()
                    validated_recurrence = validate_recurring_input(recurring_input)
                    if validated_recurrence is not None:
                        manager.update_task(task_id, recurring=validated_recurrence)
                        break
                    print("Error: Invalid recurring. Enter 0 (None), 1 (Daily), 2 (Weekly), or 3 (Monthly)")

            # T052: Success message
            print()
            print(f"Task [{task_id}] updated successfully.")
            break

        except (TaskNotFoundError, InvalidTaskDataError) as e:
            print(f"Error: {e}")


def handle_delete_task(manager: TaskManager) -> None:
    """
    Handle Delete Task option with confirmation.

    Satisfies: specs/todo-features/tasks.md - T054-T059
    """
    print()
    print(f"--- Delete Task ---")

    # T055: Prompt for task ID
    task_id_input = input("Enter Task ID: ").strip()
    task_id = validate_menu_choice(task_id_input, 1, 999999)
    if task_id is None:
        print("Error: Task ID must be a number")
        return

    # T056: Lookup task and display
    try:
        task = manager.get_task(task_id)
    except TaskNotFoundError:
        print(f"Error: Task [{task_id}] not found")
        return

    print()
    print("Task to delete:")
    print(format_task(task))
    print()

    # T057: Confirmation prompt
    confirm = input("Are you sure you want to delete this task? (y/n): ").strip().lower()

    if confirm == 'y':
        # T058: Delete task
        manager.delete_task(task_id)
        # T059: Success message
        print()
        print(f"Task [{task_id}] deleted successfully.")
    else:
        print()
        print("Delete cancelled.")


def handle_toggle_complete(manager: TaskManager) -> None:
    """
    Handle Toggle Task Completion option.

    Satisfies: specs/todo-features/tasks.md - T061-T065
    """
    print()
    print(f"--- Toggle Task Completion ---")

    # T062: Prompt for task ID
    task_id_input = input("Enter Task ID: ").strip()
    task_id = validate_menu_choice(task_id_input, 1, 999999)
    if task_id is None:
        print("Error: Task ID must be a number")
        return

    # T063: Toggle and capture result
    try:
        task, new_task = manager.toggle_complete(task_id)

        print()
        # T065: Status message
        if task.status == Status.COMPLETE:
            print(f"Task [{task_id}] marked as complete.")
            # T064: Recurring task message
            if new_task:
                print(f"New recurring task created: [{new_task.id}]")
        else:
            print(f"Task [{task_id}] marked as pending.")

    except TaskNotFoundError:
        print(f"Error: Task [{task_id}] not found")


def handle_filter_menu(manager: TaskManager) -> None:
    """
    Handle Search / Filter Tasks option with submenu.

    Satisfies: specs/todo-features/tasks.md - T067-T073
    """
    while True:
        print()
        print(f"--- Filter Tasks ---")
        print("1. By Category")
        print("2. By Priority")
        print("3. By Status")
        print("4. Back to Main Menu")
        print()

        choice_input = input("Enter your choice (1-4): ").strip()
        choice = validate_menu_choice(choice_input, 1, 4)

        if choice is None:
            print("Error: Invalid choice.")
            continue

        # T072: Back to main menu
        if choice == 4:
            break

        tasks = []

        if choice == 1:  # T069: Filter by category
            category = input("Enter category to filter: ").strip()
            if category:
                tasks = manager.get_tasks_by_category(category)

        elif choice == 2:  # T070: Filter by priority
            while True:
                priority_input = input("Enter priority (1=High, 2=Medium, 3=Low): ").strip()
                validated = validate_priority_input(priority_input)
                if validated:
                    tasks = manager.get_tasks_by_priority(validated)
                    break
                print("Error: Invalid priority. Enter 1 (High), 2 (Medium), or 3 (Low)")

        elif choice == 3:  # T071: Filter by status submenu
            print()
            print("Select status:")
            print("1. Pending")
            print("2. Complete")
            print()
            status_input = input("Enter your choice (1-2): ").strip()
            status_choice = validate_menu_choice(status_input, 1, 2)
            if status_choice == 1:
                tasks = manager.get_tasks_by_status(Status.PENDING)
            elif status_choice == 2:
                tasks = manager.get_tasks_by_status(Status.COMPLETE)
            else:
                print("Error: Invalid choice.")
                continue

        # T073: Display filtered results
        print()
        print(SEPARATOR_MAJOR)
        print("         FILTERED TASKS")
        print(SEPARATOR_MAJOR)

        if not tasks:
            print("No tasks match your filter criteria.")
        else:
            for task in tasks:
                print(format_task(task))
                print(SEPARATOR_MINOR)
            print()
            print(f"Found: {len(tasks)} task(s) matching filter")

        print(SEPARATOR_MAJOR)
        break


def handle_sort_menu(manager: TaskManager) -> None:
    """
    Handle Sort Tasks option with submenu.

    Satisfies: specs/todo-features/tasks.md - T075-T080
    """
    while True:
        print()
        print(f"--- Sort Tasks ---")
        print("1. By Due Date (ascending)")
        print("2. By Priority (High → Low)")
        print("3. Back to Main Menu")
        print()

        choice_input = input("Enter your choice (1-3): ").strip()
        choice = validate_menu_choice(choice_input, 1, 3)

        if choice is None:
            print("Error: Invalid choice.")
            continue

        # T079: Back to main menu
        if choice == 3:
            break

        sort_label = ""
        tasks = []

        if choice == 1:  # T077: Sort by due date
            tasks = manager.get_tasks_sorted_by_date()
            sort_label = "due date"

        elif choice == 2:  # T078: Sort by priority
            tasks = manager.get_tasks_sorted_by_priority()
            sort_label = "priority"

        # T080: Display sorted results
        print()
        print(SEPARATOR_MAJOR)
        print("         SORTED TASKS")
        print(SEPARATOR_MAJOR)

        if not tasks:
            print("Your task list is empty.")
        else:
            for task in tasks:
                print(format_task(task))
                print(SEPARATOR_MINOR)
            print()
            print(f"Total: {len(tasks)} task(s) (sorted by {sort_label})")

        print(SEPARATOR_MAJOR)
        break
