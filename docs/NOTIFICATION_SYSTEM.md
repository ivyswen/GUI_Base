# 通知/消息系统文档

## 功能概述

通知/消息系统为 GUI Base Template 提供了完整的通知功能，支持Toast通知、消息历史等功能。

### 主要特性

- ✅ **Toast通知**：临时的弹出通知，自动消失
- ✅ **多种类型**：信息、成功、警告、错误
- ✅ **自定义时长**：可设置显示时长或不自动关闭
- ✅ **淡入淡出动画**：平滑的显示和隐藏效果
- ✅ **消息历史**：保存所有通知记录
- ✅ **未读标记**：支持标记已读/未读
- ✅ **点击回调**：支持点击通知时执行自定义操作

## 通知类型

| 类型 | 说明 | 默认时长 | 颜色 |
|------|------|----------|------|
| INFO | 信息通知 | 3秒 | 蓝色 |
| SUCCESS | 成功通知 | 3秒 | 绿色 |
| WARNING | 警告通知 | 5秒 | 黄色 |
| ERROR | 错误通知 | 不自动关闭 | 红色 |

## 使用方法

### 基本用法

```python
from utils.notification import get_notification_manager

# 获取通知管理器
notification_manager = get_notification_manager()

# 显示信息通知
notification_manager.info("标题", "这是一条信息通知")

# 显示成功通知
notification_manager.success("成功", "操作已完成")

# 显示警告通知
notification_manager.warning("警告", "请注意")

# 显示错误通知
notification_manager.error("错误", "发生了错误")
```

### 自定义时长

```python
# 显示5秒的通知
notification_manager.info("标题", "消息", duration=5000)

# 不自动关闭的通知
notification_manager.info("标题", "消息", duration=0)
```

### 添加点击回调

```python
def on_click():
    print("通知被点击了")

notification_manager.info("标题", "点击我", action=on_click)
```

### 消息历史

```python
# 获取所有通知
all_notifications = notification_manager.get_all()

# 获取未读通知
unread = notification_manager.get_unread()

# 获取未读数量
count = notification_manager.get_unread_count()

# 标记为已读
notification_manager.mark_as_read(notification_id)

# 标记所有为已读
notification_manager.mark_all_as_read()

# 清除所有通知
notification_manager.clear()
```

## 集成到应用

### 1. 初始化通知管理器

在 `main.py` 中：

```python
from utils import setup_notification_manager

# 设置通知管理器
setup_notification_manager()
```

### 2. 创建Toast管理器

在主窗口中：

```python
from gui import ToastManager
from utils.notification import get_notification_manager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 创建Toast管理器
        self.toast_manager = ToastManager(self)
        
        # 连接通知信号
        notification_manager = get_notification_manager()
        notification_manager.notification_added.connect(self.on_notification_added)
    
    def on_notification_added(self, notification):
        """新通知添加时显示Toast"""
        self.toast_manager.show_toast(notification)
```

## Toast通知样式

Toast通知会根据类型自动应用不同的颜色：

- **信息（INFO）**：蓝色背景
- **成功（SUCCESS）**：绿色背景
- **警告（WARNING）**：黄色背景
- **错误（ERROR）**：红色背景

Toast通知特性：
- 显示在窗口右上角
- 支持多个通知堆叠显示
- 淡入淡出动画
- 点击关闭按钮或通知本身可关闭
- 自动关闭（可配置）

## 通知管理器API

### NotificationManager

#### 方法

- `show(title, message, type, duration, action)` - 显示通知
- `info(title, message, duration, action)` - 显示信息通知
- `success(title, message, duration, action)` - 显示成功通知
- `warning(title, message, duration, action)` - 显示警告通知
- `error(title, message, duration, action)` - 显示错误通知
- `remove(notification_id)` - 移除通知
- `clear()` - 清除所有通知
- `mark_as_read(notification_id)` - 标记为已读
- `mark_all_as_read()` - 标记所有为已读
- `get_all()` - 获取所有通知
- `get_unread()` - 获取未读通知
- `get_unread_count()` - 获取未读数量

#### 信号

- `notification_added` - 新通知添加时触发
- `notification_removed` - 通知移除时触发
- `notification_cleared` - 所有通知清除时触发

## 示例

### 测试通知

在欢迎页面点击"测试通知"按钮，会依次显示四种类型的通知：

```python
def test_notifications(self):
    notification_manager = get_notification_manager()
    
    notification_manager.info("信息通知", "这是一条信息通知")
    notification_manager.success("成功通知", "操作已成功完成")
    notification_manager.warning("警告通知", "请注意这个警告")
    notification_manager.error("错误通知", "发生了一个错误")
```

### 带回调的通知

```python
def open_settings():
    # 打开设置页面
    pass

notification_manager.info(
    "设置已更新",
    "点击查看详情",
    action=open_settings
)
```

## 最佳实践

1. **选择合适的类型**：根据消息的重要性选择合适的通知类型
2. **简洁的标题**：标题应简短明了
3. **清晰的消息**：消息内容应清晰易懂
4. **合理的时长**：重要消息可以设置较长的显示时间
5. **避免过多通知**：不要在短时间内显示过多通知

## 故障排除

### 问题：通知不显示

**可能原因**：
1. 通知管理器未初始化
2. Toast管理器未创建
3. 信号未连接

**解决方案**：
1. 确保调用了 `setup_notification_manager()`
2. 确保在主窗口中创建了 `ToastManager`
3. 确保连接了 `notification_added` 信号

### 问题：通知位置不正确

**可能原因**：
1. 父窗口大小改变
2. Toast管理器未正确初始化

**解决方案**：
1. Toast会自动根据父窗口大小调整位置
2. 确保传递正确的父窗口给 `ToastManager`

## 相关文档

- [异常处理文档](EXCEPTION_HANDLING.md)
- [主题系统文档](THEME_SYSTEM.md)
- [设置管理文档](SETTINGS_MANAGEMENT.md)

