import sys
from pathlib import Path
from PySide6.QtWidgets import (QApplication, QMainWindow, QTabWidget,
                               QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QStatusBar, QTextEdit, QPushButton)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QAction


class MainWindow(QMainWindow):
    """主窗口类 - GUI程序的基础模板"""

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.center_window()

    def init_ui(self):
        """初始化用户界面"""
        # 设置窗口基本属性
        self.setWindowTitle("GUI Base Template")
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

        layout.addWidget(welcome_label)
        layout.addWidget(description_label)
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

        sample_button = QPushButton("插入示例文本")
        sample_button.clicked.connect(self.insert_sample_text)

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

        layout.addWidget(title_label)
        layout.addWidget(settings_label)
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
                         "GUI Base Template v1.0\n\n"
                         "一个基础的GUI程序模板\n"
                         "基于PySide6开发")

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


def main():
    """主函数"""
    # 创建应用程序实例
    app = QApplication(sys.argv)

    # 设置应用程序属性
    app.setApplicationName("GUI Base Template")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("Your Organization")

    # 创建主窗口
    window = MainWindow()
    window.show()

    # 运行应用程序
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
