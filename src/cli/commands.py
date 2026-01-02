"""CLI command handlers and input parsing for Todo application"""

import shlex
from typing import List, Tuple
from models.task import Task, TaskNotFound
from services.todo_service import TodoService


def parse_quoted_args(command_line: str) -> List[str]:
    """
    Parse command line with quoted arguments.

    Handles both single and double quotes for arguments with spaces.
    Examples:
        'add "Buy groceries"' -> ['add', 'Buy groceries']
        'add "Buy groceries" "milk, eggs"' -> ['add', 'Buy groceries', 'milk, eggs']

    Args:
        command_line: Raw command line input from user

    Returns:
        List of parsed arguments

    Raises:
        ValueError: If quoted arguments are mismatched
    """
    try:
        # shlex handles quote parsing correctly
        return shlex.split(command_line)
    except ValueError as e:
        raise ValueError(f"Invalid quotes in command: {e}")


def format_task_table(tasks: List[Task]) -> str:
    """
    Format a list of tasks as an ASCII table.

    Columns: ID | Title | Status | Created
    Example output:
        ID | Title            | Status    | Created
        ---|------------------|-----------|------------------
        1  | Buy groceries    | pending   | 2026-01-02 01:30:00
        2  | Write report     | completed | 2026-01-02 01:31:00

    Args:
        tasks: List of Task objects to format

    Returns:
        Formatted table string ready for console output
    """
    if not tasks:
        return "No tasks"

    # Column definitions: (name, width)
    columns = [
        ("ID", 4),
        ("Title", 25),
        ("Status", 10),
        ("Created", 19),
    ]

    # Build header
    header_parts = []
    separator_parts = []
    for col_name, col_width in columns:
        header_parts.append(col_name.ljust(col_width))
        separator_parts.append("-" * col_width)

    header = " | ".join(header_parts)
    separator = "-+-".join(separator_parts)

    # Build rows
    rows = []
    for task in tasks:
        row_parts = []

        # ID (right-aligned)
        row_parts.append(str(task.id).rjust(4))

        # Title (left-aligned, truncated if too long)
        title = task.title[:23]  # Leave room for truncation indicator
        if len(task.title) > 23:
            title = title[:-2] + ".."
        row_parts.append(title.ljust(25))

        # Status (left-aligned)
        row_parts.append(task.status.ljust(10))

        # Created (left-aligned)
        row_parts.append(task.created_at.strftime("%Y-%m-%d %H:%M:%S"))

        rows.append(" | ".join(row_parts))

    # Combine all parts
    table_lines = [header, separator] + rows
    return "\n".join(table_lines)


def handle_add(args: List[str], service: TodoService) -> str:
    """
    Handle 'add' command to create a new task.

    Syntax: add "title" ["description"]
    Example: add "Buy groceries" "milk, eggs, bread"

    Args:
        args: Parsed command arguments (args[0] should be 'add')
        service: TodoService instance

    Returns:
        Confirmation message with task ID and status

    Raises:
        ValueError: If arguments are invalid (missing title, empty title)
    """
    if len(args) < 2:
        raise ValueError("Task title required. Syntax: add \"title\" [\"description\"]")

    title = args[1].strip()
    if not title:
        raise ValueError("Task title cannot be empty")

    description = args[2].strip() if len(args) > 2 else ""

    task = service.add(title, description)
    return f"[+] Task created (ID: {task.id})"


def handle_list(service: TodoService) -> str:
    """
    Handle 'list' command to display all tasks.

    Args:
        service: TodoService instance

    Returns:
        Formatted table of all tasks or "No tasks" message
    """
    tasks = service.get_all()
    return format_task_table(tasks)


