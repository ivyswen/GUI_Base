"""
主题管理模块
提供深色/浅色主题切换和系统主题检测功能
"""

import sys
import platform
import subprocess
from typing import Optional, Literal

from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from .logger import get_logger
from .config import app_config

# 获取日志记录器
logger = get_logger(__name__)

# 主题模式类型
ThemeMode = Literal["light", "dark", "auto"]

# 浅色主题颜色方案
LIGHT_COLORS = {
    "window": "#ffffff",
    "window_text": "#212529",
    "base": "#ffffff",
    "alternate_base": "#f8f9fa",
    "text": "#212529",
    "button": "#f0f0f0",
    "button_text": "#212529",
    "bright_text": "#ffffff",
    "highlight": "#007bff",
    "highlighted_text": "#ffffff",
    "link": "#007bff",
    "disabled_text": "#6c757d",
    "disabled_button": "#e9ecef",
}

# 深色主题颜色方案
DARK_COLORS = {
    "window": "#1e1e1e",
    "window_text": "#e0e0e0",
    "base": "#2d2d2d",
    "alternate_base": "#252525",
    "text": "#e0e0e0",
    "button": "#3c3c3c",
    "button_text": "#e0e0e0",
    "bright_text": "#ffffff",
    "highlight": "#0d6efd",
    "highlighted_text": "#ffffff",
    "link": "#4dabf7",
    "disabled_text": "#808080",
    "disabled_button": "#2a2a2a",
}


