---
description: "Implementation tasks for In-Memory Python Console Todo App (Phase I)"
---

# Tasks: In-Memory Python Console Todo App

**Input**: Design documents from `specs/001-console-todo-app/`
**Prerequisites**: plan.md (approved), spec.md (approved), no external dependencies required

**Organization**: Tasks grouped by user story (US1-US5) to enable independent implementation and testing. Each story is independently testable and deliverable as an MVP increment.

**Tests**: Test tasks included following TDD approach (write tests first, fail, then implement). Unit + integration tests targeting 80%+ coverage.

## Format: `- [ ] [ID] [P?] [Story] Description`

- **[ID]**: Task identifier (T001, T002, etc.)
- **[P]**: Can run in parallel (different files, no shared dependencies)
- **[Story]**: User story label (US1, US2, etc.) - shows which story owns this task
- File paths: Exact locations for each file to create/modify

---

# Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and directory structure

**Duration**: ~1 hour
**Status**: Required before any feature work

- [ ] T001 Create project root structure: `src/`, `tests/`, `pyproject.toml`, `README.md`
- [ ] T002 [P] Initialize `src/__init__.py`, `src/models/__init__.py`, `src/services/__init__.py`, `src/cli/__init__.py`
- [ ] T003 [P] Initialize test directories: `tests/__init__.py`, `tests/unit/__init__.py`, `tests/integration/__init__.py`
- [ ] T004 Create `pyproject.toml` with Python 3.13 requirement, no external dependencies
- [ ] T005 Create `README.md` with Phase I quickstart (copy from plan.md Quickstart section)

**Checkpoint**: Project structure initialized, ready for core modules

---

# Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core domain model that MUST complete before any user story work

**⚠️ CRITICAL**: All subsequent user stories depend on Task model and TodoService being complete and tested

**Duration**: ~2 hours

## Task Model & Service (Shared by all stories)

- [ ] T006 Create Task class in `src/models/task.py`:
  - Attributes: id (int), title (str), description (str, optional), status (str: "pending"/"completed"), created_at (datetime)
  - Validation: title must be non-empty (trimmed), status enum validation, id immutable
  - Methods: `__init__`, `__repr__`, `to_dict()` for display
  - 100% unit test coverage targeting 20 tests

- [ ] T007 Create TaskNotFound exception class in `src/models/task.py`
  - Custom exception for when task ID doesn't exist
  - Used by all CRUD operations

- [ ] T008 Create TodoService class in `src/services/todo_service.py`:
  - Private attributes: `__tasks` (list), `__next_id` (int counter)
  - Constructor: Initialize empty list, next_id = 1
  - Methods: `add()`, `get()`, `get_all()`, `update()`, `delete()`, `mark_complete()`
  - Deterministic: Same input → same output, no hidden state
  - Error handling: Raise TaskNotFound for missing IDs
  - 100% unit test coverage targeting 80+ tests for CRUD operations

- [ ] T009 Create test file `tests/unit/test_task_model.py`:
  - Test Task creation with valid inputs
  - Test Task validation (empty title, invalid status)
  - Test Task immutability (id, created_at cannot change)
  - Test Task to_dict() for display
  - **CRITICAL**: Write tests FIRST, they should FAIL before T006 implementation

- [ ] T010 Create test file `tests/unit/test_todo_service.py`:
  - Test add() - creates task with auto-ID, returns Task
  - Test get() - retrieves task by ID, raises TaskNotFound for invalid ID
  - Test get_all() - returns all tasks, empty list when no tasks
  - Test update() - modifies title/description, raises TaskNotFound for invalid ID
  - Test delete() - removes task, raises TaskNotFound for invalid ID, IDs not reused
  - Test mark_complete() - changes status to completed, idempotent, raises TaskNotFound for invalid ID
  - **CRITICAL**: Write tests FIRST, they should FAIL before T008 implementation

**Checkpoint**: All foundational tests written (failing), Task model and TodoService ready for implementation by remaining tasks. User story work can now begin in parallel.

---

# Phase 3: User Story 1 - Add a New Task (Priority: P1) 🎯 MVP

**Goal**: Users can create new tasks with title and optional description via CLI "add" command

**Independent Test**: Launch app → `add "Task title"` → verify task appears in list with ID and pending status

