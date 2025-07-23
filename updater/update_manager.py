"""
更新管理器
统一管理应用程序的自动更新功能
"""

import os
import sys
from pathlib import Path
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import QObject, QTimer
from .update_checker import UpdateChecker, VersionInfo
from .update_dialogs import UpdateDialog, DownloadDialog
from .file_manager import FileManager
from utils.logger import get_logger
from utils.config import app_config

logger = get_logger(__name__)


class UpdateManager(QObject):
    """更新管理器主类"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.update_checker = UpdateChecker(self)
        self.file_manager = FileManager(self)
        self.setup_connections()
        
        # 启动时检查更新的定时器
        self.startup_check_timer = QTimer(self)
        self.startup_check_timer.setSingleShot(True)
        self.startup_check_timer.timeout.connect(self.check_for_updates_silent)
    
    def setup_connections(self):
        """设置信号连接"""
        # 更新检查器信号
        self.update_checker.update_available.connect(self.on_update_available)
        self.update_checker.no_update.connect(self.on_no_update)
        self.update_checker.error_occurred.connect(self.on_check_error)
        self.update_checker.check_started.connect(self.on_check_started)
        self.update_checker.check_finished.connect(self.on_check_finished)
    
    def check_for_updates_on_startup(self):
        """启动时检查更新（延迟执行）"""
        if app_config.auto_check_updates:
            # 延迟3秒后检查，避免影响启动速度
            self.startup_check_timer.start(3000)
    
    def check_for_updates_manual(self):
        """手动检查更新"""
        if self.parent_window:
            self.parent_window.statusBar().showMessage("正在检查更新...", 0)
        self.update_checker.check_for_updates()
    
    def check_for_updates_silent(self):
        """静默检查更新（不显示状态）"""
        self.update_checker.check_for_updates()
    
    def on_check_started(self):
        """检查开始"""
        pass  # 可以在这里添加检查开始的处理逻辑
    
    def on_check_finished(self):
        """检查完成"""
        if self.parent_window:
            self.parent_window.statusBar().showMessage("就绪")
    
    def on_update_available(self, version_info: VersionInfo):
        """有更新可用"""
        logger.info(f"发现新版本可用: {version_info.version}")
        logger.info(f"更新包URL: {version_info.url}")
        # logger.info(f"更新日志: {version_info.changelog[:100]}...")

        if self.parent_window:
            self.parent_window.statusBar().showMessage("发现新版本", 3000)

        # 显示更新对话框
        self.show_update_dialog(version_info)
    
    def on_no_update(self):
        """无更新可用"""
        # 只有手动检查时才显示"已是最新版本"的消息
        if self.parent_window and hasattr(self, '_manual_check'):
            QMessageBox.information(
                self.parent_window,
                "检查更新",
                f"当前已是最新版本 {app_config.current_version}"
            )
            delattr(self, '_manual_check')
    
    def on_check_error(self, error_msg: str):
        """检查更新出错"""
        if self.parent_window:
            self.parent_window.statusBar().showMessage("检查更新失败", 3000)
            
            # 只有手动检查时才显示错误对话框
            if hasattr(self, '_manual_check'):
                QMessageBox.warning(
                    self.parent_window,
                    "检查更新失败",
                    f"无法检查更新：{error_msg}\n\n请检查网络连接或稍后重试。"
                )
                delattr(self, '_manual_check')
    
    def show_update_dialog(self, version_info: VersionInfo):
        """显示更新对话框"""
        logger.info("显示更新对话框")
        dialog = UpdateDialog(version_info, self.parent_window)
        result = dialog.exec()

        logger.info(f"用户选择结果: {result}")

        if result == 1:  # QDialog.Accepted
            # 用户选择立即更新
            logger.info("用户选择立即更新")
            self.start_download(version_info)
        elif result == 2:
            # 用户选择跳过此版本
            logger.info(f"用户选择跳过版本: {version_info.version}")
            self.skip_version(version_info.version)
        else:
            # result == 0 表示稍后提醒，不做处理
            logger.info("用户选择稍后提醒")
    
    def start_download(self, version_info: VersionInfo):
        """开始下载更新"""
        logger.info(f"开始下载更新包: {version_info.url}")

        download_dialog = DownloadDialog(version_info, self.parent_window)

        # 显示对话框并开始下载
        download_dialog.show()
        download_dialog.start_download()

        result = download_dialog.exec()

        logger.info(f"下载对话框结果: {result}")

        if result == 1:  # QDialog.Accepted
            # 下载成功，准备安装
            logger.info(f"下载成功，准备安装: {download_dialog.download_path}")
            self.install_update(version_info, download_dialog.download_path)
        else:
            # 下载取消或失败
            logger.warning("下载取消或失败")
            self.cleanup_download()
    
    def install_update(self, version_info: VersionInfo, package_path: str):
        """安装更新"""
        logger.info("开始安装更新")
        logger.info(f"更新包路径: {package_path}")
        logger.info(f"更新程序URL: {version_info.update_exe_url}")

        try:
            # 获取更新程序路径
            update_exe_path = self.get_update_exe_path()
            logger.info(f"更新程序目标路径: {update_exe_path}")

            # 检查更新程序是否存在
            exe_exists = Path(update_exe_path).exists()
            logger.info(f"更新程序是否存在: {exe_exists}")

            # 如果有更新程序URL，总是尝试下载最新版本
            if version_info.update_exe_url:
                logger.info("开始下载更新程序")
                if not self.download_update_exe(version_info):
                    logger.error("更新程序下载失败")
                    return
            else:
                logger.warning("没有提供更新程序URL")
                if not exe_exists:
                    QMessageBox.critical(
                        self.parent_window,
                        "更新程序缺失",
                        "没有找到更新程序，且服务器未提供更新程序下载链接。"
                    )
                    return

            # 记录即将更新的版本信息
            self.log_update_attempt(version_info)

            # 启动更新程序
            logger.info("准备启动更新程序")
            self.launch_update_process(update_exe_path, package_path)

        except Exception as e:
            logger.exception(f"安装更新时发生错误: {str(e)}")
            QMessageBox.critical(
                self.parent_window,
                "安装失败",
                f"安装更新时发生错误：{str(e)}"
            )
    
    def get_update_exe_path(self) -> str:
        """获取更新程序路径"""
        # 检测是否为编译后的应用程序
        is_frozen = getattr(sys, 'frozen', False)  # PyInstaller, cx_Freeze
        is_nuitka_compiled = hasattr(sys.modules[__name__], '__compiled__')  # Nuitka
        is_compiled = is_frozen or is_nuitka_compiled

        if is_compiled:
            # 编译后的应用程序
            app_exe_path = Path(os.path.abspath(sys.executable))
            app_dir = app_exe_path.parent
        else:
            # 开发环境
            app_dir = Path(__file__).parent

        update_exe_path = str(app_dir / "update.exe")
        logger.debug(f"更新程序路径: {update_exe_path}")

        return update_exe_path
    
    def download_update_exe(self, version_info: VersionInfo) -> bool:
        """下载更新程序"""
        logger.info(f"开始下载更新程序: {version_info.update_exe_url}")

        try:
            update_exe_path = self.get_update_exe_path()
            logger.info(f"更新程序保存路径: {update_exe_path}")

            # 创建目标目录
            target_dir = Path(update_exe_path).parent
            target_dir.mkdir(parents=True, exist_ok=True)

            # 使用urllib进行同步下载
            import urllib.request
            logger.info("开始下载更新程序文件...")

            # 创建请求，添加User-Agent
            request = urllib.request.Request(
                version_info.update_exe_url,
                headers={
                    'User-Agent': f'{app_config.app_name}/{app_config.current_version}'
                }
            )

            # 下载文件
            with urllib.request.urlopen(request, timeout=app_config.download_timeout) as response:
                if response.status == 200:
                    with open(update_exe_path, 'wb') as f:
                        f.write(response.read())
                    logger.success(f"更新程序下载完成: {update_exe_path}")
                else:
                    raise Exception(f"服务器返回错误状态码: {response.status}")

            # 检查文件是否存在
            if not Path(update_exe_path).exists():
                raise Exception("下载的文件不存在")

            file_size = Path(update_exe_path).stat().st_size
            logger.info(f"下载的文件大小: {file_size} 字节")

            # 校验更新程序
            if version_info.sha256_update_exe:
                logger.info("开始校验更新程序...")
                actual_hash = self.file_manager.calculate_file_sha256(update_exe_path)
                expected_hash = version_info.sha256_update_exe.lower()

                if actual_hash.lower() != expected_hash:
                    logger.error("更新程序SHA256校验失败")
                    os.remove(update_exe_path)
                    raise Exception("更新程序校验失败")
                else:
                    logger.success("更新程序校验通过")
            else:
                logger.warning("没有提供更新程序SHA256，跳过校验")

            return True

        except Exception as e:
            logger.exception(f"下载更新程序失败: {str(e)}")
            # 只有在有父窗口时才显示消息框
            if self.parent_window:
                try:
                    QMessageBox.critical(
                        self.parent_window,
                        "下载更新程序失败",
                        f"无法下载更新程序：{str(e)}"
                    )
                except:
                    # 如果无法显示消息框，只记录日志
                    logger.error("无法显示错误消息框")
            return False
    
    def launch_update_process(self, update_exe_path: str, package_path: str):
        """启动更新进程"""
        try:
            logger.info("开始准备启动更新进程")

            # 获取应用程序信息
            app_dir, app_exe_name = self._get_app_info()

            # 构建更新命令，使用您的参数格式
            cmd = f'"{update_exe_path}" --target-dir "{app_dir}" --update-package "{package_path}" --app-exe "{app_exe_name}"'
            logger.info(f"更新命令: {cmd}")

            # 启动更新程序
            logger.info("启动更新程序...")
            os.system(f'start "" {cmd}')
            logger.success("更新程序已启动")

            # 退出当前应用程序
            logger.info("准备退出当前应用程序")
            if self.parent_window:
                self.parent_window.close()

        except Exception as e:
            logger.exception(f"启动更新进程失败: {str(e)}")
            QMessageBox.critical(
                self.parent_window,
                "启动更新失败",
                f"无法启动更新程序：{str(e)}"
            )

    def _get_app_info(self) -> tuple[str, str]:
        """获取应用程序目录和可执行文件名

        Returns:
            tuple[str, str]: (应用程序目录, 可执行文件名)
        """

        # 检测是否为编译后的应用程序
        is_frozen = getattr(sys, 'frozen', False)  # PyInstaller, cx_Freeze
        is_nuitka_compiled = hasattr(sys.modules[__name__], '__compiled__')  # Nuitka
        is_compiled = is_frozen or is_nuitka_compiled

        logger.debug(f"检测编译环境: frozen={is_frozen}, nuitka={is_nuitka_compiled}, compiled={is_compiled}")

        if is_compiled:
            # 编译后的应用程序（PyInstaller, cx_Freeze, Nuitka等）
            logger.debug("检测到编译/打包环境")

            # 优先使用sys.executable，因为它在所有打包工具中都比较可靠
            app_exe_path = Path(sys.executable)
            app_dir = app_exe_path.parent
            app_exe_name = app_exe_path.name  # 直接使用文件名，包含.exe扩展名

            # 验证sys.executable指向的文件是否存在
            if not app_exe_path.exists():
                logger.warning(f"sys.executable指向的文件不存在，尝试备用方案")
                # 尝试使用sys.argv[0]作为备用方案
                app_exe_path_backup = Path(os.path.abspath(sys.argv[0]))

                if app_exe_path_backup.exists():
                    app_dir = app_exe_path_backup.parent
                    app_exe_name = app_exe_path_backup.name
                    logger.info("使用sys.argv[0]作为备用方案成功")
                else:
                    logger.warning("备用方案也失败，使用sys.executable的原始值")

        else:
            # 开发环境，使用Python脚本
            logger.debug("检测到开发环境")

            # 获取项目根目录
            app_dir = Path(__file__).parent.parent  # 回到项目根目录
            app_exe_name = "main.py"  # 开发环境下使用脚本名

            # 验证main.py是否存在
            main_py_path = app_dir / app_exe_name
            if not main_py_path.exists():
                logger.warning(f"主脚本文件不存在，尝试查找替代入口文件")
                # 尝试查找其他可能的入口文件
                possible_entries = ["app.py", "run.py", "start.py"]
                for entry in possible_entries:
                    if (app_dir / entry).exists():
                        app_exe_name = entry
                        logger.info(f"找到替代入口文件: {entry}")
                        break
                else:
                    logger.error("未找到有效的入口文件")

        app_dir_str = str(app_dir.resolve())
        logger.info(f"应用目录: {app_dir_str}, 可执行文件: {app_exe_name}")

        return app_dir_str, app_exe_name

    def log_update_attempt(self, version_info: VersionInfo):
        """记录更新尝试信息"""
        try:
            logger.info(f"准备更新到版本: {version_info.version}")
            logger.info(f"当前版本: {app_config.current_version}")
            logger.info(f"更新包URL: {version_info.url}")
            logger.info(f"更新程序URL: {version_info.update_exe_url}")

            # 记录更新尝试到专用日志
            update_logger = get_logger("update_attempt")
            update_logger.info(f"更新尝试开始 - 从 {app_config.current_version} 到 {version_info.version}")

        except Exception as e:
            logger.error(f"记录更新尝试信息时发生错误: {str(e)}")

    def sync_version_after_update(self, new_version: str):
        """更新完成后同步版本信息

        注意：此方法主要用于记录和日志，实际的版本同步在应用程序重启时进行

        Args:
            new_version: 新版本号
        """
        try:
            logger.info(f"更新完成，新版本: {new_version}")

            # 记录更新完成到专用日志
            update_logger = get_logger("update_complete")
            update_logger.success(f"更新完成 - 版本更新到 {new_version}")

            # 注意：实际的config.json版本同步会在应用程序重启时通过
            # sync_version_on_startup() 方法自动进行

        except Exception as e:
            logger.error(f"同步版本信息时发生错误: {str(e)}")

    def skip_version(self, version: str):
        """跳过指定版本"""
        logger.info(f"用户选择跳过版本: {version}")

        # 使用配置管理器跳过版本
        app_config.skip_version(version)

        # 显示状态消息
        if self.parent_window:
            skip_days = app_config.get("skip_duration_days", 30)
            self.parent_window.statusBar().showMessage(f"已跳过版本 {version}（{skip_days}天内不再提醒）", 5000)
    
    def cleanup_download(self):
        """清理下载文件"""
        self.file_manager.cleanup_temp_files()
    
    def set_manual_check_flag(self):
        """设置手动检查标志"""
        self._manual_check = True
    
    def check_for_updates_manual_with_flag(self):
        """手动检查更新（带标志）"""
        self.set_manual_check_flag()
        self.check_for_updates_manual()
    
    def get_current_version(self) -> str:
        """获取当前版本"""
        return app_config.current_version
    
    def get_app_name(self) -> str:
        """获取应用程序名称"""
        return app_config.app_name
    
    def is_auto_check_enabled(self) -> bool:
        """是否启用自动检查"""
        return app_config.auto_check_updates
    
    def set_auto_check_enabled(self, enabled: bool):
        """设置自动检查开关"""
        app_config.set_auto_check_updates(enabled)

    def get_skipped_versions_info(self) -> dict:
        """获取跳过版本的详细信息"""
        return app_config.get_skipped_versions_info()

    def clear_skipped_versions(self):
        """清除所有跳过的版本"""
        app_config.clear_skipped_versions()
        logger.info("已清除所有跳过的版本")

        if self.parent_window:
            self.parent_window.statusBar().showMessage("已清除所有跳过的版本", 3000)

    def remove_skipped_version(self, version: str) -> bool:
        """移除指定的跳过版本"""
        success = app_config.remove_skipped_version(version)

        if success:
            logger.info(f"已移除跳过版本: {version}")
            if self.parent_window:
                self.parent_window.statusBar().showMessage(f"已移除跳过版本 {version}", 3000)

        return success
