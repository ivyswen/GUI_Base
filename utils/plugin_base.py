"""
插件基类模块
定义插件的标准接口和基类
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from PySide6.QtWidgets import QWidget
from utils.logger import get_logger

logger = get_logger(__name__)


class PluginMetadata:
    """插件元数据"""
    
    def __init__(self, name: str, version: str, author: str, description: str):
        self.name = name
        self.version = version
        self.author = author
        self.description = description
    
    def to_dict(self) -> Dict[str, str]:
        """转换为字典"""
        return {
            "name": self.name,
            "version": self.version,
            "author": self.author,
            "description": self.description
        }


class BasePlugin(ABC):
    """插件基类
    
    所有插件都应该继承此类并实现必要的方法
    """
    
    def __init__(self):
        self._enabled = False
        self._main_window = None
        self._config = {}
    
    @abstractmethod
    def get_metadata(self) -> PluginMetadata:
        """获取插件元数据
        
        Returns:
            PluginMetadata: 插件元数据
        """
        pass
    
    @abstractmethod
    def initialize(self, main_window) -> bool:
        """初始化插件
        
        Args:
            main_window: 主窗口实例
            
        Returns:
            bool: 初始化是否成功
        """
        pass
    
    def enable(self) -> bool:
        """启用插件
        
        Returns:
            bool: 启用是否成功
        """
        try:
            self._enabled = True
            logger.info(f"插件已启用: {self.get_metadata().name}")
            return True
        except Exception as e:
            logger.error(f"启用插件失败: {e}")
            return False
    
    def disable(self) -> bool:
        """禁用插件
        
        Returns:
            bool: 禁用是否成功
        """
        try:
            self._enabled = False
            logger.info(f"插件已禁用: {self.get_metadata().name}")
            return True
        except Exception as e:
            logger.error(f"禁用插件失败: {e}")
            return False
    
    def cleanup(self):
        """清理插件资源"""
        pass
    
    def is_enabled(self) -> bool:
        """检查插件是否已启用"""
        return self._enabled
    
    def get_config(self) -> Dict[str, Any]:
        """获取插件配置"""
        return self._config
    
    def set_config(self, config: Dict[str, Any]):
        """设置插件配置"""
        self._config = config
    
    def get_widget(self) -> Optional[QWidget]:
        """获取插件的UI组件（可选）
        
        Returns:
            Optional[QWidget]: 插件的UI组件，如果没有则返回None
        """
        return None
    
    def get_menu_items(self) -> list:
        """获取插件的菜单项（可选）
        
        Returns:
            list: 菜单项列表，每个元素是 (name, callback) 元组
        """
        return []

