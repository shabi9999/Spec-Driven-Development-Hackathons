# Implementation Plan: In-Memory Python Console Todo App

**Branch**: `001-console-todo-app` | **Date**: 2026-01-01 | **Spec**: [specs/001-console-todo-app/spec.md](spec.md)
**Input**: Feature specification from Phase I Console App (5 CRUD features via CLI, in-memory storage)

**Note**: This plan defines architecture, component design, and CLI interface for Phase I. Implementation via `/sp.implement` will generate all code with 80%+ test coverage.

## Summary

Build a deterministic, in-memory Python console application that implements five core Todo CRUD operations (add, view, update, complete, delete) via a command-line interface. Architecture enforces clear separation of concerns: domain logic (Task model + TodoService), application services (CRUD actions), and interface layer (CLI input/output). All business logic is fully testable; no external dependencies beyond Python standard library. Output is human-readable tables; input is simple space-separated commands.

## Technical Context

**Language/Version**: Python 3.13 (per Phase I constitution)
**Primary Dependencies**: None (standard library only)
**Storage**: In-memory (Python list of dictionaries or custom Task objects)
**Testing**: unittest (Python standard library)
**Target Platform**: Linux/macOS/Windows console
**Project Type**: Single CLI application
**Performance Goals**: Immediate command response (<100ms), support 1000 tasks in memory
**Constraints**: Zero external dependencies, single-user, single-session (no persistence)
**Scale/Scope**: 5 CLI commands, ~10 service methods, ~500 LOC application code, ~500 LOC test code

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Core Principles Alignment

- ✅ **I. Spec-Driven Development**: Plan follows approved spec; gates all implementation. No code without spec approval.
- ✅ **II. Deterministic Core Logic**: TodoService operations are pure, deterministic, fully testable. No hidden state or side effects.
- ✅ **III. Simplicity First**: Single console app, minimal design. No abstractions beyond core CRUD. No hypothetical Phase II features.
- ✅ **IV. Clear Separation of Concerns**: Domain logic (Task model) separate from services (TodoService) separate from CLI (command handlers). Layer changes isolated.
- ✅ **V. AI as Assistant**: No AI in Phase I. Plan explicitly excludes AI decision-making. N/A at this stage.
- ✅ **VI. No Phase Breaks Previous Guarantees**: Phase I in-memory CRUD guarantees will remain valid when Phase II adds persistence.
- ✅ **VII. Documentation Parity**: Plan includes quickstart.md and CLI command documentation. All public methods documented.

### Phase I Standards Alignment

- ✅ Language: Python 3.13 (matches Phase I standard)
- ✅ Storage: In-memory only (matches Phase I standard)
- ✅ Interface: Console CLI (matches Phase I standard)
- ✅ Dependencies: Standard library only (matches Phase I standard)
- ✅ Testing: unittest for all business logic (matches Phase I standard)

### Testing Discipline

- ✅ Unit tests for TodoService (CRUD operations)
- ✅ Integration tests for CLI + Service interaction
- ✅ Target 80%+ coverage on business logic
- ✅ All tests deterministic and runnable in isolation

**GATE RESULT**: ✅ **PASS** — Plan fully compliant with constitution. No violations or deviations.

## Project Structure

### Documentation (this feature)

```text
specs/001-console-todo-app/
├── spec.md                          # Feature specification (APPROVED)
├── plan.md                          # This file (implementation plan)
├── checklists/
│   └── requirements.md              # Spec quality validation
├── research.md                      # Phase 0 output (not needed - no unknowns)
├── data-model.md                    # Phase 1 output (below, inline)
├── quickstart.md                    # Phase 1 output (below, inline)
├── contracts/
│   └── cli-interface.md             # Phase 1 output (below, inline)
└── tasks.md                         # Phase 2 output (/sp.tasks - TBD)
```

### Source Code (repository root)

