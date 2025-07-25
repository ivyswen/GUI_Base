"""
应用程序配置管理模块
管理应用程序的版本信息、更新服务器地址等配置项
"""

import json
import sys
import os
from pathlib import Path
from typing import Dict, Any, Optional


def get_exe_version() -> Optional[str]:
    """
    从exe文件中读取版本信息

    Returns:
        版本号字符串，如果无法读取则返回None
    """
    try:
        # 检测是否为编译后的应用程序
        is_frozen = getattr(sys, 'frozen', False)  # PyInstaller, cx_Freeze
        is_nuitka_compiled = hasattr(sys.modules.get(__name__.split('.')[0], sys.modules[__name__]), '__compiled__')  # Nuitka
        is_compiled = is_frozen or is_nuitka_compiled

        # 只在Windows下且为编译后的exe时尝试读取
        if sys.platform == 'win32' and is_compiled:
            import win32api

            # 获取当前exe文件路径
            exe_path = sys.executable

            # 读取文件版本信息
            info = win32api.GetFileVersionInfo(exe_path, "\\")
            ms = info['FileVersionMS']
            ls = info['FileVersionLS']

            # 构建版本号
            version = f"{win32api.HIWORD(ms)}.{win32api.LOWORD(ms)}.{win32api.HIWORD(ls)}.{win32api.LOWORD(ls)}"

            # 移除末尾的.0
            while version.endswith('.0') and version.count('.') > 2:
                version = version[:-2]

            return version

    except ImportError:
        # win32api 不可用，尝试使用其他方法
        pass
    except Exception as e:
        # 使用logger记录错误，但不导入logger避免循环依赖
        # 这里的错误通常不是致命的，所以静默处理
        pass

    return None


def get_exe_version_alternative() -> Optional[str]:
    """
    使用替代方法读取exe版本信息（不依赖win32api）

    Returns:
        版本号字符串，如果无法读取则返回None
    """
    try:
        # 检测是否为编译后的应用程序
        is_frozen = getattr(sys, 'frozen', False)  # PyInstaller, cx_Freeze
        is_nuitka_compiled = hasattr(sys.modules.get(__name__.split('.')[0], sys.modules[__name__]), '__compiled__')  # Nuitka
        is_compiled = is_frozen or is_nuitka_compiled

        if sys.platform == 'win32' and is_compiled:
            import subprocess

            # 使用PowerShell读取文件版本
            exe_path = sys.executable
            cmd = f'(Get-Item "{exe_path}").VersionInfo.FileVersion'

            result = subprocess.run(
                ['powershell', '-Command', cmd],
                capture_output=True,
                text=True,
                timeout=5,
                creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
            )

            if result.returncode == 0 and result.stdout.strip():
                version = result.stdout.strip()
                # 移除末尾的.0
                while version.endswith('.0') and version.count('.') > 2:
                    version = version[:-2]
                return version

    except Exception as e:
        # 使用logger记录错误，但不导入logger避免循环依赖
        # 这里的错误通常不是致命的，所以静默处理
        pass

    return None


