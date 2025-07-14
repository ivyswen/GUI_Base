"""
文件管理模块
负责文件下载、SHA256校验、临时文件管理等功能
"""

import os
import hashlib
import tempfile
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional, Callable
from PySide6.QtCore import QObject, QThread, Signal
from .config import app_config
from .logger import get_logger

logger = get_logger(__name__)


class DownloadWorker(QThread):
    """文件下载工作线程"""
    
    # 信号定义
    progress_updated = Signal(int, int)  # 已下载字节数, 总字节数
    download_finished = Signal(str)      # 下载完成, 文件路径
    download_failed = Signal(str)        # 下载失败, 错误信息
    
    def __init__(self, url: str, file_path: str, parent=None):
        super().__init__(parent)
        self.url = url
        self.file_path = file_path
        self.timeout = app_config.download_timeout
        self._cancelled = False
    
    def run(self):
        """执行下载"""
        try:
            self._download_file()
        except Exception as e:
            self.download_failed.emit(f"下载失败: {str(e)}")
    
    def cancel(self):
        """取消下载"""
        self._cancelled = True
    
    def _download_file(self):
        """下载文件"""
        logger.info(f"开始下载文件: {self.url}")
        logger.info(f"保存路径: {self.file_path}")

        try:
            # 创建请求
            request = urllib.request.Request(
                self.url,
                headers={
                    'User-Agent': f'{app_config.app_name}/{app_config.current_version}'
                }
            )

            logger.debug(f"下载超时时间: {self.timeout}秒")

            # 打开连接
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                logger.debug(f"下载响应状态码: {response.status}")

                if response.status != 200:
                    logger.error(f"服务器返回错误状态码: {response.status}")
                    self.download_failed.emit(f"服务器返回错误状态码: {response.status}")
                    return

                # 获取文件大小
                content_length = response.headers.get('Content-Length')
                total_size = int(content_length) if content_length else 0
                logger.info(f"文件大小: {total_size} 字节 ({total_size / 1024 / 1024:.2f} MB)")

                # 创建目标目录
                target_dir = Path(self.file_path).parent
                target_dir.mkdir(parents=True, exist_ok=True)
                logger.debug(f"创建目标目录: {target_dir}")

                # 下载文件
                downloaded_size = 0
                chunk_size = 8192

                logger.info("开始下载文件内容...")
                with open(self.file_path, 'wb') as f:
                    while not self._cancelled:
                        chunk = response.read(chunk_size)
                        if not chunk:
                            break

                        f.write(chunk)
                        downloaded_size += len(chunk)

                        # 发送进度信号
                        self.progress_updated.emit(downloaded_size, total_size)

                        # 每下载10MB记录一次进度
                        if downloaded_size % (10 * 1024 * 1024) == 0:
                            logger.debug(f"下载进度: {downloaded_size / 1024 / 1024:.2f} MB / {total_size / 1024 / 1024:.2f} MB")

                if self._cancelled:
                    logger.warning("下载被用户取消")
                    # 删除未完成的文件
                    try:
                        os.remove(self.file_path)
                        logger.debug("已删除未完成的下载文件")
                    except:
                        pass
                    self.download_failed.emit("下载已取消")
                else:
                    logger.success(f"文件下载完成: {self.file_path}")
                    logger.info(f"最终文件大小: {downloaded_size} 字节")
                    self.download_finished.emit(self.file_path)

        except urllib.error.URLError as e:
            logger.error(f"网络错误: {str(e)}")
            self.download_failed.emit(f"网络错误: {str(e)}")
        except Exception as e:
            logger.exception(f"下载错误: {str(e)}")
            self.download_failed.emit(f"下载错误: {str(e)}")


