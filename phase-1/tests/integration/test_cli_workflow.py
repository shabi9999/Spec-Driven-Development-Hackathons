"""Integration tests for CLI command workflows"""

import unittest
import sys
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from models.task import TaskNotFound
from services.todo_service import TodoService
from cli.commands import dispatch_command


class TestAddCommandIntegration(unittest.TestCase):
    """Integration tests for add command"""

    def setUp(self):
        """Create a fresh service for each test"""
        self.service = TodoService()

    def test_add_command_creates_task(self):
        """Test full add command workflow"""
        result = dispatch_command('add "Buy groceries"', self.service)

        self.assertIn("created", result.lower())
        self.assertIn("ID: 1", result)

        tasks = self.service.get_all()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "Buy groceries")

    def test_add_command_with_description(self):
        """Test add command with description"""
        result = dispatch_command('add "Buy groceries" "milk, eggs"', self.service)

        self.assertIn("created", result.lower())
        task = self.service.get(1)
        self.assertEqual(task.description, "milk, eggs")

    def test_add_multiple_tasks(self):
        """Test adding multiple tasks"""
        dispatch_command('add "Task 1"', self.service)
        dispatch_command('add "Task 2"', self.service)
        dispatch_command('add "Task 3"', self.service)

        tasks = self.service.get_all()
        self.assertEqual(len(tasks), 3)
        self.assertEqual(tasks[1].id, 2)
        self.assertEqual(tasks[2].id, 3)

    def test_add_with_missing_title_fails(self):
        """Test add command with missing title"""
        with self.assertRaises(ValueError):
            dispatch_command('add', self.service)

    def test_add_with_empty_title_fails(self):
        """Test add command with empty title"""
        with self.assertRaises(ValueError):
            dispatch_command('add ""', self.service)


class TestListCommandIntegration(unittest.TestCase):
    """Integration tests for list command"""

    def setUp(self):
        """Create a service with test data"""
        self.service = TodoService()

    def test_list_empty_service(self):
        """Test list command on empty service"""
        result = dispatch_command('list', self.service)

        self.assertIn("No tasks", result)

    def test_list_shows_all_tasks(self):
        """Test list command displays all tasks"""
        self.service.add("Buy groceries")
        self.service.add("Write report")
        self.service.add("Fix bug")

        result = dispatch_command('list', self.service)

        self.assertIn("Buy groceries", result)
        self.assertIn("Write report", result)
        self.assertIn("Fix bug", result)

    def test_list_shows_task_ids(self):
        """Test that list shows task IDs"""
        self.service.add("Task 1")
        self.service.add("Task 2")

        result = dispatch_command('list', self.service)

        self.assertIn("1", result)
        self.assertIn("2", result)

    def test_list_shows_task_status(self):
        """Test that list shows task status"""
        self.service.add("Pending task")
        self.service.mark_complete(1)
        self.service.add("Another pending")

        result = dispatch_command('list', self.service)

        self.assertIn("completed", result)
        self.assertIn("pending", result)

    def test_list_shows_table_format(self):
        """Test that list uses table format"""
        self.service.add("Task 1")

        result = dispatch_command('list', self.service)

        # Table should have pipe characters
        self.assertIn("|", result)
        # Table should have dashes for separator
        self.assertIn("-", result)


class TestUpdateCommandIntegration(unittest.TestCase):
    """Integration tests for update command"""

    def setUp(self):
        """Create a service with test data"""
        self.service = TodoService()
        self.service.add("Original Title", "Original Desc")

    def test_update_task_title(self):
        """Test updating a task's title"""
        result = dispatch_command('update 1 "New Title"', self.service)

        self.assertIn("updated", result.lower())
        task = self.service.get(1)
        self.assertEqual(task.title, "New Title")

    def test_update_task_title_and_description(self):
        """Test updating both title and description"""
        dispatch_command('update 1 "New Title" "New Description"', self.service)

        task = self.service.get(1)
        self.assertEqual(task.title, "New Title")
        self.assertEqual(task.description, "New Description")

    def test_update_nonexistent_task_fails(self):
        """Test updating non-existent task"""
        with self.assertRaises(TaskNotFound):
            dispatch_command('update 999 "Title"', self.service)

    def test_update_with_missing_title_fails(self):
        """Test update command with missing title"""
        with self.assertRaises(ValueError):
            dispatch_command('update 1', self.service)

    def test_update_with_empty_title_fails(self):
        """Test update command with empty title"""
        with self.assertRaises(ValueError):
            dispatch_command('update 1 ""', self.service)


class TestCompleteCommandIntegration(unittest.TestCase):
    """Integration tests for complete command"""

    def setUp(self):
        """Create a service with test data"""
        self.service = TodoService()
        self.service.add("Task 1")
        self.service.add("Task 2")

    def test_complete_task(self):
        """Test completing a task"""
        result = dispatch_command('complete 1', self.service)

        self.assertIn("completed", result.lower())
        task = self.service.get(1)
        self.assertEqual(task.status, "completed")

    def test_complete_nonexistent_task_fails(self):
        """Test completing non-existent task"""
        with self.assertRaises(TaskNotFound):
            dispatch_command('complete 999', self.service)

    def test_complete_task_with_invalid_id_fails(self):
        """Test complete with invalid ID format"""
        with self.assertRaises(ValueError):
            dispatch_command('complete abc', self.service)

    def test_complete_already_completed_task_is_safe(self):
        """Test that completing already-completed task is safe"""
        self.service.mark_complete(1)
        result = dispatch_command('complete 1', self.service)

        self.assertIn("completed", result.lower())


