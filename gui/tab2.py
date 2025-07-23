"""
文本编辑器模块
包含文本编辑功能和相关操作
"""

from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit)
from .base_tab import BaseTab


class TextEditorTab(BaseTab):
    """文本编辑器Tab"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.text_edit = None
        self.init_ui()
    
    def init_ui(self):
        """初始化用户界面"""
        layout = QVBoxLayout()
        
        # 标题
        title_label = QLabel("文本编辑器")
        title_label.setStyleSheet("margin: 10px;")
        self.apply_subtitle_font(title_label)
        
        # 文本编辑区域
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("在这里输入文本...")
        
        # 按钮区域
        button_layout = QHBoxLayout()
        
        clear_button = QPushButton("清空")
        clear_button.clicked.connect(self.clear_text)
        clear_button.setStyleSheet(self.get_button_style("warning"))
        
        sample_button = QPushButton("插入示例文本")
        sample_button.clicked.connect(self.insert_sample_text)
        sample_button.setStyleSheet(self.get_button_style("default"))
        
        button_layout.addWidget(clear_button)
        button_layout.addWidget(sample_button)
        button_layout.addStretch()
        
        layout.addWidget(title_label)
        layout.addWidget(self.text_edit)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def clear_text(self):
        """清空文本"""
        if self.text_edit:
            self.text_edit.clear()
            self.update_status_bar("文本已清空", 2000)
    
    def insert_sample_text(self):
        """插入示例文本"""
        sample_text = (
            "这是一个示例文本。\n\n"
            "您可以在这里编辑文本，使用菜单栏的复制和粘贴功能。\n\n"
            "这个GUI模板包含了基础的界面元素，"
            "您可以根据需要进行扩展和修改。"
        )
        if self.text_edit:
            self.text_edit.setPlainText(sample_text)
            self.update_status_bar("已插入示例文本", 2000)
    
    def copy_text(self):
        """复制文本"""
        if self.text_edit:
            self.text_edit.copy()
            self.update_status_bar("已复制", 2000)
    
    def paste_text(self):
        """粘贴文本"""
        if self.text_edit:
            self.text_edit.paste()
            self.update_status_bar("已粘贴", 2000)
    
    def get_text_edit(self):
        """获取文本编辑器实例，供主窗口使用"""
        return self.text_edit
