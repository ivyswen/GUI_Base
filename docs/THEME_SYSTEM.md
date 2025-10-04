# 主题系统文档

## 功能概述

主题系统为 GUI Base Template 提供了深色/浅色主题切换功能，支持手动选择和自动跟随系统主题。

### 主要特性

- ✅ **深色主题**：深色背景，减少眼睛疲劳
- ✅ **浅色主题**：明亮背景，传统视觉体验
- ✅ **跟随系统**：自动检测并跟随操作系统主题设置
- ✅ **实时切换**：主题切换立即生效，无需重启应用
- ✅ **持久化配置**：主题设置自动保存到配置文件
- ✅ **跨平台支持**：支持 Windows、macOS 和 Linux

## 工作原理

### 主题应用流程

1. **应用启动**：从配置文件读取主题设置
2. **系统检测**：如果设置为"跟随系统"，检测操作系统主题
3. **应用主题**：设置 QPalette 和全局样式表
4. **用户切换**：用户在设置页面切换主题
5. **保存配置**：新的主题设置保存到配置文件

### 系统主题检测

#### Windows
- 读取注册表：`HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize\AppsUseLightTheme`
- 值为 0 = 深色主题，值为 1 = 浅色主题

#### macOS
- 执行命令：`defaults read -g AppleInterfaceStyle`
- 返回 "Dark" = 深色主题，否则为浅色主题

#### Linux
- 执行命令：`gsettings get org.gnome.desktop.interface gtk-theme`
- 主题名称包含 "dark" = 深色主题，否则为浅色主题

## 配置说明

### 配置文件位置

主题配置位于 `config.json` 文件中的 `theme` 节：

```json
{
    "theme": {
        "mode": "auto"
    }
}
```

### 配置选项

| 配置项 | 类型 | 可选值 | 默认值 | 说明 |
|--------|------|--------|--------|------|
| `mode` | string | `"light"`, `"dark"`, `"auto"` | `"auto"` | 主题模式 |

### 配置示例

#### 使用浅色主题

```json
{
    "theme": {
        "mode": "light"
    }
}
```

#### 使用深色主题

```json
{
    "theme": {
        "mode": "dark"
    }
}
```

#### 跟随系统主题

```json
{
    "theme": {
        "mode": "auto"
    }
}
```

## 使用方法

### 在设置页面切换主题

1. 打开应用程序
2. 切换到"设置"标签页
3. 在"主题设置"分组框中选择：
   - **浅色主题**：使用明亮的配色方案
   - **深色主题**：使用深色的配色方案
   - **跟随系统**：自动跟随操作系统的主题设置
4. 主题立即生效，无需重启

### 程序化使用

```python
from utils.theme import get_theme_manager

# 获取主题管理器
theme_manager = get_theme_manager()

# 设置主题
theme_manager.set_theme("dark", save=True)  # 深色主题
theme_manager.set_theme("light", save=True)  # 浅色主题
theme_manager.set_theme("auto", save=True)  # 跟随系统

# 获取当前主题
current_theme = theme_manager.get_current_theme()  # "light", "dark", "auto"

# 判断是否为深色主题
is_dark = theme_manager.is_dark_theme()  # True/False

# 检测系统主题
system_theme = theme_manager.detect_system_theme()  # "light" or "dark"
```

## 主题自定义

### 修改颜色方案

编辑 `utils/theme.py` 中的颜色常量：

```python
# 浅色主题颜色方案
LIGHT_COLORS = {
    "window": "#ffffff",
    "window_text": "#212529",
    "base": "#ffffff",
    # ... 其他颜色
}

# 深色主题颜色方案
DARK_COLORS = {
    "window": "#1e1e1e",
    "window_text": "#e0e0e0",
    "base": "#2d2d2d",
    # ... 其他颜色
}
```

### 自定义组件样式

在 `utils/styles.py` 中为组件添加主题支持：

```python
def get_custom_widget_style(theme: Optional[str] = None):
    """获取自定义组件样式"""
    # 确定是否使用深色主题
    if theme is None:
        is_dark = _is_dark_theme()
    else:
        is_dark = (theme == "dark")
    
    if is_dark:
        return """
            QCustomWidget {
                background-color: #2d2d2d;
                color: #e0e0e0;
            }
        """
    else:
        return """
            QCustomWidget {
                background-color: #ffffff;
                color: #212529;
            }
        """
```

## 故障排除

### 问题：主题切换后部分组件样式未更新

**可能原因**：
1. 组件使用了硬编码的样式
2. 组件未使用主题感知的样式函数

**解决方案**：
1. 检查组件是否使用了 `setStyleSheet()` 设置固定样式
2. 使用 `utils/styles.py` 中的样式函数
3. 在主题切换后手动刷新组件样式

### 问题：系统主题检测失败

**可能原因**：
1. 操作系统不支持主题检测
2. 权限不足
3. 系统配置异常

**解决方案**：
1. 检查日志文件中的错误信息
2. 手动选择浅色或深色主题
3. 系统检测失败时会自动降级为浅色主题

### 问题：主题设置未保存

**可能原因**：
1. 配置文件写入权限不足
2. 磁盘空间不足

**解决方案**：
1. 检查 `config.json` 文件的写入权限
2. 确保有足够的磁盘空间
3. 查看日志文件中的错误信息

## 开发者指南

### 添加新的主题模式

1. 在 `utils/theme.py` 中定义新的颜色方案
2. 更新 `ThemeMode` 类型定义
3. 修改 `apply_theme()` 方法支持新模式
4. 在设置页面添加对应的选项

### 主题切换事件

主题切换时，应用程序会：
1. 更新 QPalette
2. 更新全局样式表
3. 保存配置（如果 `save=True`）

所有使用主题感知样式函数的组件会自动更新。

### 最佳实践

1. **使用样式函数**：始终使用 `utils/styles.py` 中的样式函数
2. **避免硬编码**：不要在组件中硬编码颜色值
3. **测试两种主题**：确保组件在深色和浅色主题下都能正常显示
4. **考虑对比度**：确保文字和背景有足够的对比度

## 相关文档

- [项目结构文档](PROJECT_STRUCTURE.md)
- [配置管理文档](../README.md#配置管理)
- [样式系统文档](../README.md#样式系统)

