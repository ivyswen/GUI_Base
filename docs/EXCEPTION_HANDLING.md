# 异常处理系统文档

## 功能概述

异常处理系统是 GUI Base Template 的核心功能之一，提供了全局的异常捕获、错误日志记录和用户友好的错误提示功能。

### 主要特性

- ✅ **全局异常捕获**：自动捕获所有未处理的异常
- ✅ **友好的错误对话框**：向用户显示清晰的错误信息
- ✅ **详细的错误报告**：自动生成包含系统信息的错误报告文件
- ✅ **日志集成**：所有异常自动记录到日志文件
- ✅ **可配置**：通过配置文件灵活控制异常处理行为
- ✅ **用户操作**：提供复制错误信息、查看日志等便捷功能

## 工作原理

### 异常捕获流程

1. **异常发生**：程序运行时发生未捕获的异常
2. **全局钩子捕获**：`sys.excepthook` 捕获异常
3. **信息收集**：收集异常类型、消息、堆栈跟踪和系统信息
4. **日志记录**：使用 loguru 记录详细的异常信息
5. **保存报告**：生成 JSON 格式的错误报告文件（可选）
6. **显示对话框**：向用户显示友好的错误提示（可选）

### 系统架构

```
异常发生
    ↓
sys.excepthook (ExceptionHandler.handle_exception)
    ↓
    ├─→ 格式化异常信息 (_format_exception)
    ├─→ 收集系统信息 (_get_system_info)
    ├─→ 记录到日志 (logger.error)
    ├─→ 保存错误报告 (_save_error_report)
    └─→ 显示错误对话框 (_show_error_dialog)
```

## 配置说明

### 配置文件位置

异常处理配置位于 `config.json` 文件中的 `exception_handler` 节：

```json
{
    "exception_handler": {
        "enabled": true,
        "show_dialog": true,
        "save_report": true,
        "report_dir": "error_reports"
    }
}
```

### 配置项说明

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `enabled` | boolean | `true` | 是否启用异常处理系统 |
| `show_dialog` | boolean | `true` | 是否显示错误对话框 |
| `save_report` | boolean | `true` | 是否保存错误报告文件 |
| `report_dir` | string | `"error_reports"` | 错误报告保存目录 |

### 配置示例

#### 禁用错误对话框（仅记录日志）

```json
{
    "exception_handler": {
        "enabled": true,
        "show_dialog": false,
        "save_report": true,
        "report_dir": "error_reports"
    }
}
```

#### 完全禁用异常处理

```json
{
    "exception_handler": {
        "enabled": false,
        "show_dialog": false,
        "save_report": false,
        "report_dir": "error_reports"
    }
}
```

## 错误报告

### 报告文件位置

- **开发环境**：`项目根目录/error_reports/`
- **生产环境**：`exe所在目录/error_reports/`

### 报告文件格式

错误报告以 JSON 格式保存，文件名格式：`error_report_YYYYMMDD_HHMMSS.json`

示例：`error_report_20251004_123456.json`

### 报告内容

```json
{
    "timestamp": "2025-10-04 12:34:56",
    "app_name": "GUI Base Template",
    "app_version": "1.0.0",
    "exception_type": "ValueError",
    "exception_message": "invalid literal for int() with base 10: 'abc'",
    "traceback": "Traceback (most recent call last):\n  File \"main.py\", line 123, in <module>\n    ...",
    "system_info": {
        "platform": "Windows-10-10.0.19045-SP0",
        "python_version": "3.11.0",
        "pyside6_version": "6.9.1",
        "machine": "AMD64",
        "processor": "Intel64 Family 6 Model 142 Stepping 12, GenuineIntel"
    }
}
```

## 错误对话框

### 对话框功能

错误对话框提供以下功能：

1. **简洁的错误信息**：显示错误类型和错误消息
2. **详细信息展开**：点击"显示详细信息"查看完整的堆栈跟踪和系统信息
3. **复制错误信息**：一键复制所有错误信息到剪贴板
4. **查看日志文件**：直接打开日志文件所在目录
5. **退出程序**：安全退出应用程序

