"""
显示优化模块
处理高DPI显示、字体渲染等显示相关问题
"""

import os
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


def setup_high_dpi_support():
    """设置高DPI支持"""
    # 设置环境变量
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    os.environ["QT_SCALE_FACTOR"] = "1"
    os.environ["QT_SCREEN_SCALE_FACTORS"] = "1"

    # 启用高DPI缩放
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)


def setup_font_rendering(app: QApplication):
    """设置字体渲染优化"""
    # 设置默认字体
    font = get_optimized_font()
    app.setFont(font)


def get_optimized_font():
    """获取优化的字体设置"""
    font = QFont()
    
    # 根据操作系统选择合适的字体
    if sys.platform == "win32":
        # Windows系统使用微软雅黑
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
    elif sys.platform == "darwin":
        # macOS系统使用系统字体
        font.setFamily("SF Pro Display")
        font.setPointSize(13)
    else:
        # Linux系统使用Noto字体
        font.setFamily("Noto Sans CJK SC")
        font.setPointSize(10)
    
    # 设置字体渲染选项
    font.setHintingPreference(QFont.HintingPreference.PreferFullHinting)
    font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
    
    return font


def get_display_scale_factor():
    """获取显示缩放因子"""
    try:
        app = QApplication.instance()
        if app:
            screen = app.primaryScreen()
            if screen:
                return screen.devicePixelRatio()
    except:
        pass
    return 1.0


def apply_font_to_widget(widget, font_size=None, font_family=None, bold=False):
    """为特定控件应用字体设置
    
    Args:
        widget: 要设置字体的控件
        font_size: 字体大小（可选）
        font_family: 字体族（可选）
        bold: 是否加粗（可选）
    """
    font = widget.font()
    
    if font_family:
        font.setFamily(font_family)
    
    if font_size:
        font.setPointSize(font_size)
    
    if bold:
        font.setBold(True)
    
    # 设置字体渲染优化
    font.setHintingPreference(QFont.HintingPreference.PreferFullHinting)
    font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
    
    widget.setFont(font)


def get_title_font():
    """获取标题字体"""
    font = get_optimized_font()
    font.setPointSize(font.pointSize() + 6)  # 标题字体更大
    font.setBold(True)
    return font


def get_subtitle_font():
    """获取副标题字体"""
    font = get_optimized_font()
    font.setPointSize(font.pointSize() + 2)  # 副标题字体稍大
    font.setBold(True)
    return font


def get_body_font():
    """获取正文字体"""
    return get_optimized_font()


def get_small_font():
    """获取小字体"""
    font = get_optimized_font()
    font.setPointSize(max(8, font.pointSize() - 1))  # 小字体，但不小于8pt
    return font
