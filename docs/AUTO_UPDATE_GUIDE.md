# 自动更新功能使用指南

## 概述

本指南详细介绍了 GUI Base Template 中新增的自动更新功能的使用方法、配置选项和部署说明。

## 功能特性

### ✅ 已实现的功能
- **版本检查**: 自动比较本地版本与远程版本
- **更新提示**: 美观的更新对话框，显示版本信息和更新日志
- **文件下载**: 支持进度显示的文件下载功能
- **安全校验**: SHA256 文件完整性验证
- **自动安装**: 启动外部更新程序完成安装
- **配置管理**: 灵活的配置文件系统
- **错误处理**: 完善的错误处理和用户提示

### 🔧 核心组件

1. **config.py**: 配置管理模块
   - 管理应用程序配置信息
   - 支持配置文件读写
   - 提供默认配置

2. **update_checker.py**: 更新检查模块
   - 异步检查远程版本信息
   - 版本号比较逻辑
   - 网络请求处理

3. **update_dialogs.py**: 更新界面模块
   - 更新提示对话框
   - 下载进度对话框
   - 统一的按钮样式

4. **file_manager.py**: 文件管理模块
   - 文件下载功能
   - SHA256 校验
   - 临时文件管理

5. **update_manager.py**: 更新管理器
   - 统一管理更新流程
   - 协调各个模块
   - 处理用户交互

## 配置说明

### config.json 配置文件

```json
{
    "app_name": "GUI Base Template",           // 应用程序名称
    "current_version": "1.0.0",               // 当前版本号
    "organization_name": "Your Organization",  // 组织名称
    "update_server": "https://your-server.com", // 更新服务器地址
    "update_check_url": "https://your-server.com/update.json", // 版本检查URL
    "auto_check_updates": true,               // 是否自动检查更新
    "update_check_timeout": 10,               // 检查更新超时时间（秒）
    "download_timeout": 300,                  // 下载超时时间（秒）
    "temp_dir_name": "app_update"             // 临时目录名称
}
```

### 远程版本信息格式

服务器端需要提供以下格式的 JSON 文件：

```json
{
    "version": "2.0.0",                       // 新版本号
    "changelog": "1. 新增自动更新功能\n2. 优化性能\n3. 修复已知问题", // 更新日志
    "url": "https://your-server.com/updates/app_v2.0.0.zip",        // 更新包下载链接
    "update_exe_url": "https://your-server.com/updates/update_v1.0.exe", // 更新程序下载链接
    "sha256": {
        "package": "a1b2c3d4e5f6...",         // 更新包SHA256值
        "update_exe": "e5f6g7h8i9j0..."       // 更新程序SHA256值
    }
}
```

## 使用方法

### 1. 手动检查更新

通过菜单栏操作：
1. 点击菜单栏中的 "帮助"
2. 选择 "检查更新"
3. 系统将检查是否有新版本可用

### 2. 自动检查更新

程序启动时会自动检查更新（可在配置中关闭）：
- 启动后延迟 3 秒开始检查
- 静默检查，不影响程序启动速度
- 发现更新时显示提示对话框

### 3. 更新流程

1. **检查阶段**: 
   - 从远程服务器获取版本信息
   - 比较版本号确定是否需要更新

2. **提示阶段**:
   - 显示更新对话框
   - 展示新版本信息和更新日志
   - 用户可选择立即更新、稍后提醒或跳过此版本

3. **下载阶段**:
   - 显示下载进度对话框
   - 实时显示下载进度和速度
   - 支持取消下载

4. **校验阶段**:
   - 使用 SHA256 验证文件完整性
   - 确保下载文件未被篡改

5. **安装阶段**:
   - 启动外部更新程序
   - 自动关闭当前应用程序
   - 更新程序完成文件替换后重启应用

## 部署指南

### 1. 服务器端配置

#### 1.1 准备更新文件
- 创建更新包（ZIP 格式）
- 准备更新程序（可执行文件）
- 计算文件的 SHA256 值

#### 1.2 创建版本信息文件
创建 `update.json` 文件，包含版本信息：

```bash
# 计算 SHA256 值
sha256sum app_v2.0.0.zip
sha256sum update_v1.0.exe
```

#### 1.3 部署到服务器
- 将更新包和更新程序上传到服务器
- 确保 `update.json` 文件可通过 HTTP 访问
- 配置正确的 CORS 头（如果需要）

### 2. 客户端配置

#### 2.1 修改配置文件
更新 `config.json` 中的服务器地址：

```json
{
    "update_check_url": "https://your-actual-server.com/update.json",
    "update_server": "https://your-actual-server.com"
}
```

#### 2.2 测试更新功能
1. 确保网络连接正常
2. 手动触发更新检查
3. 验证下载和安装流程

## 开发指南

### 1. 自定义更新逻辑

#### 1.1 扩展版本比较
修改 `update_checker.py` 中的版本比较逻辑：

```python
def _is_newer_version(self, remote_version: str, current_version: str) -> bool:
    """自定义版本比较逻辑"""
    # 添加您的版本比较逻辑
    pass
```

#### 1.2 自定义更新界面
修改 `update_dialogs.py` 中的对话框样式：

```python
class UpdateDialog(QDialog):
    def init_ui(self):
        # 自定义界面布局和样式
        pass
```

### 2. 更新程序参数格式

系统使用以下参数格式启动更新程序：

```bash
update.exe --target-dir "C:\MyApp" --update-package "d:\update_v2.0.zip" --app-exe "My.exe"
```

**参数说明**：
- `--target-dir`: 应用程序安装目录
- `--update-package`: 更新包文件路径
- `--app-exe`: 应用程序可执行文件名（不包含路径）

### 3. 添加新功能

#### 3.1 增量更新
- 实现差分更新算法
- 减少下载包大小
- 提高更新速度

#### 3.2 回滚功能
- 备份当前版本
- 支持版本回滚
- 错误恢复机制

#### 3.3 更新通知
- 邮件通知
- 系统托盘提醒
- 定时检查

## 故障排除

### 常见问题

1. **网络连接失败**
   - 检查网络连接
   - 验证服务器地址
   - 检查防火墙设置

2. **文件校验失败**
   - 重新计算 SHA256 值
   - 检查文件是否损坏
   - 验证服务器文件完整性

3. **更新程序启动失败**
   - 检查更新程序权限
   - 验证文件路径
   - 查看系统日志

### 调试方法

1. **启用详细日志**
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

2. **检查配置文件**
   ```python
   from config import app_config
   print(app_config._config)
   ```

3. **测试网络连接**
   ```python
   import urllib.request
   response = urllib.request.urlopen(app_config.update_check_url)
   print(response.read())
   ```

## 安全考虑

### 1. 文件完整性
- 使用 SHA256 校验确保文件完整性
- 验证下载文件未被篡改

### 2. 网络安全
- 使用 HTTPS 连接
- 验证服务器证书
- 防止中间人攻击

### 3. 权限控制
- 最小权限原则
- 安全的文件路径
- 防止路径遍历攻击

## 最佳实践

1. **版本管理**
   - 使用语义化版本号
   - 维护版本历史记录
   - 提供详细的更新日志

2. **用户体验**
   - 非阻塞的更新检查
   - 清晰的进度指示
   - 友好的错误提示

3. **性能优化**
   - 异步网络请求
   - 增量更新支持
   - 智能重试机制

4. **测试策略**
   - 自动化测试
   - 多环境验证
   - 回归测试

---

**注意**: 这是一个基础的自动更新实现，实际生产环境中可能需要根据具体需求进行调整和优化。