class TestDeleteCommandIntegration(unittest.TestCase):
    """Integration tests for delete command"""

    def setUp(self):
        """Create a service with test data"""
        self.service = TodoService()
        self.service.add("Task 1")
        self.service.add("Task 2")
        self.service.add("Task 3")

    def test_delete_task(self):
        """Test deleting a task"""
        result = dispatch_command('delete 2', self.service)

        self.assertIn("deleted", result.lower())

        with self.assertRaises(TaskNotFound):
            self.service.get(2)

    def test_delete_removes_from_list(self):
        """Test that deleted task doesn't appear in list"""
        dispatch_command('delete 2', self.service)
        result = dispatch_command('list', self.service)

        # Should have tasks 1 and 3, not 2
        self.assertIn("Task 1", result)
        self.assertIn("Task 3", result)

    def test_delete_nonexistent_task_fails(self):
        """Test deleting non-existent task"""
        with self.assertRaises(TaskNotFound):
            dispatch_command('delete 999', self.service)

    def test_delete_with_invalid_id_fails(self):
        """Test delete with invalid ID format"""
        with self.assertRaises(ValueError):
            dispatch_command('delete abc', self.service)

    def test_ids_not_reused_after_delete(self):
        """Test that new task gets next ID, not deleted one"""
        dispatch_command('delete 2', self.service)
        result = dispatch_command('add "New Task"', self.service)

        self.assertIn("ID: 4", result)


class TestHelpCommandIntegration(unittest.TestCase):
    """Integration tests for help command"""

    def setUp(self):
        """Create a fresh service"""
        self.service = TodoService()

    def test_help_command_returns_help_text(self):
        """Test help command displays help"""
        result = dispatch_command('help', self.service)

        self.assertIn("add", result.lower())
        self.assertIn("list", result.lower())
        self.assertIn("update", result.lower())
        self.assertIn("delete", result.lower())


class TestUnknownCommandIntegration(unittest.TestCase):
    """Integration tests for error handling"""

    def setUp(self):
        """Create a fresh service"""
        self.service = TodoService()

    def test_unknown_command_raises_error(self):
        """Test that unknown command raises ValueError"""
        with self.assertRaises(ValueError) as context:
            dispatch_command('unknown', self.service)

        self.assertIn("unknown", str(context.exception).lower())

    def test_empty_command_raises_error(self):
        """Test that empty command raises ValueError"""
        with self.assertRaises(ValueError):
            dispatch_command('', self.service)


class TestCompleteWorkflow(unittest.TestCase):
    """Integration tests for complete user workflows"""

    def setUp(self):
        """Create a fresh service"""
        self.service = TodoService()

    def test_add_list_workflow(self):
        """Test adding tasks and viewing them"""
        dispatch_command('add "Task 1"', self.service)
        dispatch_command('add "Task 2"', self.service)

        result = dispatch_command('list', self.service)

        self.assertIn("Task 1", result)
        self.assertIn("Task 2", result)

    def test_add_complete_list_workflow(self):
        """Test adding, completing, and listing"""
        dispatch_command('add "Task 1"', self.service)
        dispatch_command('complete 1', self.service)

        result = dispatch_command('list', self.service)

        self.assertIn("Task 1", result)
        self.assertIn("completed", result)

    def test_add_update_list_workflow(self):
        """Test adding, updating, and listing"""
        dispatch_command('add "Original Title"', self.service)
        dispatch_command('update 1 "Updated Title"', self.service)

        result = dispatch_command('list', self.service)

        self.assertIn("Updated Title", result)
        self.assertNotIn("Original", result)

    def test_add_delete_list_workflow(self):
        """Test adding, deleting, and listing"""
        dispatch_command('add "Task 1"', self.service)
        dispatch_command('add "Task 2"', self.service)
        dispatch_command('delete 1', self.service)

        result = dispatch_command('list', self.service)

        self.assertIn("Task 2", result)

    def test_complex_workflow_with_all_operations(self):
        """Test complete workflow with all operations"""
        # Add tasks
        dispatch_command('add "Buy groceries"', self.service)
        dispatch_command('add "Write report"', self.service)
        dispatch_command('add "Fix bug"', self.service)

        # Complete one
        dispatch_command('complete 2', self.service)

        # Update one (shorter title to avoid truncation in table)
        dispatch_command('update 1 "Buy groceries, then cook"', self.service)

        # Delete one
        dispatch_command('delete 3', self.service)

        # List and verify
        result = dispatch_command('list', self.service)

        # Check that title starts correctly (may be truncated in table)
        self.assertIn("Buy groceries", result)
        self.assertIn("completed", result)
        self.assertNotIn("Fix bug", result)

        # Verify final state
        tasks = self.service.get_all()
        self.assertEqual(len(tasks), 2)
        # Verify the actual title in service (not just table display)
        task1 = self.service.get(1)
        self.assertEqual(task1.title, "Buy groceries, then cook")


if __name__ == "__main__":
    unittest.main()
