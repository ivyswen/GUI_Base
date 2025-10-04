# GUI Base Template

一个基于PySide6的基础GUI程序模板，为快速开发桌面应用程序提供完整的起始框架。

## 功能特性

### 🎯 核心功能
- **模块化架构**: 采用模块化设计，GUI组件、工具组件分离，便于维护和扩展
- **窗口自动居中**: 程序启动时窗口自动在桌面居中显示
- **完整菜单系统**: 包含文件、编辑、帮助等常用菜单
- **多标签页界面**: 支持多个功能页面的标签页切换
- **图标支持**: 应用程序和窗口图标自动加载
- **状态栏显示**: 实时显示程序状态和操作反馈
- **全局日志系统**: 统一的日志记录，支持多种日志级别和文件输出
- **全局配置管理**: 集中的配置管理，支持版本同步和动态配置
- **高DPI显示优化**: 支持高分辨率显示器，字体清晰渲染，跨平台字体兼容
- **异常处理系统**: 全局异常捕获、友好的错误提示和详细的错误报告
- **主题系统**: 深色/浅色主题切换，支持跟随系统主题，实时切换无需重启
- **设置管理系统**: 完整的配置管理，支持分类设置、验证、重置、导入导出
- **通知/消息系统**: Toast通知、多种类型、消息历史、淡入淡出动画
- **系统托盘**: 托盘图标、托盘菜单、最小化到托盘、启动时最小化
- **插件系统**: 插件发现、动态加载、启用/禁用、插件管理UI

### 📋 界面组件
- **欢迎页面**: 程序介绍和功能说明，包含快速操作按钮
- **文本编辑器**: 基础的文本编辑功能，带有操作按钮
- **设置页面**: 可扩展的配置选项页面，包含各种设置按钮
- **菜单栏**: 文件操作、编辑功能、帮助信息
- **状态栏**: 操作提示和程序状态显示
- **统一按钮样式**: 5种不同类型的按钮样式（默认、主要、成功、警告、危险）

## 项目结构

```
GUI_Base/
├── main.py                      # 主程序文件（模块化重构后）
├── config.json                  # 应用程序配置文件
├── gui/                        # GUI组件模块（新增）
│   ├── __init__.py             # 模块初始化文件
│   ├── base_tab.py             # 基础Tab类，提供共享功能
│   ├── tab1.py                 # 欢迎页面模块
│   ├── tab2.py                 # 文本编辑器模块
│   ├── tab3.py                 # 设置页面模块
│   └── error_dialog.py         # 错误对话框组件
├── utils/                      # 全局工具模块（新增）
│   ├── __init__.py             # 模块初始化文件
│   ├── logger.py               # 全局日志组件
│   ├── config.py               # 全局配置组件
│   ├── display.py              # 显示优化组件（高DPI支持、字体渲染）
│   ├── exception_handler.py    # 全局异常处理组件
│   ├── theme.py                # 主题管理组件
│   └── styles.py               # 样式工具组件
├── updater/                    # 自动更新模块
│   ├── __init__.py             # 模块初始化文件
│   ├── update_manager.py       # 更新管理器
│   ├── update_checker.py       # 更新检查模块
│   ├── update_dialogs.py       # 更新界面模块
│   └── file_manager.py         # 文件管理模块
├── docs/                       # 文档目录
│   ├── AUTO_UPDATE_GUIDE.md    # 自动更新使用指南
│   ├── EXCEPTION_HANDLING.md   # 异常处理系统文档
│   ├── THEME_SYSTEM.md         # 主题系统文档
│   ├── SETTINGS_MANAGEMENT.md  # 设置管理系统文档
│   ├── NOTIFICATION_SYSTEM.md  # 通知/消息系统文档
│   └── REFACTORING_SUMMARY.md  # 重构总结文档
├── plugins/                   # 插件目录
│   ├── __init__.py
│   └── example_plugin/        # 示例插件
│       └── __init__.py
├── examples/                   # 示例文件目录
│   ├── example_update.json     # 示例远程版本信息
│   ├── update_example.py       # 示例更新程序
│   └── button_style_demo.py    # 按钮样式演示程序
├── Resources/                  # 资源文件目录
│   ├── favicon.ico             # 应用程序图标
│   └── icon-192.png            # 备用图标文件
├── logs/                       # 日志文件目录（自动生成）
│   ├── app_debug.log           # 详细日志
│   ├── app_error.log           # 错误日志
│   └── update.log              # 更新专用日志
├── test_refactoring.py         # 重构功能测试脚本
├── test_config_functionality.py # 配置功能测试脚本
├── build_nuitka.py             # Nuitka构建脚本
├── pyproject.toml              # 项目配置文件
├── uv.lock                     # 依赖锁定文件
└── README.md                   # 项目说明文档
```

