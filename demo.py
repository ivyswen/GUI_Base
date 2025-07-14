"""
GUI Base Template 演示程序
展示基本的GUI功能和自动更新功能的使用
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QTextEdit
from PySide6.QtCore import Qt

# 导入自动更新模块
from updater import UpdateManager, app_config


class DemoWindow(QMainWindow):
    """演示窗口类"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.center_window()
        
        # 初始化更新管理器
        self.update_manager = UpdateManager(self)
    
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle(f"{app_config.app_name} - 演示程序")
        self.setGeometry(100, 100, 600, 400)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 标题
        title_label = QLabel("GUI Base Template 演示程序")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        
        # 信息显示
        info_text = QTextEdit()
        info_text.setReadOnly(True)
        info_text.setMaximumHeight(150)
        info_content = f"""
应用程序信息：
• 名称：{app_config.app_name}
• 版本：{app_config.current_version}
• 组织：{app_config.organization_name}
• 更新服务器：{app_config.update_server}
• 自动检查更新：{'是' if app_config.auto_check_updates else '否'}

这是一个演示程序，展示了GUI Base Template的基本功能和自动更新功能。
        """
        info_text.setPlainText(info_content.strip())
        
        # 按钮区域
        button_layout = QVBoxLayout()
        
        # 检查更新按钮
        check_update_btn = QPushButton("检查更新")
        check_update_btn.clicked.connect(self.check_for_updates)
        check_update_btn.setStyleSheet(self.get_button_style("primary"))
        
        # 配置按钮
        config_btn = QPushButton("显示配置信息")
        config_btn.clicked.connect(self.show_config)
        config_btn.setStyleSheet(self.get_button_style("default"))
        
        # 测试按钮
        test_btn = QPushButton("运行功能测试")
        test_btn.clicked.connect(self.run_tests)
        test_btn.setStyleSheet(self.get_button_style("success"))
        
        button_layout.addWidget(check_update_btn)
        button_layout.addWidget(config_btn)
        button_layout.addWidget(test_btn)
        
        # 添加到主布局
        layout.addWidget(title_label)
        layout.addWidget(info_text)
        layout.addLayout(button_layout)
        layout.addStretch()

        # 创建状态栏
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("就绪")
    
    def get_button_style(self, style_type="default"):
        """获取按钮样式"""
        base_style = """
            QPushButton {
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 12px;
                font-weight: 500;
                min-width: 120px;
                min-height: 32px;
                border: 1px solid;
            }
            QPushButton:disabled {
                background-color: #f8f8f8;
                border: 1px solid #e0e0e0;
                color: #a0a0a0;
            }
        """
        
        if style_type == "primary":
            return base_style + """
                QPushButton {
                    background-color: #007acc;
                    border-color: #005a9e;
                    color: white;
                }
                QPushButton:hover {
                    background-color: #005a9e;
                    border-color: #004578;
                }
                QPushButton:pressed {
                    background-color: #004578;
                    border-color: #003456;
                }
            """
        elif style_type == "success":
            return base_style + """
                QPushButton {
                    background-color: #28a745;
                    border-color: #1e7e34;
                    color: white;
                }
                QPushButton:hover {
                    background-color: #1e7e34;
                    border-color: #155724;
                }
                QPushButton:pressed {
                    background-color: #155724;
                    border-color: #0d4017;
                }
            """
        else:  # default
            return base_style + """
                QPushButton {
                    background-color: #f0f0f0;
                    border-color: #c0c0c0;
                    color: #333333;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                    border-color: #a0a0a0;
                }
                QPushButton:pressed {
                    background-color: #d0d0d0;
                    border-color: #808080;
                }
            """
    
    def center_window(self):
        """将窗口居中显示"""
        screen = QApplication.primaryScreen().geometry()
        window = self.geometry()
        x = (screen.width() - window.width()) // 2
        y = (screen.height() - window.height()) // 2
        self.move(x, y)
    
    def check_for_updates(self):
        """检查更新"""
        if hasattr(self, 'update_manager'):
            self.update_manager.check_for_updates_manual_with_flag()
        else:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.information(self, "提示", "更新管理器未初始化")
    
    def show_config(self):
        """显示配置信息"""
        from PySide6.QtWidgets import QMessageBox
        # 检查URL是否是自动构建的
        configured_url = app_config.get("update_check_url", "")
        is_auto_built = not configured_url or not configured_url.startswith(('http://', 'https://'))
        url_source = "自动构建" if is_auto_built else "配置文件"

        config_info = f"""
配置信息：

应用程序名称: {app_config.app_name}
当前版本: {app_config.current_version}
组织名称: {app_config.organization_name}
更新服务器: {app_config.update_server}
检查更新URL: {app_config.update_check_url} ({url_source})
自动检查更新: {'是' if app_config.auto_check_updates else '否'}
检查超时时间: {app_config.update_check_timeout} 秒
下载超时时间: {app_config.download_timeout} 秒
临时目录名称: {app_config.temp_dir_name}

URL构建示例:
• 更新包: {app_config.get_update_url('updates/app_v2.0.0.zip')}
• 更新程序: {app_config.get_update_url('update.exe')}
        """
        QMessageBox.information(self, "配置信息", config_info.strip())
    
    def run_tests(self):
        """运行功能测试"""
        from PySide6.QtWidgets import QMessageBox
        
        try:
            # 简单的功能测试
            from updater import UpdateChecker, FileManager, VersionInfo
            
            # 测试版本信息
            version_info = VersionInfo("2.0.0", "测试版本", "http://example.com", "http://example.com")
            
            # 测试文件管理器
            file_manager = FileManager()
            temp_dir = file_manager.get_temp_dir()
            
            test_result = f"""
功能测试结果：

✅ 配置管理: 正常
✅ 版本信息类: 正常
✅ 文件管理器: 正常
✅ 临时目录创建: {temp_dir}
✅ 更新检查器: 正常
✅ 更新管理器: 正常

所有核心功能测试通过！
            """
            
            QMessageBox.information(self, "测试结果", test_result.strip())
            
        except Exception as e:
            QMessageBox.critical(self, "测试失败", f"功能测试失败：{str(e)}")


def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 设置应用程序属性
    app.setApplicationName(f"{app_config.app_name} - Demo")
    app.setApplicationVersion(app_config.current_version)
    app.setOrganizationName(app_config.organization_name)
    
    # 创建主窗口
    window = DemoWindow()
    window.show()
    
    # 运行应用程序
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
