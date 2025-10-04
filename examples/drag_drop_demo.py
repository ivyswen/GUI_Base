"""
拖放文件支持演示
展示如何使用拖放功能
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTextEdit, QPushButton, QGroupBox
)
from PySide6.QtCore import Qt
from utils import create_drag_drop_area, DragDropWidget, file_utils


class DragDropDemo(QMainWindow):
    """拖放演示窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("拖放文件支持演示")
        self.setGeometry(100, 100, 800, 600)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout(central_widget)
        
        # 标题
        title = QLabel("拖放文件支持演示")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # 示例1：基本拖放区域
        layout.addWidget(self.create_basic_example())
        
        # 示例2：限制文件类型
        layout.addWidget(self.create_filtered_example())
        
        # 示例3：单文件拖放
        layout.addWidget(self.create_single_file_example())
        
        # 示例4：允许目录
        layout.addWidget(self.create_directory_example())
        
        # 日志区域
        layout.addWidget(self.create_log_area())
        
        # 清除按钮
        clear_btn = QPushButton("清除日志")
        clear_btn.clicked.connect(self.clear_log)
        layout.addWidget(clear_btn)
    
    def create_basic_example(self):
        """创建基本拖放示例"""
        group = QGroupBox("示例1：基本拖放（允许所有文件）")
        layout = QVBoxLayout()
        
        drop_area = create_drag_drop_area(
            on_files_dropped=lambda files: self.handle_files("基本拖放", files),
            drop_hint="拖放任何文件到这里",
            min_height=80
        )
        layout.addWidget(drop_area)
        
        group.setLayout(layout)
        return group
    
    def create_filtered_example(self):
        """创建限制文件类型示例"""
        group = QGroupBox("示例2：限制文件类型（仅 .txt, .py, .json）")
        layout = QVBoxLayout()
        
        drop_area = create_drag_drop_area(
            on_files_dropped=lambda files: self.handle_files("限制类型", files),
            allowed_extensions=['.txt', '.py', '.json'],
            drop_hint="拖放 .txt, .py 或 .json 文件到这里",
            min_height=80
        )
        layout.addWidget(drop_area)
        
        group.setLayout(layout)
        return group
    
    def create_single_file_example(self):
        """创建单文件拖放示例"""
        group = QGroupBox("示例3：单文件拖放")
        layout = QVBoxLayout()
        
        drop_area = create_drag_drop_area(
            on_files_dropped=lambda files: self.handle_files("单文件", files),
            multiple_files=False,
            drop_hint="拖放单个文件到这里",
            min_height=80
        )
        layout.addWidget(drop_area)
        
        group.setLayout(layout)
        return group
    
    def create_directory_example(self):
        """创建允许目录示例"""
        group = QGroupBox("示例4：允许目录")
        layout = QVBoxLayout()
        
        drop_area = create_drag_drop_area(
            on_files_dropped=lambda files: self.handle_files("目录", files),
            allow_directories=True,
            drop_hint="拖放文件或目录到这里",
            min_height=80
        )
        layout.addWidget(drop_area)
        
        group.setLayout(layout)
        return group
    
    def create_log_area(self):
        """创建日志区域"""
        group = QGroupBox("拖放日志")
        layout = QVBoxLayout()
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(150)
        layout.addWidget(self.log_text)
        
        group.setLayout(layout)
        return group
    
    def handle_files(self, example_name: str, files: list):
        """处理拖放的文件"""
        self.log(f"\n[{example_name}] 收到 {len(files)} 个文件/目录:")
        
        for file_path in files:
            if os.path.isdir(file_path):
                # 目录
                self.log(f"  📁 {file_path}")
                # 列出目录中的文件
                dir_files = file_utils.list_files(file_path, recursive=True)
                self.log(f"     包含 {len(dir_files)} 个文件")
            else:
                # 文件
                size = file_utils.get_file_size(file_path)
                formatted_size = file_utils.format_file_size(size)
                ext = file_utils.get_file_extension(file_path)
                name = file_utils.get_file_name(file_path)
                
                self.log(f"  📄 {name}")
                self.log(f"     路径: {file_path}")
                self.log(f"     大小: {formatted_size}")
                self.log(f"     扩展名: {ext}")
    
    def log(self, message: str):
        """添加日志"""
        self.log_text.append(message)
        # 滚动到底部
        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum()
        )
    
    def clear_log(self):
        """清除日志"""
        self.log_text.clear()


def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    window = DragDropDemo()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

