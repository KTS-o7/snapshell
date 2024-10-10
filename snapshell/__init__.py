# snapshell/__init__.py
from .cli import main
from .llm_api import LLMClient
from .utils import create_database, update_database, save_command_suggestion, fetch_system_info ,print_color , view_history, clear_history
from .package_managers import detect_package_manager

__all__ = [
    'main', 'LLMClient',
    'create_database', 'update_database', 'save_command_suggestion',
    'fetch_system_info', 'detect_package_manager', 'print_color', 
    'view_history', 'clear_history'
]