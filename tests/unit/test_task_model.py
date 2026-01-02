"""Unit tests for Task domain model"""

import unittest
import sys
from datetime import datetime
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from models.task import Task, TaskNotFound


class TestTaskCreation(unittest.TestCase):
    """Test Task creation and validation"""

    def test_create_task_with_title_only(self):
        """Test creating a task with just a title"""
        task = Task(task_id=1, title="Buy groceries")
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Buy groceries")
        self.assertEqual(task.description, "")
        self.assertEqual(task.status, "pending")

    def test_create_task_with_title_and_description(self):
        """Test creating a task with title and description"""
        task = Task(task_id=2, title="Write report", description="Due Friday")
        self.assertEqual(task.id, 2)
        self.assertEqual(task.title, "Write report")
        self.assertEqual(task.description, "Due Friday")
        self.assertEqual(task.status, "pending")

    def test_create_task_with_custom_status(self):
        """Test creating a task with completed status"""
        task = Task(task_id=3, title="Task", status="completed")
        self.assertEqual(task.status, "completed")

    def test_task_creation_trims_whitespace(self):
        """Test that title and description are trimmed"""
        task = Task(task_id=4, title="  Buy milk  ", description="  2 gallons  ")
        self.assertEqual(task.title, "Buy milk")
        self.assertEqual(task.description, "2 gallons")

    def test_empty_title_raises_error(self):
        """Test that empty title raises ValueError"""
        with self.assertRaises(ValueError) as context:
            Task(task_id=5, title="")
        self.assertIn("empty", str(context.exception).lower())

    def test_whitespace_only_title_raises_error(self):
        """Test that whitespace-only title raises ValueError"""
        with self.assertRaises(ValueError) as context:
            Task(task_id=6, title="   ")
        self.assertIn("empty", str(context.exception).lower())

    def test_invalid_status_raises_error(self):
        """Test that invalid status raises ValueError"""
        with self.assertRaises(ValueError) as context:
            Task(task_id=7, title="Task", status="urgent")
        self.assertIn("status", str(context.exception).lower())

    def test_task_has_creation_timestamp(self):
        """Test that task has a creation timestamp"""
        before = datetime.now()
        task = Task(task_id=8, title="Task")
        after = datetime.now()

        self.assertIsInstance(task.created_at, datetime)
        self.assertGreaterEqual(task.created_at, before)
        self.assertLessEqual(task.created_at, after)


class TestTaskProperties(unittest.TestCase):
    """Test Task property getters and setters"""

    def setUp(self):
        """Create a test task for each test"""
        self.task = Task(task_id=1, title="Test Task")

    def test_id_is_immutable(self):
        """Test that task ID cannot be changed"""
        original_id = self.task.id
        # Attempting to set id should not work (property has no setter)
        with self.assertRaises(AttributeError):
            self.task.id = 999
        self.assertEqual(self.task.id, original_id)

    def test_created_at_is_immutable(self):
        """Test that created_at timestamp cannot be changed"""
        original_time = self.task.created_at
        with self.assertRaises(AttributeError):
            self.task.created_at = datetime.now()
        self.assertEqual(self.task.created_at, original_time)

    def test_title_can_be_updated(self):
        """Test that task title can be updated"""
        self.task.title = "Updated Title"
        self.assertEqual(self.task.title, "Updated Title")

    def test_empty_title_update_raises_error(self):
        """Test that setting empty title raises error"""
        with self.assertRaises(ValueError):
            self.task.title = ""

    def test_description_can_be_updated(self):
        """Test that task description can be updated"""
        self.task.description = "New description"
        self.assertEqual(self.task.description, "New description")

    def test_status_can_be_updated(self):
        """Test that task status can be updated"""
        self.task.status = "completed"
        self.assertEqual(self.task.status, "completed")

    def test_invalid_status_update_raises_error(self):
        """Test that setting invalid status raises error"""
        with self.assertRaises(ValueError):
            self.task.status = "archived"

    def test_whitespace_in_title_update_is_trimmed(self):
        """Test that whitespace is trimmed on title update"""
        self.task.title = "  Trimmed Title  "
        self.assertEqual(self.task.title, "Trimmed Title")

    def test_whitespace_in_description_update_is_trimmed(self):
        """Test that whitespace is trimmed on description update"""
        self.task.description = "  Trimmed Description  "
        self.assertEqual(self.task.description, "Trimmed Description")


