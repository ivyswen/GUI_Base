"""
工具模块
包含全局可用的工具和组件
"""

from .logger import get_logger, app_logger, update_logger
from .config import app_config

__all__ = [
    'get_logger',
    'app_logger',
    'update_logger',
    'app_config'
]

__version__ = '1.0.0'
__author__ = 'GUI Base Template'
__description__ = '工具组件模块'