class AppConfig:
    """应用程序配置管理类"""
    
    # 默认配置
    DEFAULT_CONFIG = {
        "app_name": "GUI Base Template",
        "current_version": "1.0.0",
        "organization_name": "Your Organization",
        "update_server": "https://your-server.com",
        "update_check_url": "",  # 留空，将自动从 update_server 构建
        "auto_check_updates": True,
        "update_check_timeout": 10,  # 秒
        "download_timeout": 300,     # 秒
        "temp_dir_name": "app_update",
        "skipped_versions": {},      # 跳过的版本：{"version": expire_timestamp}
        "skip_duration_days": 30     # 跳过版本的有效期（天）
    }
    
    def __init__(self, config_file: str = "config.json"):
        """
        初始化配置管理器
        
        Args:
            config_file: 配置文件路径
        """
        self.config_file = Path(config_file)
        self._config = self.DEFAULT_CONFIG.copy()
        self.load_config()
    
    def load_config(self) -> None:
        """从配置文件加载配置"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    file_config = json.load(f)
                    # 更新配置，保留默认值
                    self._config.update(file_config)
        except Exception as e:
            print(f"加载配置文件失败: {e}")
            # 使用默认配置
    
    def save_config(self) -> None:
        """保存配置到文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"保存配置文件失败: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置项
        
        Args:
            key: 配置项键名
            default: 默认值
            
        Returns:
            配置项值
        """
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """
        设置配置项
        
        Args:
            key: 配置项键名
            value: 配置项值
        """
        self._config[key] = value
    
    def update(self, config_dict: Dict[str, Any]) -> None:
        """
        批量更新配置
        
        Args:
            config_dict: 配置字典
        """
        self._config.update(config_dict)
    
    @property
    def app_name(self) -> str:
        """应用程序名称"""
        return self.get("app_name")
    
    @property
    def current_version(self) -> str:
        """当前版本号"""
        # 首先尝试从配置文件读取
        config_version = self.get("current_version")

        # 如果配置文件中的版本为空或为默认值，尝试从exe读取
        if not config_version or config_version == "1.0.0":
            exe_version = self.get_version_from_exe()
            if exe_version:
                return exe_version

        return config_version or "1.0.0"
    
    @property
    def organization_name(self) -> str:
        """组织名称"""
        return self.get("organization_name")
    
    @property
    def update_server(self) -> str:
        """更新服务器地址"""
        return self.get("update_server")
    
    @property
    def update_check_url(self) -> str:
        """更新检查URL"""
        # 如果配置中有完整的URL，直接使用
        configured_url = self.get("update_check_url")
        if configured_url and configured_url.startswith(('http://', 'https://')):
            return configured_url

        # 否则基于 update_server 构建URL
        base_server = self.update_server.rstrip('/')
        return f"{base_server}/update.json"
    
    @property
    def auto_check_updates(self) -> bool:
        """是否自动检查更新"""
        return self.get("auto_check_updates", True)
    
    @property
    def update_check_timeout(self) -> int:
        """更新检查超时时间（秒）"""
        return self.get("update_check_timeout", 10)
    
    @property
    def download_timeout(self) -> int:
        """下载超时时间（秒）"""
        return self.get("download_timeout", 300)
    
    @property
    def temp_dir_name(self) -> str:
        """临时目录名称"""
        return self.get("temp_dir_name", "app_update")
    
    def set_current_version(self, version: str) -> None:
        """
        设置当前版本号
        
        Args:
            version: 版本号
        """
        self.set("current_version", version)
        self.save_config()
    
    def set_auto_check_updates(self, enabled: bool) -> None:
        """
        设置是否自动检查更新

        Args:
            enabled: 是否启用自动检查
        """
        self.set("auto_check_updates", enabled)
        self.save_config()

    def get_update_url(self, path: str) -> str:
        """
        基于更新服务器地址构建完整URL

        Args:
            path: 相对路径，如 "updates/app_v2.0.0.zip"

        Returns:
            完整的URL
        """
        base_server = self.update_server.rstrip('/')
        path = path.lstrip('/')
        return f"{base_server}/{path}"

    def set_update_server(self, server_url: str):
        """
        设置更新服务器地址

        Args:
            server_url: 服务器地址
        """
        self.set("update_server", server_url)
        # 清除可能存在的完整URL配置，让系统自动构建
        if self.get("update_check_url", "").startswith(('http://', 'https://')):
            self.set("update_check_url", "")
        self.save_config()

    def get_version_from_exe(self) -> Optional[str]:
        """
        从exe文件中读取版本信息

        Returns:
            版本号字符串，如果无法读取则返回None
        """
        # 首先尝试使用win32api
        version = get_exe_version()
        if version:
            return version

        # 如果win32api不可用，尝试使用PowerShell
        version = get_exe_version_alternative()
        if version:
            return version

        return None

    def update_version_from_exe(self) -> bool:
        """
        从exe文件更新配置中的版本号

        Returns:
            是否成功更新
        """
        exe_version = self.get_version_from_exe()
        if exe_version:
            self.set("current_version", exe_version)
            self.save_config()
            return True
        return False

    def skip_version(self, version: str, duration_days: int = None):
        """
        跳过指定版本

        Args:
            version: 要跳过的版本号
            duration_days: 跳过的有效期（天），如果不指定则使用配置中的默认值
        """
        import time

        duration = duration_days or self.get("skip_duration_days", 30)
        expire_time = time.time() + (duration * 24 * 60 * 60)

        skipped = self.get("skipped_versions", {})
        skipped[version] = expire_time
        self.set("skipped_versions", skipped)
        self.save_config()

        # 记录日志（延迟导入避免循环依赖）
        try:
            from utils.logger import get_logger
            logger = get_logger(__name__)
            logger.info(f"跳过版本 {version}，有效期 {duration} 天")
        except ImportError:
            # 如果导入失败，使用print作为备选
            print(f"跳过版本 {version}，有效期 {duration} 天")

    def is_version_skipped(self, version: str) -> bool:
        """
        检查版本是否被跳过（考虑过期时间）

        Args:
            version: 要检查的版本号

        Returns:
            是否被跳过
        """
        import time

        skipped = self.get("skipped_versions", {})

        if version not in skipped:
            return False

        # 检查是否过期
        if time.time() > skipped[version]:
            # 已过期，移除并返回False
            del skipped[version]
            self.set("skipped_versions", skipped)
            self.save_config()

            # 记录日志
            from .logger import get_logger
            logger = get_logger(__name__)
            logger.info(f"跳过版本 {version} 已过期，自动移除")
            return False

        return True

    def clear_skipped_versions(self):
        """清除所有跳过的版本"""
        skipped_count = len(self.get("skipped_versions", {}))
        self.set("skipped_versions", {})
        self.save_config()

        # 记录日志
        from .logger import get_logger
        logger = get_logger(__name__)
        logger.info(f"清除了 {skipped_count} 个跳过的版本")

    def get_skipped_versions_info(self) -> dict:
        """
        获取跳过版本的详细信息

        Returns:
            包含版本和过期时间信息的字典
        """
        import time
        from datetime import datetime

        skipped = self.get("skipped_versions", {})
        result = {}

        for version, expire_timestamp in skipped.items():
            expire_date = datetime.fromtimestamp(expire_timestamp)
            is_expired = time.time() > expire_timestamp

            result[version] = {
                "expire_timestamp": expire_timestamp,
                "expire_date": expire_date.strftime("%Y-%m-%d %H:%M:%S"),
                "is_expired": is_expired,
                "days_remaining": max(0, int((expire_timestamp - time.time()) / (24 * 60 * 60)))
            }

        return result

    def remove_skipped_version(self, version: str) -> bool:
        """
        移除指定的跳过版本

        Args:
            version: 要移除的版本号

        Returns:
            是否成功移除
        """
        skipped = self.get("skipped_versions", {})

        if version in skipped:
            del skipped[version]
            self.set("skipped_versions", skipped)
            self.save_config()

            # 记录日志
            from .logger import get_logger
            logger = get_logger(__name__)
            logger.info(f"手动移除跳过版本: {version}")
            return True

        return False


# 全局配置实例
app_config = AppConfig()
