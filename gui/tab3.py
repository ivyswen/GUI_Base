"""
设置页面模块
包含各种设置选项和配置功能
"""

from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox)
from .base_tab import BaseTab


class SettingsTab(BaseTab):
    """设置页面Tab"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """初始化用户界面"""
        layout = QVBoxLayout()
        
        # 标题
        title_label = QLabel("设置")
        title_label.setStyleSheet("font-size: 14px; font-weight: bold; margin: 10px;")
        
        # 设置内容
        settings_label = QLabel(
            "这里可以添加各种设置选项：\n\n"
            "• 主题设置\n"
            "• 语言设置\n"
            "• 字体设置\n"
            "• 其他配置选项\n\n"
            "根据您的需求自定义此页面。"
        )
        settings_label.setStyleSheet("font-size: 12px; margin: 20px;")
        
        # 示例设置按钮
        button_layout = QHBoxLayout()
        
        theme_button = QPushButton("切换主题")
        theme_button.clicked.connect(self.toggle_theme)
        theme_button.setStyleSheet(self.get_button_style("primary"))
        
        language_button = QPushButton("语言设置")
        language_button.clicked.connect(self.language_settings)
        language_button.setStyleSheet(self.get_button_style("default"))
        
        font_button = QPushButton("字体设置")
        font_button.clicked.connect(self.font_settings)
        font_button.setStyleSheet(self.get_button_style("default"))
        
        reset_button = QPushButton("重置设置")
        reset_button.clicked.connect(self.reset_settings)
        reset_button.setStyleSheet(self.get_button_style("danger"))
        
        button_layout.addWidget(theme_button)
        button_layout.addWidget(language_button)
        button_layout.addWidget(font_button)
        button_layout.addWidget(reset_button)
        button_layout.addStretch()
        
        layout.addWidget(title_label)
        layout.addWidget(settings_label)
        layout.addLayout(button_layout)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def toggle_theme(self):
        """切换主题"""
        self.update_status_bar("主题切换功能待实现", 2000)
    
    def language_settings(self):
        """语言设置"""
        self.update_status_bar("语言设置功能待实现", 2000)
    
    def font_settings(self):
        """字体设置"""
        self.update_status_bar("字体设置功能待实现", 2000)
    
    def reset_settings(self):
        """重置设置"""
        reply = QMessageBox.question(
            self, 
            "确认重置",
            "确定要重置所有设置吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.update_status_bar("设置已重置", 2000)
        else:
            self.update_status_bar("取消重置", 2000)
