"""
示例插件
演示如何创建一个简单的插件
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from utils.plugin_base import BasePlugin, PluginMetadata
from utils.logger import get_logger

logger = get_logger(__name__)


class ExamplePlugin(BasePlugin):
    """示例插件类"""
    
    def __init__(self):
        super().__init__()
        self.widget = None
    
    def get_metadata(self) -> PluginMetadata:
        """获取插件元数据"""
        return PluginMetadata(
            name="示例插件",
            version="1.0.0",
            author="Your Name",
            description="这是一个示例插件，演示插件系统的基本功能"
        )
    
    def initialize(self, main_window) -> bool:
        """初始化插件"""
        try:
            self._main_window = main_window
            logger.info("示例插件初始化成功")
            return True
        except Exception as e:
            logger.error(f"示例插件初始化失败: {e}")
            return False
    
    def enable(self) -> bool:
        """启用插件"""
        if super().enable():
            logger.info("示例插件已启用")
            return True
        return False
    
    def disable(self) -> bool:
        """禁用插件"""
        if super().disable():
            logger.info("示例插件已禁用")
            return True
        return False
    
    def get_widget(self) -> QWidget:
        """获取插件的UI组件"""
        if self.widget is None:
            self.widget = QWidget()
            layout = QVBoxLayout()
            
            # 标题
            title = QLabel("示例插件")
            title.setStyleSheet("font-size: 16px; font-weight: bold;")
            layout.addWidget(title)
            
            # 描述
            desc = QLabel("这是一个示例插件，演示插件系统的基本功能。")
            layout.addWidget(desc)
            
            # 按钮
            button = QPushButton("点击我")
            button.clicked.connect(self.on_button_clicked)
            layout.addWidget(button)
            
            layout.addStretch()
            self.widget.setLayout(layout)
        
        return self.widget
    
    def on_button_clicked(self):
        """按钮点击事件"""
        logger.info("示例插件按钮被点击")
        from utils.notification import get_notification_manager
        notification_manager = get_notification_manager()
        notification_manager.info("示例插件", "按钮被点击了！")
    
    def get_menu_items(self) -> list:
        """获取插件的菜单项"""
        return [
            ("示例插件动作", self.on_menu_action)
        ]
    
    def on_menu_action(self):
        """菜单动作"""
        logger.info("示例插件菜单动作被触发")
        from utils.notification import get_notification_manager
        notification_manager = get_notification_manager()
        notification_manager.success("示例插件", "菜单动作被触发！")

