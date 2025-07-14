# PySide6-Fluent-Widgets 迁移指南

本文档展示如何将现有的标准PyQt组件替换为PySide6-Fluent-Widgets的美化组件。

## 核心组件替换对照表

### 1. 主窗口类型

**原始代码 (main.py):**
```python
from PySide6.QtWidgets import QMainWindow, QTabWidget
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)
```

**Fluent-Widgets版本 (main_fluent.py):**
```python
from qfluentwidgets import FluentWindow, NavigationItemPosition, FluentIcon
class FluentMainWindow(FluentWindow):
    def __init__(self):
        super().__init__()
        # 使用导航界面替代标签页
        self.addSubInterface(interface, FluentIcon.HOME, "欢迎", NavigationItemPosition.TOP)
```

### 2. 按钮组件

**原始代码:**
```python
from PySide6.QtWidgets import QPushButton
button = QPushButton("按钮文本")
button.setStyleSheet(self.get_button_style("primary"))  # 自定义样式
```

**Fluent-Widgets版本:**
```python
from qfluentwidgets import PushButton, PrimaryPushButton, FluentIcon
# 普通按钮
button = PushButton("按钮文本")
button.setIcon(FluentIcon.PLAY)

# 主要按钮（自带蓝色样式）
primary_button = PrimaryPushButton("主要按钮")
primary_button.setIcon(FluentIcon.SAVE)
```

### 3. 文本组件

**原始代码:**
```python
from PySide6.QtWidgets import QLabel, QTextEdit
title = QLabel("标题文本")
title.setStyleSheet("font-size: 18px; font-weight: bold;")
text_edit = QTextEdit()
```

**Fluent-Widgets版本:**
```python
from qfluentwidgets import TitleLabel, BodyLabel, CaptionLabel, TextEdit
# 标题标签（自带样式）
title = TitleLabel("标题文本")
# 正文标签
body = BodyLabel("正文内容")
# 说明文字
caption = CaptionLabel("说明文字")
# 文本编辑器
text_edit = TextEdit()
```

### 4. 消息提示

**原始代码:**
```python
from PySide6.QtWidgets import QMessageBox
QMessageBox.information(self, "标题", "消息内容")
# 状态栏消息
self.status_bar.showMessage("消息", 2000)
```

**Fluent-Widgets版本:**
```python
from qfluentwidgets import InfoBar, InfoBarPosition, MessageBox
# 信息栏（现代化提示）
InfoBar.success(
    title="成功",
    content="操作完成",
    orient=Qt.Horizontal,
    isClosable=True,
    position=InfoBarPosition.TOP,
    duration=2000,
    parent=self
)
# 对话框
MessageBox("标题", "消息内容", self).exec()
```

## 主要改进点

### 1. 设计语言升级
- **原始**: 传统的桌面应用样式
- **Fluent**: 现代化的Fluent Design设计语言
- **优势**: 更美观、更现代的视觉效果

### 2. 导航方式改进
- **原始**: 标签页导航 (`QTabWidget`)
- **Fluent**: 侧边栏导航 (`FluentWindow`)
- **优势**: 更直观的导航体验，支持图标和分组

### 3. 按钮样式简化
- **原始**: 需要手动编写CSS样式
- **Fluent**: 内置多种按钮类型
- **优势**: 开箱即用，样式统一

### 4. 主题支持
- **原始**: 需要手动实现主题切换
- **Fluent**: 内置深色/浅色主题支持
- **优势**: 一行代码切换主题

## 兼容性保持

### 1. 窗口居中
两个版本都保持了窗口居中启动的功能：
```python
def center_window(self):
    screen = QApplication.primaryScreen().geometry()
    window = self.geometry()
    x = (screen.width() - window.width()) // 2
    y = (screen.height() - window.height()) // 2
    self.move(x, y)
```

### 2. 图标支持
两个版本都支持从Resources目录加载图标：
```python
def set_window_icon(self):
    resources_dir = Path(__file__).parent / "Resources"
    # 图标加载逻辑保持一致
```

### 3. 功能完整性
所有原有功能都在Fluent版本中得到保留：
- 欢迎页面
- 文本编辑功能
- 设置页面
- 消息提示

## 使用建议

### 1. 渐进式迁移
建议先创建新的Fluent版本文件，测试无误后再替换原文件。

### 2. 主题配置
```python
from qfluentwidgets import setTheme, Theme, setThemeColor, ThemeColor
# 设置主题色
setThemeColor(ThemeColor.BLUE)
# 设置主题模式
setTheme(Theme.LIGHT)  # 或 Theme.DARK
```

### 3. 图标使用
Fluent-Widgets提供了丰富的内置图标：
```python
from qfluentwidgets import FluentIcon
button.setIcon(FluentIcon.PLAY)      # 播放图标
button.setIcon(FluentIcon.SAVE)      # 保存图标
button.setIcon(FluentIcon.DELETE)    # 删除图标
```

## 性能对比

### 启动速度
- **原始版本**: 快速启动
- **Fluent版本**: 略慢（需要加载主题资源）

### 内存占用
- **原始版本**: 较低
- **Fluent版本**: 略高（包含更多样式资源）

### 用户体验
- **原始版本**: 传统桌面应用体验
- **Fluent版本**: 现代化、流畅的用户体验

## 下一步计划

1. 测试Fluent版本的功能完整性
2. 优化主题切换功能
3. 添加更多Fluent组件示例
4. 更新项目文档
5. 提供迁移脚本（可选）