**User Story**: Add a New Task
**Spec Reference**: spec.md User Story 1
**Acceptance Criteria**:
1. Task created with "pending" status when added
2. Task assigned unique, auto-incrementing ID
3. Task timestamp (created_at) auto-generated
4. Empty/missing title rejected with error message
5. Task immediately visible in list command

### Tests for User Story 1

> **WRITE TESTS FIRST**: All tests below must be written and FAIL before implementation begins

- [ ] T011 [P] [US1] Create test file `tests/unit/test_add_command.py`:
  - Test valid add command creates task
  - Test invalid add command (missing title) shows error
  - Test added task appears in get_all()
  - Test task ID increments correctly
  - **Must fail before T014 implementation**

- [ ] T012 [P] [US1] Create integration test file `tests/integration/test_add_workflow.py`:
  - Test full workflow: parse "add 'title'" command → service add → display confirmation
  - Test error case: parse "add" with no title → display error message
  - Test newly added task visible in list command
  - **Must fail before T015 implementation**

### Implementation for User Story 1

- [ ] T013 [US1] Implement add command handler in `src/cli/commands.py`:
  - Function: `handle_add(args: List[str], service: TodoService) -> str`
  - Parse command: `add "title" ["description"]`
  - Validate: title required, non-empty
  - Call: `service.add(title, description)`
  - Return: Confirmation message with task ID and status
  - Error: Clear error message if validation fails

- [ ] T014 [US1] Implement input parsing for add command in `src/cli/commands.py`:
  - Parse quoted arguments: `add "Buy groceries" "eggs, milk"` → ("Buy groceries", "eggs, milk")
  - Handle single-quoted and double-quoted strings
  - Trim whitespace
  - Helper: `parse_quoted_args(command_string) -> List[str]`

- [ ] T015 [US1] Create main command loop and CLI controller in `src/main.py`:
  - Initialize TodoService instance
  - Command loop: Read user input → parse command → dispatch to handler
  - Valid commands: add, list, update, complete, delete, help, exit
  - Invalid command: Show help or "unknown command" error
  - Graceful exit on "exit" or EOF

### Validation for User Story 1

- [ ] T016 [US1] Run all tests for User Story 1:
  - `python -m unittest tests/unit/test_add_command.py -v`
  - `python -m unittest tests/integration/test_add_workflow.py -v`
  - Verify: All tests pass, 100% coverage of add functionality

- [ ] T017 [US1] Manual validation of User Story 1:
  - Start app: `python src/main.py`
  - Add task: `add "Buy groceries"`
  - Verify: Confirmation message with ID and status
  - Add another: `add "Write report" "Due Friday"`
  - Verify: Second task has ID 2
  - Run list: `list` → Both tasks visible
  - Test error: `add` (no title) → Error message shown
  - Exit: `exit`

**Checkpoint**: User Story 1 (Add Task) fully functional and tested independently. MVP is 50% complete.

---

# Phase 4: User Story 2 - View All Tasks (Priority: P1)

**Goal**: Users can view all tasks in formatted table showing ID, title, status, and creation date

**Independent Test**: Create multiple tasks → `list` → verify formatted table displays all tasks correctly

**User Story**: View All Tasks
**Spec Reference**: spec.md User Story 2
**Acceptance Criteria**:
1. Empty task list shows "No tasks" message
2. Tasks displayed in table format: ID | Title | Status | Created
3. Completed tasks show "completed" status
4. Timestamps in ISO format (YYYY-MM-DD HH:MM:SS)
5. Table aligned and readable

### Tests for User Story 2

> **WRITE TESTS FIRST**: All tests below must be written and FAIL before implementation begins

- [ ] T018 [P] [US2] Create test file `tests/unit/test_list_command.py`:
  - Test list with no tasks shows "No tasks"
  - Test list with one task shows single row
  - Test list with three tasks shows all three
  - Test pending status displays correctly
  - Test completed status displays correctly
  - **Must fail before T021 implementation**

- [ ] T019 [P] [US2] Create integration test file `tests/integration/test_list_workflow.py`:
  - Test: Add 3 tasks → list → verify table format
  - Test: Add task → complete task → list → verify status shows completed
  - Test: List output columns (ID, Title, Status, Created)
  - **Must fail before T022 implementation**