class ThemeManager:
    """主题管理器类"""
    
    def __init__(self, app: Optional[QApplication] = None):
        """初始化主题管理器
        
        Args:
            app: QApplication 实例
        """
        self.app = app
        self._current_theme: ThemeMode = "light"
        self._is_dark = False
        logger.info("主题管理器已初始化")
    
    def detect_system_theme(self) -> Literal["light", "dark"]:
        """检测系统主题
        
        Returns:
            "light" 或 "dark"
        """
        system = platform.system()
        
        try:
            if system == "Windows":
                return self._detect_windows_theme()
            elif system == "Darwin":  # macOS
                return self._detect_macos_theme()
            elif system == "Linux":
                return self._detect_linux_theme()
            else:
                logger.warning(f"不支持的操作系统: {system}，使用默认浅色主题")
                return "light"
        except Exception as e:
            logger.error(f"检测系统主题失败: {e}，使用默认浅色主题")
            return "light"
    
    def _detect_windows_theme(self) -> Literal["light", "dark"]:
        """检测 Windows 系统主题
        
        Returns:
            "light" 或 "dark"
        """
        try:
            import winreg
            
            # 读取注册表
            registry_path = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_path)
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            winreg.CloseKey(key)
            
            # 0 = 深色主题, 1 = 浅色主题
            theme = "light" if value == 1 else "dark"
            logger.info(f"检测到 Windows 系统主题: {theme}")
            return theme
        except Exception as e:
            logger.warning(f"无法检测 Windows 系统主题: {e}")
            return "light"
    
    def _detect_macos_theme(self) -> Literal["light", "dark"]:
        """检测 macOS 系统主题
        
        Returns:
            "light" 或 "dark"
        """
        try:
            # 执行命令检测主题
            result = subprocess.run(
                ["defaults", "read", "-g", "AppleInterfaceStyle"],
                capture_output=True,
                text=True,
                timeout=2
            )
            
            # 如果返回 "Dark"，则为深色主题
            theme = "dark" if "Dark" in result.stdout else "light"
            logger.info(f"检测到 macOS 系统主题: {theme}")
            return theme
        except subprocess.TimeoutExpired:
            logger.warning("检测 macOS 系统主题超时")
            return "light"
        except Exception as e:
            logger.warning(f"无法检测 macOS 系统主题: {e}")
            return "light"
    
    def _detect_linux_theme(self) -> Literal["light", "dark"]:
        """检测 Linux 系统主题
        
        Returns:
            "light" 或 "dark"
        """
        try:
            # 尝试使用 gsettings 检测 GNOME 主题
            result = subprocess.run(
                ["gsettings", "get", "org.gnome.desktop.interface", "gtk-theme"],
                capture_output=True,
                text=True,
                timeout=2
            )
            
            # 检查主题名称中是否包含 "dark"
            theme_name = result.stdout.strip().lower()
            theme = "dark" if "dark" in theme_name else "light"
            logger.info(f"检测到 Linux 系统主题: {theme} (主题名: {theme_name})")
            return theme
        except subprocess.TimeoutExpired:
            logger.warning("检测 Linux 系统主题超时")
            return "light"
        except Exception as e:
            logger.warning(f"无法检测 Linux 系统主题: {e}")
            return "light"
    
    def _apply_palette(self, is_dark: bool):
        """应用调色板
        
        Args:
            is_dark: 是否为深色主题
        """
        if not self.app:
            logger.warning("QApplication 未设置，无法应用调色板")
            return
        
        # 选择颜色方案
        colors = DARK_COLORS if is_dark else LIGHT_COLORS
        
        # 创建调色板
        palette = QPalette()
        
        # 设置各种颜色角色
        palette.setColor(QPalette.ColorRole.Window, QColor(colors["window"]))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(colors["window_text"]))
        palette.setColor(QPalette.ColorRole.Base, QColor(colors["base"]))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(colors["alternate_base"]))
        palette.setColor(QPalette.ColorRole.Text, QColor(colors["text"]))
        palette.setColor(QPalette.ColorRole.Button, QColor(colors["button"]))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(colors["button_text"]))
        palette.setColor(QPalette.ColorRole.BrightText, QColor(colors["bright_text"]))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(colors["highlight"]))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(colors["highlighted_text"]))
        palette.setColor(QPalette.ColorRole.Link, QColor(colors["link"]))
        
        # 设置禁用状态的颜色
        palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, QColor(colors["disabled_text"]))
        palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, QColor(colors["disabled_text"]))
        palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, QColor(colors["disabled_button"]))
        
        # 应用调色板
        self.app.setPalette(palette)
        logger.debug(f"已应用{'深色' if is_dark else '浅色'}主题调色板")
    
    def _get_stylesheet(self, is_dark: bool) -> str:
        """获取全局样式表
        
        Args:
            is_dark: 是否为深色主题
            
        Returns:
            QSS 样式表字符串
        """
        if is_dark:
            # 深色主题样式表
            return """
                QMainWindow {
                    background-color: #1e1e1e;
                    color: #e0e0e0;
                }
                QMenuBar {
                    background-color: #2d2d2d;
                    color: #e0e0e0;
                }
                QMenuBar::item:selected {
                    background-color: #3c3c3c;
                }
                QMenu {
                    background-color: #2d2d2d;
                    color: #e0e0e0;
                    border: 1px solid #3c3c3c;
                }
                QMenu::item:selected {
                    background-color: #0d6efd;
                }
                QStatusBar {
                    background-color: #2d2d2d;
                    color: #e0e0e0;
                }
                QTabWidget::pane {
                    border: 1px solid #3c3c3c;
                    background-color: #1e1e1e;
                }
                QTabBar::tab {
                    background-color: #2d2d2d;
                    color: #e0e0e0;
                    padding: 8px 16px;
                    border: 1px solid #3c3c3c;
                }
                QTabBar::tab:selected {
                    background-color: #1e1e1e;
                    border-bottom-color: #1e1e1e;
                }
                QTextEdit, QPlainTextEdit {
                    background-color: #2d2d2d;
                    color: #e0e0e0;
                    border: 1px solid #3c3c3c;
                }
                QLabel {
                    color: #e0e0e0;
                }
                QGroupBox {
                    color: #e0e0e0;
                    border: 2px solid #3c3c3c;
                }
            """
        else:
            # 浅色主题样式表
            return """
                QMainWindow {
                    background-color: #ffffff;
                    color: #212529;
                }
                QMenuBar {
                    background-color: #f8f9fa;
                    color: #212529;
                }
                QMenuBar::item:selected {
                    background-color: #e9ecef;
                }
                QMenu {
                    background-color: #ffffff;
                    color: #212529;
                    border: 1px solid #dee2e6;
                }
                QMenu::item:selected {
                    background-color: #007bff;
                    color: #ffffff;
                }
                QStatusBar {
                    background-color: #f8f9fa;
                    color: #212529;
                }
                QTabWidget::pane {
                    border: 1px solid #dee2e6;
                    background-color: #ffffff;
                }
                QTabBar::tab {
                    background-color: #f8f9fa;
                    color: #212529;
                    padding: 8px 16px;
                    border: 1px solid #dee2e6;
                }
                QTabBar::tab:selected {
                    background-color: #ffffff;
                    border-bottom-color: #ffffff;
                }
                QTextEdit, QPlainTextEdit {
                    background-color: #ffffff;
                    color: #212529;
                    border: 1px solid #ced4da;
                }
                QLabel {
                    color: #212529;
                }
                QGroupBox {
                    color: #212529;
                    border: 2px solid #cccccc;
                }
            """
    
    def apply_theme(self, theme_mode: ThemeMode):
        """应用主题
        
        Args:
            theme_mode: 主题模式 ("light", "dark", "auto")
        """
        # 确定实际主题
        if theme_mode == "auto":
            actual_theme = self.detect_system_theme()
        else:
            actual_theme = theme_mode
        
        self._is_dark = (actual_theme == "dark")
        self._current_theme = theme_mode
        
        # 应用调色板
        self._apply_palette(self._is_dark)
        
        # 应用样式表
        if self.app:
            stylesheet = self._get_stylesheet(self._is_dark)
            self.app.setStyleSheet(stylesheet)
        
        logger.info(f"已应用主题: {theme_mode} (实际: {actual_theme})")
    
    def get_current_theme(self) -> ThemeMode:
        """获取当前主题模式
        
        Returns:
            当前主题模式
        """
        return self._current_theme
    
    def is_dark_theme(self) -> bool:
        """判断当前是否为深色主题
        
        Returns:
            True 如果当前为深色主题
        """
        return self._is_dark
    
    def set_theme(self, theme_mode: ThemeMode, save: bool = True):
        """设置主题
        
        Args:
            theme_mode: 主题模式 ("light", "dark", "auto")
            save: 是否保存到配置文件
        """
        # 应用主题
        self.apply_theme(theme_mode)
        
        # 保存配置
        if save:
            app_config.set_theme_mode(theme_mode)
            logger.info(f"主题设置已保存: {theme_mode}")


# 全局主题管理器实例
_theme_manager: Optional[ThemeManager] = None


def setup_theme_manager(app: QApplication):
    """设置主题管理器
    
    Args:
        app: QApplication 实例
    """
    global _theme_manager
    
    _theme_manager = ThemeManager(app)
    
    # 从配置加载主题
    theme_mode = app_config.theme_mode
    _theme_manager.apply_theme(theme_mode)
    
    logger.info(f"主题管理器已设置，当前主题: {theme_mode}")


def get_theme_manager() -> ThemeManager:
    """获取主题管理器实例
    
    Returns:
        ThemeManager 实例
        
    Raises:
        RuntimeError: 如果主题管理器未初始化
    """
    if _theme_manager is None:
        raise RuntimeError("主题管理器未初始化，请先调用 setup_theme_manager()")
    return _theme_manager

