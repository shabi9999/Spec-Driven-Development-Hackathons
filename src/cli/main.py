#!/usr/bin/env python3
"""
CLI module entry point for In-Memory Python Console Todo Application

Starts the command loop and handles user interactions.
Supports execution as: python -m src.cli.main
"""

import sys
import os

# Add parent directory to path to support module execution
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.task import TaskNotFound
from services.todo_service import TodoService
from cli.commands import dispatch_command


def show_menu() -> None:
    """Display the main menu."""
    print("\n=== Todo Application Menu ===")
    print("1. Add Task")
    print("2. View All Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Mark Task Complete")
    print("6. Mark Task Incomplete")
    print("7. Exit")


def map_choice_to_command(choice: str) -> str | None:
    """
    Convert menu choice into CLI command string
    that dispatch_command already understands.
    """
    if choice == "1":
        title = input("Enter task title: ").strip()
        return f'add "{title}"'

    elif choice == "2":
        return "list"

    elif choice == "3":
        task_id = input("Enter task ID: ").strip()
        new_title = input("Enter new task title: ").strip()
        return f'update {task_id} "{new_title}"'

    elif choice == "4":
        task_id = input("Enter task ID: ").strip()
        return f"delete {task_id}"

    elif choice == "5":
        task_id = input("Enter task ID: ").strip()
        return f"complete {task_id}"

    elif choice == "6":
        task_id = input("Enter task ID: ").strip()
        return f"incomplete {task_id}"

    elif choice == "7":
        return "exit"

    return None


def main():
    """
    Main application loop.

    Initializes the TodoService and enters an interactive menu loop.
    """
    service = TodoService()

    print("Welcome to Todo App")
    print("Select an option from the menu below.")

    while True:
        try:
            show_menu()
            choice = input("\nChoose an option (1-7): ").strip()

            command = map_choice_to_command(choice)

            if not command:
                print("Invalid option. Please choose between 1 and 7.")
                continue

            if command == "exit":
                print("Goodbye!")
                break

            result = dispatch_command(command, service)
            print("\n" + result)

        except TaskNotFound:
            print("Error: Task not found")
            print("Hint: Use 'View All Tasks' to see task IDs")

        except ValueError as e:
            print(f"Error: {str(e)}")

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break

        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            print("Please try again.")


if __name__ == "__main__":
    main()
