"""Task domain model for Todo application"""

from datetime import datetime
from typing import Optional


class TaskNotFound(Exception):
    """Exception raised when a task with a given ID cannot be found"""
    pass


class Task:
    """
    Represents a single todo item with immutable ID and creation timestamp.

    Attributes:
        id: Auto-incrementing unique identifier (immutable)
        title: Task title (required, non-empty)
        description: Optional task description
        status: Current status ('pending' or 'completed')
        created_at: Timestamp when task was created (immutable)
    """

    def __init__(self, task_id: int, title: str, description: str = "", status: str = "pending"):
        """
        Initialize a Task with validation.

        Args:
            task_id: Unique task identifier
            title: Task title (required, non-empty after trimming)
            description: Optional task description (defaults to empty string)
            status: Task status, either 'pending' or 'completed' (defaults to 'pending')

        Raises:
            ValueError: If title is empty or status is invalid
        """
        # Validate title
        title_trimmed = title.strip() if isinstance(title, str) else ""
        if not title_trimmed:
            raise ValueError("Task title cannot be empty")

        # Validate status
        if status not in ("pending", "completed"):
            raise ValueError(f"Status must be 'pending' or 'completed', got '{status}'")

        # Set immutable fields
        self._id = task_id
        self._created_at = datetime.now()

        # Set mutable fields
        self._title = title_trimmed
        self._description = description.strip() if isinstance(description, str) else ""
        self._status = status

    @property
    def id(self) -> int:
        """Get task ID (immutable)"""
        return self._id

    @property
    def title(self) -> str:
        """Get task title"""
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        """Set task title with validation"""
        value_trimmed = value.strip() if isinstance(value, str) else ""
        if not value_trimmed:
            raise ValueError("Task title cannot be empty")
        self._title = value_trimmed

    @property
    def description(self) -> str:
        """Get task description"""
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        """Set task description"""
        self._description = value.strip() if isinstance(value, str) else ""

    @property
    def status(self) -> str:
        """Get task status"""
        return self._status

    @status.setter
    def status(self, value: str) -> None:
        """Set task status with validation"""
        if value not in ("pending", "completed"):
            raise ValueError(f"Status must be 'pending' or 'completed', got '{value}'")
        self._status = value

    @property
    def created_at(self) -> datetime:
        """Get task creation timestamp (immutable)"""
        return self._created_at

    def to_dict(self) -> dict:
        """
        Convert task to dictionary for display/serialization.

        Returns:
            Dictionary with task attributes
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }

    def __repr__(self) -> str:
        """String representation of task"""
        return f"Task(id={self.id}, title='{self.title}', status='{self.status}')"

    def __eq__(self, other) -> bool:
        """Check equality based on ID and content"""
        if not isinstance(other, Task):
            return False
        return (self.id == other.id and
                self.title == other.title and
                self.description == other.description and
                self.status == other.status)
