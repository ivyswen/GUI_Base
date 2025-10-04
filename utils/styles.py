"""
通用样式工具模块
提供统一的UI样式定义，供所有组件使用
支持深色和浅色主题
"""

from typing import Optional


def _get_theme_manager():
    """获取主题管理器（延迟导入避免循环依赖）"""
    try:
        from .theme import get_theme_manager
        return get_theme_manager()
    except (ImportError, RuntimeError):
        # 主题管理器未初始化或导入失败，返回 None
        return None


def _is_dark_theme() -> bool:
    """判断当前是否为深色主题"""
    theme_manager = _get_theme_manager()
    if theme_manager:
        return theme_manager.is_dark_theme()
    return False


def get_button_style(style_type="default", theme: Optional[str] = None):
    """获取按钮样式，确保视觉一致性

    Args:
        style_type: 样式类型，可选值：
            - "default": 默认样式（浅灰）
            - "primary": 主要按钮样式（蓝色）
            - "secondary": 次要按钮样式（深灰）
            - "success": 成功按钮样式（绿色）
            - "info": 信息按钮样式（青色）
            - "warning": 警告按钮样式（橙色）
            - "danger": 危险按钮样式（红色）
            - "light": 浅色按钮样式（白色）
            - "dark": 深色按钮样式（黑色）
            - "purple": 紫色按钮样式
            - "pink": 粉色按钮样式
            - "indigo": 靛蓝按钮样式
            - "teal": 青绿按钮样式
        theme: 主题类型，可选值：
            - None: 使用当前主题（默认）
            - "light": 强制使用浅色主题样式
            - "dark": 强制使用深色主题样式
    """
    # 确定是否使用深色主题
    if theme is None:
        is_dark = _is_dark_theme()
    else:
        is_dark = (theme == "dark")

    # 基础样式
    if is_dark:
        base_style = """
            QPushButton {
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 12px;
                font-weight: 500;
                min-width: 60px;
                min-height: 20px;
                border: 1px solid;
            }
            QPushButton:disabled {
                background-color: #2a2a2a;
                border: 1px solid #3c3c3c;
                color: #808080;
            }
        """
    else:
        base_style = """
            QPushButton {
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 12px;
                font-weight: 500;
                min-width: 60px;
                min-height: 20px;
                border: 1px solid;
            }
            QPushButton:disabled {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                color: #6c757d;
            }
        """
    
    if style_type == "primary":
        return base_style + """
            QPushButton {
                background-color: #007bff;
                border-color: #0056b3;
                color: white;
            }
            QPushButton:hover {
                background-color: #0056b3;
                border-color: #004085;
            }
            QPushButton:pressed {
                background-color: #004085;
                border-color: #002752;
            }
            QPushButton:disabled {
                background-color: #6c9bd1;
                border: 1px solid #5a8bc4;
                color: #ffffff;
                opacity: 0.6;
            }
        """
    elif style_type == "secondary":
        return base_style + """
            QPushButton {
                background-color: #6c757d;
                border-color: #495057;
                color: white;
            }
            QPushButton:hover {
                background-color: #495057;
                border-color: #343a40;
            }
            QPushButton:pressed {
                background-color: #343a40;
                border-color: #212529;
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
            QPushButton:disabled {
                background-color: #7bc97e;
                border: 1px solid #6bb76e;
                color: #ffffff;
                opacity: 0.6;
            }
        """
    elif style_type == "info":
        return base_style + """
            QPushButton {
                background-color: #17a2b8;
                border-color: #117a8b;
                color: white;
            }
            QPushButton:hover {
                background-color: #117a8b;
                border-color: #0c5460;
            }
            QPushButton:pressed {
                background-color: #0c5460;
                border-color: #062c33;
            }
            QPushButton:disabled {
                background-color: #7bc3d1;
                border: 1px solid #6bb6c7;
                color: #ffffff;
                opacity: 0.6;
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
            QPushButton:disabled {
                background-color: #ffdb6b;
                border: 1px solid #e6c757;
                color: #6c757d;
                opacity: 0.6;
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
    elif style_type == "light":
        return base_style + """
            QPushButton {
                background-color: #f8f9fa;
                border-color: #dee2e6;
                color: #212529;
            }
            QPushButton:hover {
                background-color: #e9ecef;
                border-color: #adb5bd;
            }
            QPushButton:pressed {
                background-color: #dee2e6;
                border-color: #6c757d;
            }
        """
    elif style_type == "dark":
        return base_style + """
            QPushButton {
                background-color: #343a40;
                border-color: #212529;
                color: white;
            }
            QPushButton:hover {
                background-color: #212529;
                border-color: #16181b;
            }
            QPushButton:pressed {
                background-color: #16181b;
                border-color: #0a0c0d;
            }
        """
    elif style_type == "purple":
        return base_style + """
            QPushButton {
                background-color: #6f42c1;
                border-color: #5a32a3;
                color: white;
            }
            QPushButton:hover {
                background-color: #5a32a3;
                border-color: #4c2a85;
            }
            QPushButton:pressed {
                background-color: #4c2a85;
                border-color: #3e2167;
            }
        """
    elif style_type == "pink":
        return base_style + """
            QPushButton {
                background-color: #e83e8c;
                border-color: #d91a72;
                color: white;
            }
            QPushButton:hover {
                background-color: #d91a72;
                border-color: #c51162;
            }
            QPushButton:pressed {
                background-color: #c51162;
                border-color: #a91e4f;
            }
        """
    elif style_type == "indigo":
        return base_style + """
            QPushButton {
                background-color: #6610f2;
                border-color: #520dc2;
                color: white;
            }
            QPushButton:hover {
                background-color: #520dc2;
                border-color: #4209a3;
            }
            QPushButton:pressed {
                background-color: #4209a3;
                border-color: #320785;
            }
        """
    elif style_type == "teal":
        return base_style + """
            QPushButton {
                background-color: #20c997;
                border-color: #1aa179;
                color: white;
            }
            QPushButton:hover {
                background-color: #1aa179;
                border-color: #148a64;
            }
            QPushButton:pressed {
                background-color: #148a64;
                border-color: #0e6b4f;
            }
        """
    else:  # default
        if is_dark:
            return base_style + """
                QPushButton {
                    background-color: #3c3c3c;
                    border-color: #555555;
                    color: #e0e0e0;
                }
                QPushButton:hover {
                    background-color: #4a4a4a;
                    border-color: #666666;
                }
                QPushButton:pressed {
                    background-color: #2d2d2d;
                    border-color: #444444;
                }
                QPushButton:disabled {
                    background-color: #2a2a2a;
                    border: 1px solid #3c3c3c;
                    color: #808080;
                    opacity: 0.6;
                }
            """
        else:
            return base_style + """
                QPushButton {
                    background-color: #f8f9fa;
                    border-color: #ced4da;
                    color: #495057;
                }
                QPushButton:hover {
                    background-color: #e9ecef;
                    border-color: #adb5bd;
                }
                QPushButton:pressed {
                    background-color: #dee2e6;
                    border-color: #6c757d;
                }
                QPushButton:disabled {
                    background-color: #f8f9fa;
                    border: 1px solid #dee2e6;
                    color: #6c757d;
                    opacity: 0.6;
                }
            """


def get_dialog_button_style(style_type="default", theme: Optional[str] = None):
    """获取对话框按钮样式（稍大一些的按钮）

    Args:
        style_type: 样式类型，与 get_button_style 相同
        theme: 主题类型，可选值：
            - None: 使用当前主题（默认）
            - "light": 强制使用浅色主题样式
            - "dark": 强制使用深色主题样式
    """
    # 确定是否使用深色主题
    if theme is None:
        is_dark = _is_dark_theme()
    else:
        is_dark = (theme == "dark")

    # 基础样式
    if is_dark:
        base_style = """
            QPushButton {
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 12px;
                font-weight: 500;
                min-width: 80px;
                min-height: 24px;
                border: 1px solid;
            }
            QPushButton:disabled {
                background-color: #2a2a2a;
                border: 1px solid #3c3c3c;
                color: #808080;
            }
        """
    else:
        base_style = """
            QPushButton {
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 12px;
                font-weight: 500;
                min-width: 80px;
                min-height: 24px;
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
    else:  # default
        if is_dark:
            return base_style + """
                QPushButton {
                    background-color: #3c3c3c;
                    border-color: #555555;
                    color: #e0e0e0;
                }
                QPushButton:hover {
                    background-color: #4a4a4a;
                    border-color: #666666;
                }
                QPushButton:pressed {
                    background-color: #2d2d2d;
                    border-color: #444444;
                }
            """
        else:
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


# 其他常用样式
def get_group_box_style(theme: Optional[str] = None):
    """获取分组框样式

    Args:
        theme: 主题类型，可选值：
            - None: 使用当前主题（默认）
            - "light": 强制使用浅色主题样式
            - "dark": 强制使用深色主题样式
    """
    # 确定是否使用深色主题
    if theme is None:
        is_dark = _is_dark_theme()
    else:
        is_dark = (theme == "dark")

    if is_dark:
        return """
            QGroupBox {
                font-weight: bold;
                border: 2px solid #3c3c3c;
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
                color: #e0e0e0;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """
    else:
        return """
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """


def get_table_style(theme: Optional[str] = None):
    """获取表格样式

    Args:
        theme: 主题类型，可选值：
            - None: 使用当前主题（默认）
            - "light": 强制使用浅色主题样式
            - "dark": 强制使用深色主题样式
    """
    # 确定是否使用深色主题
    if theme is None:
        is_dark = _is_dark_theme()
    else:
        is_dark = (theme == "dark")

    if is_dark:
        return """
            QTableWidget {
                gridline-color: #3c3c3c;
                background-color: #2d2d2d;
                alternate-background-color: #252525;
                color: #e0e0e0;
            }
            QTableWidget::item {
                padding: 5px;
                border: none;
            }
            QTableWidget::item:selected {
                background-color: #0d6efd;
                color: white;
            }
            QHeaderView::section {
                background-color: #3c3c3c;
                padding: 5px;
                border: 1px solid #555555;
                font-weight: bold;
                color: #e0e0e0;
            }
        """
    else:
        return """
            QTableWidget {
                gridline-color: #d0d0d0;
                background-color: white;
                alternate-background-color: #f8f8f8;
            }
            QTableWidget::item {
                padding: 5px;
                border: none;
            }
            QTableWidget::item:selected {
                background-color: #007acc;
                color: white;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                padding: 5px;
                border: 1px solid #d0d0d0;
                font-weight: bold;
            }
        """


def get_label_style(theme: Optional[str] = None):
    """获取标签样式

    Args:
        theme: 主题类型，可选值：
            - None: 使用当前主题（默认）
            - "light": 强制使用浅色主题样式
            - "dark": 强制使用深色主题样式
    """
    # 确定是否使用深色主题
    if theme is None:
        is_dark = _is_dark_theme()
    else:
        is_dark = (theme == "dark")

    if is_dark:
        return """
            QLabel {
                color: #e0e0e0;
            }
        """
    else:
        return """
            QLabel {
                color: #212529;
            }
        """


def get_text_edit_style(theme: Optional[str] = None):
    """获取文本编辑器样式

    Args:
        theme: 主题类型，可选值：
            - None: 使用当前主题（默认）
            - "light": 强制使用浅色主题样式
            - "dark": 强制使用深色主题样式
    """
    # 确定是否使用深色主题
    if theme is None:
        is_dark = _is_dark_theme()
    else:
        is_dark = (theme == "dark")

    if is_dark:
        return """
            QTextEdit, QPlainTextEdit {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #3c3c3c;
                selection-background-color: #0d6efd;
                selection-color: white;
            }
        """
    else:
        return """
            QTextEdit, QPlainTextEdit {
                background-color: #ffffff;
                color: #212529;
                border: 1px solid #ced4da;
                selection-background-color: #007bff;
                selection-color: white;
            }
        """


def get_spinbox_style(theme: Optional[str] = None):
    """获取数字输入框样式

    Args:
        theme: 主题类型，可选值：
            - None: 使用当前主题（默认）
            - "light": 强制使用浅色主题样式
            - "dark": 强制使用深色主题样式
    """
    # 确定是否使用深色主题
    if theme is None:
        is_dark = _is_dark_theme()
    else:
        is_dark = (theme == "dark")

    if is_dark:
        return """
            QSpinBox {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #3c3c3c;
                padding: 4px;
                border-radius: 4px;
            }
            QSpinBox:hover {
                border: 1px solid #555555;
            }
            QSpinBox:focus {
                border: 1px solid #0d6efd;
            }
        """
    else:
        return """
            QSpinBox {
                background-color: #ffffff;
                color: #212529;
                border: 1px solid #ced4da;
                padding: 4px;
                border-radius: 4px;
            }
            QSpinBox:hover {
                border: 1px solid #86b7fe;
            }
            QSpinBox:focus {
                border: 1px solid #0d6efd;
            }
        """


def get_combobox_style(theme: Optional[str] = None):
    """获取下拉框样式

    Args:
        theme: 主题类型，可选值：
            - None: 使用当前主题（默认）
            - "light": 强制使用浅色主题样式
            - "dark": 强制使用深色主题样式
    """
    # 确定是否使用深色主题
    if theme is None:
        is_dark = _is_dark_theme()
    else:
        is_dark = (theme == "dark")

    if is_dark:
        return """
            QComboBox {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #3c3c3c;
                padding: 4px;
                border-radius: 4px;
                min-width: 100px;
            }
            QComboBox:hover {
                border: 1px solid #555555;
            }
            QComboBox:focus {
                border: 1px solid #0d6efd;
            }
            QComboBox QAbstractItemView {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #3c3c3c;
                selection-background-color: #0d6efd;
                selection-color: white;
            }
        """
    else:
        return """
            QComboBox {
                background-color: #ffffff;
                color: #212529;
                border: 1px solid #ced4da;
                padding: 4px;
                border-radius: 4px;
                min-width: 100px;
            }
            QComboBox:hover {
                border: 1px solid #86b7fe;
            }
            QComboBox:focus {
                border: 1px solid #0d6efd;
            }
            QComboBox QAbstractItemView {
                background-color: #ffffff;
                color: #212529;
                border: 1px solid #ced4da;
                selection-background-color: #007bff;
                selection-color: white;
            }
        """


def get_message_box_style(theme: Optional[str] = None):
    """获取消息框样式

    Args:
        theme: 主题类型，可选值：
            - None: 使用当前主题（默认）
            - "light": 强制使用浅色主题样式
            - "dark": 强制使用深色主题样式
    """
    # 确定使用的主题
    if theme is None:
        is_dark = _is_dark_theme()
    else:
        is_dark = (theme == "dark")

    if is_dark:
        return """
            QMessageBox {
                background-color: #2d2d2d;
                color: #e0e0e0;
            }
            QMessageBox QLabel {
                color: #e0e0e0;
                background-color: transparent;
            }
            QMessageBox QPushButton {
                background-color: #3d3d3d;
                color: #e0e0e0;
                border: 1px solid #555555;
                border-radius: 4px;
                padding: 5px 15px;
                min-width: 60px;
            }
            QMessageBox QPushButton:hover {
                background-color: #4d4d4d;
                border-color: #666666;
            }
            QMessageBox QPushButton:pressed {
                background-color: #2d2d2d;
            }
        """
    else:
        return """
            QMessageBox {
                background-color: #ffffff;
                color: #212529;
            }
            QMessageBox QLabel {
                color: #212529;
                background-color: transparent;
            }
            QMessageBox QPushButton {
                background-color: #f0f0f0;
                color: #212529;
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 5px 15px;
                min-width: 60px;
            }
            QMessageBox QPushButton:hover {
                background-color: #e0e0e0;
                border-color: #adb5bd;
            }
            QMessageBox QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """
