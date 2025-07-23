import sys
import os
from pathlib import Path

# 在导入PySide6之前设置OpenGL属性
os.environ["QT_OPENGL"] = "desktop"

from PySide6.QtWidgets import (QApplication, QMainWindow, QTabWidget,
                               QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QStatusBar, QTextEdit, QPushButton)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QAction, QFont

# 导入自动更新相关模块
from updater import UpdateManager
from utils import app_logger, app_config
from utils.display import setup_high_dpi_support, setup_font_rendering

# 导入GUI模块
from gui import WelcomeTab, TextEditorTab, SettingsTab


class MainWindow(QMainWindow):
    """主窗口类 - GUI程序的基础模板"""

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.center_window()

        # 同步版本信息（从exe文件更新配置中的版本号）
        self.sync_version_on_startup()

        # 初始化更新管理器
        self.update_manager = UpdateManager(self)

        # 启动时检查更新（延迟执行）
        self.update_manager.check_for_updates_on_startup()



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

        # 创建第一个标签页 - 欢迎页面
        self.welcome_tab = WelcomeTab(self)
        self.tab_widget.addTab(self.welcome_tab, "欢迎")

        # 创建第二个标签页 - 文本编辑器
        self.text_editor_tab = TextEditorTab(self)
        self.tab_widget.addTab(self.text_editor_tab, "文本编辑")

        # 保存文本编辑器的引用，供菜单功能使用
        self.text_edit = self.text_editor_tab.get_text_edit()

        # 创建第三个标签页 - 设置
        self.settings_tab = SettingsTab(self)
        self.tab_widget.addTab(self.settings_tab, "设置")







    def create_status_bar(self):
        """创建状态栏"""
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)
        self.statusBar().showMessage("就绪")

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

    def sync_version_on_startup(self):
        """启动时同步版本信息"""
        try:
            # 尝试从exe文件更新配置中的版本号
            if app_config.update_version_from_exe():
                app_logger.info(f"版本信息已同步: {app_config.current_version}")
            else:
                app_logger.debug("无需同步版本信息或同步失败")
        except Exception as e:
            app_logger.error(f"同步版本信息时发生错误: {str(e)}")

    # 菜单动作处理函数
    def new_file(self):
        """新建文件"""
        self.statusBar().showMessage("新建文件", 2000)

    def open_file(self):
        """打开文件"""
        self.statusBar().showMessage("打开文件", 2000)

    def copy_text(self):
        """复制文本"""
        if hasattr(self, 'text_edit') and self.text_edit:
            self.text_edit.copy()
            self.statusBar().showMessage("已复制", 2000)

    def paste_text(self):
        """粘贴文本"""
        if hasattr(self, 'text_edit') and self.text_edit:
            self.text_edit.paste()
            self.statusBar().showMessage("已粘贴", 2000)

    def show_about(self):
        """显示关于信息"""
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.about(self, "关于",
                         f"{app_config.app_name} v{app_config.current_version}\n\n"
                         "一个基础的GUI程序模板\n"
                         "基于PySide6开发\n\n"
                         f"组织: {app_config.organization_name}")



    def check_for_updates(self):
        """检查更新"""
        app_logger.info("用户手动触发检查更新")
        if hasattr(self, 'update_manager'):
            self.update_manager.check_for_updates_manual_with_flag()
        else:
            app_logger.error("更新管理器未初始化")
            self.statusBar().showMessage("更新功能不可用", 2000)


def main():
    """主函数"""
    # 设置高DPI支持（在创建QApplication之前）
    setup_high_dpi_support()

    # 创建应用程序实例
    app = QApplication(sys.argv)

    # 设置字体渲染优化
    setup_font_rendering(app)

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
