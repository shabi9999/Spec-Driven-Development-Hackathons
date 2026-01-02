"""Unit tests for TodoService"""

import unittest
import sys
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from models.task import Task, TaskNotFound
from services.todo_service import TodoService


class TestTodoServiceAdd(unittest.TestCase):
    """Test TodoService.add() method"""

    def setUp(self):
        """Create a fresh TodoService for each test"""
        self.service = TodoService()

    def test_add_task_with_title_only(self):
        """Test adding a task with just title"""
        task = self.service.add("Buy groceries")

        self.assertIsInstance(task, Task)
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Buy groceries")
        self.assertEqual(task.description, "")
        self.assertEqual(task.status, "pending")

    def test_add_task_with_description(self):
        """Test adding a task with title and description"""
        task = self.service.add("Write report", "Due Friday")

        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Write report")
        self.assertEqual(task.description, "Due Friday")

    def test_add_multiple_tasks_auto_increments_id(self):
        """Test that multiple tasks get sequential IDs"""
        task1 = self.service.add("Task 1")
        task2 = self.service.add("Task 2")
        task3 = self.service.add("Task 3")

        self.assertEqual(task1.id, 1)
        self.assertEqual(task2.id, 2)
        self.assertEqual(task3.id, 3)

    def test_add_task_with_empty_title_raises_error(self):
        """Test that adding task with empty title raises ValueError"""
        with self.assertRaises(ValueError):
            self.service.add("")

    def test_add_task_appears_in_get_all(self):
        """Test that added task appears in get_all()"""
        self.service.add("Task 1")
        self.service.add("Task 2")

        tasks = self.service.get_all()
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0].title, "Task 1")
        self.assertEqual(tasks[1].title, "Task 2")


class TestTodoServiceGet(unittest.TestCase):
    """Test TodoService.get() method"""

    def setUp(self):
        """Create a service and add test tasks"""
        self.service = TodoService()
        self.task1 = self.service.add("Task 1")
        self.task2 = self.service.add("Task 2")
        self.task3 = self.service.add("Task 3")

    def test_get_existing_task(self):
        """Test retrieving an existing task"""
        task = self.service.get(2)

        self.assertEqual(task.id, 2)
        self.assertEqual(task.title, "Task 2")

    def test_get_first_task(self):
        """Test retrieving the first task"""
        task = self.service.get(1)
        self.assertEqual(task.id, 1)

    def test_get_last_task(self):
        """Test retrieving the last task"""
        task = self.service.get(3)
        self.assertEqual(task.id, 3)

    def test_get_nonexistent_task_raises_error(self):
        """Test that getting non-existent task raises TaskNotFound"""
        with self.assertRaises(TaskNotFound):
            self.service.get(999)

    def test_get_returns_same_object(self):
        """Test that get() returns the actual task object"""
        task = self.service.get(1)
        # Modify the task
        task.title = "Modified"

        # Get it again and verify modification persisted
        retrieved = self.service.get(1)
        self.assertEqual(retrieved.title, "Modified")


class TestTodoServiceGetAll(unittest.TestCase):
    """Test TodoService.get_all() method"""

    def test_get_all_empty_service(self):
        """Test get_all on empty service"""
        service = TodoService()
        tasks = service.get_all()

        self.assertEqual(tasks, [])
        self.assertIsInstance(tasks, list)

    def test_get_all_returns_all_tasks(self):
        """Test that get_all returns all tasks"""
        service = TodoService()
        service.add("Task 1")
        service.add("Task 2")
        service.add("Task 3")

        tasks = service.get_all()
        self.assertEqual(len(tasks), 3)

    def test_get_all_returns_copy(self):
        """Test that get_all returns a copy, not the internal list"""
        service = TodoService()
        service.add("Task 1")

        tasks1 = service.get_all()
        tasks1.append(Task(task_id=999, title="Fake Task"))

        tasks2 = service.get_all()
        self.assertEqual(len(tasks2), 1)  # Original still has 1 task


class TestTodoServiceUpdate(unittest.TestCase):
    """Test TodoService.update() method"""

    def setUp(self):
        """Create a service and add test tasks"""
        self.service = TodoService()
        self.service.add("Original Title", "Original Desc")
        self.service.add("Task 2")

    def test_update_title(self):
        """Test updating a task's title"""
        task = self.service.update(1, "New Title", "Original Desc")

        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "New Title")
        # Description should be preserved when passed explicitly
        self.assertEqual(task.description, "Original Desc")

    def test_update_description(self):
        """Test updating a task's description"""
        task = self.service.update(1, "Original Title", "New Description")

        self.assertEqual(task.title, "Original Title")
        self.assertEqual(task.description, "New Description")

    def test_update_both_title_and_description(self):
        """Test updating both title and description"""
        task = self.service.update(1, "New Title", "New Description")

        self.assertEqual(task.title, "New Title")
        self.assertEqual(task.description, "New Description")

    def test_update_nonexistent_task_raises_error(self):
        """Test that updating non-existent task raises TaskNotFound"""
        with self.assertRaises(TaskNotFound):
            self.service.update(999, "Title")

    def test_update_with_empty_title_raises_error(self):
        """Test that updating with empty title raises ValueError"""
        with self.assertRaises(ValueError):
            self.service.update(1, "")

    def test_update_persists_changes(self):
        """Test that updates persist in service"""
        self.service.update(1, "Updated Title")

        retrieved = self.service.get(1)
        self.assertEqual(retrieved.title, "Updated Title")


