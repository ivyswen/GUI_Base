"""
工具模块
包含全局可用的工具和组件
"""

from .logger import get_logger, app_logger, update_logger
from .config import app_config
from .exception_handler import setup_exception_handler, get_exception_handler
from .theme import setup_theme_manager, get_theme_manager
from .notification import setup_notification_manager, get_notification_manager
from .system_tray import SystemTray
from .plugin_manager import setup_plugin_manager, get_plugin_manager

__all__ = [
    'get_logger',
    'app_logger',
    'update_logger',
    'app_config',
    'setup_exception_handler',
    'get_exception_handler',
    'setup_theme_manager',
    'get_theme_manager',
    'setup_notification_manager',
    'get_notification_manager',
    'SystemTray',
    'setup_plugin_manager',
    'get_plugin_manager'
]

__version__ = '1.0.0'
__author__ = 'GUI Base Template'
__description__ = '工具组件模块'