```text
src/
├── __init__.py                      # Package marker
├── models/
│   ├── __init__.py
│   └── task.py                      # Task entity (id, title, status, created_at)
├── services/
│   ├── __init__.py
│   └── todo_service.py              # TodoService (add, get, update, delete, list, complete)
├── cli/
│   ├── __init__.py
│   └── commands.py                  # CLI command handlers (add, list, update, complete, delete, help)
├── main.py                          # Application entry point and command loop

tests/
├── __init__.py
├── unit/
│   ├── __init__.py
│   ├── test_task_model.py           # Task entity tests
│   └── test_todo_service.py         # TodoService CRUD tests
└── integration/
    ├── __init__.py
    └── test_cli_workflow.py         # CLI + Service integration tests

pyproject.toml                       # Project metadata, Python version, tool config
README.md                            # Phase I quickstart and feature documentation
```

**Structure Decision**: Single project structure (Option 1) — Phase I is a single CLI application with no frontend/backend separation. Models → Services → CLI layers enable clean separation and testability.

## Complexity Tracking

No constitution violations. All design decisions justified by Phase I standards and simplicity principle. No additional complexity justification required.

---

# Design Details (Phase 1)

## Data Model (data-model.md)

### Task Entity

```python
class Task:
    id: int                    # Auto-incrementing, unique identifier (starts at 1)
    title: str                 # Required, non-empty string
    description: str           # Optional, defaults to empty string
    status: str                # "pending" or "completed" (enum)
    created_at: datetime       # ISO 8601 timestamp, auto-generated on creation
```

**Validation**:
- `title` must be non-empty (trimmed)
- `status` must be one of: "pending", "completed"
- `id` assigned sequentially; never reused after deletion
- `created_at` immutable after creation

**State Transitions**:
- New task → status = "pending"
- mark_complete() → status changes to "completed" (idempotent)
- title/description updatable at any time
- Deletion removes task entirely (no soft delete)

### TodoService (In-Memory Store)

```python
class TodoService:
    __tasks: List[Task]              # Internal list, private
    __next_id: int                   # Auto-increment counter

    def add(title: str, description: str = "") -> Task
    def get(id: int) -> Task or raises TaskNotFound
    def get_all() -> List[Task]
    def update(id: int, title: str, description: str = "") -> Task or raises TaskNotFound
    def delete(id: int) -> None or raises TaskNotFound
    def mark_complete(id: int) -> Task or raises TaskNotFound
```

**Deterministic Guarantees**:
- All operations are pure functions (same input → same output)
- No side effects beyond task state mutation
- Errors are explicit (TaskNotFound exception, validation errors)
- Order of operations is reproducible

---

## CLI Interface Design (contracts/cli-interface.md)

### Command Syntax

```
todo> add "Task title" [optional description]
todo> list
todo> update <id> "New title" [optional description]
todo> complete <id>
todo> delete <id>
todo> help
todo> exit
```

### Command Specifications

#### ADD
```
Syntax: add "<title>" ["description"]
Purpose: Create a new task
Input validation:
  - title required, non-empty
  - description optional
Returns:
  - Confirmation message with task ID and status
Error handling:
  - Missing title → "Error: Task title required"
  - Empty title → "Error: Task title cannot be empty"
```

#### LIST
```
Syntax: list
Purpose: Display all tasks in table format
Input validation: None
Returns:
  - Table with columns: [ID] [Title] [Status] [Created]
  - "No tasks" if list is empty
  - Completed tasks marked with [✓] or "completed"
Error handling: None
```

#### UPDATE
```
Syntax: update <id> "<new_title>" ["new_description"]
Purpose: Modify task title/description
Input validation:
  - ID must be integer
  - title required, non-empty
Returns:
  - Confirmation with updated task
Error handling:
  - Invalid ID format → "Error: Invalid task ID"
  - Task not found → "Error: Task not found"
  - Missing title → "Error: Task title required"
```

#### COMPLETE
```
Syntax: complete <id>
Purpose: Mark task as completed
Input validation:
  - ID must be integer
Returns:
  - Confirmation message with updated status
Error handling:
  - Invalid ID format → "Error: Invalid task ID"
  - Task not found → "Error: Task not found"
  - Already completed → Show current status (idempotent)
```

#### DELETE
```
Syntax: delete <id>
Purpose: Remove task from list
Input validation:
  - ID must be integer
Returns:
  - Confirmation: "Task <id> deleted"
Error handling:
  - Invalid ID format → "Error: Invalid task ID"
  - Task not found → "Error: Task not found"
```

