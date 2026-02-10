#!/usr/bin/env python3
"""
Main entry point for In-Memory Python Console Todo Application

Starts the command loop and handles user interactions.
Supports execution as: python src/main.py
"""

import sys
import os

# Add parent directory to path to support 'python src/main.py' execution
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.task import TaskNotFound
from services.todo_service import TodoService
from cli.commands import dispatch_command


def main():
    """
    Main application loop.

    Initializes the TodoService and enters an interactive command loop.
    Handles user input, dispatches commands, and displays results.
    """
    service = TodoService()

    print("Welcome to Todo App")
    print("Type 'help' for available commands\n")

    while True:
        try:
            # Read user input
            user_input = input("todo> ").strip()

            # Skip empty input
            if not user_input:
                continue

            # Check for exit commands
            if user_input.lower() in ("exit", "quit"):
                print("Goodbye!")
                break

            # Dispatch command and display result
            result = dispatch_command(user_input, service)
            print(result)

        except TaskNotFound as e:
            print(f"Error: Task not found")
            print(f"Hint: Use 'list' to see all task IDs")

        except ValueError as e:
            print(f"Error: {str(e)}")

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break

        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            print(f"Type 'help' for command syntax")


if __name__ == "__main__":
    main()
