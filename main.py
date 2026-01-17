#!/usr/bin/env python3
"""
Todo CLI Enhanced - Main entry point with numeric menu system.

Satisfies: specs/002-enhanced-todo-features/tasks.md - T025, T026, T027, T029, T039, T045, T053, T060, T066, T074, T081
"""

from src.services.task_manager import TaskManager
from src.cli.commands import (
    display_main_menu, get_menu_choice, handle_exit,
    handle_add_task, handle_view_tasks, handle_update_task,
    handle_delete_task, handle_toggle_complete,
    handle_filter_menu, handle_sort_menu
)


def main_menu_loop(manager: TaskManager) -> None:
    """
    Main menu loop for numeric menu selection.

    Satisfies: specs/002-enhanced-todo-features/tasks.md - T025, T026
    """
    while True:
        display_main_menu()
        choice = get_menu_choice()

        if choice is None:
            continue

        # T026, T029, T039, T045, T053, T060, T066, T074, T081: Wire menu options to handlers
        if choice == 1:
            handle_add_task(manager)
        elif choice == 2:
            handle_view_tasks(manager)
        elif choice == 3:
            handle_update_task(manager)
        elif choice == 4:
            handle_delete_task(manager)
        elif choice == 5:
            handle_toggle_complete(manager)
        elif choice == 6:
            handle_filter_menu(manager)
        elif choice == 7:
            handle_sort_menu(manager)
        elif choice == 8:
            handle_exit()
            break


def main() -> None:
    """
    Main entry point for Todo CLI Enhanced.

    Satisfies: specs/002-enhanced-todo-features/tasks.md - T027
    """
    manager = TaskManager()

    try:
        main_menu_loop(manager)
    except KeyboardInterrupt:
        print("\n")
        handle_exit()


if __name__ == "__main__":
    main()
