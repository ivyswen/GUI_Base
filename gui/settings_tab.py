"""
设置页面模块
包含各种设置选项和配置功能
"""

from typing import Literal
from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                               QMessageBox, QGroupBox, QRadioButton, QButtonGroup,
                               QCheckBox, QComboBox, QFileDialog, QScrollArea,
                               QWidget)
from PySide6.QtCore import Qt
from .base_tab import BaseTab
from utils.theme import get_theme_manager, ThemeMode
from utils.config import app_config
from utils.styles import get_group_box_style, get_button_style, get_combobox_style


class SettingsTab(BaseTab):
    """设置页面Tab"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """初始化用户界面"""
        # 创建滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        
        # 创建内容部件
        content_widget = QWidget()
        layout = QVBoxLayout()
        content_widget.setLayout(layout)
        
        # 标题
        title_label = QLabel("设置")
        title_label.setStyleSheet("margin: 10px;")
        self.apply_subtitle_font(title_label)
        layout.addWidget(title_label)
        
        # 主题设置
        layout.addWidget(self.create_theme_group())
        
        # 外观设置
        layout.addWidget(self.create_appearance_group())
        
        # 行为设置
        layout.addWidget(self.create_behavior_group())
        
        # 更新设置
        layout.addWidget(self.create_update_group())
        
        # 高级设置
        layout.addWidget(self.create_advanced_group())
        
        # 操作按钮
        layout.addWidget(self.create_action_buttons())
        
        layout.addStretch()
        
        # 设置滚动区域
        scroll.setWidget(content_widget)
        
        # 主布局
        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)
    
    def create_theme_group(self):
        """创建主题设置分组"""
        group = QGroupBox("主题设置")
        group.setStyleSheet(get_group_box_style())
        layout = QVBoxLayout()
        
        # 单选按钮
        self.light_radio = QRadioButton("浅色主题")
        self.dark_radio = QRadioButton("深色主题")
        self.auto_radio = QRadioButton("跟随系统")
        
        # 按钮组
        self.theme_button_group = QButtonGroup()
        self.theme_button_group.addButton(self.light_radio, 0)
        self.theme_button_group.addButton(self.dark_radio, 1)
        self.theme_button_group.addButton(self.auto_radio, 2)
        
        # 设置默认选中
        current_theme = app_config.theme_mode
        if current_theme == "light":
            self.light_radio.setChecked(True)
        elif current_theme == "dark":
            self.dark_radio.setChecked(True)
        else:
            self.auto_radio.setChecked(True)
        
        # 连接信号
        self.light_radio.toggled.connect(lambda checked: self.on_theme_changed("light", checked))
        self.dark_radio.toggled.connect(lambda checked: self.on_theme_changed("dark", checked))
        self.auto_radio.toggled.connect(lambda checked: self.on_theme_changed("auto", checked))
        
        layout.addWidget(self.light_radio)
        layout.addWidget(self.dark_radio)
        layout.addWidget(self.auto_radio)
        
        group.setLayout(layout)
        return group
    
    def create_appearance_group(self):
        """创建外观设置分组"""
        group = QGroupBox("外观设置")
        group.setStyleSheet(get_group_box_style())
        layout = QVBoxLayout()

        # 记住窗口大小
        self.remember_size_check = QCheckBox("记住窗口大小")
        self.remember_size_check.setChecked(app_config.remember_window_size)
        self.remember_size_check.toggled.connect(self.on_remember_size_changed)
        layout.addWidget(self.remember_size_check)

        group.setLayout(layout)
        return group
    
    def create_behavior_group(self):
        """创建行为设置分组"""
        group = QGroupBox("行为设置")
        group.setStyleSheet(get_group_box_style())
        layout = QVBoxLayout()
        
        # 最小化到托盘
        self.minimize_to_tray_check = QCheckBox("最小化到托盘")
        self.minimize_to_tray_check.setChecked(app_config.minimize_to_tray)
        self.minimize_to_tray_check.toggled.connect(self.on_minimize_to_tray_changed)
        layout.addWidget(self.minimize_to_tray_check)

        # 关闭时最小化到托盘
        self.close_to_tray_check = QCheckBox("关闭时最小化到托盘")
        self.close_to_tray_check.setChecked(app_config.close_to_tray)
        self.close_to_tray_check.toggled.connect(self.on_close_to_tray_changed)
        layout.addWidget(self.close_to_tray_check)

        # 退出时确认
        self.confirm_exit_check = QCheckBox("退出时确认")
        self.confirm_exit_check.setChecked(app_config.confirm_on_exit)
        self.confirm_exit_check.toggled.connect(self.on_confirm_exit_changed)
        layout.addWidget(self.confirm_exit_check)

        # 启动时最小化
        self.start_minimized_check = QCheckBox("启动时最小化")
        self.start_minimized_check.setChecked(app_config.start_minimized)
        self.start_minimized_check.toggled.connect(self.on_start_minimized_changed)
        layout.addWidget(self.start_minimized_check)

        group.setLayout(layout)
        return group
    
    def create_update_group(self):
        """创建更新设置分组"""
        group = QGroupBox("更新设置")
        group.setStyleSheet(get_group_box_style())
        layout = QVBoxLayout()
        
        # 自动检查更新
        self.auto_update_check = QCheckBox("自动检查更新")
        self.auto_update_check.setChecked(app_config.auto_check_updates)
        self.auto_update_check.toggled.connect(self.on_auto_update_changed)
        layout.addWidget(self.auto_update_check)
        
        group.setLayout(layout)
        return group
    
    def create_advanced_group(self):
        """创建高级设置分组"""
        group = QGroupBox("高级设置")
        group.setStyleSheet(get_group_box_style())
        layout = QVBoxLayout()
        
        # 日志级别
        log_layout = QHBoxLayout()
        log_layout.addWidget(QLabel("日志级别:"))
        self.log_level_combo = QComboBox()
        self.log_level_combo.addItems(["DEBUG", "INFO", "WARNING", "ERROR"])
        self.log_level_combo.setCurrentText(app_config.log_level)
        self.log_level_combo.setStyleSheet(get_combobox_style())
        self.log_level_combo.currentTextChanged.connect(self.on_log_level_changed)
        log_layout.addWidget(self.log_level_combo)
        log_layout.addStretch()
        layout.addLayout(log_layout)
        
        # 调试模式
        self.debug_mode_check = QCheckBox("调试模式")
        self.debug_mode_check.setChecked(app_config.debug_mode)
        self.debug_mode_check.toggled.connect(self.on_debug_mode_changed)
        layout.addWidget(self.debug_mode_check)
        
        group.setLayout(layout)
        return group
    
    def create_action_buttons(self):
        """创建操作按钮"""
        group = QGroupBox("配置管理")
        group.setStyleSheet(get_group_box_style())
        layout = QHBoxLayout()
        
        # 重置按钮
        reset_btn = QPushButton("重置到默认值")
        reset_btn.setStyleSheet(get_button_style("warning"))
        reset_btn.clicked.connect(self.on_reset_config)
        layout.addWidget(reset_btn)
        
        # 导出按钮
        export_btn = QPushButton("导出配置")
        export_btn.setStyleSheet(get_button_style("info"))
        export_btn.clicked.connect(self.on_export_config)
        layout.addWidget(export_btn)
        
        # 导入按钮
        import_btn = QPushButton("导入配置")
        import_btn.setStyleSheet(get_button_style("info"))
        import_btn.clicked.connect(self.on_import_config)
        layout.addWidget(import_btn)
        
        layout.addStretch()
        
        group.setLayout(layout)
        return group
    
    # 事件处理方法
    def on_theme_changed(self, theme_mode: str, checked: bool):
        """主题切换事件"""
        if not checked:
            return
        
        try:
            theme_manager = get_theme_manager()
            mode: ThemeMode = theme_mode  # type: ignore
            theme_manager.set_theme(mode, save=True)
            
            theme_names = {"light": "浅色主题", "dark": "深色主题", "auto": "跟随系统"}
            self.update_status_bar(f"已切换到{theme_names.get(theme_mode, theme_mode)}", 2000)
        except Exception as e:
            self.update_status_bar(f"主题切换失败: {e}", 3000)
    
    def on_remember_size_changed(self, checked: bool):
        """记住窗口大小改变"""
        if "appearance" not in app_config._config:
            app_config._config["appearance"] = {}
        app_config._config["appearance"]["remember_window_size"] = checked
        app_config.save_config()
        self.update_status_bar(f"记住窗口大小: {'已启用' if checked else '已禁用'}", 2000)
    
    def on_minimize_to_tray_changed(self, checked: bool):
        """最小化到托盘改变"""
        if "behavior" not in app_config._config:
            app_config._config["behavior"] = {}
        app_config._config["behavior"]["minimize_to_tray"] = checked
        app_config.save_config()
        self.update_status_bar(f"最小化到托盘: {'已启用' if checked else '已禁用'}", 2000)

    def on_close_to_tray_changed(self, checked: bool):
        """关闭到托盘改变"""
        if "behavior" not in app_config._config:
            app_config._config["behavior"] = {}
        app_config._config["behavior"]["close_to_tray"] = checked
        app_config.save_config()
        self.update_status_bar(f"关闭时最小化到托盘: {'已启用' if checked else '已禁用'}", 2000)

    def on_confirm_exit_changed(self, checked: bool):
        """退出确认改变"""
        if "behavior" not in app_config._config:
            app_config._config["behavior"] = {}
        app_config._config["behavior"]["confirm_on_exit"] = checked
        app_config.save_config()
        self.update_status_bar(f"退出确认: {'已启用' if checked else '已禁用'}", 2000)

    def on_start_minimized_changed(self, checked: bool):
        """启动最小化改变"""
        if "behavior" not in app_config._config:
            app_config._config["behavior"] = {}
        app_config._config["behavior"]["start_minimized"] = checked
        app_config.save_config()
        self.update_status_bar(f"启动时最小化: {'已启用' if checked else '已禁用'}", 2000)
    
    def on_auto_update_changed(self, checked: bool):
        """自动更新改变"""
        app_config.set_auto_check_updates(checked)
        self.update_status_bar(f"自动检查更新: {'已启用' if checked else '已禁用'}", 2000)
    
    def on_log_level_changed(self, level: str):
        """日志级别改变"""
        if "advanced" not in app_config._config:
            app_config._config["advanced"] = {}
        app_config._config["advanced"]["log_level"] = level
        app_config.save_config()
        self.update_status_bar(f"日志级别已设置为 {level}（重启后生效）", 2000)
    
    def on_debug_mode_changed(self, checked: bool):
        """调试模式改变"""
        if "advanced" not in app_config._config:
            app_config._config["advanced"] = {}
        app_config._config["advanced"]["debug_mode"] = checked
        app_config.save_config()
        self.update_status_bar(f"调试模式: {'已启用' if checked else '已禁用'}（重启后生效）", 2000)
    
    def on_reset_config(self):
        """重置配置"""
        reply = QMessageBox.question(
            self, "确认重置",
            "确定要将所有设置重置到默认值吗？\n此操作不可撤销。",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            app_config.reset_to_defaults()
            self.update_status_bar("配置已重置到默认值，请重启应用", 3000)
            QMessageBox.information(self, "重置成功", "配置已重置到默认值，请重启应用程序使更改生效。")
    
    def on_export_config(self):
        """导出配置"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "导出配置", "config_backup.json", "JSON Files (*.json)"
        )
        
        if file_path:
            if app_config.export_config(file_path):
                self.update_status_bar(f"配置已导出到 {file_path}", 3000)
                QMessageBox.information(self, "导出成功", f"配置已成功导出到:\n{file_path}")
            else:
                QMessageBox.warning(self, "导出失败", "配置导出失败，请检查文件路径和权限。")
    
    def on_import_config(self):
        """导入配置"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "导入配置", "", "JSON Files (*.json)"
        )
        
        if file_path:
            reply = QMessageBox.question(
                self, "确认导入",
                "导入配置将覆盖当前设置，确定继续吗？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                if app_config.import_config(file_path):
                    self.update_status_bar("配置已导入，请重启应用", 3000)
                    QMessageBox.information(self, "导入成功", "配置已成功导入，请重启应用程序使更改生效。")
                else:
                    QMessageBox.warning(self, "导入失败", "配置导入失败，请检查文件格式。")

