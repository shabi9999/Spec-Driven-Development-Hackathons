# In-Memory Python Console Todo App

**Phase I of AI-Native Todo Application** - A spec-driven, deterministic todo application built entirely in Python with zero external dependencies.

## Quick Start

### Installation

```bash
# Ensure Python 3.13+ installed
python --version

# Clone and navigate to repository
cd Hackthon-2-phase-1

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
1  | Buy groceries    | pending | 2026-01-02 01:30
2  | Write report     | pending | 2026-01-02 01:30

todo> complete 1
✓ Task 1 marked as completed

todo> list
ID | Title            | Status    | Created
---|------------------|-----------|------------------
1  | Buy groceries    | completed | 2026-01-02 01:30
2  | Write report     | pending   | 2026-01-02 01:30

todo> update 2 "Write report and presentation"
✓ Task 2 updated

todo> delete 2
✓ Task 2 deleted

todo> exit
Goodbye!
```

## Commands

| Command | Syntax | Purpose |
|---------|--------|---------|
| add | `add "title" ["description"]` | Create a new task |
| list | `list` | Display all tasks in table format |
| update | `update <id> "title" ["description"]` | Modify task title/description |
| complete | `complete <id>` | Mark task as completed |
| delete | `delete <id>` | Remove task permanently |
| help | `help` | Show command reference |
| exit | `exit` | Quit application |

## Testing

```bash
# Run all tests
python -m unittest discover -s tests -p "test_*.py" -v

# Run only unit tests
python -m unittest discover -s tests/unit -p "test_*.py" -v

# Run integration tests
python -m unittest discover -s tests/integration -p "test_*.py" -v

# Run with coverage report
python -m coverage run -m unittest discover -s tests -p "test_*.py"
python -m coverage report
```

## Architecture

### Three-Layer Design

**Domain Models** (`src/models/`)
- Task entity with validation and state management
- TaskNotFound exception for error handling

**Services** (`src/services/`)
- TodoService with in-memory task store
- CRUD operations: add, get, update, delete, list, mark_complete
- Deterministic, pure functions for all operations

**CLI Interface** (`src/cli/` + `src/main.py`)
- Command parser and input validation
- Command handlers for each operation
- Formatted output (tables, messages, errors)
- Main event loop

### In-Memory Storage

- Tasks stored in a Python list
- Auto-incrementing IDs (never reused after deletion)
- Single-user, single-session application
- All data lost when app exits (by design - Phase I)

## Key Features

✅ **Spec-Driven Development**
- Implementation follows strict specification
- All features have acceptance criteria
- Tests written before code (TDD)

✅ **Deterministic Core Logic**
- No hidden state or side effects
- Same input always produces same output
- Fully testable operations

✅ **Zero External Dependencies**
- Python standard library only
- No pip packages required
- Fully portable

✅ **80%+ Test Coverage**
- Unit tests for all domain logic
- Integration tests for CLI workflows
- Both are passing

## Constraints

- **Storage**: In-memory only (no persistence to files/database)
- **Users**: Single-user application
- **Concurrency**: Single-threaded, no concurrent operations
- **Features**: Basic CRUD only (no tags, priorities, due dates)
- **Scope**: Phase I only (see constitution for future phases)

## Project Structure

```
src/
├── models/
│   └── task.py              # Task entity, TaskNotFound exception
├── services/
│   └── todo_service.py      # TodoService (CRUD operations)
├── cli/
│   └── commands.py          # Command handlers, input parsing, output formatting
└── main.py                  # Application entry point, command loop

tests/
├── unit/
│   ├── test_task_model.py   # Task entity tests
│   └── test_todo_service.py # TodoService CRUD tests
└── integration/
    └── test_cli_workflow.py # Full CLI workflow tests

pyproject.toml               # Python 3.13+ configuration
README.md                    # This file
```

## Phase I Success Criteria

- ✅ All 5 core features (add, view, update, complete, delete) implemented
- ✅ Zero external dependencies
- ✅ Clean, readable Python code (PEP 8)
- ✅ 80%+ test coverage on business logic
- ✅ Full workflow completes in <30 seconds
- ✅ Clear error messages for all edge cases

## Next Phase (Phase II)

Future enhancement will add:
- Persistent database storage (PostgreSQL)
- REST API (FastAPI)
- Web frontend (Next.js)
- User authentication
- Advanced features (tags, priorities, due dates)

*See constitution.md for complete multi-phase roadmap*

## Development

Built with [Spec-Kit Plus](https://github.com/anthropics/claude-code) and [Claude Code](https://claude.com/claude-code), following spec-driven development (SDD) principles.

Created: 2026-01-01
Status: Phase I Complete ✅
