"""
异常处理系统测试脚本
演示各种异常场景和错误对话框功能

使用方法：
    python examples/test_exception_handler.py

注意：
    - 此脚本会故意触发各种异常来测试异常处理系统
    - 每次运行会生成错误报告文件
    - 可以通过修改 config.json 中的 exception_handler 配置来测试不同行为
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 设置OpenGL属性
os.environ["QT_OPENGL"] = "desktop"

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt, QTimer

from utils import setup_exception_handler, app_config
from utils.display import setup_high_dpi_support


class ExceptionTestWindow(QMainWindow):
    """异常测试窗口"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle("异常处理系统测试")
        self.setGeometry(100, 100, 600, 400)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # 添加说明标签
        info_label = QLabel(
            "点击下面的按钮测试不同的异常场景\n"
            "每个按钮会触发一个特定类型的异常\n"
            "观察错误对话框和错误报告的生成"
        )
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_label.setStyleSheet("padding: 20px; font-size: 12px;")
        layout.addWidget(info_label)
        
        # 添加测试按钮
        self.add_test_button(layout, "测试 ValueError", self.test_value_error)
        self.add_test_button(layout, "测试 TypeError", self.test_type_error)
        self.add_test_button(layout, "测试 ZeroDivisionError", self.test_zero_division)
        self.add_test_button(layout, "测试 IndexError", self.test_index_error)
        self.add_test_button(layout, "测试 KeyError", self.test_key_error)
        self.add_test_button(layout, "测试 AttributeError", self.test_attribute_error)
        self.add_test_button(layout, "测试自定义异常", self.test_custom_exception)
        self.add_test_button(layout, "测试延迟异常（3秒后）", self.test_delayed_exception)
        
        layout.addStretch()
    
    def add_test_button(self, layout, text, callback):
        """添加测试按钮"""
        button = QPushButton(text)
        button.clicked.connect(callback)
        button.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                border: 1px solid #c0c0c0;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 12px;
                min-height: 24px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """)
        layout.addWidget(button)
    
    def test_value_error(self):
        """测试 ValueError"""
        print("\n=== 测试 ValueError ===")
        # 故意触发 ValueError
        int("not a number")
    
    def test_type_error(self):
        """测试 TypeError"""
        print("\n=== 测试 TypeError ===")
        # 故意触发 TypeError
        "string" + 123
    
    def test_zero_division(self):
        """测试 ZeroDivisionError"""
        print("\n=== 测试 ZeroDivisionError ===")
        # 故意触发 ZeroDivisionError
        result = 1 / 0
    
    def test_index_error(self):
        """测试 IndexError"""
        print("\n=== 测试 IndexError ===")
        # 故意触发 IndexError
        my_list = [1, 2, 3]
        value = my_list[10]
    
    def test_key_error(self):
        """测试 KeyError"""
        print("\n=== 测试 KeyError ===")
        # 故意触发 KeyError
        my_dict = {"a": 1, "b": 2}
        value = my_dict["nonexistent_key"]
    
    def test_attribute_error(self):
        """测试 AttributeError"""
        print("\n=== 测试 AttributeError ===")
        # 故意触发 AttributeError
        obj = object()
        obj.nonexistent_attribute
    
    def test_custom_exception(self):
        """测试自定义异常"""
        print("\n=== 测试自定义异常 ===")
        
        class CustomTestException(Exception):
            """自定义测试异常"""
            pass
        
        # 故意触发自定义异常
        raise CustomTestException("这是一个自定义的测试异常，用于演示异常处理系统")
    
    def test_delayed_exception(self):
        """测试延迟异常（使用 QTimer）"""
        print("\n=== 测试延迟异常（3秒后触发）===")
        
        def trigger_exception():
            print("延迟异常即将触发...")
            raise RuntimeError("这是一个延迟触发的异常，用于测试异步场景")
        
        # 3秒后触发异常
        QTimer.singleShot(3000, trigger_exception)


def main():
    """主函数"""
    print("=" * 60)
    print("异常处理系统测试")
    print("=" * 60)
    print(f"应用名称: {app_config.app_name}")
    print(f"当前版本: {app_config.current_version}")
    print(f"异常处理启用: {app_config.exception_handler_enabled}")
    print(f"显示错误对话框: {app_config.exception_handler_show_dialog}")
    print(f"保存错误报告: {app_config.exception_handler_save_report}")
    print(f"错误报告目录: {app_config.exception_handler_report_dir}")
    print("=" * 60)
    print()
    
    # 设置高DPI支持
    setup_high_dpi_support()
    
    # 创建应用程序
    app = QApplication(sys.argv)
    
    # 设置应用程序属性
    app.setApplicationName("异常处理测试")
    app.setApplicationVersion("1.0.0")
    
    # 设置全局异常处理器
    setup_exception_handler(app)
    
    # 创建并显示测试窗口
    window = ExceptionTestWindow()
    window.show()
    
    print("测试窗口已显示")
    print("点击按钮测试不同的异常场景")
    print("观察错误对话框和日志输出")
    print()
    
    # 运行应用程序
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

