"""TodoService for managing in-memory task store"""

from typing import List, Optional
from models.task import Task, TaskNotFound


class TodoService:
    """
    Service layer for Todo CRUD operations with in-memory storage.

    Implements a deterministic, fully testable interface for all task management operations.
    All operations are pure functions - same input always produces same output.
    No hidden state or side effects beyond declared task mutations.
    """

    def __init__(self):
        """Initialize TodoService with empty task list and ID counter"""
        self._tasks: List[Task] = []
        self._next_id: int = 1

    def add(self, title: str, description: str = "") -> Task:
        """
        Create a new task and add it to the store.

        Args:
            title: Task title (required, non-empty)
            description: Optional task description

        Returns:
            The created Task object with assigned ID

        Raises:
            ValueError: If title is empty or invalid
        """
        task = Task(task_id=self._next_id, title=title, description=description, status="pending")
        self._tasks.append(task)
        self._next_id += 1
        return task

    def get(self, task_id: int) -> Task:
        """
        Retrieve a task by ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            The Task object with the given ID

        Raises:
            TaskNotFound: If no task with the given ID exists
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        raise TaskNotFound(f"Task with ID {task_id} not found")

    def get_all(self) -> List[Task]:
        """
        Get all tasks in the store.

        Returns:
            List of all Task objects (empty list if no tasks exist)
        """
        return self._tasks.copy()

    def update(self, task_id: int, title: str, description: str = "") -> Task:
        """
        Update a task's title and/or description.

        Args:
            task_id: The ID of the task to update
            title: New task title (required, non-empty)
            description: New task description

        Returns:
            The updated Task object

        Raises:
            TaskNotFound: If no task with the given ID exists
            ValueError: If title is empty or invalid
        """
        task = self.get(task_id)  # Raises TaskNotFound if not found
        task.title = title  # May raise ValueError if title is empty
        task.description = description
        return task

    def delete(self, task_id: int) -> None:
        """
        Delete a task by ID (permanent removal).

        Args:
            task_id: The ID of the task to delete

        Raises:
            TaskNotFound: If no task with the given ID exists

        Note:
            Task IDs are not reused after deletion. Auto-increment counter continues
            from the last assigned ID, ensuring each task has a unique ID throughout
            the application's lifetime.
        """
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                del self._tasks[i]
                return
        raise TaskNotFound(f"Task with ID {task_id} not found")

    def mark_complete(self, task_id: int) -> Task:
        """
        Mark a task as completed.

        Args:
            task_id: The ID of the task to mark complete

        Returns:
            The updated Task object with status='completed'

        Raises:
            TaskNotFound: If no task with the given ID exists

        Note:
            This operation is idempotent - marking an already-completed task
            as complete again is safe and returns the task unchanged.
        """
        task = self.get(task_id)  # Raises TaskNotFound if not found
        task.status = "completed"
        return task

    def mark_pending(self, task_id: int) -> Task:
        """
        Mark a task as pending (revert from completed).

        Args:
            task_id: The ID of the task to mark pending

        Returns:
            The updated Task object with status='pending'

        Raises:
            TaskNotFound: If no task with the given ID exists

        Note:
            Idempotent operation.
        """
        task = self.get(task_id)  # Raises TaskNotFound if not found
        task.status = "pending"
        return task

    def count(self) -> int:
        """
        Get the total number of tasks in the store.

        Returns:
            Number of tasks
        """
        return len(self._tasks)

    def clear(self) -> None:
        """Clear all tasks from the store (for testing)"""
        self._tasks.clear()
        self._next_id = 1