### Implementation for User Story 2

- [ ] T020 [US2] Implement list command handler in `src/cli/commands.py`:
  - Function: `handle_list(service: TodoService) -> str`
  - Call: `service.get_all()` to retrieve all tasks
  - Format output as table if tasks exist
  - Return: "No tasks" message if list empty
  - Return: Formatted table otherwise

- [ ] T021 [US2] Implement table formatter in `src/cli/commands.py`:
  - Function: `format_task_table(tasks: List[Task]) -> str`
  - Columns: ID | Title | Status | Created
  - Column widths: ID=4, Title=25, Status=10, Created=19
  - Separator row with dashes
  - Status display: "pending" or "completed"
  - Timestamp format: "YYYY-MM-DD HH:MM:SS"
  - Align left for strings, right for ID

- [ ] T022 [US2] Wire list command to main loop in `src/main.py`:
  - Dispatch "list" command to `handle_list()`
  - Display formatted output to user

### Validation for User Story 2

- [ ] T023 [US2] Run all tests for User Story 2:
  - `python -m unittest tests/unit/test_list_command.py -v`
  - `python -m unittest tests/integration/test_list_workflow.py -v`
  - Verify: All tests pass, 100% coverage of list functionality

- [ ] T024 [US2] Manual validation of User Story 2:
  - Start app: `python src/main.py`
  - Test empty list: `list` → "No tasks" shown
  - Add 3 tasks: `add "Task 1"`, `add "Task 2"`, `add "Task 3"`
  - List all: `list` → Table with 3 rows, IDs 1-3, all pending
  - Complete one: `complete 1`
  - List again: `list` → Task 1 shows "completed", others "pending"
  - Verify column alignment and spacing

**Checkpoint**: User Story 2 (View Tasks) fully functional and tested independently. MVP is now 100% complete! (Users can add and view tasks)

---

# Phase 5: User Story 3 - Update a Task (Priority: P2)

**Goal**: Users can modify task title and description by ID via "update" command

**Independent Test**: Create task → `update 1 "New title"` → `list` shows updated title

**User Story**: Update a Task
**Spec Reference**: spec.md User Story 3
**Acceptance Criteria**:
1. Task updated with new title and/or description
2. Invalid ID shows "Task not found" error
3. Missing title shows error
4. Updated task immediately visible in list
5. Update is idempotent (same update twice = same result)

### Tests for User Story 3

> **WRITE TESTS FIRST**: All tests below must be written and FAIL before implementation begins

- [ ] T025 [P] [US3] Create test file `tests/unit/test_update_command.py`:
  - Test update valid ID with new title
  - Test update invalid ID shows error
  - Test update missing title shows error
  - Test updated title visible in get()
  - Test update with description
  - **Must fail before T028 implementation**

- [ ] T026 [P] [US3] Create integration test file `tests/integration/test_update_workflow.py`:
  - Test: Add task → update title → list shows updated
  - Test: Add task → update description → list shows updated
  - Test: Update nonexistent ID → error displayed
  - **Must fail before T029 implementation**

### Implementation for User Story 3

- [ ] T027 [US3] Implement update command handler in `src/cli/commands.py`:
  - Function: `handle_update(args: List[str], service: TodoService) -> str`
  - Parse: `update <id> "new title" ["new description"]`
  - Validate: ID is integer, title non-empty
  - Call: `service.update(id, title, description)`
  - Return: Confirmation with updated task
  - Error: Handle TaskNotFound and validation errors

- [ ] T028 [US3] Add update method tests in `tests/unit/test_todo_service.py`:
  - If not already included in T010, test update() separately
  - Test updating title changes task title
  - Test updating description changes task description
  - Test immutable fields (ID, created_at cannot change)
  - Test TaskNotFound raised for invalid ID

- [ ] T029 [US3] Wire update command to main loop in `src/main.py`:
  - Dispatch "update" command to `handle_update()`
  - Display confirmation or error to user

### Validation for User Story 3

- [ ] T030 [US3] Run all tests for User Story 3:
  - `python -m unittest tests/unit/test_update_command.py -v`
  - `python -m unittest tests/integration/test_update_workflow.py -v`
  - Verify: All tests pass, 100% coverage of update functionality

