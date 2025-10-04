"""
异常处理模块
提供全局异常捕获、错误日志记录和用户友好的错误提示功能
"""

import sys
import traceback
import platform
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

from utils.logger import get_logger
from utils.config import app_config

logger = get_logger(__name__)


class ExceptionHandler:
    """全局异常处理器"""
    
    def __init__(self):
        """初始化异常处理器"""
        self.logger = logger
        self.app = None  # QApplication 实例
        self._original_excepthook = sys.excepthook
        
    def setup(self, app=None):
        """
        设置全局异常处理
        
        Args:
            app: QApplication 实例（可选，用于显示对话框）
        """
        self.app = app
        
        # 检查是否启用异常处理
        if not app_config.exception_handler_enabled:
            self.logger.info("异常处理器已禁用")
            return
        
        # 设置全局异常钩子
        sys.excepthook = self.handle_exception
        self.logger.info("全局异常处理器已启用")
        
    def handle_exception(self, exc_type, exc_value, exc_traceback):
        """
        处理未捕获的异常
        
        Args:
            exc_type: 异常类型
            exc_value: 异常值
            exc_traceback: 异常回溯
        """
        # 忽略 KeyboardInterrupt
        if issubclass(exc_type, KeyboardInterrupt):
            self._original_excepthook(exc_type, exc_value, exc_traceback)
            return
        
        # 格式化异常信息
        error_info = self._format_exception(exc_type, exc_value, exc_traceback)
        
        # 记录到日志
        self.logger.error(f"未捕获的异常: {error_info['exception_type']}: {error_info['exception_message']}")
        self.logger.error(f"异常堆栈:\n{error_info['traceback']}")
        
        # 保存错误报告
        if app_config.exception_handler_save_report:
            report_path = self._save_error_report(error_info)
            if report_path:
                self.logger.info(f"错误报告已保存: {report_path}")
        
        # 显示错误对话框
        if app_config.exception_handler_show_dialog and self.app:
            self._show_error_dialog(error_info)
        
        # 调用原始的异常钩子（用于调试）
        # self._original_excepthook(exc_type, exc_value, exc_traceback)
    
    def _format_exception(self, exc_type, exc_value, exc_traceback) -> Dict[str, Any]:
        """
        格式化异常信息
        
        Args:
            exc_type: 异常类型
            exc_value: 异常值
            exc_traceback: 异常回溯
            
        Returns:
            格式化的异常信息字典
        """
        # 获取异常堆栈
        tb_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        tb_text = ''.join(tb_lines)
        
        # 获取系统信息
        system_info = self._get_system_info()
        
        # 构建错误信息
        error_info = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'app_name': app_config.app_name,
            'app_version': app_config.current_version,
            'exception_type': exc_type.__name__,
            'exception_message': str(exc_value),
            'traceback': tb_text,
            'system_info': system_info
        }
        
        return error_info
    
    def _get_system_info(self) -> Dict[str, str]:
        """
        获取系统信息
        
        Returns:
            系统信息字典
        """
        try:
            # 获取 PySide6 版本
            try:
                from PySide6 import __version__ as pyside6_version
            except:
                pyside6_version = "Unknown"
            
            system_info = {
                'platform': platform.platform(),
                'python_version': platform.python_version(),
                'pyside6_version': pyside6_version,
                'machine': platform.machine(),
                'processor': platform.processor(),
            }
            
            return system_info
        except Exception as e:
            self.logger.error(f"获取系统信息失败: {e}")
            return {'error': str(e)}
    
    def _save_error_report(self, error_info: Dict[str, Any]) -> Optional[str]:
        """
        保存错误报告到文件
        
        Args:
            error_info: 错误信息字典
            
        Returns:
            报告文件路径，失败返回 None
        """
        try:
            # 获取报告目录
            report_dir_name = app_config.exception_handler_report_dir
            
            # 检测是否为编译后的应用程序
            is_frozen = getattr(sys, 'frozen', False)
            is_nuitka_compiled = hasattr(sys.modules.get(__name__.split('.')[0], sys.modules[__name__]), '__compiled__')
            is_compiled = is_frozen or is_nuitka_compiled
            
            if is_compiled:
                # 打包后的应用程序，报告放在exe同目录下
                report_dir = Path(sys.executable).parent / report_dir_name
            else:
                # 开发环境，报告放在项目根目录下
                report_dir = Path(__file__).parent.parent / report_dir_name
            
            # 创建报告目录
            report_dir.mkdir(exist_ok=True)
            
            # 生成报告文件名（使用时间戳）
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_filename = f"error_report_{timestamp}.json"
            report_path = report_dir / report_filename
            
            # 保存报告
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(error_info, f, indent=4, ensure_ascii=False)
            
            return str(report_path)
        
        except Exception as e:
            self.logger.error(f"保存错误报告失败: {e}")
            return None
    
    def _show_error_dialog(self, error_info: Dict[str, Any]):
        """
        显示错误对话框
        
        Args:
            error_info: 错误信息字典
        """
        try:
            # 延迟导入避免循环依赖
            from gui.error_dialog import ErrorDialog
            
            # 创建并显示对话框
            dialog = ErrorDialog(error_info, parent=None)
            dialog.exec()
            
        except Exception as e:
            self.logger.error(f"显示错误对话框失败: {e}")
            # 如果对话框显示失败，至少在控制台输出错误信息
            print(f"\n{'='*60}")
            print(f"程序错误: {error_info['exception_type']}")
            print(f"错误信息: {error_info['exception_message']}")
            print(f"{'='*60}\n")


# 全局异常处理器实例
_exception_handler = ExceptionHandler()


def setup_exception_handler(app=None):
    """
    设置全局异常处理器
    
    Args:
        app: QApplication 实例（可选）
    """
    _exception_handler.setup(app)


def get_exception_handler() -> ExceptionHandler:
    """
    获取全局异常处理器实例
    
    Returns:
        ExceptionHandler 实例
    """
    return _exception_handler

