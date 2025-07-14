import sys
from pathlib import Path
from PySide6.QtWidgets import (QApplication, QMainWindow, QTabWidget,
                               QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QStatusBar, QTextEdit, QPushButton)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QAction

# 导入自动更新相关模块
from updater import UpdateManager, app_config, app_logger


class MainWindow(QMainWindow):
    """主窗口类 - GUI程序的基础模板"""

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.center_window()

        # 初始化更新管理器
        self.update_manager = UpdateManager(self)

        # 启动时检查更新（延迟执行）
        self.update_manager.check_for_updates_on_startup()

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
        # 设置窗口基本属性
        self.setWindowTitle(app_config.app_name)
        self.setGeometry(100, 100, 800, 600)

        # 设置窗口图标
        self.set_window_icon()

        # 创建菜单栏
        self.create_menu_bar()

        # 创建中央部件和标签页
        self.create_central_widget()

        # 创建状态栏
        self.create_status_bar()

    def set_window_icon(self):
        """设置窗口图标"""
        # 获取Resources目录路径
        resources_dir = Path(__file__).parent / "Resources"

        # 尝试设置图标，优先使用.ico文件
        icon_files = ["favicon.ico", "icon-192.png"]

        for icon_file in icon_files:
            icon_path = resources_dir / icon_file
            if icon_path.exists():
                icon = QIcon(str(icon_path))
                self.setWindowIcon(icon)
                break

    def create_menu_bar(self):
        """创建菜单栏"""
        menubar = self.menuBar()

        # 文件菜单
        file_menu = menubar.addMenu('文件(&F)')

        # 新建动作
        new_action = QAction('新建(&N)', self)
        new_action.setShortcut('Ctrl+N')
        new_action.setStatusTip('创建新文件')
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)

        # 打开动作
        open_action = QAction('打开(&O)', self)
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip('打开文件')
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        file_menu.addSeparator()

        # 退出动作
        exit_action = QAction('退出(&X)', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('退出应用程序')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # 编辑菜单
        edit_menu = menubar.addMenu('编辑(&E)')

        # 复制动作
        copy_action = QAction('复制(&C)', self)
        copy_action.setShortcut('Ctrl+C')
        copy_action.setStatusTip('复制选中内容')
        copy_action.triggered.connect(self.copy_text)
        edit_menu.addAction(copy_action)

        # 粘贴动作
        paste_action = QAction('粘贴(&V)', self)
        paste_action.setShortcut('Ctrl+V')
        paste_action.setStatusTip('粘贴内容')
        paste_action.triggered.connect(self.paste_text)
        edit_menu.addAction(paste_action)

        # 帮助菜单
        help_menu = menubar.addMenu('帮助(&H)')

        # 检查更新动作
        check_update_action = QAction('检查更新(&U)', self)
        check_update_action.setStatusTip('检查软件更新')
        check_update_action.triggered.connect(self.check_for_updates)
        help_menu.addAction(check_update_action)

        help_menu.addSeparator()

        # 关于动作
        about_action = QAction('关于(&A)', self)
        about_action.setStatusTip('关于此程序')
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def create_central_widget(self):
        """创建中央部件和标签页"""
        # 创建标签页控件
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        # 创建第一个标签页
        self.create_tab1()

        # 创建第二个标签页
        self.create_tab2()

        # 创建第三个标签页
        self.create_tab3()

    def create_tab1(self):
        """创建第一个标签页 - 欢迎页面"""
        tab1 = QWidget()
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

        tab1.setLayout(layout)
        self.tab_widget.addTab(tab1, "欢迎")

    def create_tab2(self):
        """创建第二个标签页 - 文本编辑器"""
        tab2 = QWidget()
        layout = QVBoxLayout()

        # 标题
        title_label = QLabel("文本编辑器")
        title_label.setStyleSheet("font-size: 14px; font-weight: bold; margin: 10px;")

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

        tab2.setLayout(layout)
        self.tab_widget.addTab(tab2, "文本编辑")

    def create_tab3(self):
        """创建第三个标签页 - 设置"""
        tab3 = QWidget()
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

        tab3.setLayout(layout)
        self.tab_widget.addTab(tab3, "设置")

    def create_status_bar(self):
        """创建状态栏"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("就绪")

    def center_window(self):
        """将窗口居中显示"""
        # 获取屏幕几何信息
        screen = QApplication.primaryScreen().geometry()

        # 获取窗口几何信息
        window = self.geometry()

        # 计算居中位置
        x = (screen.width() - window.width()) // 2
        y = (screen.height() - window.height()) // 2

        # 移动窗口到居中位置
        self.move(x, y)

    # 菜单动作处理函数
    def new_file(self):
        """新建文件"""
        self.status_bar.showMessage("新建文件", 2000)

    def open_file(self):
        """打开文件"""
        self.status_bar.showMessage("打开文件", 2000)

    def copy_text(self):
        """复制文本"""
        if hasattr(self, 'text_edit'):
            self.text_edit.copy()
            self.status_bar.showMessage("已复制", 2000)

    def paste_text(self):
        """粘贴文本"""
        if hasattr(self, 'text_edit'):
            self.text_edit.paste()
            self.status_bar.showMessage("已粘贴", 2000)

    def show_about(self):
        """显示关于信息"""
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.about(self, "关于",
                         f"{app_config.app_name} v{app_config.current_version}\n\n"
                         "一个基础的GUI程序模板\n"
                         "基于PySide6开发\n\n"
                         f"组织: {app_config.organization_name}")

    # 标签页功能函数
    def clear_text(self):
        """清空文本"""
        self.text_edit.clear()
        self.status_bar.showMessage("文本已清空", 2000)

    def insert_sample_text(self):
        """插入示例文本"""
        sample_text = (
            "这是一个示例文本。\n\n"
            "您可以在这里编辑文本，使用菜单栏的复制和粘贴功能。\n\n"
            "这个GUI模板包含了基础的界面元素，"
            "您可以根据需要进行扩展和修改。"
        )
        self.text_edit.setPlainText(sample_text)
        self.status_bar.showMessage("已插入示例文本", 2000)

    # 欢迎页面功能函数
    def start_using(self):
        """开始使用 - 切换到文本编辑标签页"""
        self.tab_widget.setCurrentIndex(1)  # 切换到文本编辑标签页
        self.status_bar.showMessage("已切换到文本编辑页面", 2000)

    def show_help(self):
        """显示帮助信息"""
        from PySide6.QtWidgets import QMessageBox
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
        self.tab_widget.setCurrentIndex(1)  # 切换到文本编辑标签页
        # 插入演示文本
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
        if hasattr(self, 'text_edit'):
            self.text_edit.setPlainText(demo_text)
        self.status_bar.showMessage("演示已启动，请查看文本编辑页面", 3000)

    # 设置页面功能函数
    def toggle_theme(self):
        """切换主题"""
        self.status_bar.showMessage("主题切换功能待实现", 2000)

    def language_settings(self):
        """语言设置"""
        self.status_bar.showMessage("语言设置功能待实现", 2000)

    def font_settings(self):
        """字体设置"""
        self.status_bar.showMessage("字体设置功能待实现", 2000)

    def reset_settings(self):
        """重置设置"""
        from PySide6.QtWidgets import QMessageBox
        reply = QMessageBox.question(self, "确认重置",
                                   "确定要重置所有设置吗？",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.status_bar.showMessage("设置已重置", 2000)
        else:
            self.status_bar.showMessage("取消重置", 2000)

    def check_for_updates(self):
        """检查更新"""
        app_logger.info("用户手动触发检查更新")
        if hasattr(self, 'update_manager'):
            self.update_manager.check_for_updates_manual_with_flag()
        else:
            app_logger.error("更新管理器未初始化")
            self.status_bar.showMessage("更新功能不可用", 2000)


def main():
    """主函数"""
    # 创建应用程序实例
    app = QApplication(sys.argv)

    # 设置应用程序属性
    app.setApplicationName(app_config.app_name)
    app.setApplicationVersion(app_config.current_version)
    app.setOrganizationName(app_config.organization_name)

    # 创建主窗口
    window = MainWindow()
    window.show()

    # 运行应用程序
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