## 安装和运行

### 环境要求
- Python 3.11+
- PySide6 6.9.1+
- PySide6-Fluent-Widgets 1.8.3+

### 安装依赖
```bash
# 使用uv安装依赖（推荐）
uv sync

# 或使用pip安装
pip install pyside6>=6.9.1 pyside6-fluent-widgets>=1.8.3
```

### 运行程序
```bash
# 运行主程序（模块化重构后）
uv run python main.py

# 运行重构功能测试
python test_refactoring.py

# 运行配置功能测试
python test_config_functionality.py

# 运行按钮样式演示
python examples/button_style_demo.py
```

## 使用说明

### 基本操作
1. **启动程序**: 运行main.py文件
2. **菜单操作**: 使用顶部菜单栏进行文件和编辑操作
3. **标签页切换**: 点击不同标签页查看各功能模块
4. **文本编辑**: 在"文本编辑"标签页中进行文本操作
5. **查看状态**: 底部状态栏显示当前操作状态

### 快捷键
- `Ctrl+N`: 新建文件
- `Ctrl+O`: 打开文件
- `Ctrl+C`: 复制
- `Ctrl+V`: 粘贴
- `Ctrl+Q`: 退出程序

## 自定义开发

### 模块化架构说明
项目采用模块化设计，主要模块包括：

