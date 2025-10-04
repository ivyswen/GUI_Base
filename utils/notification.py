"""
通知/消息系统模块
提供Toast通知、消息中心等功能
"""

from typing import Optional, Callable, List
from datetime import datetime
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QTimer, Signal, QObject
from utils.logger import get_logger

logger = get_logger(__name__)


class NotificationType:
    """通知类型"""
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"


class Notification:
    """通知消息类"""
    
    def __init__(self, title: str, message: str, type: str = NotificationType.INFO,
                 duration: int = 3000, action: Optional[Callable] = None):
        """
        初始化通知
        
        Args:
            title: 通知标题
            message: 通知内容
            type: 通知类型（info/success/warning/error）
            duration: 显示时长（毫秒），0表示不自动关闭
            action: 点击通知时的回调函数
        """
        self.id = id(self)
        self.title = title
        self.message = message
        self.type = type
        self.duration = duration
        self.action = action
        self.timestamp = datetime.now()
        self.read = False
    
    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "title": self.title,
            "message": self.message,
            "type": self.type,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "read": self.read
        }


class NotificationManager(QObject):
    """通知管理器"""
    
    # 信号
    notification_added = Signal(object)  # 新通知添加
    notification_removed = Signal(int)   # 通知移除
    notification_cleared = Signal()      # 所有通知清除
    
    def __init__(self):
        super().__init__()
        self._notifications: List[Notification] = []
        self._max_history = 100  # 最大历史记录数
        logger.info("通知管理器已初始化")
    
    def show(self, title: str, message: str, type: str = NotificationType.INFO,
             duration: int = 3000, action: Optional[Callable] = None) -> Notification:
        """
        显示通知
        
        Args:
            title: 通知标题
            message: 通知内容
            type: 通知类型
            duration: 显示时长（毫秒）
            action: 点击回调
            
        Returns:
            Notification对象
        """
        notification = Notification(title, message, type, duration, action)
        self._notifications.append(notification)
        
        # 限制历史记录数量
        if len(self._notifications) > self._max_history:
            self._notifications.pop(0)
        
        # 发送信号
        self.notification_added.emit(notification)
        
        logger.info(f"显示通知: [{type}] {title} - {message}")
        return notification
    
    def info(self, title: str, message: str, duration: int = 3000,
             action: Optional[Callable] = None) -> Notification:
        """显示信息通知"""
        return self.show(title, message, NotificationType.INFO, duration, action)
    
    def success(self, title: str, message: str, duration: int = 3000,
                action: Optional[Callable] = None) -> Notification:
        """显示成功通知"""
        return self.show(title, message, NotificationType.SUCCESS, duration, action)
    
    def warning(self, title: str, message: str, duration: int = 5000,
                action: Optional[Callable] = None) -> Notification:
        """显示警告通知"""
        return self.show(title, message, NotificationType.WARNING, duration, action)
    
    def error(self, title: str, message: str, duration: int = 0,
              action: Optional[Callable] = None) -> Notification:
        """显示错误通知（默认不自动关闭）"""
        return self.show(title, message, NotificationType.ERROR, duration, action)
    
    def remove(self, notification_id: int):
        """移除通知"""
        self._notifications = [n for n in self._notifications if n.id != notification_id]
        self.notification_removed.emit(notification_id)
        logger.debug(f"移除通知: {notification_id}")
    
    def clear(self):
        """清除所有通知"""
        self._notifications.clear()
        self.notification_cleared.emit()
        logger.info("清除所有通知")
    
    def mark_as_read(self, notification_id: int):
        """标记通知为已读"""
        for notification in self._notifications:
            if notification.id == notification_id:
                notification.read = True
                logger.debug(f"标记通知为已读: {notification_id}")
                break
    
    def mark_all_as_read(self):
        """标记所有通知为已读"""
        for notification in self._notifications:
            notification.read = False
        logger.info("标记所有通知为已读")
    
    def get_all(self) -> List[Notification]:
        """获取所有通知"""
        return self._notifications.copy()
    
    def get_unread(self) -> List[Notification]:
        """获取未读通知"""
        return [n for n in self._notifications if not n.read]
    
    def get_unread_count(self) -> int:
        """获取未读通知数量"""
        return len(self.get_unread())


# 全局通知管理器实例
_notification_manager: Optional[NotificationManager] = None


def setup_notification_manager() -> NotificationManager:
    """设置通知管理器"""
    global _notification_manager
    if _notification_manager is None:
        _notification_manager = NotificationManager()
        logger.info("全局通知管理器已创建")
    return _notification_manager


def get_notification_manager() -> NotificationManager:
    """获取通知管理器"""
    global _notification_manager
    if _notification_manager is None:
        raise RuntimeError("通知管理器未初始化，请先调用 setup_notification_manager()")
    return _notification_manager

