"""
自动更新模块
提供完整的应用程序自动更新功能
"""

from .config import app_config
from .update_manager import UpdateManager
from .update_checker import UpdateChecker, VersionInfo
from .update_dialogs import UpdateDialog, DownloadDialog
from .file_manager import FileManager
from .logger import get_logger, app_logger, update_logger

__all__ = [
    'app_config',
    'UpdateManager',
    'UpdateChecker',
    'VersionInfo',
    'UpdateDialog',
    'DownloadDialog',
    'FileManager',
    'get_logger',
    'app_logger',
    'update_logger'
]

__version__ = '1.0.0'
__author__ = 'GUI Base Template'
__description__ = '自动更新功能模块'
