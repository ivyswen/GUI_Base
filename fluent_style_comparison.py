import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QLabel, QPushButton, QFrame)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

# 导入Fluent-Widgets组件
from qfluentwidgets import (
    PushButton as FluentPushButton, 
    PrimaryPushButton, 
    FluentIcon,
    TitleLabel, BodyLabel,
    setTheme, Theme
)


class StyleComparisonWindow(QMainWindow):
    """样式对比演示窗口"""

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.center_window()

    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("PySide6-Fluent-Widgets 样式对比演示")
        self.setGeometry(100, 100, 1000, 600)

        # 设置Fluent主题
        setTheme(Theme.LIGHT)

        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(30)
        main_layout.setContentsMargins(40, 40, 40, 40)

        # 标题
        title = TitleLabel("PySide6-Fluent-Widgets 样式对比")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # 创建对比区域
        comparison_layout = QHBoxLayout()
        comparison_layout.setSpacing(40)

        # 原始样式区域
        original_frame = self.create_original_style_frame()
        comparison_layout.addWidget(original_frame)

        # 分隔线
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.VLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        comparison_layout.addWidget(separator)

        # Fluent样式区域
        fluent_frame = self.create_fluent_style_frame()
        comparison_layout.addWidget(fluent_frame)

        main_layout.addLayout(comparison_layout)

        # 说明文字
        description = BodyLabel(
            "左侧展示原始PyQt样式，右侧展示PySide6-Fluent-Widgets的现代化样式。\n"
            "Fluent-Widgets提供了更美观、更现代的用户界面组件。"
        )
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description.setWordWrap(True)
        main_layout.addWidget(description)

    def create_original_style_frame(self):
        """创建原始样式演示区域"""
        frame = QFrame()
        frame.setFrameStyle(QFrame.Shape.Box)
        frame.setStyleSheet("QFrame { border: 1px solid #ccc; border-radius: 8px; padding: 20px; }")

        layout = QVBoxLayout(frame)
        layout.setSpacing(20)

        # 标题
        title = QLabel("原始 PyQt 样式")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # 按钮样式方法（从原main.py复制）
        def get_button_style(style_type="default"):
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

        # 创建原始样式按钮
        original_buttons = [
            ("默认按钮", "default"),
            ("主要按钮", "primary"),
        ]

        for text, style in original_buttons:
            btn = QPushButton(text)
            btn.setStyleSheet(get_button_style(style))
            btn.clicked.connect(lambda checked, t=text: self.show_message(f"点击了原始样式的{t}"))
            layout.addWidget(btn)

        # 原始样式文本标签
        label = QLabel("这是普通的QLabel文本")
        label.setStyleSheet("color: #333; font-size: 12px;")
        layout.addWidget(label)

        layout.addStretch()
        return frame

    def create_fluent_style_frame(self):
        """创建Fluent样式演示区域"""
        frame = QFrame()
        frame.setFrameStyle(QFrame.Shape.Box)
        frame.setStyleSheet("QFrame { border: 1px solid #ccc; border-radius: 8px; padding: 20px; }")

        layout = QVBoxLayout(frame)
        layout.setSpacing(20)

        # 标题
        title = QLabel("PySide6-Fluent-Widgets 样式")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # 创建Fluent样式按钮
        default_btn = FluentPushButton("默认按钮")
        default_btn.setIcon(FluentIcon.BUTTON)
        default_btn.clicked.connect(lambda: self.show_message("点击了Fluent样式的默认按钮"))
        layout.addWidget(default_btn)

        primary_btn = PrimaryPushButton("主要按钮")
        primary_btn.setIcon(FluentIcon.ACCEPT)
        primary_btn.clicked.connect(lambda: self.show_message("点击了Fluent样式的主要按钮"))
        layout.addWidget(primary_btn)

        # Fluent样式文本标签
        fluent_label = BodyLabel("这是Fluent-Widgets的BodyLabel文本")
        layout.addWidget(fluent_label)

        layout.addStretch()
        return frame

    def show_message(self, message):
        """显示消息"""
        print(f"消息: {message}")

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
    
    app.setApplicationName("Fluent-Widgets Style Comparison")
    app.setApplicationVersion("1.0")
    
    window = StyleComparisonWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
