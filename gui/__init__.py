"""
GUI模块
包含所有GUI相关的组件和页面
"""

from .base_tab import BaseTab
from .tab1 import WelcomeTab
from .tab2 import TextEditorTab
from .settings_tab import SettingsTab
from .error_dialog import ErrorDialog
from .toast import ToastWidget, ToastManager

__all__ = [
    'BaseTab',
    'WelcomeTab',
    'TextEditorTab',
    'SettingsTab',
    'ErrorDialog',
    'ToastWidget',
    'ToastManager'
]

__version__ = '1.0.0'
__author__ = 'GUI Base Template'
__description__ = 'GUI组件模块'
