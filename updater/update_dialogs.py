"""
更新相关的对话框组件
包括更新提示对话框和下载进度对话框
"""

import os
import sys
from pathlib import Path
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QTextEdit, QProgressBar, QMessageBox
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from .update_checker import VersionInfo
from .file_manager import FileManager
from utils.logger import get_logger
from utils.config import app_config

logger = get_logger(__name__)


class UpdateDialog(QDialog):
    """更新提示对话框"""
    
    def __init__(self, version_info: VersionInfo, parent=None):
        super().__init__(parent)
        self.version_info = version_info
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle("发现新版本")
        self.setFixedSize(500, 400)
        self.setModal(True)
        
        # 主布局
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 标题
        title_label = QLabel(f"发现新版本 {self.version_info.version}")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 当前版本信息
        current_version_label = QLabel(f"当前版本: {app_config.current_version}")
        current_version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        current_version_label.setStyleSheet("color: #666666;")
        
        # 更新日志标签
        changelog_label = QLabel("更新内容:")
        changelog_font = QFont()
        changelog_font.setBold(True)
        changelog_label.setFont(changelog_font)
        
        # 更新日志内容
        self.changelog_text = QTextEdit()
        self.changelog_text.setPlainText(self.version_info.changelog or "暂无更新日志")
        self.changelog_text.setReadOnly(True)
        self.changelog_text.setMaximumHeight(150)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        # 立即更新按钮
        self.update_button = QPushButton("立即更新")
        self.update_button.clicked.connect(self.accept)
        self.update_button.setStyleSheet(self.get_button_style("primary"))
        
        # 稍后提醒按钮
        self.later_button = QPushButton("稍后提醒")
        self.later_button.clicked.connect(self.reject)
        self.later_button.setStyleSheet(self.get_button_style("default"))
        
        # 跳过此版本按钮
        self.skip_button = QPushButton("跳过此版本")
        self.skip_button.clicked.connect(self.skip_version)
        self.skip_button.setStyleSheet(self.get_button_style("default"))
        
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.later_button)
        button_layout.addWidget(self.skip_button)
        
        # 添加到主布局
        layout.addWidget(title_label)
        layout.addWidget(current_version_label)
        layout.addSpacing(10)
        layout.addWidget(changelog_label)
        layout.addWidget(self.changelog_text)
        layout.addSpacing(10)
        layout.addLayout(button_layout)
    
    def get_button_style(self, style_type="default"):
        """获取按钮样式"""
        base_style = """
            QPushButton {
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 12px;
                font-weight: 500;
                min-width: 80px;
                min-height: 32px;
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
    
    def skip_version(self):
        """跳过此版本"""
        # 这里可以保存跳过的版本信息
        self.done(2)  # 返回特殊值表示跳过


class DownloadDialog(QDialog):
    """下载进度对话框"""
    
    def __init__(self, version_info: VersionInfo, parent=None):
        super().__init__(parent)
        self.version_info = version_info
        self.file_manager = FileManager(self)
        self.download_path = ""
        self.init_ui()
        self.setup_connections()
    
    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle("下载更新")
        self.setFixedSize(450, 250)
        self.setModal(True)
        
        # 禁用关闭按钮
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowCloseButtonHint)
        
        # 主布局
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 标题
        title_label = QLabel(f"正在下载版本 {self.version_info.version}")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 状态标签
        self.status_label = QLabel("准备下载...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        
        # 进度信息标签
        self.progress_info_label = QLabel("0 / 0 MB")
        self.progress_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_info_label.setStyleSheet("color: #666666;")
        
        # 按钮布局
        button_layout = QHBoxLayout()
        
        # 取消按钮
        self.cancel_button = QPushButton("取消")
        self.cancel_button.clicked.connect(self.cancel_download)
        self.cancel_button.setStyleSheet(self.get_button_style("default"))
        
        button_layout.addStretch()
        button_layout.addWidget(self.cancel_button)
        button_layout.addStretch()
        
        # 添加到主布局
        layout.addWidget(title_label)
        layout.addWidget(self.status_label)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.progress_info_label)
        layout.addSpacing(10)
        layout.addLayout(button_layout)
    
    def get_button_style(self, style_type="default"):
        """获取按钮样式"""
        base_style = """
            QPushButton {
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 12px;
                font-weight: 500;
                min-width: 80px;
                min-height: 32px;
                border: 1px solid;
            }
        """
        
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
    
    def setup_connections(self):
        """设置信号连接"""
        self.file_manager.download_progress.connect(self.update_progress)
        self.file_manager.download_finished.connect(self.on_download_finished)
        self.file_manager.download_failed.connect(self.on_download_failed)
        self.file_manager.verification_finished.connect(self.on_verification_finished)
    
    def start_download(self):
        """开始下载"""
        logger.info(f"DownloadDialog: 开始下载 {self.version_info.version}")

        if not self.version_info.url:
            logger.error("下载链接为空")
            self.on_download_failed("下载链接为空")
            return

        logger.info(f"下载URL: {self.version_info.url}")
        self.status_label.setText("正在下载...")
        filename = f"update_{self.version_info.version}.zip"
        logger.info(f"下载文件名: {filename}")

        self.download_path = self.file_manager.download_file(self.version_info.url, filename)
        logger.info(f"下载路径: {self.download_path}")
    
    def update_progress(self, downloaded: int, total: int):
        """更新下载进度"""
        if total > 0:
            progress = int((downloaded / total) * 100)
            self.progress_bar.setValue(progress)
            
            # 转换为MB显示
            downloaded_mb = downloaded / (1024 * 1024)
            total_mb = total / (1024 * 1024)
            self.progress_info_label.setText(f"{downloaded_mb:.1f} / {total_mb:.1f} MB")
        else:
            # 未知大小的情况
            self.progress_info_label.setText(f"{downloaded / (1024 * 1024):.1f} MB")
    
    def on_download_finished(self, file_path: str):
        """下载完成处理"""
        self.status_label.setText("正在验证文件...")
        self.progress_bar.setRange(0, 0)  # 显示不确定进度
        
        # 开始文件校验
        if self.version_info.sha256_package:
            self.file_manager.verify_file_sha256(file_path, self.version_info.sha256_package)
        else:
            # 没有校验值，直接完成
            self.on_verification_finished(True)
    
    def on_verification_finished(self, success: bool):
        """文件校验完成"""
        if success:
            self.status_label.setText("下载完成，准备安装...")
            QTimer.singleShot(1000, self.start_installation)
        else:
            self.on_download_failed("文件校验失败")
    
    def start_installation(self):
        """开始安装"""
        try:
            # 这里实现安装逻辑
            # 可以启动外部更新程序或直接替换文件
            self.accept()
        except Exception as e:
            self.on_download_failed(f"安装失败: {str(e)}")
    
    def on_download_failed(self, error_msg: str):
        """下载失败处理"""
        QMessageBox.critical(self, "下载失败", error_msg)
        self.reject()
    
    def cancel_download(self):
        """取消下载"""
        self.file_manager.cancel_download()
        self.reject()
    
    def closeEvent(self, event):
        """关闭事件处理"""
        self.file_manager.cancel_download()
        event.accept()