class FileManager(QObject):
    """文件管理器"""
    
    # 信号定义
    download_progress = Signal(int, int)  # 下载进度
    download_finished = Signal(str)       # 下载完成
    download_failed = Signal(str)         # 下载失败
    verification_finished = Signal(bool)  # 校验完成
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.download_worker = None
        self.temp_dir = None
    
    def get_temp_dir(self) -> Path:
        """
        获取临时目录
        
        Returns:
            临时目录路径
        """
        if not self.temp_dir:
            temp_base = Path(tempfile.gettempdir())
            self.temp_dir = temp_base / app_config.temp_dir_name
            self.temp_dir.mkdir(exist_ok=True)
        return self.temp_dir
    
    def download_file(self, url: str, filename: str) -> str:
        """
        下载文件
        
        Args:
            url: 下载链接
            filename: 文件名
            
        Returns:
            目标文件路径
        """
        if self.download_worker and self.download_worker.isRunning():
            return ""  # 已经在下载中
        
        # 确定下载路径
        temp_dir = self.get_temp_dir()
        file_path = str(temp_dir / filename)
        
        # 创建下载线程
        self.download_worker = DownloadWorker(url, file_path)
        
        # 连接信号
        self.download_worker.progress_updated.connect(self.download_progress.emit)
        self.download_worker.download_finished.connect(self._on_download_finished)
        self.download_worker.download_failed.connect(self._on_download_failed)
        
        # 启动下载
        self.download_worker.start()
        
        return file_path
    
    def cancel_download(self):
        """取消下载"""
        if self.download_worker and self.download_worker.isRunning():
            self.download_worker.cancel()
    
    def verify_file_sha256(self, file_path: str, expected_hash: str) -> bool:
        """
        验证文件SHA256
        
        Args:
            file_path: 文件路径
            expected_hash: 期望的SHA256值
            
        Returns:
            校验是否通过
        """
        try:
            if not expected_hash:
                # 如果没有提供期望的hash值，跳过校验
                return True
            
            # 计算文件SHA256
            actual_hash = self.calculate_file_sha256(file_path)
            
            # 比较hash值（忽略大小写）
            result = actual_hash.lower() == expected_hash.lower()
            self.verification_finished.emit(result)
            return result
            
        except Exception as e:
            print(f"文件校验失败: {e}")
            self.verification_finished.emit(False)
            return False
    
    def calculate_file_sha256(self, file_path: str) -> str:
        """
        计算文件SHA256
        
        Args:
            file_path: 文件路径
            
        Returns:
            SHA256值
        """
        sha256_hash = hashlib.sha256()
        
        with open(file_path, "rb") as f:
            # 分块读取文件，避免大文件占用过多内存
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        
        return sha256_hash.hexdigest()
    
    def cleanup_temp_files(self):
        """清理临时文件"""
        try:
            if self.temp_dir and self.temp_dir.exists():
                # 删除临时目录中的所有文件
                for file_path in self.temp_dir.iterdir():
                    if file_path.is_file():
                        file_path.unlink()
                
                # 尝试删除临时目录（如果为空）
                try:
                    self.temp_dir.rmdir()
                except OSError:
                    pass  # 目录不为空，保留
                    
        except Exception as e:
            print(f"清理临时文件失败: {e}")
    
    def get_file_size(self, file_path: str) -> int:
        """
        获取文件大小
        
        Args:
            file_path: 文件路径
            
        Returns:
            文件大小（字节）
        """
        try:
            return os.path.getsize(file_path)
        except:
            return 0
    
    def file_exists(self, file_path: str) -> bool:
        """
        检查文件是否存在
        
        Args:
            file_path: 文件路径
            
        Returns:
            文件是否存在
        """
        return Path(file_path).exists()
    
    def _on_download_finished(self, file_path: str):
        """处理下载完成"""
        self.download_finished.emit(file_path)
        if self.download_worker:
            self.download_worker.deleteLater()
            self.download_worker = None
    
    def _on_download_failed(self, error_msg: str):
        """处理下载失败"""
        self.download_failed.emit(error_msg)
        if self.download_worker:
            self.download_worker.deleteLater()
            self.download_worker = None