- **gui/**: GUI组件模块，每个Tab页面对应一个独立文件
- **utils/**: 全局工具模块，包含日志和配置组件
- **updater/**: 自动更新模块，提供完整的更新功能

### 添加新标签页
1. 在`gui/`目录下创建新的Tab模块文件：

```python
# gui/tab4.py
from .base_tab import BaseTab
from PySide6.QtWidgets import QVBoxLayout, QLabel

class NewFeatureTab(BaseTab):
    """新功能Tab"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        label = QLabel("新功能页面")
        layout.addWidget(label)
        self.setLayout(layout)
```

2. 在`gui/__init__.py`中导出新的Tab类：

```python
from .tab4 import NewFeatureTab
__all__ = [..., 'NewFeatureTab']
```

3. 在`main.py`中使用新的Tab：

```python
from gui import ..., NewFeatureTab

# 在create_central_widget方法中添加
self.new_feature_tab = NewFeatureTab(self)
self.tab_widget.addTab(self.new_feature_tab, "新功能")
```

### 添加菜单项
在`create_menu_bar`方法中添加新的菜单和动作：

```python
# 添加新菜单
new_menu = menubar.addMenu('新菜单(&N)')

# 添加新动作
new_action = QAction('新功能(&F)', self)
new_action.triggered.connect(self.new_function)
new_menu.addAction(new_action)
```

### 更换图标
将新的图标文件放入`Resources`目录，支持的格式：
- `.ico` 文件（Windows推荐）
- `.png` 文件（跨平台）

程序会自动按优先级加载图标文件。

### 按钮样式系统
模板提供了5种不同类型的按钮样式，现在通过BaseTab类提供：

```python
# 在任何继承自BaseTab的类中使用按钮样式
button = QPushButton("按钮文本")
button.setStyleSheet(self.get_button_style("样式类型"))
```

**可用样式类型：**
- `"default"`: 默认样式（灰色）- 适用于一般操作
- `"primary"`: 主要样式（蓝色）- 适用于重要操作
- `"success"`: 成功样式（绿色）- 适用于确认、保存操作
- `"warning"`: 警告样式（黄色）- 适用于需要注意的操作
- `"danger"`: 危险样式（红色）- 适用于删除、重置操作

**样式特性：**
- 统一的圆角边框和内边距
- 悬停和按下状态的视觉反馈
- 禁用状态的灰化效果
- 响应式的最小尺寸设置

**使用示例：**
```python
# 在Tab模块中使用（继承自BaseTab）
class MyTab(BaseTab):
    def init_ui(self):
        # 主要操作按钮
        save_button = QPushButton("保存")
        save_button.setStyleSheet(self.get_button_style("primary"))

        # 删除操作按钮
        delete_button = QPushButton("删除")
        delete_button.setStyleSheet(self.get_button_style("danger"))
```

## 🏗️ 模块化架构（重构后）

### 架构概述
项目经过模块化重构，采用了清晰的分层架构：

```
应用层 (main.py)
    ↓
GUI组件层 (gui/)
    ↓
工具组件层 (utils/)
    ↓
业务逻辑层 (updater/)
```

### 核心模块说明

#### GUI组件模块 (gui/)
- **base_tab.py**: 基础Tab类，提供共享功能（按钮样式、状态栏更新等）
- **tab1.py**: 欢迎页面，包含程序介绍和快速操作
- **tab2.py**: 文本编辑器，提供基础文本编辑功能
- **tab3.py**: 设置页面，包含各种配置选项

#### 工具组件模块 (utils/)
- **logger.py**: 全局日志组件，提供统一的日志记录功能
- **config.py**: 全局配置组件，管理应用程序配置和版本信息
- **display.py**: 显示优化组件，提供高DPI支持和字体渲染优化

#### 更新模块 (updater/)
- **update_manager.py**: 更新管理器，统一管理更新流程
- **update_checker.py**: 更新检查，处理版本比较和远程版本获取
- **update_dialogs.py**: 更新界面，包含更新提示和下载进度对话框
- **file_manager.py**: 文件管理，处理文件下载、校验和临时文件管理

### 重构优势
1. **模块化设计**: 每个功能模块独立，便于维护和测试
2. **代码复用**: BaseTab类提供共享功能，避免代码重复
3. **全局组件**: logger和config作为全局组件，整个应用程序都可以使用
4. **清晰职责**: 每个模块都有明确的职责和功能边界
5. **易于扩展**: 新增功能只需创建新的模块文件

### 使用全局组件

#### 日志组件
```python
from utils import app_logger, update_logger, get_logger

# 使用预定义的日志记录器
app_logger.info("应用程序信息")
update_logger.info("更新相关信息")

# 创建自定义日志记录器
custom_logger = get_logger("my_module")
custom_logger.debug("调试信息")
```

#### 配置组件
```python
from utils import app_config

# 读取配置
app_name = app_config.app_name
current_version = app_config.current_version

# 修改配置
app_config.set("custom_setting", "value")
app_config.save_config()

# 版本管理
app_config.update_version_from_exe()  # 从exe同步版本
```

## PySide6-Fluent-Widgets 集成

### 🎨 现代化UI设计
本项目现已集成PySide6-Fluent-Widgets库，提供现代化的Fluent Design用户界面。

### 主要特性
- **现代化设计语言**: 基于Microsoft Fluent Design System
- **流畅动画效果**: 丰富的过渡动画和交互反馈
- **导航系统**: 侧边栏导航替代传统标签页
- **主题支持**: 内置深色/浅色主题切换
- **丰富组件**: 现代化的按钮、文本框、标签等组件
- **图标系统**: 内置大量Fluent图标

### 版本对比

| 特性 | 原始版本 (main.py) | Fluent版本 (main_fluent.py) |
|------|-------------------|----------------------------|
| 设计风格 | 传统桌面应用 | 现代化Fluent Design |
| 导航方式 | 标签页 | 侧边栏导航 |
| 按钮样式 | 手动CSS样式 | 内置组件样式 |
| 主题支持 | 需手动实现 | 一键切换 |
| 动画效果 | 无 | 流畅过渡动画 |
| 图标支持 | 外部图标文件 | 内置图标库 |

### 快速体验
```bash
# 运行样式对比演示
uv run python fluent_style_comparison.py

# 查看迁移指南
cat fluent_migration_guide.md
```

### 组件替换示例
```python
# 原始PyQt组件
from PySide6.QtWidgets import QPushButton, QLabel
button = QPushButton("按钮")
label = QLabel("文本")

# Fluent-Widgets组件
from qfluentwidgets import PushButton, PrimaryPushButton, TitleLabel, BodyLabel
button = PushButton("按钮")
primary_button = PrimaryPushButton("主要按钮")
title = TitleLabel("标题")
body = BodyLabel("正文")
```

## 技术架构

### 主要类结构
- `MainWindow`: 主窗口类，继承自QMainWindow
- 使用PySide6的信号槽机制处理用户交互
- 模块化的界面组件设计，便于扩展

### 设计模式
- **单一职责**: 每个方法负责特定功能
- **模块化设计**: 界面组件分离，便于维护
- **事件驱动**: 基于Qt的信号槽机制

## 🔄 自动更新功能（新增）

### 功能概述
新增的自动更新功能提供了完整的软件更新解决方案：

- ✅ 版本检查机制（比较本地版本与远程版本）
- ✅ 更新提示界面，显示更新日志
- ✅ 文件下载和 SHA256 校验
- ✅ 更新进度显示
- ✅ 安全性和可靠性保证
- ✅ 可配置的更新设置

### 核心模块
- `utils/config.py`: 全局配置管理模块（重构后）
- `utils/logger.py`: 全局日志组件（重构后）
- `updater/update_manager.py`: 更新管理器
- `updater/update_checker.py`: 更新检查模块
- `updater/update_dialogs.py`: 更新相关对话框
- `updater/file_manager.py`: 文件管理模块

### 配置文件
应用程序配置存储在 `config.json` 文件中：

```json
{
    "app_name": "GUI Base Template",
    "current_version": "1.0.0",
    "organization_name": "Your Organization",
    "update_server": "https://your-server.com",
    "update_check_url": "",
    "auto_check_updates": true,
    "update_check_timeout": 10,
    "download_timeout": 300,
    "temp_dir_name": "app_update"
}
```

**配置说明**：
- `current_version`: 当前版本号
  - 开发环境：从配置文件读取
  - 生产环境（exe）：优先从exe文件版本信息读取，配置文件作为备用
- `update_server`: 更新服务器基础地址，用于构建所有相关URL
- `update_check_url`:
  - 如果为空或不是完整URL，系统会自动基于 `update_server` 构建为 `{update_server}/update.json`
  - 如果是完整URL（以 http:// 或 https:// 开头），则直接使用该URL

**配置方式**：
1. **简单配置**：只设置 `update_server`，让 `update_check_url` 为空，系统自动构建
2. **自定义配置**：设置完整的 `update_check_url`，系统直接使用
3. **版本管理**：
   - 开发时在 `config.json` 中设置版本号
   - 打包时通过 Nuitka 的 `--file-version` 参数设置版本，程序会自动读取

### 远程版本信息格式
服务器端的版本信息应使用以下 JSON 格式：

```json
{
    "version": "2.0.0",
    "changelog": "1. 新增自动更新功能\n2. 优化性能\n3. 修复已知问题",
    "url": "https://your-server.com/updates/app_v2.0.0.zip",
    "update_exe_url": "https://your-server.com/updates/update_v1.0.exe",
    "sha256": {
        "package": "a1b2c3d4...",
        "update_exe": "e5f6g7h8..."
    }
}
```

### 使用方法
1. **手动检查更新**: 通过菜单栏 "帮助" → "检查更新"
2. **自动检查更新**: 程序启动时自动检查（可在配置中关闭）
3. **更新流程**: 检查远程版本信息 → 显示更新对话框 → 下载更新包 → 验证文件完整性 → 启动更新程序并重启应用

### 自定义更新服务器
1. 修改 `config.json` 中的 `update_check_url`
2. 确保服务器返回正确格式的 JSON 数据
3. 提供更新包和更新程序的下载链接

### 测试功能
运行测试脚本验证功能：
```bash
# 测试重构后的模块化功能
python test_refactoring.py

# 测试配置组件功能
python test_config_functionality.py

# 测试自动更新功能（如果可用）
python test_update.py
```

### 更新程序参数格式
系统使用以下参数格式启动更新程序：
```bash
update.exe --target-dir "C:\MyApp" --update-package "d:\update_v2.0.zip" --app-exe "My.exe"
```

**参数说明**：
- `--target-dir`: 应用程序安装目录
- `--update-package`: 更新包文件路径
- `--app-exe`: 应用程序可执行文件名（不包含路径）

### 文档和示例
- 详细使用指南：`docs/AUTO_UPDATE_GUIDE.md`
- 重构总结文档：`docs/REFACTORING_SUMMARY.md`
- 示例文件：`examples/` 目录
- 远程版本信息示例：`examples/example_update.json`
- 更新程序示例：`examples/update_example.py`
- 按钮样式演示：`examples/button_style_demo.py`

## 🛡️ 异常处理系统（新增）

### 功能概述
全局异常处理系统提供了完整的错误捕获和用户反馈机制：

- ✅ **全局异常捕获**：自动捕获所有未处理的异常
- ✅ **友好的错误对话框**：向用户显示清晰的错误信息
- ✅ **详细的错误报告**：自动生成包含系统信息的错误报告文件
- ✅ **日志集成**：所有异常自动记录到日志文件
- ✅ **可配置**：通过配置文件灵活控制异常处理行为
- ✅ **用户操作**：提供复制错误信息、查看日志等便捷功能

### 核心模块
- `utils/exception_handler.py`: 全局异常处理器
- `gui/error_dialog.py`: 错误对话框组件

### 配置选项
在 `config.json` 中配置异常处理行为：

```json
{
    "exception_handler": {
        "enabled": true,         // 是否启用异常处理
        "show_dialog": true,     // 是否显示错误对话框
        "save_report": true,     // 是否保存错误报告
        "report_dir": "error_reports"  // 错误报告目录
    }
}
```

### 错误报告
- **位置**：`error_reports/` 目录（开发环境在项目根目录，生产环境在exe同目录）
- **格式**：JSON 格式，包含时间戳、异常信息、堆栈跟踪和系统信息
- **文件名**：`error_report_YYYYMMDD_HHMMSS.json`

### 错误对话框功能
1. 显示简洁的错误信息
2. 可展开查看详细的技术信息
3. 一键复制错误信息到剪贴板
4. 直接打开日志文件所在目录
5. 安全退出应用程序

### 使用方法
异常处理系统会自动工作，无需手动调用。当程序发生未捕获的异常时：
1. 异常信息自动记录到日志文件
2. 生成详细的错误报告文件（如果启用）
3. 显示友好的错误对话框（如果启用）

### 文档
- 详细文档：`docs/EXCEPTION_HANDLING.md`
- 测试示例：`examples/test_exception_handler.py`

## 🎨 主题系统（新增）

### 功能概述
主题系统提供了深色/浅色主题切换功能，支持手动选择和自动跟随系统主题：

- ✅ **深色主题**：深色背景，减少眼睛疲劳
- ✅ **浅色主题**：明亮背景，传统视觉体验
- ✅ **跟随系统**：自动检测并跟随操作系统主题设置
- ✅ **实时切换**：主题切换立即生效，无需重启应用
- ✅ **持久化配置**：主题设置自动保存到配置文件
- ✅ **跨平台支持**：支持 Windows、macOS 和 Linux

### 核心模块
- `utils/theme.py`: 主题管理器
- `utils/styles.py`: 主题感知的样式工具

### 配置选项
在 `config.json` 中配置主题：

```json
{
    "theme": {
        "mode": "auto"  // "light", "dark", "auto"
    }
}
```

### 使用方法
1. **在设置页面切换**：打开应用 → 设置标签页 → 主题设置 → 选择主题
2. **程序化使用**：
```python
from utils.theme import get_theme_manager

theme_manager = get_theme_manager()
theme_manager.set_theme("dark", save=True)  # 深色主题
theme_manager.set_theme("light", save=True)  # 浅色主题
theme_manager.set_theme("auto", save=True)  # 跟随系统
```

### 系统主题检测
- **Windows**：读取注册表 `AppsUseLightTheme`
- **macOS**：执行 `defaults read -g AppleInterfaceStyle`
- **Linux**：执行 `gsettings get org.gnome.desktop.interface gtk-theme`

### 文档
- 详细文档：`docs/THEME_SYSTEM.md`
- 测试示例：`examples/test_theme.py`

## ⚙️ 设置/偏好管理系统（新增）

### 功能概述
完整的配置管理系统，支持设置分类、验证、重置、导入导出等功能：

- ✅ **设置分类**：主题、外观、行为、更新、高级设置
- ✅ **配置验证**：自动验证配置项的有效性
- ✅ **配置重置**：一键重置到默认值
- ✅ **导入导出**：支持配置文件的导入导出
- ✅ **实时生效**：部分设置实时生效，部分需要重启
- ✅ **持久化存储**：所有设置自动保存到配置文件

### 设置分类
1. **主题设置**：主题模式（浅色/深色/自动）
2. **外观设置**：字体大小、窗口大小、记住窗口大小
3. **行为设置**：退出确认、启动最小化
4. **更新设置**：自动检查更新
5. **高级设置**：日志级别、调试模式

### 配置管理功能
- **重置到默认值**：一键恢复所有默认设置
- **导出配置**：备份当前配置到文件
- **导入配置**：从文件恢复配置
- **配置验证**：自动验证配置有效性

### 使用方法
1. **在设置页面修改**：打开应用 → 设置标签页 → 修改相应设置
2. **程序化使用**：
```python
from utils.config import app_config

# 读取设置
font_size = app_config.font_size
theme_mode = app_config.theme_mode

# 重置配置
app_config.reset_to_defaults()

# 导出/导入配置
app_config.export_config("backup.json")
app_config.import_config("backup.json")
```

### 文档
- 详细文档：`docs/SETTINGS_MANAGEMENT.md`

## 📢 通知/消息系统（新增）

### 功能概述
完整的通知系统，支持Toast通知、消息历史等功能：

- ✅ **Toast通知**：临时的弹出通知，自动消失
- ✅ **多种类型**：信息、成功、警告、错误
- ✅ **自定义时长**：可设置显示时长或不自动关闭
- ✅ **淡入淡出动画**：平滑的显示和隐藏效果
- ✅ **消息历史**：保存所有通知记录
- ✅ **未读标记**：支持标记已读/未读
- ✅ **点击回调**：支持点击通知时执行自定义操作

### 通知类型
- **INFO**：信息通知（蓝色，3秒）
- **SUCCESS**：成功通知（绿色，3秒）
- **WARNING**：警告通知（黄色，5秒）
- **ERROR**：错误通知（红色，不自动关闭）

### 使用方法
```python
from utils.notification import get_notification_manager

notification_manager = get_notification_manager()

# 显示不同类型的通知
notification_manager.info("标题", "这是一条信息通知")
notification_manager.success("成功", "操作已完成")
notification_manager.warning("警告", "请注意")
notification_manager.error("错误", "发生了错误")

# 自定义时长和回调
notification_manager.info("标题", "消息", duration=5000, action=callback_func)
```

### 测试通知
在欢迎页面点击"测试通知"按钮，可以看到四种类型的通知效果。

### 文档
- 详细文档：`docs/NOTIFICATION_SYSTEM.md`

## 🔌 插件系统（新增）

### 功能概述
完整的插件系统，支持插件的发现、加载、管理和扩展：

- ✅ **插件发现**：自动扫描 `plugins/` 目录
- ✅ **动态加载**：运行时加载插件
- ✅ **插件管理**：启用/禁用插件
- ✅ **插件接口**：标准的插件基类
- ✅ **插件UI**：插件可以提供UI组件
- ✅ **插件菜单**：插件可以添加菜单项
- ✅ **错误隔离**：插件错误不影响主程序

### 插件架构
- **插件目录**：`plugins/`
- **插件格式**：Python包（目录 + `__init__.py`）
- **插件基类**：`BasePlugin`
- **插件管理器**：`PluginManager`

### 创建插件

#### 1. 创建插件目录
```
plugins/my_plugin/
└── __init__.py
```

#### 2. 实现插件类
```python
from utils.plugin_base import BasePlugin, PluginMetadata

class MyPlugin(BasePlugin):
    def get_metadata(self):
        return PluginMetadata(
            name="我的插件",
            version="1.0.0",
            author="Your Name",
            description="插件描述"
        )

    def initialize(self, main_window):
        self._main_window = main_window
        return True

    def enable(self):
        super().enable()
        # 启用逻辑
        return True

    def disable(self):
        super().disable()
        # 禁用逻辑
        return True
```

#### 3. 可选：添加UI组件
```python
def get_widget(self):
    widget = QWidget()
    # 创建UI
    return widget
```

#### 4. 可选：添加菜单项
```python
def get_menu_items(self):
    return [
        ("菜单项名称", self.on_menu_action)
    ]
```

### 管理插件

1. 打开应用
2. 切换到"设置"标签页
3. 滚动到"插件管理"分组
4. 查看已加载的插件
5. 点击"启用"/"禁用"按钮

### 示例插件

项目包含一个示例插件（`plugins/example_plugin`），演示：
- 插件元数据
- 初始化和启用/禁用
- UI组件
- 菜单项
- 通知集成

### 插件API

#### BasePlugin 方法
- `get_metadata()` - 返回插件元数据（必须实现）
- `initialize(main_window)` - 初始化插件（必须实现）
- `enable()` - 启用插件
- `disable()` - 禁用插件
- `cleanup()` - 清理资源
- `get_widget()` - 返回UI组件（可选）
- `get_menu_items()` - 返回菜单项（可选）
- `is_enabled()` - 检查是否已启用
- `get_config()` / `set_config()` - 配置管理

#### PluginManager 方法
- `discover_plugins()` - 发现所有插件
- `load_plugin(name)` - 加载指定插件
- `unload_plugin(name)` - 卸载指定插件
- `enable_plugin(name)` - 启用指定插件
- `disable_plugin(name)` - 禁用指定插件
- `get_plugin(name)` - 获取插件实例
- `get_all_plugins()` - 获取所有插件

### 最佳实践

1. **错误处理**：在插件中使用 try-except 捕获异常
2. **日志记录**：使用 `utils.logger.get_logger(__name__)` 记录日志
3. **资源清理**：在 `cleanup()` 方法中释放资源
4. **配置管理**：使用 `get_config()` 和 `set_config()` 管理配置
5. **通知集成**：使用 `utils.notification.get_notification_manager()` 显示通知

## 扩展建议

### 常见扩展方向
1. **新增Tab页面**: 在gui/目录下创建新的Tab模块
2. **工具组件扩展**: 在utils/目录下添加数据库、网络等工具组件
3. **主题系统**: 实现深色/浅色主题切换，可添加到utils/目录
4. **国际化支持**: 添加多语言支持组件
5. **插件系统**: 支持动态加载功能模块
6. **自动更新扩展**: 增量更新、回滚功能、更新通知等
7. **配置界面**: 为utils/config.py创建可视化配置界面

### 性能优化
- 使用QThread处理耗时操作
- 实现延迟加载减少启动时间
- 添加缓存机制提升响应速度
- 优化更新包大小和下载速度

## 许可证

本项目采用MIT许可证，您可以自由使用、修改和分发。

## 贡献

欢迎提交Issue和Pull Request来改进这个模板！

---

**开发提示**: 这个模板提供了GUI应用程序的模块化基础框架，经过重构后具有更好的可维护性和可扩展性。建议在开发过程中：
1. 遵循模块化设计原则，将功能分离到不同模块
2. 使用全局组件（logger、config）确保一致性
3. 继承BaseTab类来创建新的Tab页面
4. 将通用工具添加到utils/目录下
5. 保持代码的清晰职责和良好的文档