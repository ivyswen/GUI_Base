#!/usr/bin/env python3
"""
按钮样式演示程序

这个文件展示了GUI Base Template中所有可用的按钮样式。
运行此程序可以预览不同样式的按钮效果。
"""

import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, 
                               QVBoxLayout, QHBoxLayout, QLabel, QPushButton)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

class ButtonStyleDemo(QMainWindow):
    """按钮样式演示窗口"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.center_window()
        
    def get_button_style(self, style_type="default"):
        """获取按钮样式 - 与main.py中的样式保持一致"""
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
    
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("按钮样式演示 - GUI Base Template")
        self.setGeometry(100, 100, 600, 400)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # 标题
        title_label = QLabel("GUI Base Template - 按钮样式演示")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 20px;")
        main_layout.addWidget(title_label)
        
        # 说明文字
        desc_label = QLabel("以下展示了所有可用的按钮样式类型，每种样式都有悬停和按下效果：")
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setStyleSheet("font-size: 12px; margin: 10px;")
        main_layout.addWidget(desc_label)
        
        # 按钮样式演示区域
        self.create_style_demos(main_layout)
        
        # 状态说明
        status_label = QLabel("提示：将鼠标悬停在按钮上可以看到悬停效果，点击可以看到按下效果")
        status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status_label.setStyleSheet("font-size: 10px; color: #666; margin: 20px;")
        main_layout.addWidget(status_label)
        
    def create_style_demos(self, main_layout):
        """创建样式演示区域"""
        # Default 样式
        self.create_style_row(main_layout, "Default", "default", 
                             "默认样式 - 适用于一般操作按钮")
        
        # Primary 样式
        self.create_style_row(main_layout, "Primary", "primary", 
                             "主要样式 - 适用于重要操作按钮")
        
        # Success 样式
        self.create_style_row(main_layout, "Success", "success", 
                             "成功样式 - 适用于确认、保存等操作")
        
        # Warning 样式
        self.create_style_row(main_layout, "Warning", "warning", 
                             "警告样式 - 适用于需要注意的操作")
        
        # Danger 样式
        self.create_style_row(main_layout, "Danger", "danger", 
                             "危险样式 - 适用于删除、重置等操作")
        
        # 禁用状态演示
        self.create_disabled_demo(main_layout)
        
    def create_style_row(self, main_layout, name, style_type, description):
        """创建一行样式演示"""
        row_layout = QHBoxLayout()
        
        # 样式名称标签
        name_label = QLabel(f"{name}:")
        name_label.setMinimumWidth(80)
        name_label.setStyleSheet("font-weight: bold;")
        
        # 示例按钮
        demo_button = QPushButton(f"{name} 按钮")
        demo_button.setStyleSheet(self.get_button_style(style_type))
        demo_button.clicked.connect(lambda: self.button_clicked(name))
        
        # 描述标签
        desc_label = QLabel(description)
        desc_label.setStyleSheet("color: #666; font-size: 11px;")
        
        row_layout.addWidget(name_label)
        row_layout.addWidget(demo_button)
        row_layout.addWidget(desc_label)
        row_layout.addStretch()
        
        main_layout.addLayout(row_layout)
        
    def create_disabled_demo(self, main_layout):
        """创建禁用状态演示"""
        row_layout = QHBoxLayout()
        
        name_label = QLabel("Disabled:")
        name_label.setMinimumWidth(80)
        name_label.setStyleSheet("font-weight: bold;")
        
        disabled_button = QPushButton("禁用按钮")
        disabled_button.setStyleSheet(self.get_button_style("default"))
        disabled_button.setEnabled(False)
        
        desc_label = QLabel("禁用状态 - 所有样式的禁用效果都相同")
        desc_label.setStyleSheet("color: #666; font-size: 11px;")
        
        row_layout.addWidget(name_label)
        row_layout.addWidget(disabled_button)
        row_layout.addWidget(desc_label)
        row_layout.addStretch()
        
        main_layout.addLayout(row_layout)
        
    def button_clicked(self, style_name):
        """按钮点击处理"""
        print(f"点击了 {style_name} 样式的按钮")
        
    def center_window(self):
        """将窗口居中显示"""
        screen = QApplication.primaryScreen().geometry()
        window = self.geometry()
        x = (screen.width() - window.width()) // 2
        y = (screen.height() - window.height()) // 2
        self.move(x, y)

def main():
    """主函数"""
    app = QApplication(sys.argv)
    app.setApplicationName("Button Style Demo")
    
    window = ButtonStyleDemo()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
