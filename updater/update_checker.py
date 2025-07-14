"""
更新检查模块
负责检查远程版本信息，比较版本号，处理更新逻辑
"""

import json
import urllib.request
import urllib.error
from typing import Dict, Any, Optional, Tuple
from packaging import version
from PySide6.QtCore import QObject, QThread, Signal
from .config import app_config
from .logger import get_logger

logger = get_logger(__name__)


def clean_url(url: str) -> str:
    """
    清理URL，修复常见的格式问题

    Args:
        url: 原始URL

    Returns:
        清理后的URL
    """
    if not url:
        return url

    # 修复重复的协议前缀
    if url.startswith('https://https://'):
        cleaned_url = url.replace('https://https://', 'https://')
        logger.warning(f"修复重复的https协议: {url} -> {cleaned_url}")
        return cleaned_url
    elif url.startswith('http://https://'):
        cleaned_url = url.replace('http://https://', 'https://')
        logger.warning(f"修复混合协议: {url} -> {cleaned_url}")
        return cleaned_url
    elif url.startswith('http://http://'):
        cleaned_url = url.replace('http://http://', 'http://')
        logger.warning(f"修复重复的http协议: {url} -> {cleaned_url}")
        return cleaned_url

    # 移除多余的斜杠
    if '://' in url:
        protocol, rest = url.split('://', 1)
        # 移除多余的斜杠，但保留路径中的斜杠
        rest = rest.replace('//', '/')
        cleaned_url = f"{protocol}://{rest}"
        if cleaned_url != url:
            logger.debug(f"清理URL中的多余斜杠: {url} -> {cleaned_url}")
        return cleaned_url

    return url


class VersionInfo:
    """版本信息类"""
    
    def __init__(self, version_str: str, changelog: str = "", 
                 url: str = "", update_exe_url: str = "", 
                 sha256_package: str = "", sha256_update_exe: str = ""):
        """
        初始化版本信息
        
        Args:
            version_str: 版本号字符串
            changelog: 更新日志
            url: 下载链接
            update_exe_url: 更新程序下载链接
            sha256_package: 安装包SHA256
            sha256_update_exe: 更新程序SHA256
        """
        self.version = version_str
        self.changelog = changelog
        self.url = clean_url(url)
        self.update_exe_url = clean_url(update_exe_url)
        self.sha256_package = sha256_package
        self.sha256_update_exe = sha256_update_exe
    
    def __str__(self) -> str:
        return f"Version {self.version}"
    
    def __repr__(self) -> str:
        return f"VersionInfo(version='{self.version}', url='{self.url}')"


