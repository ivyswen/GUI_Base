# GUI Base Template

一个基于PySide6的基础GUI程序模板，为快速开发桌面应用程序提供完整的起始框架。

## 功能特性

### 🎯 核心功能
- **窗口自动居中**: 程序启动时窗口自动在桌面居中显示
- **完整菜单系统**: 包含文件、编辑、帮助等常用菜单
- **多标签页界面**: 支持多个功能页面的标签页切换
- **图标支持**: 应用程序和窗口图标自动加载
- **状态栏显示**: 实时显示程序状态和操作反馈

### 📋 界面组件
- **欢迎页面**: 程序介绍和功能说明
- **文本编辑器**: 基础的文本编辑功能
- **设置页面**: 可扩展的配置选项页面
- **菜单栏**: 文件操作、编辑功能、帮助信息
- **状态栏**: 操作提示和程序状态显示

## 项目结构

```
GUI_Base/
├── main.py              # 主程序文件
├── Resources/           # 资源文件目录
│   ├── favicon.ico      # 应用程序图标
│   └── icon-192.png     # 备用图标文件
├── pyproject.toml       # 项目配置文件
├── uv.lock             # 依赖锁定文件
└── README.md           # 项目说明文档
```

## 安装和运行

### 环境要求
- Python 3.11+
- PySide6 6.9.1+

### 安装依赖
```bash
# 使用uv安装依赖（推荐）
uv sync

# 或使用pip安装
pip install pyside6>=6.9.1
```

### 运行程序
```bash
# 使用uv运行
uv run python main.py

# 或直接运行
python main.py
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

### 添加新标签页
在`MainWindow`类中添加新的标签页创建方法：

```python
def create_new_tab(self):
    """创建新标签页"""
    new_tab = QWidget()
    layout = QVBoxLayout()

    # 添加您的组件
    label = QLabel("新功能页面")
    layout.addWidget(label)

    new_tab.setLayout(layout)
    self.tab_widget.addTab(new_tab, "新功能")
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

## 技术架构

### 主要类结构
- `MainWindow`: 主窗口类，继承自QMainWindow
- 使用PySide6的信号槽机制处理用户交互
- 模块化的界面组件设计，便于扩展

### 设计模式
- **单一职责**: 每个方法负责特定功能
- **模块化设计**: 界面组件分离，便于维护
- **事件驱动**: 基于Qt的信号槽机制

## 扩展建议

### 常见扩展方向
1. **数据库集成**: 添加SQLite或其他数据库支持
2. **文件操作**: 实现完整的文件读写功能
3. **网络功能**: 添加HTTP请求或WebSocket支持
4. **主题系统**: 实现深色/浅色主题切换
5. **插件系统**: 支持动态加载功能模块

### 性能优化
- 使用QThread处理耗时操作
- 实现延迟加载减少启动时间
- 添加缓存机制提升响应速度

## 许可证

本项目采用MIT许可证，您可以自由使用、修改和分发。

## 贡献

欢迎提交Issue和Pull Request来改进这个模板！

---

**开发提示**: 这个模板提供了GUI应用程序的基础框架，您可以根据具体需求进行扩展和定制。建议在开发过程中保持代码的模块化和可维护性。