def handle_update(args: List[str], service: TodoService) -> str:
    """
    Handle 'update' command to modify a task's title and/or description.

    Syntax: update <id> "new title" ["new description"]
    Example: update 1 "Buy groceries and cook dinner"

    Args:
        args: Parsed command arguments
        service: TodoService instance

    Returns:
        Confirmation message with updated task

    Raises:
        ValueError: If arguments are invalid (missing ID, invalid ID format, missing title)
        TaskNotFound: If task with given ID doesn't exist
    """
    if len(args) < 3:
        raise ValueError("Task ID and new title required. Syntax: update <id> \"title\" [\"description\"]")

    # Parse and validate task ID
    try:
        task_id = int(args[1])
    except ValueError:
        raise ValueError(f"Invalid task ID: '{args[1]}'. Must be a number.")

    title = args[2].strip()
    if not title:
        raise ValueError("Task title cannot be empty")

    description = args[3].strip() if len(args) > 3 else ""

    task = service.update(task_id, title, description)
    return f"[+] Task {task.id} updated"


def handle_complete(args: List[str], service: TodoService) -> str:
    """
    Handle 'complete' command to mark a task as completed.

    Syntax: complete <id>
    Example: complete 1

    Args:
        args: Parsed command arguments
        service: TodoService instance

    Returns:
        Confirmation message with updated status

    Raises:
        ValueError: If arguments are invalid (missing ID, invalid ID format)
        TaskNotFound: If task with given ID doesn't exist
    """
    if len(args) < 2:
        raise ValueError("Task ID required. Syntax: complete <id>")

    try:
        task_id = int(args[1])
    except ValueError:
        raise ValueError(f"Invalid task ID: '{args[1]}'. Must be a number.")

    task = service.mark_complete(task_id)
    return f"[+] Task {task.id} marked as completed"


def handle_delete(args: List[str], service: TodoService) -> str:
    """
    Handle 'delete' command to permanently remove a task.

    Syntax: delete <id>
    Example: delete 1

    Args:
        args: Parsed command arguments
        service: TodoService instance

    Returns:
        Confirmation message

    Raises:
        ValueError: If arguments are invalid (missing ID, invalid ID format)
        TaskNotFound: If task with given ID doesn't exist
    """
    if len(args) < 2:
        raise ValueError("Task ID required. Syntax: delete <id>")

    try:
        task_id = int(args[1])
    except ValueError:
        raise ValueError(f"Invalid task ID: '{args[1]}'. Must be a number.")

    service.delete(task_id)
    return f"[-] Task {task_id} deleted"


def handle_help() -> str:
    """
    Handle 'help' command to display available commands.

    Returns:
        Help text with all available commands and their syntax
    """
    return """Available commands:

  add <title> [description]      Create a new task
                                 Example: add "Buy groceries"

  list                           Show all tasks in table format

  update <id> <title> [desc]     Update a task's title/description
                                 Example: update 1 "New title"

  complete <id>                  Mark a task as completed
                                 Example: complete 1

  delete <id>                    Delete a task permanently
                                 Example: delete 1

  help                           Show this help message

  exit                           Quit the application

Tips:
  • Use quotes for titles with spaces: add "Buy milk and bread"
  • Use "list" to see task IDs before updating/completing/deleting
  • Task IDs are unique and never reused
"""


def dispatch_command(command_line: str, service: TodoService) -> str:
    """
    Parse and dispatch a command to its handler.

    Args:
        command_line: Raw command input from user
        service: TodoService instance

    Returns:
        Result message from command handler

    Raises:
        ValueError: If command is invalid or arguments are malformed
        TaskNotFound: If command references non-existent task
    """
    # Parse command line
    try:
        args = parse_quoted_args(command_line.strip())
    except ValueError as e:
        raise ValueError(f"Invalid command syntax: {e}")

    if not args:
        raise ValueError("Empty command. Type 'help' for available commands.")

    command = args[0].lower()

    # Dispatch to appropriate handler
    if command == "add":
        return handle_add(args, service)
    elif command == "list":
        return handle_list(service)
    elif command == "update":
        return handle_update(args, service)
    elif command == "complete":
        return handle_complete(args, service)
    elif command == "delete":
        return handle_delete(args, service)
    elif command == "help":
        return handle_help()
    else:
        raise ValueError(f"Unknown command: '{command}'. Type 'help' for available commands.")
