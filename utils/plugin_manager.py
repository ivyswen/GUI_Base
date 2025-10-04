"""
插件管理器模块
负责插件的发现、加载、管理和卸载
"""

import os
import sys
import importlib
import importlib.util
from typing import Dict, List, Optional
from pathlib import Path
from utils.logger import get_logger
from utils.plugin_base import BasePlugin

logger = get_logger(__name__)


class PluginManager:
    """插件管理器"""
    
    def __init__(self, plugin_dir: str = "plugins"):
        self.plugin_dir = plugin_dir
        self.plugins: Dict[str, BasePlugin] = {}
        self._main_window = None
        
        # 确保插件目录存在
        os.makedirs(self.plugin_dir, exist_ok=True)
        
        logger.info(f"插件管理器已初始化，插件目录: {self.plugin_dir}")
    
    def set_main_window(self, main_window):
        """设置主窗口引用"""
        self._main_window = main_window
    
    def discover_plugins(self) -> List[str]:
        """发现所有可用的插件
        
        Returns:
            List[str]: 发现的插件名称列表
        """
        discovered = []
        plugin_path = Path(self.plugin_dir)
        
        if not plugin_path.exists():
            logger.warning(f"插件目录不存在: {self.plugin_dir}")
            return discovered
        
        # 遍历插件目录
        for item in plugin_path.iterdir():
            if item.is_dir() and not item.name.startswith('_'):
                # 检查是否有 __init__.py
                init_file = item / "__init__.py"
                if init_file.exists():
                    discovered.append(item.name)
                    logger.debug(f"发现插件: {item.name}")
        
        logger.info(f"共发现 {len(discovered)} 个插件")
        return discovered
    
    def load_plugin(self, plugin_name: str) -> bool:
        """加载指定的插件
        
        Args:
            plugin_name: 插件名称
            
        Returns:
            bool: 加载是否成功
        """
        try:
            # 构建插件模块路径
            module_path = f"{self.plugin_dir}.{plugin_name}"
            
            # 导入插件模块
            module = importlib.import_module(module_path)
            
            # 查找插件类（应该继承自BasePlugin）
            plugin_class = None
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (isinstance(attr, type) and 
                    issubclass(attr, BasePlugin) and 
                    attr is not BasePlugin):
                    plugin_class = attr
                    break
            
            if plugin_class is None:
                logger.error(f"插件 {plugin_name} 中未找到有效的插件类")
                return False
            
            # 实例化插件
            plugin = plugin_class()
            
            # 初始化插件
            if self._main_window:
                if not plugin.initialize(self._main_window):
                    logger.error(f"插件 {plugin_name} 初始化失败")
                    return False
            
            # 保存插件实例
            self.plugins[plugin_name] = plugin
            
            logger.info(f"插件已加载: {plugin_name}")
            return True
            
        except Exception as e:
            logger.error(f"加载插件 {plugin_name} 失败: {e}")
            return False
    
    def unload_plugin(self, plugin_name: str) -> bool:
        """卸载指定的插件
        
        Args:
            plugin_name: 插件名称
            
        Returns:
            bool: 卸载是否成功
        """
        try:
            if plugin_name not in self.plugins:
                logger.warning(f"插件 {plugin_name} 未加载")
                return False
            
            plugin = self.plugins[plugin_name]
            
            # 禁用插件
            if plugin.is_enabled():
                plugin.disable()
            
            # 清理插件资源
            plugin.cleanup()
            
            # 从字典中移除
            del self.plugins[plugin_name]
            
            logger.info(f"插件已卸载: {plugin_name}")
            return True
            
        except Exception as e:
            logger.error(f"卸载插件 {plugin_name} 失败: {e}")
            return False
    
    def enable_plugin(self, plugin_name: str) -> bool:
        """启用指定的插件
        
        Args:
            plugin_name: 插件名称
            
        Returns:
            bool: 启用是否成功
        """
        if plugin_name not in self.plugins:
            logger.warning(f"插件 {plugin_name} 未加载")
            return False
        
        return self.plugins[plugin_name].enable()
    
    def disable_plugin(self, plugin_name: str) -> bool:
        """禁用指定的插件
        
        Args:
            plugin_name: 插件名称
            
        Returns:
            bool: 禁用是否成功
        """
        if plugin_name not in self.plugins:
            logger.warning(f"插件 {plugin_name} 未加载")
            return False
        
        return self.plugins[plugin_name].disable()
    
    def get_plugin(self, plugin_name: str) -> Optional[BasePlugin]:
        """获取指定的插件实例
        
        Args:
            plugin_name: 插件名称
            
        Returns:
            Optional[BasePlugin]: 插件实例，如果不存在则返回None
        """
        return self.plugins.get(plugin_name)
    
    def get_all_plugins(self) -> Dict[str, BasePlugin]:
        """获取所有已加载的插件"""
        return self.plugins.copy()
    
    def load_all_plugins(self):
        """加载所有发现的插件"""
        discovered = self.discover_plugins()
        for plugin_name in discovered:
            self.load_plugin(plugin_name)
    
    def cleanup_all(self):
        """清理所有插件"""
        for plugin_name in list(self.plugins.keys()):
            self.unload_plugin(plugin_name)


# 全局插件管理器实例
_plugin_manager: Optional[PluginManager] = None


def setup_plugin_manager(plugin_dir: str = "plugins") -> PluginManager:
    """设置插件管理器"""
    global _plugin_manager
    if _plugin_manager is None:
        _plugin_manager = PluginManager(plugin_dir)
        logger.info("全局插件管理器已创建")
    return _plugin_manager


def get_plugin_manager() -> PluginManager:
    """获取插件管理器"""
    global _plugin_manager
    if _plugin_manager is None:
        raise RuntimeError("插件管理器未初始化，请先调用 setup_plugin_manager()")
    return _plugin_manager

