"""
主题系统测试脚本
演示主题切换、系统主题检测等功能

使用方法：
    python examples/test_theme.py

功能：
    - 显示当前主题信息
    - 演示主题切换功能
    - 演示系统主题检测
    - 展示各种组件在不同主题下的效果
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 设置OpenGL属性
os.environ["QT_OPENGL"] = "desktop"

from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QPushButton, QLabel, QGroupBox, QTextEdit)
from PySide6.QtCore import Qt

from utils import setup_theme_manager, app_config
from utils.theme import get_theme_manager
from utils.display import setup_high_dpi_support
from utils.styles import get_button_style, get_group_box_style, get_text_edit_style


class ThemeTestWindow(QMainWindow):
    """主题测试窗口"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle("主题系统测试")
        self.setGeometry(100, 100, 800, 600)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # 标题
        title_label = QLabel("主题系统测试")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 20px;")
        layout.addWidget(title_label)
        
        # 主题信息分组
        info_group = self.create_info_group()
        layout.addWidget(info_group)
        
        # 主题切换按钮分组
        theme_group = self.create_theme_buttons_group()
        layout.addWidget(theme_group)
        
        # 组件演示分组
        demo_group = self.create_demo_group()
        layout.addWidget(demo_group)
        
        layout.addStretch()
    
    def create_info_group(self):
        """创建主题信息分组"""
        group = QGroupBox("主题信息")
        group.setStyleSheet(get_group_box_style())
        layout = QVBoxLayout()
        
        # 获取主题管理器
        theme_manager = get_theme_manager()
        
        # 当前主题模式
        current_mode = app_config.theme_mode
        self.mode_label = QLabel(f"当前主题模式: {current_mode}")
        layout.addWidget(self.mode_label)
        
        # 实际主题
        is_dark = theme_manager.is_dark_theme()
        actual_theme = "深色" if is_dark else "浅色"
        self.actual_label = QLabel(f"实际应用主题: {actual_theme}")
        layout.addWidget(self.actual_label)
        
        # 系统主题
        system_theme = theme_manager.detect_system_theme()
        self.system_label = QLabel(f"系统主题: {system_theme}")
        layout.addWidget(self.system_label)
        
        group.setLayout(layout)
        return group
    
    def create_theme_buttons_group(self):
        """创建主题切换按钮分组"""
        group = QGroupBox("主题切换")
        group.setStyleSheet(get_group_box_style())
        layout = QHBoxLayout()
        
        # 浅色主题按钮
        light_btn = QPushButton("切换到浅色主题")
        light_btn.setStyleSheet(get_button_style("primary"))
        light_btn.clicked.connect(lambda: self.switch_theme("light"))
        layout.addWidget(light_btn)
        
        # 深色主题按钮
        dark_btn = QPushButton("切换到深色主题")
        dark_btn.setStyleSheet(get_button_style("secondary"))
        dark_btn.clicked.connect(lambda: self.switch_theme("dark"))
        layout.addWidget(dark_btn)
        
        # 跟随系统按钮
        auto_btn = QPushButton("跟随系统主题")
        auto_btn.setStyleSheet(get_button_style("info"))
        auto_btn.clicked.connect(lambda: self.switch_theme("auto"))
        layout.addWidget(auto_btn)
        
        # 刷新信息按钮
        refresh_btn = QPushButton("刷新信息")
        refresh_btn.setStyleSheet(get_button_style("success"))
        refresh_btn.clicked.connect(self.refresh_info)
        layout.addWidget(refresh_btn)
        
        group.setLayout(layout)
        return group
    
    def create_demo_group(self):
        """创建组件演示分组"""
        group = QGroupBox("组件演示")
        group.setStyleSheet(get_group_box_style())
        layout = QVBoxLayout()
        
        # 说明文字
        desc_label = QLabel("以下组件会根据当前主题自动调整样式：")
        layout.addWidget(desc_label)
        
        # 按钮演示
        button_layout = QHBoxLayout()
        
        default_btn = QPushButton("默认按钮")
        default_btn.setStyleSheet(get_button_style("default"))
        button_layout.addWidget(default_btn)
        
        primary_btn = QPushButton("主要按钮")
        primary_btn.setStyleSheet(get_button_style("primary"))
        button_layout.addWidget(primary_btn)
        
        success_btn = QPushButton("成功按钮")
        success_btn.setStyleSheet(get_button_style("success"))
        button_layout.addWidget(success_btn)
        
        warning_btn = QPushButton("警告按钮")
        warning_btn.setStyleSheet(get_button_style("warning"))
        button_layout.addWidget(warning_btn)
        
        danger_btn = QPushButton("危险按钮")
        danger_btn.setStyleSheet(get_button_style("danger"))
        button_layout.addWidget(danger_btn)
        
        layout.addLayout(button_layout)
        
        # 文本编辑器演示
        text_edit = QTextEdit()
        text_edit.setStyleSheet(get_text_edit_style())
        text_edit.setPlainText(
            "这是一个文本编辑器示例。\n"
            "它会根据当前主题自动调整背景色和文字颜色。\n\n"
            "浅色主题：白色背景，深色文字\n"
            "深色主题：深色背景，浅色文字"
        )
        text_edit.setMaximumHeight(100)
        layout.addWidget(text_edit)
        
        group.setLayout(layout)
        return group
    
    def switch_theme(self, mode: str):
        """切换主题
        
        Args:
            mode: 主题模式 ("light", "dark", "auto")
        """
        try:
            theme_manager = get_theme_manager()
            theme_manager.set_theme(mode, save=True)  # type: ignore
            
            # 刷新信息
            self.refresh_info()
            
            # 显示提示
            self.statusBar().showMessage(f"已切换到 {mode} 主题", 3000)
        except Exception as e:
            self.statusBar().showMessage(f"主题切换失败: {e}", 3000)
    
    def refresh_info(self):
        """刷新主题信息"""
        theme_manager = get_theme_manager()
        
        # 更新主题模式
        current_mode = app_config.theme_mode
        self.mode_label.setText(f"当前主题模式: {current_mode}")
        
        # 更新实际主题
        is_dark = theme_manager.is_dark_theme()
        actual_theme = "深色" if is_dark else "浅色"
        self.actual_label.setText(f"实际应用主题: {actual_theme}")
        
        # 更新系统主题
        system_theme = theme_manager.detect_system_theme()
        self.system_label.setText(f"系统主题: {system_theme}")
        
        self.statusBar().showMessage("信息已刷新", 2000)


def main():
    """主函数"""
    print("=" * 60)
    print("主题系统测试")
    print("=" * 60)
    print(f"应用名称: {app_config.app_name}")
    print(f"当前版本: {app_config.current_version}")
    print(f"主题模式: {app_config.theme_mode}")
    print("=" * 60)
    print()
    
    # 设置高DPI支持
    setup_high_dpi_support()
    
    # 创建应用程序
    app = QApplication(sys.argv)
    
    # 设置应用程序属性
    app.setApplicationName("主题系统测试")
    app.setApplicationVersion("1.0.0")
    
    # 设置主题系统
    setup_theme_manager(app)
    
    # 创建并显示测试窗口
    window = ThemeTestWindow()
    window.show()
    
    print("测试窗口已显示")
    print("使用窗口中的按钮测试主题切换功能")
    print()
    
    # 运行应用程序
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