class TestTodoServiceDelete(unittest.TestCase):
    """Test TodoService.delete() method"""

    def setUp(self):
        """Create a service and add test tasks"""
        self.service = TodoService()
        self.service.add("Task 1")
        self.service.add("Task 2")
        self.service.add("Task 3")

    def test_delete_existing_task(self):
        """Test deleting an existing task"""
        self.service.delete(2)

        with self.assertRaises(TaskNotFound):
            self.service.get(2)

    def test_delete_removes_from_get_all(self):
        """Test that deleted task doesn't appear in get_all"""
        self.service.delete(1)

        tasks = self.service.get_all()
        self.assertEqual(len(tasks), 2)
        self.assertNotIn(1, [t.id for t in tasks])

    def test_delete_nonexistent_task_raises_error(self):
        """Test that deleting non-existent task raises TaskNotFound"""
        with self.assertRaises(TaskNotFound):
            self.service.delete(999)

    def test_delete_does_not_reuse_id(self):
        """Test that deleted task IDs are not reused"""
        self.service.delete(2)

        # Add a new task - it should get ID 4, not 2
        new_task = self.service.add("New Task")
        self.assertEqual(new_task.id, 4)

    def test_delete_first_task(self):
        """Test deleting the first task"""
        self.service.delete(1)

        remaining = self.service.get_all()
        self.assertEqual(len(remaining), 2)
        self.assertEqual(remaining[0].id, 2)

    def test_delete_last_task(self):
        """Test deleting the last task"""
        self.service.delete(3)

        remaining = self.service.get_all()
        self.assertEqual(len(remaining), 2)
        self.assertEqual(remaining[-1].id, 2)


class TestTodoServiceMarkComplete(unittest.TestCase):
    """Test TodoService.mark_complete() method"""

    def setUp(self):
        """Create a service and add test tasks"""
        self.service = TodoService()
        self.service.add("Task 1")
        self.service.add("Task 2")

    def test_mark_complete_changes_status(self):
        """Test that mark_complete changes status to 'completed'"""
        task = self.service.mark_complete(1)

        self.assertEqual(task.status, "completed")

    def test_mark_complete_returns_task(self):
        """Test that mark_complete returns the updated task"""
        task = self.service.mark_complete(1)

        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Task 1")

    def test_mark_complete_nonexistent_raises_error(self):
        """Test that marking non-existent task raises TaskNotFound"""
        with self.assertRaises(TaskNotFound):
            self.service.mark_complete(999)

    def test_mark_complete_persists(self):
        """Test that completion status persists"""
        self.service.mark_complete(1)

        retrieved = self.service.get(1)
        self.assertEqual(retrieved.status, "completed")

    def test_mark_complete_is_idempotent(self):
        """Test that marking already-completed task again is safe"""
        self.service.mark_complete(1)
        task = self.service.mark_complete(1)

        self.assertEqual(task.status, "completed")

    def test_mark_complete_does_not_affect_other_tasks(self):
        """Test that completing one task doesn't affect others"""
        self.service.mark_complete(1)

        task2 = self.service.get(2)
        self.assertEqual(task2.status, "pending")


class TestTodoServiceMarkPending(unittest.TestCase):
    """Test TodoService.mark_pending() method"""

    def setUp(self):
        """Create a service and add a completed task"""
        self.service = TodoService()
        self.service.add("Task 1")
        self.service.mark_complete(1)

    def test_mark_pending_changes_status(self):
        """Test that mark_pending changes status to 'pending'"""
        task = self.service.mark_pending(1)

        self.assertEqual(task.status, "pending")

    def test_mark_pending_nonexistent_raises_error(self):
        """Test that marking non-existent task raises TaskNotFound"""
        with self.assertRaises(TaskNotFound):
            self.service.mark_pending(999)


class TestTodoServiceCount(unittest.TestCase):
    """Test TodoService.count() method"""

    def test_count_empty_service(self):
        """Test count on empty service"""
        service = TodoService()
        self.assertEqual(service.count(), 0)

    def test_count_after_adding_tasks(self):
        """Test count increases after adding tasks"""
        service = TodoService()
        service.add("Task 1")
        self.assertEqual(service.count(), 1)

        service.add("Task 2")
        self.assertEqual(service.count(), 2)

    def test_count_after_deleting_task(self):
        """Test count decreases after deleting task"""
        service = TodoService()
        service.add("Task 1")
        service.add("Task 2")
        self.assertEqual(service.count(), 2)

        service.delete(1)
        self.assertEqual(service.count(), 1)


class TestTodoServiceDeterminism(unittest.TestCase):
    """Test deterministic behavior of TodoService"""

    def test_add_same_task_twice_creates_two_different_tasks(self):
        """Test that adding same title twice creates different IDs"""
        service = TodoService()
        task1 = service.add("Same Title")
        task2 = service.add("Same Title")

        self.assertEqual(task1.title, task2.title)
        self.assertNotEqual(task1.id, task2.id)

    def test_operations_are_deterministic(self):
        """Test that same operations produce same results"""
        service1 = TodoService()
        service1.add("Task")
        task1 = service1.get(1)

        service2 = TodoService()
        service2.add("Task")
        task2 = service2.get(1)

        self.assertEqual(task1.title, task2.title)
        self.assertEqual(task1.status, task2.status)


if __name__ == "__main__":
    unittest.main()
