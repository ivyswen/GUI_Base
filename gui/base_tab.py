"""
基础Tab类
提供所有Tab页面的共享功能和样式
"""

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QObject


class BaseTab(QWidget):
    """基础Tab类，提供共享的功能和样式"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
    
    def get_button_style(self, style_type="default"):
        """获取按钮样式，确保视觉一致性
        
        Args:
            style_type: 样式类型，可选值：
                - "default": 默认样式
                - "primary": 主要按钮样式（蓝色）
                - "success": 成功按钮样式（绿色）
                - "warning": 警告按钮样式（橙色）
                - "danger": 危险按钮样式（红色）
        """
        base_style = """
            QPushButton {
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 12px;
                font-weight: 500;
                min-width: 80px;
                min-height: 28px;
                border: 1px solid;
            }
            QPushButton:disabled {
                background-color: #f8f8f8;
                border: 1px solid #e0e0e0;
                color: #a0a0a0;
            }
        """
        
        if style_type == "primary":
            return base_style + """
                QPushButton {
                    background-color: #007acc;
                    border-color: #005a9e;
                    color: white;
                }
                QPushButton:hover {
                    background-color: #005a9e;
                    border-color: #004578;
                }
                QPushButton:pressed {
                    background-color: #004578;
                    border-color: #003456;
                }
            """
        elif style_type == "success":
            return base_style + """
                QPushButton {
                    background-color: #28a745;
                    border-color: #1e7e34;
                    color: white;
                }
                QPushButton:hover {
                    background-color: #1e7e34;
                    border-color: #155724;
                }
                QPushButton:pressed {
                    background-color: #155724;
                    border-color: #0d4017;
                }
            """
        elif style_type == "warning":
            return base_style + """
                QPushButton {
                    background-color: #ffc107;
                    border-color: #d39e00;
                    color: #212529;
                }
                QPushButton:hover {
                    background-color: #e0a800;
                    border-color: #b08800;
                }
                QPushButton:pressed {
                    background-color: #d39e00;
                    border-color: #a08000;
                }
            """
        elif style_type == "danger":
            return base_style + """
                QPushButton {
                    background-color: #dc3545;
                    border-color: #bd2130;
                    color: white;
                }
                QPushButton:hover {
                    background-color: #c82333;
                    border-color: #a71e2a;
                }
                QPushButton:pressed {
                    background-color: #bd2130;
                    border-color: #9c1e2a;
                }
            """
        else:  # default
            return base_style + """
                QPushButton {
                    background-color: #f0f0f0;
                    border-color: #c0c0c0;
                    color: #333333;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                    border-color: #a0a0a0;
                }
                QPushButton:pressed {
                    background-color: #d0d0d0;
                    border-color: #808080;
                }
            """
    
    def update_status_bar(self, message, timeout=2000):
        """更新状态栏消息
        
        Args:
            message: 要显示的消息
            timeout: 消息显示时间（毫秒）
        """
        if self.main_window and hasattr(self.main_window, 'status_bar'):
            self.main_window.status_bar.showMessage(message, timeout)
