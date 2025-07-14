import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

# 导入Fluent-Widgets组件
from qfluentwidgets import (
    FluentWindow, NavigationItemPosition, FluentIcon,
    PushButton, PrimaryPushButton, ToolButton,
    TextEdit, TitleLabel, BodyLabel, CaptionLabel,
    InfoBar, InfoBarPosition, MessageBox,
    setTheme, Theme, isDarkTheme, qconfig
)


class FluentMainWindow(FluentWindow):
    """基于Fluent-Widgets的主窗口类"""

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.center_window()

    def init_ui(self):
        """初始化用户界面"""
        # 设置窗口基本属性
        self.setWindowTitle("GUI Base Template - Fluent Design")
        self.resize(900, 700)

        # 设置窗口图标
        self.set_window_icon()

        # 设置主题
        self.setup_theme()

        # 创建导航界面
        self.create_navigation_interface()

    def set_window_icon(self):
        """设置窗口图标"""
        resources_dir = Path(__file__).parent / "Resources"
        icon_files = ["favicon.ico", "icon-192.png"]

        for icon_file in icon_files:
            icon_path = resources_dir / icon_file
            if icon_path.exists():
                icon = QIcon(str(icon_path))
                self.setWindowIcon(icon)
                break

    def setup_theme(self):
        """设置主题和颜色"""
        # 可以根据需要设置深色或浅色主题
        # setTheme(Theme.DARK)  # 深色主题
        setTheme(Theme.LIGHT)   # 浅色主题

    def create_navigation_interface(self):
        """创建导航界面"""
        # 创建欢迎页面
        self.welcome_interface = WelcomeInterface(self)
        self.welcome_interface.setObjectName("welcome_interface")
        self.addSubInterface(
            self.welcome_interface,
            FluentIcon.HOME,
            "欢迎",
            NavigationItemPosition.TOP
        )

        # 创建文本编辑页面
        self.editor_interface = EditorInterface(self)
        self.editor_interface.setObjectName("editor_interface")
        self.addSubInterface(
            self.editor_interface,
            FluentIcon.EDIT,
            "文本编辑",
            NavigationItemPosition.TOP
        )

        # 创建设置页面
        self.settings_interface = SettingsInterface(self)
        self.settings_interface.setObjectName("settings_interface")
        self.addSubInterface(
            self.settings_interface,
            FluentIcon.SETTING,
            "设置",
            NavigationItemPosition.BOTTOM
        )

        # 设置默认显示的界面
        self.stackedWidget.setCurrentWidget(self.welcome_interface)

    def center_window(self):
        """将窗口居中显示"""
        screen = QApplication.primaryScreen().geometry()
        window = self.geometry()
        x = (screen.width() - window.width()) // 2
        y = (screen.height() - window.height()) // 2
        self.move(x, y)

    def show_success_message(self, message):
        """显示成功消息"""
        InfoBar.success(
            title="成功",
            content=message,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self
        )

    def show_info_message(self, message):
        """显示信息消息"""
        InfoBar.info(
            title="信息",
            content=message,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self
        )


