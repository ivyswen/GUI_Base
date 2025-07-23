"""
自动更新模块
提供完整的应用程序自动更新功能
"""

from .update_manager import UpdateManager
from .update_checker import UpdateChecker, VersionInfo
from .update_dialogs import UpdateDialog, DownloadDialog
from .file_manager import FileManager

__all__ = [
    'UpdateManager',
    'UpdateChecker',
    'VersionInfo',
    'UpdateDialog',
    'DownloadDialog',
    'FileManager'
]

__version__ = '1.0.0'
__author__ = 'GUI Base Template'
__description__ = '自动更新功能模块'
