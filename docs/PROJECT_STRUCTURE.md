# 项目结构说明

## 📁 目录结构

```
GUI_Base/
├── 📄 main.py                      # 主程序文件
├── 📄 demo.py                      # 演示程序
├── 📄 config.json                  # 应用程序配置文件
├── 📄 test_update.py              # 自动更新功能测试脚本
├── 📁 updater/                    # 🔄 自动更新模块
│   ├── 📄 __init__.py             # 模块初始化文件
│   ├── 📄 config.py               # 配置管理模块
│   ├── 📄 update_manager.py       # 更新管理器
│   ├── 📄 update_checker.py       # 更新检查模块
│   ├── 📄 update_dialogs.py       # 更新界面模块
│   └── 📄 file_manager.py         # 文件管理模块
├── 📁 docs/                       # 📚 文档目录
│   └── 📄 AUTO_UPDATE_GUIDE.md    # 自动更新使用指南
├── 📁 examples/                   # 📋 示例文件目录
│   ├── 📄 example_update.json     # 示例远程版本信息
│   └── 📄 update_example.py       # 示例更新程序
├── 📁 fluent_style_demo/          # 🎨 Fluent Design 风格演示
│   ├── 📄 main_fluent.py          # Fluent 风格主程序
│   ├── 📄 fluent_migration_guide.md # 迁移指南
│   ├── 📄 fluent_style_comparison.py # 样式对比演示
│   ├── 📄 build_fluent_example.py # Fluent 版本构建示例
│   └── 📄 build_fluent_nuitka.py  # Fluent 版本专用构建脚本
├── 📁 Resources/                  # 🖼️ 资源文件目录
│   ├── 📄 favicon.ico             # 应用程序图标
│   └── 📄 icon-192.png            # 备用图标文件
├── 📄 button_style_demo.py        # 按钮样式演示程序
├── 📄 build_nuitka.py             # Nuitka构建脚本
├── 📄 build_example.py            # 构建脚本使用示例
├── 📄 resources.qrc               # Qt资源文件
├── 📄 resources_rc.py             # Qt资源编译文件
├── 📄 pyproject.toml              # 项目配置文件
├── 📄 uv.lock                     # 依赖锁定文件
├── 📄 README.md                   # 项目说明文档
└── 📄 PROJECT_STRUCTURE.md        # 项目结构说明（本文件）
```

## 🔧 核心文件说明

### 主程序文件
- **main.py**: 主程序入口，包含完整的GUI界面和自动更新功能
- **demo.py**: 演示程序，展示基本功能和自动更新功能的使用
- **config.json**: 应用程序配置文件，包含版本信息、更新服务器地址等

### 🔄 自动更新模块 (updater/)
- **__init__.py**: 模块初始化，导出主要类和函数
- **config.py**: 配置管理，处理配置文件读写和默认值
- **update_manager.py**: 更新管理器，统一管理整个更新流程
- **update_checker.py**: 更新检查，处理版本比较和远程版本获取
- **update_dialogs.py**: 更新界面，包含更新提示和下载进度对话框
- **file_manager.py**: 文件管理，处理文件下载、校验和临时文件管理

### 📚 文档和示例
- **docs/AUTO_UPDATE_GUIDE.md**: 详细的自动更新功能使用指南
- **examples/example_update.json**: 远程版本信息JSON格式示例
- **examples/update_example.py**: 更新程序实现示例
- **test_update.py**: 功能测试脚本，验证各模块是否正常工作

### 🎨 界面和样式
- **button_style_demo.py**: 按钮样式演示程序
- **fluent_style_demo/**: Fluent Design风格的现代化界面演示

### 🔨 构建和部署
- **build_nuitka.py**: 使用Nuitka进行应用程序打包
- **build_example.py**: 构建脚本使用示例
- **pyproject.toml**: 项目依赖和配置管理

## 🚀 快速开始

### 运行主程序
```bash
uv run python main.py
```

### 运行演示程序
```bash
uv run python demo.py
```

### 测试自动更新功能
```bash
uv run python test_update.py
```

### 查看按钮样式演示
```bash
uv run python button_style_demo.py
```

## 📦 模块依赖关系

```
main.py
├── updater.UpdateManager
├── updater.app_config
└── PySide6 (GUI框架)

updater/
├── config.py (配置管理)
├── update_manager.py
│   ├── update_checker.py
│   ├── update_dialogs.py
│   ├── file_manager.py
│   └── config.py
├── update_checker.py
│   ├── config.py
│   └── packaging (版本比较)
├── update_dialogs.py
│   ├── update_checker.py
│   ├── file_manager.py
│   └── config.py
└── file_manager.py
    └── config.py
```

## 🔧 自定义和扩展

### 添加新功能
1. 在相应模块中添加新的类或方法
2. 更新 `updater/__init__.py` 导出新的接口
3. 在主程序中导入和使用新功能

### 修改配置
1. 编辑 `config.json` 文件
2. 或在代码中使用 `app_config.set()` 方法

### 自定义界面
1. 修改 `main.py` 中的界面布局
2. 调整 `update_dialogs.py` 中的对话框样式
3. 使用 `get_button_style()` 方法保持样式一致性

## 📋 开发规范

### 代码组织
- 每个模块职责单一，功能明确
- 使用相对导入 (from .module import ...)
- 保持接口简洁，隐藏实现细节

### 错误处理
- 所有网络请求都有超时和错误处理
- 文件操作包含异常捕获
- 用户界面提供友好的错误提示

### 测试
- 每个模块都有对应的测试用例
- 使用 `test_update.py` 进行集成测试
- 确保所有功能在不同环境下正常工作

## 🔄 版本管理

### 版本号格式
使用语义化版本号：`主版本.次版本.修订版本`
- 主版本：不兼容的API修改
- 次版本：向下兼容的功能性新增
- 修订版本：向下兼容的问题修正

### 更新流程
1. 修改 `config.json` 中的版本号
2. 更新 `examples/example_update.json` 中的版本信息
3. 准备更新包和更新程序
4. 部署到更新服务器
5. 测试自动更新功能

---

**注意**: 这个项目结构设计考虑了模块化、可维护性和可扩展性，适合作为GUI应用程序开发的起始模板。