class WelcomeInterface(QWidget):
    """欢迎页面界面"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent_window = parent
        self.init_ui()

    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        # 欢迎标题
        welcome_title = TitleLabel("欢迎使用GUI Base Template!")
        welcome_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 描述文本
        description = BodyLabel(
            "这是一个基于PySide6-Fluent-Widgets的现代化GUI程序模板，包含以下功能：\n\n"
            "• 现代化的Fluent Design设计语言\n"
            "• 流畅的动画效果和交互体验\n"
            "• 完整的导航系统\n"
            "• 美观的组件样式\n"
            "• 主题切换支持\n\n"
            "您可以基于此模板开发自己的现代化GUI应用程序。"
        )
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description.setWordWrap(True)

        # 快速操作按钮
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        # 主要按钮 - 使用PrimaryPushButton
        start_button = PrimaryPushButton("开始使用", self)
        start_button.setIcon(FluentIcon.PLAY)
        start_button.clicked.connect(self.start_using)

        # 普通按钮
        help_button = PushButton("查看帮助", self)
        help_button.setIcon(FluentIcon.HELP)
        help_button.clicked.connect(self.show_help)

        # 成功样式按钮
        demo_button = PushButton("运行演示", self)
        demo_button.setIcon(FluentIcon.PLAY_SOLID)
        demo_button.clicked.connect(self.run_demo)

        button_layout.addStretch()
        button_layout.addWidget(start_button)
        button_layout.addWidget(help_button)
        button_layout.addWidget(demo_button)
        button_layout.addStretch()

        # 添加到主布局
        layout.addStretch()
        layout.addWidget(welcome_title)
        layout.addWidget(description)
        layout.addSpacing(30)
        layout.addLayout(button_layout)
        layout.addStretch()

    def start_using(self):
        """开始使用 - 切换到文本编辑页面"""
        if self.parent_window:
            self.parent_window.stackedWidget.setCurrentWidget(
                self.parent_window.editor_interface
            )
            self.parent_window.show_info_message("已切换到文本编辑页面")

    def show_help(self):
        """显示帮助信息"""
        help_text = (
            "GUI Base Template 使用帮助\n\n"
            "1. 欢迎页面：查看程序介绍和快速操作\n"
            "2. 文本编辑：进行文本编辑和操作\n"
            "3. 设置页面：配置程序选项\n\n"
            "使用左侧导航栏可以在不同页面间切换。\n"
            "顶部会显示操作反馈信息。"
        )
        MessageBox("使用帮助", help_text, self).exec()

    def run_demo(self):
        """运行演示"""
        if self.parent_window:
            # 切换到文本编辑页面
            self.parent_window.stackedWidget.setCurrentWidget(
                self.parent_window.editor_interface
            )
            # 插入演示文本
            demo_text = (
                "🎉 欢迎体验GUI Base Template演示！\n\n"
                "这是一个基于PySide6-Fluent-Widgets的现代化GUI程序模板，包含：\n\n"
                "✅ 现代化的Fluent Design设计语言\n"
                "✅ 流畅的动画效果\n"
                "✅ 完整的导航系统\n"
                "✅ 美观的组件样式\n"
                "✅ 主题切换支持\n"
                "✅ 图标支持\n\n"
                "您可以基于此模板快速开发自己的现代化应用程序！\n\n"
                "试试使用左侧导航栏的功能，或者点击下方的按钮。"
            )
            self.parent_window.editor_interface.text_edit.setPlainText(demo_text)
            self.parent_window.show_success_message("演示已启动，请查看文本编辑页面")


class EditorInterface(QWidget):
    """文本编辑界面"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent_window = parent
        self.init_ui()

    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        # 标题
        title = TitleLabel("文本编辑器")

        # 文本编辑区域 - 使用Fluent-Widgets的TextEdit
        self.text_edit = TextEdit(self)
        self.text_edit.setPlaceholderText("在这里输入文本...")

        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        # 清空按钮
        clear_button = PushButton("清空", self)
        clear_button.setIcon(FluentIcon.DELETE)
        clear_button.clicked.connect(self.clear_text)

        # 插入示例文本按钮
        sample_button = PushButton("插入示例文本", self)
        sample_button.setIcon(FluentIcon.DOCUMENT)
        sample_button.clicked.connect(self.insert_sample_text)

        button_layout.addWidget(clear_button)
        button_layout.addWidget(sample_button)
        button_layout.addStretch()

        # 添加到主布局
        layout.addWidget(title)
        layout.addWidget(self.text_edit)
        layout.addLayout(button_layout)

    def clear_text(self):
        """清空文本"""
        self.text_edit.clear()
        if self.parent_window:
            self.parent_window.show_info_message("文本已清空")

    def insert_sample_text(self):
        """插入示例文本"""
        sample_text = (
            "这是一个示例文本。\n\n"
            "您可以在这里编辑文本，体验Fluent-Widgets的现代化文本编辑组件。\n\n"
            "这个GUI模板使用了最新的Fluent Design设计语言，"
            "提供了流畅的用户体验和美观的界面设计。"
        )
        self.text_edit.setPlainText(sample_text)
        if self.parent_window:
            self.parent_window.show_success_message("已插入示例文本")


class SettingsInterface(QWidget):
    """设置界面"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent_window = parent
        self.init_ui()

    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        # 标题
        title = TitleLabel("设置")

        # 设置内容
        settings_label = BodyLabel(
            "这里可以添加各种设置选项：\n\n"
            "• 主题设置（浅色/深色）\n"
            "• 主题色设置\n"
            "• 语言设置\n"
            "• 字体设置\n"
            "• 其他配置选项\n\n"
            "根据您的需求自定义此页面。"
        )
        settings_label.setWordWrap(True)

        # 示例设置按钮
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        # 主题切换按钮
        theme_button = PushButton("切换主题", self)
        theme_button.setIcon(FluentIcon.BRUSH)
        theme_button.clicked.connect(self.toggle_theme)

        # 主题色按钮
        color_button = PushButton("主题色设置", self)
        color_button.setIcon(FluentIcon.PALETTE)
        color_button.clicked.connect(self.theme_color_settings)

        # 语言设置按钮
        language_button = PushButton("语言设置", self)
        language_button.setIcon(FluentIcon.LANGUAGE)
        language_button.clicked.connect(self.language_settings)

        button_layout.addWidget(theme_button)
        button_layout.addWidget(color_button)
        button_layout.addWidget(language_button)
        button_layout.addStretch()

        # 添加到主布局
        layout.addWidget(title)
        layout.addWidget(settings_label)
        layout.addSpacing(20)
        layout.addLayout(button_layout)
        layout.addStretch()

    def toggle_theme(self):
        """切换主题"""
        if isDarkTheme():
            setTheme(Theme.LIGHT)
            theme_name = "浅色主题"
        else:
            setTheme(Theme.DARK)
            theme_name = "深色主题"

        if self.parent_window:
            self.parent_window.show_success_message(f"已切换到{theme_name}")

    def theme_color_settings(self):
        """主题色设置"""
        # 这里可以添加颜色选择器
        if self.parent_window:
            self.parent_window.show_info_message("主题色设置功能待实现")

    def language_settings(self):
        """语言设置"""
        if self.parent_window:
            self.parent_window.show_info_message("语言设置功能待实现")


def main():
    """主函数"""
    # 创建应用程序实例
    app = QApplication(sys.argv)

    # 设置应用程序属性
    app.setApplicationName("GUI Base Template - Fluent")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("Your Organization")

    # 创建主窗口
    window = FluentMainWindow()
    window.show()

    # 运行应用程序
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