- [ ] T031 [US3] Manual validation of User Story 3:
  - Start app: `python src/main.py`
  - Add task: `add "Buy groceries"`
  - Update it: `update 1 "Buy groceries and cook dinner"`
  - List: `list` → Shows updated title
  - Update description: `update 1 "Buy all ingredients" "For tonight's dinner"`
  - List: `list` → Shows updated description
  - Test error: `update 999 "title"` → "Task not found" error
  - Test error: `update 1` → "title required" error

**Checkpoint**: User Story 3 (Update Task) fully functional. Core CRUD is now 75% complete.

---

# Phase 6: User Story 4 - Mark Task Complete (Priority: P2)

**Goal**: Users can mark tasks as completed via "complete" command, changing status from "pending" to "completed"

**Independent Test**: Create task → `complete 1` → `list` shows "completed" status

**User Story**: Mark Task Complete
**Spec Reference**: spec.md User Story 4
**Acceptance Criteria**:
1. Task status changes from "pending" to "completed"
2. Invalid ID shows "Task not found" error
3. Complete already-completed task shows confirmation (idempotent)
4. Completed status visible in list command
5. Completed tasks can still be updated or deleted

### Tests for User Story 4

> **WRITE TESTS FIRST**: All tests below must be written and FAIL before implementation begins

- [ ] T032 [P] [US4] Create test file `tests/unit/test_complete_command.py`:
  - Test complete valid ID changes status to completed
  - Test complete invalid ID shows error
  - Test complete already-completed task (idempotent)
  - Test mark_complete() returns updated task
  - **Must fail before T035 implementation**

- [ ] T033 [P] [US4] Create integration test file `tests/integration/test_complete_workflow.py`:
  - Test: Add task → complete → list shows completed
  - Test: Complete nonexistent ID → error displayed
  - Test: Add task → complete → complete again → no error
  - **Must fail before T036 implementation**

### Implementation for User Story 4

- [ ] T034 [US4] Implement complete command handler in `src/cli/commands.py`:
  - Function: `handle_complete(args: List[str], service: TodoService) -> str`
  - Parse: `complete <id>`
  - Validate: ID is integer
  - Call: `service.mark_complete(id)`
  - Return: Confirmation with updated task
  - Error: Handle TaskNotFound and validation errors

- [ ] T035 [US4] Add mark_complete method tests in `tests/unit/test_todo_service.py`:
  - If not already included in T010, test mark_complete() separately
  - Test mark_complete() changes status to "completed"
  - Test idempotent: marking completed task again is safe
  - Test TaskNotFound raised for invalid ID

- [ ] T036 [US4] Wire complete command to main loop in `src/main.py`:
  - Dispatch "complete" command to `handle_complete()`
  - Display confirmation or error to user

### Validation for User Story 4

- [ ] T037 [US4] Run all tests for User Story 4:
  - `python -m unittest tests/unit/test_complete_command.py -v`
  - `python -m unittest tests/integration/test_complete_workflow.py -v`
  - Verify: All tests pass, 100% coverage of complete functionality

- [ ] T038 [US4] Manual validation of User Story 4:
  - Start app: `python src/main.py`
  - Add 2 tasks: `add "Task 1"`, `add "Task 2"`
  - Complete task 1: `complete 1`
  - List: `list` → Task 1 shows "completed", Task 2 shows "pending"
  - Complete already-done: `complete 1` → Confirmation shown (no error)
  - Test error: `complete 999` → "Task not found" error
  - Test error: `complete abc` → "Invalid ID" error

**Checkpoint**: User Story 4 (Mark Complete) fully functional. Core CRUD is now 90% complete.

---

# Phase 7: User Story 5 - Delete a Task (Priority: P3)

**Goal**: Users can permanently remove tasks via "delete" command. Deleted tasks cannot be recovered.

**Independent Test**: Create task → `delete 1` → `list` does not show deleted task

**User Story**: Delete a Task
**Spec Reference**: spec.md User Story 5
**Acceptance Criteria**:
1. Task removed from list permanently
2. Invalid ID shows "Task not found" error
3. Deleted task no longer visible in list
4. Task IDs not reused after deletion (auto-increment continues)
5. Delete is idempotent (cannot delete already-deleted task)

