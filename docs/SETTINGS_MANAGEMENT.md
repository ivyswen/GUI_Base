# 设置/偏好管理系统文档

## 功能概述

设置/偏好管理系统为 GUI Base Template 提供了完整的配置管理功能，支持设置分类、验证、重置、导入导出等功能。

### 主要特性

- ✅ **设置分类**：主题、外观、行为、更新、高级设置
- ✅ **配置验证**：自动验证配置项的有效性
- ✅ **配置重置**：一键重置到默认值
- ✅ **导入导出**：支持配置文件的导入导出
- ✅ **实时生效**：部分设置实时生效，部分需要重启
- ✅ **持久化存储**：所有设置自动保存到配置文件

## 设置分类

### 1. 主题设置

| 设置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| mode | string | "auto" | 主题模式：light/dark/auto |

**实时生效**：是

### 2. 外观设置

| 设置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| font_size | int | 10 | 字体大小（8-24） |
| window_width | int | 1024 | 窗口宽度 |
| window_height | int | 768 | 窗口高度 |
| remember_window_size | bool | true | 是否记住窗口大小 |

**实时生效**：部分（字体大小需要重启）

### 3. 行为设置

| 设置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| minimize_to_tray | bool | false | 最小化到托盘 |
| close_to_tray | bool | false | 关闭到托盘 |
| start_minimized | bool | false | 启动时最小化 |
| confirm_on_exit | bool | true | 退出时确认 |

**实时生效**：是

### 4. 更新设置

| 设置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| auto_check_updates | bool | true | 自动检查更新 |
| update_check_timeout | int | 10 | 更新检查超时（秒） |
| download_timeout | int | 300 | 下载超时（秒） |

**实时生效**：是

### 5. 高级设置

| 设置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| log_level | string | "INFO" | 日志级别：DEBUG/INFO/WARNING/ERROR |
| debug_mode | bool | false | 调试模式 |
| enable_console | bool | false | 启用控制台 |

**实时生效**：否（需要重启）

## 使用方法

### 在设置页面修改

1. 打开应用程序
2. 切换到"设置"标签页
3. 在相应的分组中修改设置
4. 设置自动保存

### 程序化使用

```python
from utils.config import app_config

# 读取设置
font_size = app_config.font_size
theme_mode = app_config.theme_mode
confirm_exit = app_config.confirm_on_exit

# 修改设置
app_config._config["appearance"]["font_size"] = 12
app_config.save_config()

# 重置到默认值
app_config.reset_to_defaults()

# 导出配置
app_config.export_config("backup.json")

# 导入配置
app_config.import_config("backup.json")

# 验证配置
is_valid, errors = app_config.validate_config()
if not is_valid:
    print("配置错误:", errors)
```

## 配置文件格式

配置文件位于项目根目录的 `config.json`：

```json
{
    "theme": {
        "mode": "auto"
    },
    "appearance": {
        "font_size": 10,
        "window_width": 1024,
        "window_height": 768,
        "remember_window_size": true
    },
    "behavior": {
        "minimize_to_tray": false,
        "close_to_tray": false,
        "start_minimized": false,
        "confirm_on_exit": true
    },
    "advanced": {
        "log_level": "INFO",
        "debug_mode": false,
        "enable_console": false
    }
}
```

## 配置管理功能

### 重置到默认值

在设置页面点击"重置到默认值"按钮，或使用代码：

```python
app_config.reset_to_defaults()
```

**注意**：此操作不可撤销，建议先导出配置备份。

### 导出配置

在设置页面点击"导出配置"按钮，选择保存位置，或使用代码：

```python
app_config.export_config("path/to/backup.json")
```

### 导入配置

在设置页面点击"导入配置"按钮，选择配置文件，或使用代码：

```python
app_config.import_config("path/to/backup.json")
```

**注意**：导入配置会覆盖当前设置，建议先备份。

### 配置验证

系统会自动验证配置的有效性：

```python
is_valid, errors = app_config.validate_config()
if not is_valid:
    for error in errors:
        print(f"配置错误: {error}")
```

验证规则：
- 字体大小：8-24
- 窗口大小：最小 800x600
- 日志级别：DEBUG/INFO/WARNING/ERROR
- 主题模式：light/dark/auto

## 故障排除

### 问题：设置修改后未生效

**可能原因**：
1. 某些设置需要重启应用
2. 配置文件保存失败

**解决方案**：
1. 检查设置说明中的"实时生效"标记
2. 重启应用程序
3. 检查配置文件写入权限

### 问题：配置文件损坏

**解决方案**：
1. 删除 `config.json` 文件
2. 重启应用，系统会自动创建默认配置
3. 或从备份导入配置

### 问题：导入配置失败

**可能原因**：
1. 配置文件格式错误
2. 配置项不兼容

**解决方案**：
1. 检查 JSON 格式是否正确
2. 确保配置文件来自相同版本的应用
3. 使用文本编辑器手动修复

## 开发者指南

### 添加新的设置项

1. 在 `utils/config.py` 的 `DEFAULT_CONFIG` 中添加默认值
2. 添加对应的属性方法
3. 在 `gui/settings_tab.py` 中添加 UI 控件
4. 添加事件处理方法
5. 更新验证规则（如需要）
6. 更新文档

### 最佳实践

1. **使用属性方法**：通过 `app_config.property_name` 访问配置
2. **保存配置**：修改后调用 `app_config.save_config()`
3. **验证输入**：在保存前验证用户输入
4. **提供反馈**：通过状态栏或对话框告知用户操作结果
5. **备份重要配置**：在重大更改前提示用户备份

## 相关文档

- [主题系统文档](THEME_SYSTEM.md)
- [异常处理文档](EXCEPTION_HANDLING.md)
- [项目结构文档](PROJECT_STRUCTURE.md)

