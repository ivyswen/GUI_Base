"""
工具模块
包含全局可用的工具和组件
"""

# 延迟导入避免循环依赖
def get_logger(name=None):
    """获取日志记录器"""
    from .logger import get_logger as _get_logger
    return _get_logger(name)

# 延迟导入的属性
def __getattr__(name):
    if name == 'app_logger':
        from .logger import app_logger
        return app_logger
    elif name == 'update_logger':
        from .logger import update_logger
        return update_logger
    elif name == 'app_config':
        from .config import app_config
        return app_config
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

__all__ = [
    'get_logger',
    'app_logger',
    'update_logger',
    'app_config'
]

__version__ = '1.0.0'
__author__ = 'GUI Base Template'
__description__ = '工具组件模块'