### Tests for User Story 5

> **WRITE TESTS FIRST**: All tests below must be written and FAIL before implementation begins

- [ ] T039 [P] [US5] Create test file `tests/unit/test_delete_command.py`:
  - Test delete valid ID removes task
  - Test delete invalid ID shows error
  - Test deleted task not in get_all()
  - Test delete is not idempotent (second delete raises error)
  - **Must fail before T042 implementation**

- [ ] T040 [P] [US5] Create integration test file `tests/integration/test_delete_workflow.py`:
  - Test: Add 3 tasks → delete task 2 → list shows 1 and 3 only
  - Test: Delete nonexistent ID → error displayed
  - Test: Delete same ID twice → error on second attempt
  - **Must fail before T043 implementation**

### Implementation for User Story 5

- [ ] T041 [US5] Implement delete command handler in `src/cli/commands.py`:
  - Function: `handle_delete(args: List[str], service: TodoService) -> str`
  - Parse: `delete <id>`
  - Validate: ID is integer
  - Call: `service.delete(id)`
  - Return: Confirmation message
  - Error: Handle TaskNotFound and validation errors

- [ ] T042 [US5] Add delete method tests in `tests/unit/test_todo_service.py`:
  - If not already included in T010, test delete() separately
  - Test delete() removes task from list
  - Test delete() prevents ID reuse (next new task gets next ID, not deleted one)
  - Test TaskNotFound raised for already-deleted ID
  - Test TaskNotFound raised for never-existed ID

- [ ] T043 [US5] Wire delete command to main loop in `src/main.py`:
  - Dispatch "delete" command to `handle_delete()`
  - Display confirmation or error to user

### Validation for User Story 5

- [ ] T044 [US5] Run all tests for User Story 5:
  - `python -m unittest tests/unit/test_delete_command.py -v`
  - `python -m unittest tests/integration/test_delete_workflow.py -v`
  - Verify: All tests pass, 100% coverage of delete functionality

- [ ] T045 [US5] Manual validation of User Story 5:
  - Start app: `python src/main.py`
  - Add 3 tasks: `add "Task 1"`, `add "Task 2"`, `add "Task 3"`
  - List: `list` → All 3 visible with IDs 1-3
  - Delete task 2: `delete 2`
  - List: `list` → Only tasks 1 and 3 visible
  - Add new task: `add "Task 4"` → Gets ID 4 (not 2)
  - Test error: `delete 2` → "Task not found" error (already deleted)
  - Test error: `delete 999` → "Task not found" error

**Checkpoint**: User Story 5 (Delete Task) fully functional. ALL user stories now complete!

---

# Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Comprehensive testing, documentation, and final validation

**Duration**: ~2 hours

- [ ] T046 Implement help command in `src/cli/commands.py`:
  - Function: `handle_help() -> str`
  - Display all available commands with brief descriptions
  - Wire to main loop: dispatch "help" command

- [ ] T047 [P] Implement error handling in main loop (`src/main.py`):
  - Catch all exceptions from command handlers
  - Display user-friendly error messages
  - Continue command loop on error (no crash)
  - Show help hint on invalid command

- [ ] T048 [P] Add input validation and trimming in `src/cli/commands.py`:
  - Strip whitespace from user input
  - Handle empty commands (show help or prompt again)
  - Validate ID arguments are numeric
  - Consistent error message format across all commands

- [ ] T049 Create comprehensive unit test suite in `tests/unit/`:
  - Run: `python -m unittest discover -s tests/unit -p "test_*.py" -v`
  - Verify: All tests pass
  - Target: 80%+ code coverage
  - Report: `python -m coverage run -m unittest discover -s tests/unit && coverage report`

- [ ] T050 Create comprehensive integration test suite in `tests/integration/`:
  - Run: `python -m unittest discover -s tests/integration -p "test_*.py" -v`
  - Verify: All tests pass
  - Test complete workflows: add → list → update → complete → delete
  - Target: 80%+ overall coverage

- [ ] T051 Implement final documentation in `README.md`:
  - Installation instructions
  - Quick start example (copy from plan.md)
  - Command reference (help command output)
  - Testing instructions
  - Known limitations (in-memory only, single-session)
  - Phase I completion summary