class UpdateCheckWorker(QThread):
    """更新检查工作线程"""
    
    # 信号定义
    update_available = Signal(VersionInfo)  # 有更新可用
    no_update = Signal()                    # 无更新
    error_occurred = Signal(str)            # 发生错误
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.check_url = app_config.update_check_url
        self.current_version = app_config.current_version
        self.timeout = app_config.update_check_timeout
    
    def run(self):
        """执行更新检查"""
        logger.info(f"开始检查更新，当前版本: {self.current_version}")
        logger.info(f"检查URL: {self.check_url}")

        try:
            # 获取远程版本信息
            logger.debug("正在获取远程版本信息...")
            remote_info = self._fetch_remote_version_info()
            if not remote_info:
                logger.error("无法获取远程版本信息")
                self.error_occurred.emit("无法获取远程版本信息")
                return

            logger.debug(f"获取到远程版本信息: {remote_info}")

            # 解析版本信息
            version_info = self._parse_version_info(remote_info)
            if not version_info:
                logger.error("版本信息格式错误")
                self.error_occurred.emit("版本信息格式错误")
                return

            logger.info(f"解析版本信息成功: {version_info.version}")

            # 比较版本
            if self._is_newer_version(version_info.version, self.current_version):
                logger.info(f"发现新版本: {version_info.version} > {self.current_version}")
                self.update_available.emit(version_info)
            else:
                logger.info(f"当前已是最新版本: {self.current_version}")
                self.no_update.emit()

        except Exception as e:
            logger.exception(f"检查更新时发生错误: {str(e)}")
            self.error_occurred.emit(f"检查更新时发生错误: {str(e)}")
    
    def _fetch_remote_version_info(self) -> Optional[Dict[str, Any]]:
        """
        获取远程版本信息

        Returns:
            远程版本信息字典，失败返回None
        """
        try:
            logger.debug(f"创建HTTP请求到: {self.check_url}")

            # 创建请求
            request = urllib.request.Request(
                self.check_url,
                headers={
                    'User-Agent': f'{app_config.app_name}/{self.current_version}',
                    'Accept': 'application/json'
                }
            )

            logger.debug(f"请求头: User-Agent={app_config.app_name}/{self.current_version}")
            logger.debug(f"超时时间: {self.timeout}秒")

            # 发送请求
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                logger.debug(f"收到响应，状态码: {response.status}")

                if response.status == 200:
                    data = response.read().decode('utf-8')
                    logger.debug(f"响应数据长度: {len(data)} 字符")
                    logger.debug(f"响应内容: {data[:500]}...")  # 只记录前500字符

                    json_data = json.loads(data)
                    logger.info("成功解析JSON响应")
                    return json_data
                else:
                    logger.error(f"服务器返回错误状态码: {response.status}")
                    return None

        except urllib.error.URLError as e:
            logger.error(f"网络请求失败: {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"JSON解析失败: {e}")
            return None
        except Exception as e:
            logger.exception(f"获取远程版本信息失败: {e}")
            return None
    
    def _parse_version_info(self, remote_info: Dict[str, Any]) -> Optional[VersionInfo]:
        """
        解析版本信息
        
        Args:
            remote_info: 远程版本信息字典
            
        Returns:
            VersionInfo对象，失败返回None
        """
        try:
            # 必需字段
            version_str = remote_info.get("version")
            if not version_str:
                return None
            
            # 可选字段
            changelog = remote_info.get("changelog", "")
            url = remote_info.get("url", "")
            update_exe_url = remote_info.get("update_exe_url", "")
            
            # SHA256校验值
            sha256_info = remote_info.get("sha256", {})
            sha256_package = sha256_info.get("package", "") if isinstance(sha256_info, dict) else ""
            sha256_update_exe = sha256_info.get("update_exe", "") if isinstance(sha256_info, dict) else ""
            
            return VersionInfo(
                version_str=version_str,
                changelog=changelog,
                url=clean_url(url),
                update_exe_url=clean_url(update_exe_url),
                sha256_package=sha256_package,
                sha256_update_exe=sha256_update_exe
            )
            
        except Exception as e:
            print(f"解析版本信息失败: {e}")
            return None
    
    def _is_newer_version(self, remote_version: str, current_version: str) -> bool:
        """
        比较版本号
        
        Args:
            remote_version: 远程版本号
            current_version: 当前版本号
            
        Returns:
            远程版本是否更新
        """
        try:
            return version.parse(remote_version) > version.parse(current_version)
        except Exception as e:
            logger.error(f"版本比较失败: {e}")
            return False




class UpdateChecker(QObject):
    """更新检查器主类"""
    
    # 信号定义
    update_available = Signal(VersionInfo)  # 有更新可用
    no_update = Signal()                    # 无更新
    error_occurred = Signal(str)            # 发生错误
    check_started = Signal()                # 开始检查
    check_finished = Signal()               # 检查完成
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.worker = None
    
    def check_for_updates(self) -> None:
        """开始检查更新"""
        if self.worker and self.worker.isRunning():
            return  # 已经在检查中
        
        self.check_started.emit()
        
        # 创建工作线程
        self.worker = UpdateCheckWorker()
        
        # 连接信号
        self.worker.update_available.connect(self._on_update_available)
        self.worker.no_update.connect(self._on_no_update)
        self.worker.error_occurred.connect(self._on_error_occurred)
        self.worker.finished.connect(self._on_check_finished)
        
        # 启动线程
        self.worker.start()
    
    def _on_update_available(self, version_info: VersionInfo) -> None:
        """处理有更新可用"""
        self.update_available.emit(version_info)
    
    def _on_no_update(self) -> None:
        """处理无更新"""
        self.no_update.emit()
    
    def _on_error_occurred(self, error_msg: str) -> None:
        """处理错误"""
        self.error_occurred.emit(error_msg)
    
    def _on_check_finished(self) -> None:
        """处理检查完成"""
        self.check_finished.emit()
        if self.worker:
            self.worker.deleteLater()
            self.worker = None
