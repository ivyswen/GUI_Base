"""
错误对话框组件
显示用户友好的错误信息和详细的技术信息
"""

import sys
import os
from pathlib import Path
from typing import Dict, Any

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QTextBrowser, QApplication
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon

from utils.styles import get_dialog_button_style
from utils.config import app_config


class ErrorDialog(QDialog):
    """错误对话框"""
    
    def __init__(self, error_info: Dict[str, Any], parent=None):
        """
        初始化错误对话框
        
        Args:
            error_info: 错误信息字典
            parent: 父窗口
        """
        super().__init__(parent)
        self.error_info = error_info
        self.details_visible = False
        self.init_ui()
    
    def init_ui(self):
        """初始化用户界面"""
        # 设置窗口属性
        self.setWindowTitle("程序错误")
        self.setMinimumWidth(600)
        self.setMinimumHeight(200)
        
        # 创建主布局
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 错误标题区域
        title_layout = QHBoxLayout()
        
        # 错误图标（使用系统图标或文本）
        icon_label = QLabel("❌")
        icon_font = QFont()
        icon_font.setPointSize(32)
        icon_label.setFont(icon_font)
        title_layout.addWidget(icon_label)
        
        # 错误消息
        message_layout = QVBoxLayout()
        
        error_title = QLabel("程序遇到了一个错误")
        error_title_font = QFont()
        error_title_font.setPointSize(14)
        error_title_font.setBold(True)
        error_title.setFont(error_title_font)
        
        error_type = QLabel(f"错误类型: {self.error_info.get('exception_type', 'Unknown')}")
        error_message = QLabel(f"错误信息: {self.error_info.get('exception_message', 'Unknown error')}")
        error_message.setWordWrap(True)
        
        message_layout.addWidget(error_title)
        message_layout.addWidget(error_type)
        message_layout.addWidget(error_message)
        message_layout.addStretch()
        
        title_layout.addLayout(message_layout, 1)
        layout.addLayout(title_layout)
        
        # 详细信息区域（初始隐藏）
        self.details_widget = QTextBrowser()
        self.details_widget.setReadOnly(True)
        self.details_widget.setMinimumHeight(200)
        self.details_widget.setVisible(False)
        
        # 构建详细信息文本
        details_text = self._build_details_text()
        self.details_widget.setPlainText(details_text)
        
        layout.addWidget(self.details_widget)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        # 显示/隐藏详细信息按钮
        self.details_button = QPushButton("显示详细信息 ▼")
        self.details_button.clicked.connect(self.toggle_details)
        self.details_button.setStyleSheet(get_dialog_button_style("default"))
        
        # 复制错误信息按钮
        copy_button = QPushButton("复制错误信息")
        copy_button.clicked.connect(self.copy_error_info)
        copy_button.setStyleSheet(get_dialog_button_style("default"))
        
        # 查看日志按钮
        log_button = QPushButton("查看日志文件")
        log_button.clicked.connect(self.open_log_file)
        log_button.setStyleSheet(get_dialog_button_style("default"))
        
        # 退出程序按钮
        exit_button = QPushButton("退出程序")
        exit_button.clicked.connect(self.exit_application)
        exit_button.setStyleSheet(get_dialog_button_style("danger"))
        
        button_layout.addWidget(self.details_button)
        button_layout.addWidget(copy_button)
        button_layout.addWidget(log_button)
        button_layout.addStretch()
        button_layout.addWidget(exit_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def _build_details_text(self) -> str:
        """
        构建详细信息文本
        
        Returns:
            格式化的详细信息文本
        """
        details = []
        details.append("=" * 60)
        details.append("错误详细信息")
        details.append("=" * 60)
        details.append("")
        
        # 基本信息
        details.append(f"时间: {self.error_info.get('timestamp', 'Unknown')}")
        details.append(f"应用程序: {self.error_info.get('app_name', 'Unknown')} v{self.error_info.get('app_version', 'Unknown')}")
        details.append(f"错误类型: {self.error_info.get('exception_type', 'Unknown')}")
        details.append(f"错误信息: {self.error_info.get('exception_message', 'Unknown')}")
        details.append("")
        
        # 系统信息
        details.append("-" * 60)
        details.append("系统信息")
        details.append("-" * 60)
        system_info = self.error_info.get('system_info', {})
        for key, value in system_info.items():
            details.append(f"{key}: {value}")
        details.append("")
        
        # 异常堆栈
        details.append("-" * 60)
        details.append("异常堆栈")
        details.append("-" * 60)
        details.append(self.error_info.get('traceback', 'No traceback available'))
        details.append("")
        details.append("=" * 60)
        
        return "\n".join(details)
    
    def toggle_details(self):
        """切换详细信息显示/隐藏"""
        self.details_visible = not self.details_visible
        self.details_widget.setVisible(self.details_visible)
        
        if self.details_visible:
            self.details_button.setText("隐藏详细信息 ▲")
            self.setMinimumHeight(500)
        else:
            self.details_button.setText("显示详细信息 ▼")
            self.setMinimumHeight(200)
    
    def copy_error_info(self):
        """复制错误信息到剪贴板"""
        try:
            clipboard = QApplication.clipboard()
            details_text = self._build_details_text()
            clipboard.setText(details_text)
            
            # 临时更改按钮文本以提供反馈
            sender = self.sender()
            if sender:
                original_text = sender.text()
                sender.setText("已复制 ✓")
                sender.setEnabled(False)
                
                # 2秒后恢复
                from PySide6.QtCore import QTimer
                QTimer.singleShot(2000, lambda: self._restore_button(sender, original_text))
        
        except Exception as e:
            print(f"复制错误信息失败: {e}")
    
    def _restore_button(self, button, text):
        """恢复按钮文本和状态"""
        if button:
            button.setText(text)
            button.setEnabled(True)
    
    def open_log_file(self):
        """打开日志文件所在目录"""
        try:
            # 获取日志目录
            is_frozen = getattr(sys, 'frozen', False)
            is_nuitka_compiled = hasattr(sys.modules.get(__name__.split('.')[0], sys.modules[__name__]), '__compiled__')
            is_compiled = is_frozen or is_nuitka_compiled
            
            if is_compiled:
                log_dir = Path(sys.executable).parent / "logs"
            else:
                log_dir = Path(__file__).parent.parent / "logs"
            
            # 打开目录
            if sys.platform == 'win32':
                os.startfile(str(log_dir))
            elif sys.platform == 'darwin':  # macOS
                os.system(f'open "{log_dir}"')
            else:  # Linux
                os.system(f'xdg-open "{log_dir}"')
        
        except Exception as e:
            print(f"打开日志目录失败: {e}")
    
    def exit_application(self):
        """退出应用程序"""
        self.accept()
        QApplication.quit()
        sys.exit(1)

