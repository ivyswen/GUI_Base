"""
日志配置模块
使用 loguru 提供统一的日志记录功能
"""

import sys
import os
from pathlib import Path
from loguru import logger
from .config import app_config


def setup_logger():
    """设置日志配置"""
    # 移除默认的控制台输出
    logger.remove()

    # 检测是否为编译后的应用程序
    is_frozen = getattr(sys, 'frozen', False)  # PyInstaller, cx_Freeze
    is_nuitka_compiled = hasattr(sys.modules.get(__name__.split('.')[0], sys.modules[__name__]), '__compiled__')  # Nuitka
    is_compiled = is_frozen or is_nuitka_compiled

    # 获取日志目录
    if is_compiled:
        # 打包后的应用程序，日志放在exe同目录下
        log_dir = Path(sys.executable).parent / "logs"
    else:
        # 开发环境，日志放在项目根目录下
        log_dir = Path(__file__).parent.parent / "logs"

    # 创建日志目录
    log_dir.mkdir(exist_ok=True)

    # 根据环境设置日志级别
    if is_compiled:
        # 生产环境：使用INFO级别
        console_level = "INFO"
        file_level = "INFO"
    else:
        # 开发环境：使用DEBUG级别
        console_level = "DEBUG"
        file_level = "DEBUG"

    # 控制台输出（开发环境）
    if not is_compiled:
        logger.add(
            sys.stderr,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            level=console_level,
            colorize=True
        )
    
    # 详细日志文件
    logger.add(
        log_dir / "app_debug.log",
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
        level=file_level,
        rotation="10 MB",
        retention="7 days",
        compression="zip",
        encoding="utf-8"
    )
    
    # 错误日志文件（只记录错误）
    logger.add(
        log_dir / "app_error.log",
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
        level="ERROR",
        rotation="5 MB",
        retention="30 days",
        compression="zip",
        encoding="utf-8"
    )
    
    # 更新相关的专用日志文件
    logger.add(
        log_dir / "update.log",
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
        level="INFO",
        rotation="5 MB",
        retention="30 days",
        compression="zip",
        encoding="utf-8",
        filter=lambda record: "update" in (record.get("name", "") or "").lower() or "update" in record["message"].lower()
    )
    
    # 记录启动信息
    logger.info(f"应用程序启动: {app_config.app_name} v{app_config.current_version}")
    logger.info(f"日志目录: {log_dir}")
    logger.info(f"运行环境: {'生产环境 (exe)' if is_compiled else '开发环境'}")
    logger.info(f"日志级别: {file_level}")
    
    return logger


def get_logger(name: str | None = None):
    """
    获取日志记录器
    
    Args:
        name: 日志记录器名称，通常使用 __name__
        
    Returns:
        配置好的日志记录器
    """
    if name:
        return logger.bind(name=name)
    return logger


# 初始化日志系统
setup_logger()

# 导出常用的日志记录器
app_logger = get_logger("app")
update_logger = get_logger("updater")
