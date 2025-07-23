"""
欢迎页面模块
包含欢迎信息、程序介绍和快速操作功能
"""

from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QPushButton)
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox
from .base_tab import BaseTab


class WelcomeTab(BaseTab):
    """欢迎页面Tab"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """初始化用户界面"""
        layout = QVBoxLayout()
        
        # 欢迎标题
        welcome_label = QLabel("欢迎使用GUI Base Template!")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 20px;")
        
        # 描述文本
        description_label = QLabel(
            "这是一个基础的GUI程序模板，包含以下功能：\n\n"
            "• 窗口自动居中显示\n"
            "• 完整的菜单栏系统\n"
            "• 多标签页界面\n"
            "• 应用程序和窗口图标\n"
            "• 状态栏显示\n\n"
            "您可以基于此模板开发自己的GUI应用程序。"
        )
        description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description_label.setStyleSheet("font-size: 12px; margin: 20px;")
        
        # 快速操作按钮
        quick_actions_layout = QHBoxLayout()
        
        start_button = QPushButton("开始使用")
        start_button.clicked.connect(self.start_using)
        start_button.setStyleSheet(self.get_button_style("primary"))
        
        help_button = QPushButton("查看帮助")
        help_button.clicked.connect(self.show_help)
        help_button.setStyleSheet(self.get_button_style("default"))
        
        demo_button = QPushButton("运行演示")
        demo_button.clicked.connect(self.run_demo)
        demo_button.setStyleSheet(self.get_button_style("success"))
        
        quick_actions_layout.addStretch()
        quick_actions_layout.addWidget(start_button)
        quick_actions_layout.addWidget(help_button)
        quick_actions_layout.addWidget(demo_button)
        quick_actions_layout.addStretch()
        
        layout.addWidget(welcome_label)
        layout.addWidget(description_label)
        layout.addLayout(quick_actions_layout)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def start_using(self):
        """开始使用 - 切换到文本编辑标签页"""
        if self.main_window and hasattr(self.main_window, 'tab_widget'):
            self.main_window.tab_widget.setCurrentIndex(1)  # 切换到文本编辑标签页
            self.update_status_bar("已切换到文本编辑页面", 2000)
    
    def show_help(self):
        """显示帮助信息"""
        help_text = (
            "GUI Base Template 使用帮助\n\n"
            "1. 欢迎页面：查看程序介绍和快速操作\n"
            "2. 文本编辑：进行文本编辑和操作\n"
            "3. 设置页面：配置程序选项\n\n"
            "使用菜单栏可以进行文件操作和其他功能。\n"
            "状态栏会显示当前操作的反馈信息。"
        )
        QMessageBox.information(self, "使用帮助", help_text)
    
    def run_demo(self):
        """运行演示"""
        if self.main_window and hasattr(self.main_window, 'tab_widget'):
            self.main_window.tab_widget.setCurrentIndex(1)  # 切换到文本编辑标签页
            
            # 插入演示文本到文本编辑器
            demo_text = (
                "🎉 欢迎体验GUI Base Template演示！\n\n"
                "这是一个功能完整的GUI程序模板，包含：\n\n"
                "✅ 现代化的用户界面设计\n"
                "✅ 完整的菜单系统\n"
                "✅ 多标签页布局\n"
                "✅ 统一的按钮样式\n"
                "✅ 状态栏反馈\n"
                "✅ 图标支持\n\n"
                "您可以基于此模板快速开发自己的应用程序！\n\n"
                "试试使用菜单栏的功能，或者点击下方的按钮。"
            )
            
            # 获取文本编辑器并设置演示文本
            if hasattr(self.main_window, 'text_edit'):
                self.main_window.text_edit.setPlainText(demo_text)
            
            self.update_status_bar("演示已启动，请查看文本编辑页面", 3000)
