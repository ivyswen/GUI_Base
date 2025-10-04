"""
系统托盘模块
提供系统托盘图标和菜单功能
"""

from PySide6.QtWidgets import QSystemTrayIcon, QMenu
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import QObject, Signal
from utils.logger import get_logger
from utils.config import app_config

logger = get_logger(__name__)


class SystemTray(QObject):
    """系统托盘类"""
    
    # 信号
    show_window_requested = Signal()
    quit_requested = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.tray_icon = None
        self.tray_menu = None
        
        # 初始化托盘
        self.init_tray()
    
    def init_tray(self):
        """初始化系统托盘"""
        # 创建托盘图标
        self.tray_icon = QSystemTrayIcon(self.parent_window)

        # 设置图标
        icon = QIcon("Resources/favicon.ico")
        if icon.isNull():
            logger.warning("托盘图标文件不存在，使用默认图标")
            # 尝试使用窗口图标
            if self.parent_window:
                icon = self.parent_window.windowIcon()
        self.tray_icon.setIcon(icon)
        
        # 设置提示文字
        self.tray_icon.setToolTip(app_config.app_name)
        
        # 创建托盘菜单
        self.create_tray_menu()
        
        # 连接信号
        self.tray_icon.activated.connect(self.on_tray_activated)
        
        logger.info("系统托盘已初始化")
    
    def create_tray_menu(self):
        """创建托盘菜单"""
        self.tray_menu = QMenu()
        
        # 显示主窗口
        show_action = QAction("显示主窗口", self.tray_menu)
        show_action.triggered.connect(self.show_window)
        self.tray_menu.addAction(show_action)
        
        # 分隔符
        self.tray_menu.addSeparator()
        
        # 退出
        quit_action = QAction("退出", self.tray_menu)
        quit_action.triggered.connect(self.quit_application)
        self.tray_menu.addAction(quit_action)
        
        # 设置菜单
        self.tray_icon.setContextMenu(self.tray_menu)
    
    def show(self):
        """显示托盘图标"""
        if self.tray_icon:
            self.tray_icon.show()
            logger.info("系统托盘图标已显示")
    
    def hide(self):
        """隐藏托盘图标"""
        if self.tray_icon:
            self.tray_icon.hide()
            logger.info("系统托盘图标已隐藏")
    
    def show_message(self, title: str, message: str, icon=QSystemTrayIcon.MessageIcon.Information, duration: int = 3000):
        """显示托盘消息
        
        Args:
            title: 消息标题
            message: 消息内容
            icon: 消息图标类型
            duration: 显示时长（毫秒）
        """
        if self.tray_icon and self.tray_icon.isVisible():
            self.tray_icon.showMessage(title, message, icon, duration)
            logger.debug(f"托盘消息: {title} - {message}")
    
    def on_tray_activated(self, reason):
        """托盘图标激活事件
        
        Args:
            reason: 激活原因
        """
        # 双击或单击托盘图标时显示主窗口
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick or reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.show_window()
    
    def show_window(self):
        """显示主窗口"""
        self.show_window_requested.emit()
        logger.debug("请求显示主窗口")
    
    def quit_application(self):
        """退出应用程序"""
        self.quit_requested.emit()
        logger.debug("请求退出应用程序")
    
    def cleanup(self):
        """清理资源"""
        if self.tray_icon:
            self.tray_icon.hide()
            self.tray_icon = None
        logger.info("系统托盘已清理")