- [ ] T052 Run complete validation suite:
  - All unit tests pass: `python -m unittest discover -s tests/unit -v`
  - All integration tests pass: `python -m unittest discover -s tests/integration -v`
  - Overall coverage >= 80%: `python -m coverage report`
  - Manual walkthrough of spec acceptance criteria
  - Code follows PEP 8: Check with `python -m py_compile src/**/*.py`

- [ ] T053 Manual end-to-end validation against spec:
  - Spec User Story 1 (Add): ✓ Can add tasks with title and optional description
  - Spec User Story 2 (View): ✓ Can view all tasks in formatted table
  - Spec User Story 3 (Update): ✓ Can update task title and description
  - Spec User Story 4 (Complete): ✓ Can mark tasks as completed
  - Spec User Story 5 (Delete): ✓ Can delete tasks
  - Edge Cases: ✓ Invalid commands, malformed input, missing fields, invalid IDs
  - Error Handling: ✓ All errors display clear messages with hints
  - Performance: ✓ All commands respond in < 100ms

**Checkpoint**: Phase I complete! All 5 user stories implemented, tested, and validated.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies - can start immediately
- **Phase 2 (Foundational)**: Depends on Setup completion
  - ⚠️ **BLOCKS ALL USER STORIES** - must complete before Phase 3+
- **Phase 3 (US1 - Add)**: Depends on Phase 2 completion - Can run independently
- **Phase 4 (US2 - View)**: Depends on Phase 2 completion - Can run in parallel with US1 (different files)
- **Phase 5 (US3 - Update)**: Depends on Phase 2 completion - Can run in parallel with US1/US2
- **Phase 6 (US4 - Complete)**: Depends on Phase 2 completion - Can run in parallel with US1/US2/US3
- **Phase 7 (US5 - Delete)**: Depends on Phase 2 completion - Can run in parallel with US1/US2/US3/US4
- **Phase 8 (Polish)**: Depends on all user stories (Phase 3-7) completion

### Within Phases

- **Phase 1 (Setup)**: Tasks T001-T005 sequential (structure must exist first)
- **Phase 2 (Foundational)**:
  - Tests (T009, T010) must be written FIRST before models/services
  - T006-T008 can run in parallel after tests exist
- **User Stories (Phase 3+)**:
  - Tests (marked [P]) can run in parallel
  - Models can run in parallel
  - Services depend on models being complete
  - Commands depend on services being complete
  - Integration depends on all components done

### Parallel Opportunities

**After Setup (Phase 1) completion**:
- Foundational model/service tests (T009, T010) can be written in parallel

**After Foundational (Phase 2) completion**:
- All 5 User Stories (Phase 3-7) can proceed in parallel by different developers:
  - Developer A: US1 (Add Task) - Tasks T011-T017
  - Developer B: US2 (View Tasks) - Tasks T018-T024
  - Developer C: US3 (Update Task) - Tasks T025-T031
  - Developer D: US4 (Complete Task) - Tasks T032-T038
  - Developer E: US5 (Delete Task) - Tasks T039-T045

**Within each User Story**:
- All tests (marked [P]) can be written in parallel
- Multiple command handlers can be implemented in parallel (different functions in same file)

---

## Parallel Example: Full Team Approach

```
Day 1 (4 hours):
  Team: Complete Phase 1 (Setup) - T001-T005
  → Project structure ready

Day 1-2 (6 hours):
  Team: Complete Phase 2 (Foundational) - T006-T010
  → Tests written (failing), Task model & TodoService defined
  → Foundation ready, user story work can begin

Day 2-3 (8 hours) - PARALLEL:
  Dev A: US1 (Add) - T011-T017       // 6-7 hours
  Dev B: US2 (View) - T018-T024      // 5-6 hours
  Dev C: US3 (Update) - T025-T031    // 5-6 hours
  Dev D: US4 (Complete) - T032-T038  // 5-6 hours
  Dev E: US5 (Delete) - T039-T045    // 5-6 hours

Day 3-4 (2-3 hours):
  Team: Phase 8 (Polish & Cross-cutting) - T046-T053
  → Final testing, documentation, validation

Total: ~24-28 developer-hours, ~3-4 calendar days with team

MVP (Just US1 + US2):
  Day 1: Phase 1 + Phase 2 (4-6 hours)
  Day 2: US1 + US2 (10-12 hours)
  Day 3: Polish (2-3 hours)
  Total: ~16-21 hours, ~2 calendar days
```

