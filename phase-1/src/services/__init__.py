"""Application services for Todo operations"""

import sys
import os

# Ensure src directory is in path for module execution (python -m src.cli.main)
_src_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _src_dir not in sys.path:
    sys.path.insert(0, _src_dir)

from .todo_service import TodoService

__all__ = ["TodoService"]
