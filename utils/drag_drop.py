"""
拖放文件支持
提供文件拖放功能的基类和工具
"""

from PySide6.QtCore import Qt, Signal, QUrl
from PySide6.QtCore import Qt as QtCore
from PySide6.QtWidgets import QWidget
from typing import List, Callable, Optional
from utils.logger import get_logger

logger = get_logger(__name__)


class DragDropMixin:
    """拖放功能混入类

    为任何 QWidget 添加拖放文件功能

    使用方法:
        class MyWidget(QWidget, DragDropMixin):
            def __init__(self):
                super().__init__()
                self.setup_drag_drop(
                    on_files_dropped=self.handle_files,
                    allowed_extensions=['.txt', '.pdf']
                )

            def handle_files(self, files):
                print(f"收到文件: {files}")
    """

    def setup_drag_drop(
        self,
        on_files_dropped: Optional[Callable[[List[str]], None]] = None,
        allowed_extensions: Optional[List[str]] = None,
        allow_directories: bool = False,
        multiple_files: bool = True
    ):
        """设置拖放功能

        Args:
            on_files_dropped: 文件拖放时的回调函数
            allowed_extensions: 允许的文件扩展名列表（如 ['.txt', '.pdf']），None 表示允许所有
            allow_directories: 是否允许拖放目录
            multiple_files: 是否允许多个文件
        """
        self._allowed_extensions = allowed_extensions
        self._allow_directories = allow_directories
        self._multiple_files = multiple_files
        self._on_files_dropped = on_files_dropped

        # 启用拖放
        self.setAcceptDrops(True)

        logger.debug(f"拖放功能已设置: extensions={allowed_extensions}, dirs={allow_directories}, multiple={multiple_files}")
    
    def dragEnterEvent(self, event):
        """拖动进入事件"""
        mime_data = event.mimeData()
        if mime_data.hasUrls():
            event.setDropAction(Qt.DropAction.CopyAction)
            event.accept()
            logger.debug(f"拖动进入: 接受拖放")
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        """拖动移动事件"""
        mime_data = event.mimeData()
        if mime_data.hasUrls():
            event.setDropAction(Qt.DropAction.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        """拖放事件"""
        mime_data = event.mimeData()
        if mime_data.hasUrls():
            urls = mime_data.urls()
            valid_files = self._get_valid_files(urls)

            if valid_files:
                logger.info(f"文件已拖放: {valid_files}")
                if self._on_files_dropped:
                    self._on_files_dropped(valid_files)
                event.setDropAction(Qt.DropAction.CopyAction)
                event.accept()
            else:
                event.ignore()
                logger.warning("拖放的文件不符合要求")
        else:
            event.ignore()
    
    def _get_valid_files(self, urls: List[QUrl]) -> List[str]:
        """获取有效的文件路径列表
        
        Args:
            urls: URL 列表
            
        Returns:
            List[str]: 有效的文件路径列表
        """
        import os
        
        valid_files = []
        
        for url in urls:
            if url.isLocalFile():
                file_path = url.toLocalFile()
                
                # 检查是否是目录
                if os.path.isdir(file_path):
                    if self._allow_directories:
                        valid_files.append(file_path)
                    continue
                
                # 检查是否是文件
                if os.path.isfile(file_path):
                    # 检查扩展名
                    if self._allowed_extensions:
                        _, ext = os.path.splitext(file_path)
                        if ext.lower() not in [e.lower() for e in self._allowed_extensions]:
                            logger.debug(f"文件扩展名不允许: {file_path}")
                            continue
                    
                    valid_files.append(file_path)
                    
                    # 如果不允许多个文件，只返回第一个
                    if not self._multiple_files:
                        break
        
        return valid_files


class DragDropWidget(QWidget):
    """支持拖放的 QWidget

    可以直接使用的拖放组件

    使用方法:
        widget = DragDropWidget()
        widget.setup_drag_drop(on_files_dropped=handle_files)
        widget.set_drop_hint("拖放文件到这里")
    """

    # 信号：文件被拖放时触发
    files_dropped = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._drop_hint = "拖放文件到这里"
        self._is_dragging = False
        self._callback = None
        self._allowed_extensions = None
        self._allow_directories = False
        self._multiple_files = True
        # 启用拖放
        self.setAcceptDrops(True)

    def setup_drag_drop(
        self,
        on_files_dropped: Optional[Callable[[List[str]], None]] = None,
        allowed_extensions: Optional[List[str]] = None,
        allow_directories: bool = False,
        multiple_files: bool = True
    ):
        """设置拖放功能"""
        self._callback = on_files_dropped
        self._allowed_extensions = allowed_extensions
        self._allow_directories = allow_directories
        self._multiple_files = multiple_files
        logger.debug(f"拖放功能已设置: extensions={allowed_extensions}, dirs={allow_directories}, multiple={multiple_files}")

    def set_drop_hint(self, hint: str):
        """设置拖放提示文本

        Args:
            hint: 提示文本
        """
        self._drop_hint = hint
        self.update()

    def dragEnterEvent(self, event):
        """拖动进入事件"""
        mime_data = event.mimeData()
        if mime_data.hasUrls():
            event.setDropAction(Qt.DropAction.CopyAction)
            event.accept()
            self._is_dragging = True
            self.update()
            logger.debug(f"拖动进入: 接受拖放")
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        """拖动移动事件"""
        mime_data = event.mimeData()
        if mime_data.hasUrls():
            event.setDropAction(Qt.DropAction.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        """拖动离开事件"""
        self._is_dragging = False
        self.update()

    def dropEvent(self, event):
        """拖放事件"""
        mime_data = event.mimeData()
        if mime_data.hasUrls():
            urls = mime_data.urls()
            valid_files = self._get_valid_files(urls)

            if valid_files:
                logger.info(f"文件已拖放: {valid_files}")
                # 发射信号
                self.files_dropped.emit(valid_files)
                # 调用回调
                if self._callback:
                    self._callback(valid_files)
                event.setDropAction(Qt.DropAction.CopyAction)
                event.accept()
            else:
                event.ignore()
                logger.warning("拖放的文件不符合要求")
        else:
            event.ignore()

        self._is_dragging = False
        self.update()

    def _get_valid_files(self, urls: List[QUrl]) -> List[str]:
        """获取有效的文件路径列表"""
        import os

        valid_files = []

        for url in urls:
            if url.isLocalFile():
                file_path = url.toLocalFile()

                # 检查是否是目录
                if os.path.isdir(file_path):
                    if self._allow_directories:
                        valid_files.append(file_path)
                    continue

                # 检查是否是文件
                if os.path.isfile(file_path):
                    # 检查扩展名
                    if self._allowed_extensions:
                        _, ext = os.path.splitext(file_path)
                        if ext.lower() not in [e.lower() for e in self._allowed_extensions]:
                            logger.debug(f"文件扩展名不允许: {file_path}")
                            continue

                    valid_files.append(file_path)

                    # 如果不允许多个文件，只返回第一个
                    if not self._multiple_files:
                        break

        return valid_files
    
    def paintEvent(self, event):
        """绘制事件"""
        from PySide6.QtGui import QPainter, QPen, QColor
        from PySide6.QtCore import Qt
        
        super().paintEvent(event)
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 绘制边框
        if self._is_dragging:
            pen = QPen(QColor(0, 120, 215), 2, Qt.DashLine)
            painter.setPen(pen)
            painter.drawRect(self.rect().adjusted(1, 1, -1, -1))
        else:
            pen = QPen(QColor(200, 200, 200), 1, Qt.DashLine)
            painter.setPen(pen)
            painter.drawRect(self.rect().adjusted(1, 1, -1, -1))
        
        # 绘制提示文本
        painter.setPen(QColor(150, 150, 150))
        painter.drawText(self.rect(), Qt.AlignCenter, self._drop_hint)


def create_drag_drop_area(
    parent=None,
    on_files_dropped: Optional[Callable[[List[str]], None]] = None,
    allowed_extensions: Optional[List[str]] = None,
    allow_directories: bool = False,
    multiple_files: bool = True,
    drop_hint: str = "拖放文件到这里",
    min_height: int = 100
) -> DragDropWidget:
    """创建拖放区域
    
    便捷函数，用于快速创建拖放区域
    
    Args:
        parent: 父组件
        on_files_dropped: 文件拖放时的回调函数
        allowed_extensions: 允许的文件扩展名列表
        allow_directories: 是否允许拖放目录
        multiple_files: 是否允许多个文件
        drop_hint: 拖放提示文本
        min_height: 最小高度
        
    Returns:
        DragDropWidget: 拖放组件
    """
    widget = DragDropWidget(parent)
    widget.setup_drag_drop(
        on_files_dropped=on_files_dropped,
        allowed_extensions=allowed_extensions,
        allow_directories=allow_directories,
        multiple_files=multiple_files
    )
    widget.set_drop_hint(drop_hint)
    widget.setMinimumHeight(min_height)
    
    return widget