#### HELP
```
Syntax: help
Purpose: Display command reference
Returns: List of all commands with brief descriptions
```

#### EXIT
```
Syntax: exit or quit
Purpose: Terminate application
Returns: None (application exits)
```

### Output Format

**Table Format** (for list command):
```
ID | Title                    | Status    | Created
---|--------------------------|-----------|------------------
1  | Buy groceries           | pending   | 2026-01-01 10:00:00
2  | Write report            | completed | 2026-01-01 09:30:00
3  | Fix bug in login        | pending   | 2026-01-01 11:15:00
```

**Error Format**:
```
Error: [Brief description]
Hint: [How to fix or get help]
```

**Confirmation Format**:
```
✓ Task created (ID: 1)
✓ Task completed
```

---

## Quickstart (quickstart.md)

### Installation

```bash
# Clone repository
git clone <repo-url>
cd Hackthon-2-phase-1

# Ensure Python 3.13+ installed
python --version

# Run application
python src/main.py
```

### Basic Usage

```bash
$ python src/main.py
Welcome to Todo App
todo> add "Buy groceries"
✓ Task created (ID: 1)

todo> add "Write report" "Due by Friday"
✓ Task created (ID: 2)

todo> list
ID | Title            | Status  | Created
---|------------------|---------|------------------
1  | Buy groceries    | pending | 2026-01-01 10:00
2  | Write report     | pending | 2026-01-01 10:01

todo> complete 1
✓ Task 1 marked as completed

todo> list
ID | Title            | Status    | Created
---|------------------|-----------|------------------
1  | Buy groceries    | completed | 2026-01-01 10:00
2  | Write report     | pending   | 2026-01-01 10:01

todo> delete 2
✓ Task 2 deleted

todo> list
ID | Title            | Status    | Created
---|------------------|-----------|------------------
1  | Buy groceries    | completed | 2026-01-01 10:00

todo> exit
Goodbye!
```

### Testing

```bash
# Run all tests
python -m unittest discover -s tests -p "test_*.py" -v

# Run only unit tests
python -m unittest discover -s tests/unit -p "test_*.py" -v

# Run with coverage
python -m coverage run -m unittest discover -s tests -p "test_*.py"
python -m coverage report
```

---

## Implementation Milestones

1. **Module 1 - Domain Model** (`src/models/task.py`)
   - Task class with attributes and validation
   - Task factory for creation with auto-IDs
   - Passing: 100% unit test coverage

2. **Module 2 - Service Layer** (`src/services/todo_service.py`)
   - TodoService with CRUD operations
   - In-memory task store
   - Error handling (TaskNotFound exceptions)
   - Passing: 100% unit test coverage

3. **Module 3 - CLI Handler** (`src/cli/commands.py`)
   - Command parser for user input
   - Command handlers (add, list, update, complete, delete, help)
   - Output formatting (tables, error messages)
   - Passing: Integration tests for each command

4. **Module 4 - Main Application** (`src/main.py`)
   - Command loop (read → parse → execute → display)
   - Error handling and user feedback
   - Graceful exit
   - Passing: End-to-end integration tests

5. **Test Suite** (`tests/`)
   - Unit tests: Task model + TodoService (100 tests, ~800 LOC)
   - Integration tests: CLI workflows (50 tests, ~400 LOC)
   - Target: 80%+ overall coverage

---

## Success Criteria (from spec)

- ✅ **SC-001**: All 5 features independently testable
- ✅ **SC-002**: Zero external dependencies (standard library only)
- ✅ **SC-003**: Full workflow in <30 seconds
- ✅ **SC-004**: Clear error messages
- ✅ **SC-005**: Clean, readable code (PEP 8)
- ✅ **SC-006**: 80%+ coverage on business logic

---

## Next Steps

1. **Phase 0 (Research)**: None required—no unknowns or clarifications needed
2. **Phase 1 (Design)**: ✅ Complete (this document)
3. **Phase 2 (Tasks)**: Run `/sp.tasks` to generate testable implementation tasks
4. **Phase 3 (Implementation)**: Run `/sp.implement` to generate all code via Claude Code