### 对话框截图

```
┌─────────────────────────────────────────────┐
│ ❌  程序遇到了一个错误                        │
│                                             │
│ 错误类型: ValueError                         │
│ 错误信息: invalid literal for int()...      │
│                                             │
│ [显示详细信息 ▼] [复制错误信息] [查看日志]    │
│                                   [退出程序] │
└─────────────────────────────────────────────┘
```

## 日志记录

### 日志文件位置

- **开发环境**：`项目根目录/logs/`
- **生产环境**：`exe所在目录/logs/`

### 相关日志文件

1. **app_debug.log**：包含所有级别的日志，包括异常信息
2. **app_error.log**：仅包含错误级别的日志
3. **update.log**：更新相关的日志

### 日志格式

```
2025-10-04 12:34:56.789 | ERROR    | utils.exception_handler:handle_exception:67 - 未捕获的异常: ValueError: invalid literal for int() with base 10: 'abc'
2025-10-04 12:34:56.790 | ERROR    | utils.exception_handler:handle_exception:68 - 异常堆栈:
Traceback (most recent call last):
  File "main.py", line 123, in <module>
    ...
```

## 开发者指南

### 在代码中使用

异常处理系统会自动捕获所有未处理的异常，无需在代码中显式调用。

#### 正常的异常处理

```python
try:
    # 可能抛出异常的代码
    result = int("abc")
except ValueError as e:
    # 处理已知的异常
    logger.error(f"转换失败: {e}")
```

#### 让异常被全局处理器捕获

```python
# 不捕获异常，让全局处理器处理
result = int("abc")  # 这会触发全局异常处理器
```

### 自定义异常处理

如果需要在特定情况下自定义异常处理：

```python
from utils import get_exception_handler

# 获取异常处理器实例
handler = get_exception_handler()

# 手动处理异常
try:
    # 代码
    pass
except Exception as e:
    import sys
    handler.handle_exception(type(e), e, e.__traceback__)
```

### 临时禁用异常处理

```python
import sys
from utils import get_exception_handler

# 保存原始的 excepthook
original_hook = sys.excepthook

# 恢复 Python 默认的异常处理
sys.excepthook = get_exception_handler()._original_excepthook

# 执行代码...

# 恢复异常处理
sys.excepthook = original_hook
```

## 故障排除

### 问题：错误对话框没有显示

**可能原因**：
1. 配置中 `show_dialog` 设置为 `false`
2. QApplication 未正确初始化
3. 异常发生在 QApplication 创建之前

**解决方案**：
1. 检查 `config.json` 中的 `exception_handler.show_dialog` 配置
2. 确保异常发生在 `setup_exception_handler(app)` 调用之后
3. 查看日志文件确认异常是否被记录

### 问题：错误报告文件未生成

**可能原因**：
1. 配置中 `save_report` 设置为 `false`
2. 没有写入权限
3. 磁盘空间不足

**解决方案**：
1. 检查 `config.json` 中的 `exception_handler.save_report` 配置
2. 检查错误报告目录的写入权限
3. 确保有足够的磁盘空间

### 问题：某些异常没有被捕获

**可能原因**：
1. 异常在子线程中发生
2. 异常被其他代码捕获
3. Qt 特定的异常处理机制

**解决方案**：
1. 在子线程中也设置异常处理
2. 检查代码中的 try-except 块
3. 查看日志文件确认异常信息

## 最佳实践

1. **保持异常处理启用**：在生产环境中始终启用异常处理
2. **定期检查错误报告**：定期查看错误报告文件，及时发现和修复问题
3. **合理使用异常**：不要过度依赖全局异常处理，应该在代码中处理已知的异常
4. **提供用户反馈**：在错误对话框中提供清晰的错误信息和解决建议
5. **保护敏感信息**：确保错误报告中不包含敏感信息（如密码、密钥等）

## 相关文档

- [项目结构文档](PROJECT_STRUCTURE.md)
- [日志系统文档](../README.md#日志系统)
- [配置管理文档](../README.md#配置管理)

