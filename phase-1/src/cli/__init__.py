"""CLI interface and command handlers"""

import sys
import os

# Ensure src directory is in path for module execution (python -m src.cli.main)
_src_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _src_dir not in sys.path:
    sys.path.insert(0, _src_dir)

from .commands import handle_add, handle_list, handle_update, handle_complete, handle_delete, handle_help

__all__ = ["handle_add", "handle_list", "handle_update", "handle_complete", "handle_delete", "handle_help"]