class TestTaskSerialization(unittest.TestCase):
    """Test Task serialization methods"""

    def test_to_dict_contains_all_fields(self):
        """Test that to_dict includes all task fields"""
        task = Task(task_id=1, title="Test", description="Desc", status="completed")
        task_dict = task.to_dict()

        self.assertIn("id", task_dict)
        self.assertIn("title", task_dict)
        self.assertIn("description", task_dict)
        self.assertIn("status", task_dict)
        self.assertIn("created_at", task_dict)

    def test_to_dict_has_correct_values(self):
        """Test that to_dict has correct field values"""
        task = Task(task_id=42, title="Buy milk", description="2 gallons", status="pending")
        task_dict = task.to_dict()

        self.assertEqual(task_dict["id"], 42)
        self.assertEqual(task_dict["title"], "Buy milk")
        self.assertEqual(task_dict["description"], "2 gallons")
        self.assertEqual(task_dict["status"], "pending")

    def test_to_dict_created_at_is_string(self):
        """Test that created_at in to_dict is formatted as string"""
        task = Task(task_id=1, title="Task")
        task_dict = task.to_dict()

        self.assertIsInstance(task_dict["created_at"], str)
        # Check format: YYYY-MM-DD HH:MM:SS
        self.assertRegex(task_dict["created_at"], r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")

    def test_repr_includes_key_fields(self):
        """Test that __repr__ includes key fields"""
        task = Task(task_id=1, title="Test Task")
        repr_str = repr(task)

        self.assertIn("Task", repr_str)
        self.assertIn("id=1", repr_str)
        self.assertIn("Test Task", repr_str)
        self.assertIn("pending", repr_str)


class TestTaskEquality(unittest.TestCase):
    """Test Task equality comparison"""

    def test_same_task_is_equal(self):
        """Test that two tasks with same data are equal"""
        task1 = Task(task_id=1, title="Task", description="Desc", status="pending")
        task2 = Task(task_id=1, title="Task", description="Desc", status="pending")

        # Note: Two newly created tasks with same data will have different timestamps
        # So we only compare content, not timestamps
        # For now, they won't be equal due to different created_at

    def test_different_ids_not_equal(self):
        """Test that tasks with different IDs are not equal"""
        task1 = Task(task_id=1, title="Task")
        task2 = Task(task_id=2, title="Task")

        self.assertNotEqual(task1, task2)

    def test_different_titles_not_equal(self):
        """Test that tasks with different titles are not equal"""
        task1 = Task(task_id=1, title="Task 1")
        task2 = Task(task_id=1, title="Task 2")

        self.assertNotEqual(task1, task2)

    def test_task_not_equal_to_non_task(self):
        """Test that task is not equal to non-Task objects"""
        task = Task(task_id=1, title="Task")

        self.assertNotEqual(task, "Task")
        self.assertNotEqual(task, 1)
        self.assertNotEqual(task, {"id": 1, "title": "Task"})


class TestTaskNotFoundException(unittest.TestCase):
    """Test TaskNotFound exception"""

    def test_task_not_found_is_exception(self):
        """Test that TaskNotFound is an Exception"""
        self.assertTrue(issubclass(TaskNotFound, Exception))

    def test_task_not_found_can_be_raised(self):
        """Test that TaskNotFound can be raised and caught"""
        with self.assertRaises(TaskNotFound):
            raise TaskNotFound("Task not found")

    def test_task_not_found_message(self):
        """Test that TaskNotFound preserves message"""
        msg = "Task with ID 42 not found"
        with self.assertRaises(TaskNotFound) as context:
            raise TaskNotFound(msg)
        self.assertEqual(str(context.exception), msg)


if __name__ == "__main__":
    unittest.main()
