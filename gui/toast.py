"""
Toast通知组件
显示临时的通知消息
"""

from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QGraphicsOpacityEffect
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont
from utils.notification import Notification, NotificationType


class ToastWidget(QWidget):
    """Toast通知部件"""
    
    def __init__(self, notification: Notification, parent=None):
        super().__init__(parent)
        self.notification = notification
        self.init_ui()
        
        # 设置窗口属性
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        
        # 淡入动画
        self.fade_in()
        
        # 自动关闭定时器
        if notification.duration > 0:
            QTimer.singleShot(notification.duration, self.fade_out)
    
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(5)
        
        # 标题
        title_label = QLabel(self.notification.title)
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(10)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        # 消息
        message_label = QLabel(self.notification.message)
        message_label.setWordWrap(True)
        layout.addWidget(message_label)
        
        # 关闭按钮
        close_btn = QPushButton("×")
        close_btn.setFixedSize(20, 20)
        close_btn.clicked.connect(self.fade_out)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 0.1);
            }
        """)
        
        # 顶部布局（标题 + 关闭按钮）
        top_layout = QHBoxLayout()
        top_layout.addWidget(title_label)
        top_layout.addStretch()
        top_layout.addWidget(close_btn)
        
        # 主布局
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addLayout(top_layout)
        main_layout.addWidget(message_label)
        
        self.setLayout(main_layout)
        
        # 设置样式
        self.apply_style()
        
        # 设置固定宽度
        self.setFixedWidth(300)
        self.adjustSize()
    
    def apply_style(self):
        """应用样式"""
        # 根据通知类型设置颜色
        colors = {
            NotificationType.INFO: ("#e7f3ff", "#0d6efd", "#084298"),
            NotificationType.SUCCESS: ("#d1e7dd", "#198754", "#0f5132"),
            NotificationType.WARNING: ("#fff3cd", "#ffc107", "#997404"),
            NotificationType.ERROR: ("#f8d7da", "#dc3545", "#842029")
        }
        
        bg_color, border_color, text_color = colors.get(
            self.notification.type,
            colors[NotificationType.INFO]
        )
        
        self.setStyleSheet(f"""
            ToastWidget {{
                background-color: {bg_color};
                border: 2px solid {border_color};
                border-radius: 8px;
            }}
            QLabel {{
                color: {text_color};
                background-color: transparent;
            }}
        """)
    
    def fade_in(self):
        """淡入动画"""
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(300)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.animation.start()
    
    def fade_out(self):
        """淡出动画"""
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(300)
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.animation.finished.connect(self.close)
        self.animation.start()
    
    def mousePressEvent(self, event):
        """鼠标点击事件"""
        if self.notification.action:
            self.notification.action()
        self.fade_out()


class ToastManager:
    """Toast管理器"""
    
    def __init__(self, parent_widget: QWidget):
        self.parent = parent_widget
        self.toasts: list[ToastWidget] = []
        self.spacing = 10
        self.margin = 20
    
    def show_toast(self, notification: Notification):
        """显示Toast"""
        toast = ToastWidget(notification, self.parent)
        self.toasts.append(toast)
        
        # 定位Toast
        self.reposition_toasts()
        
        toast.show()
        
        # Toast关闭时从列表移除
        toast.destroyed.connect(lambda: self.remove_toast(toast))
    
    def remove_toast(self, toast: ToastWidget):
        """移除Toast"""
        if toast in self.toasts:
            self.toasts.remove(toast)
            self.reposition_toasts()

    def reposition_toasts(self):
        """重新定位所有Toast"""
        # 检查父窗口是否仍然有效
        if not self.parent:
            return

        try:
            parent_rect = self.parent.rect()
        except RuntimeError:
            # 父窗口已被删除，清空Toast列表
            self.toasts.clear()
            return

        y = self.margin

        for toast in self.toasts:
            x = parent_rect.width() - toast.width() - self.margin
            toast.move(x, y)
            y += toast.height() + self.spacing