---

## Implementation Strategy

### Option A: MVP First (Recommended for Learning)

1. ✅ Complete Phase 1 (Setup) - ~1 hour
2. ✅ Complete Phase 2 (Foundational) - ~2 hours
3. ✅ Complete Phase 3 (US1 - Add Task) - ~3 hours
4. ✅ Complete Phase 4 (US2 - View Tasks) - ~2 hours
5. 🎯 **STOP and VALIDATE MVP**:
   - Users can add tasks ✓
   - Users can view all tasks ✓
   - Full workflow works: add → list ✓
   - Tests pass: 80%+ coverage ✓
   - Manual validation complete ✓
6. **Deploy/Demo MVP** (if ready)
7. Continue with Phase 5+ if time allows

**MVP Completion**: ~8-10 hours, provides full value for core workflow

### Option B: Full Feature (Sequential)

1. Complete Phase 1-2 (Setup + Foundation) - ~3 hours
2. Complete Phase 3 (US1) - ~3 hours → Test independently
3. Complete Phase 4 (US2) - ~2 hours → Test independently
4. Complete Phase 5 (US3) - ~3 hours → Test independently
5. Complete Phase 6 (US4) - ~3 hours → Test independently
6. Complete Phase 7 (US5) - ~3 hours → Test independently
7. Complete Phase 8 (Polish) - ~2 hours → Final validation

**Full Feature**: ~22-24 hours, all 5 CRUD operations fully tested

### Option C: Parallel Team (Most Efficient)

With 5 developers:
1. Everyone: Phase 1-2 together (Setup + Foundation) - ~3 hours
2. Parallel: Each dev takes one US (Phase 3-7) - ~5-6 hours each
3. Everyone: Phase 8 together (Polish) - ~2 hours

**Total Calendar Time**: ~9-10 hours with team, ~40-50 developer-hours

---

## Task Checklist Summary

- **Total Tasks**: 53
- **Setup Phase**: 5 tasks
- **Foundation Phase**: 6 tasks (must complete before user stories)
- **User Story 1 (Add)**: 7 tasks
- **User Story 2 (View)**: 7 tasks
- **User Story 3 (Update)**: 7 tasks
- **User Story 4 (Complete)**: 7 tasks
- **User Story 5 (Delete)**: 7 tasks
- **Polish Phase**: 8 tasks

**Test Coverage**:
- Unit tests: 14 test files (T009-T010, T011, T018, T025, T032, T039, plus existing)
- Integration tests: 10 test files (T012, T019, T026, T033, T040)
- Target: 80%+ code coverage on business logic

**Code Estimates**:
- Application code: ~500 LOC (models, services, CLI, main)
- Test code: ~500 LOC (unit + integration tests)
- Total: ~1000 LOC for complete Phase I

---

## Notes & Best Practices

- **✅ DO**: Write tests first (TDD), verify they FAIL before implementation
- **✅ DO**: Mark tests with [P] to enable parallel test writing
- **✅ DO**: Commit after each task or logical group completion
- **✅ DO**: Run tests frequently to catch regressions
- **✅ DO**: Stop at each checkpoint to validate story independently
- **✅ DO**: Follow exact file paths shown in tasks

- **❌ DON'T**: Skip tests or write them after code
- **❌ DON'T**: Create tasks that share the same file (merge into one task)
- **❌ DON'T**: Create cross-story dependencies that break independence
- **❌ DON'T**: Add features beyond spec (YAGNI principle)
- **❌ DON'T**: Skip validation/testing steps

**Spec References**:
- User stories: `specs/001-console-todo-app/spec.md`
- Architecture: `specs/001-console-todo-app/plan.md`
- Acceptance criteria: This file (tasks.md) + spec.md

**Success Criteria** (from spec, validated here):
- ✅ All 5 features independently implemented and testable
- ✅ Zero external dependencies (standard library only)
- ✅ Clean, readable code (PEP 8 compliant)
- ✅ 80%+ unit test coverage on business logic
- ✅ Clear error messages for all edge cases
- ✅ Full workflow completes in < 30 seconds
