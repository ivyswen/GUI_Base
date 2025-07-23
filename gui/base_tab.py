"""
基础Tab类
提供所有Tab页面的共享功能和样式
"""

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QObject
from utils.display import apply_font_to_widget
from utils.styles import get_button_style


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
        return get_button_style(style_type)
    
    def update_status_bar(self, message, timeout=2000):
        """更新状态栏消息

        Args:
            message: 要显示的消息
            timeout: 消息显示时间（毫秒）
        """
        if self.main_window and hasattr(self.main_window, 'statusBar'):
            self.main_window.statusBar().showMessage(message, timeout)

    def apply_title_font(self, widget):
        """为控件应用标题字体"""
        apply_font_to_widget(widget, font_size=14, bold=True)

    def apply_subtitle_font(self, widget):
        """为控件应用副标题字体"""
        apply_font_to_widget(widget, font_size=12, bold=True)

    def apply_body_font(self, widget):
        """为控件应用正文字体"""
        apply_font_to_widget(widget, font_size=9)

    def apply_small_font(self, widget):
        """为控件应用小字体"""
        apply_font_to_widget(widget, font_size=8)
