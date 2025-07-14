#!/usr/bin/env python3
"""
Nuitka构建脚本 - 灵活配置版本

这个脚本使用Nuitka将Python GUI应用程序打包为独立的可执行文件。
所有的产品信息（名称、版本、描述等）都可以通过BUILD_CONFIG字典进行配置。

使用方法:
1. 直接运行: python build_nuitka.py
2. 自定义配置后运行:
   - 修改BUILD_CONFIG字典中的值
   - 或者调用update_build_config()函数

配置项说明:
- company_name: 公司名称
- product_name: 产品名称（也用作可执行文件名）
- file_version: 文件版本号
- product_version: 产品版本号
- file_description: 文件描述
- copyright: 版权信息
- main_script: 主Python脚本文件名
- output_dir: 构建输出目录
- resources_dir: 资源文件目录
- executable_name: 最终可执行文件名
- data_dirs: 需要复制的额外目录列表（如果目录存在就复制）

作者: @心福口福
日期: 2025
"""

import os
import sys
import subprocess
import shutil

# 构建配置变量
BUILD_CONFIG = {
    "company_name": "@心福口福",
    "product_name": "gui-base",
    "file_version": "1.1.0",
    "product_version": "1.1.0",
    "file_description": "GUI Base Template - 基础GUI程序模板",
    "copyright": "Copyright 2025 @心福口福",
    "main_script": "main.py",
    "output_dir": "build",
    "resources_dir": "Resources",  # 注意这里改为大写R，匹配项目结构
    "executable_name": "gui-base",
    "data_dirs": [  # 需要复制的额外目录列表
        "docs",     # 文档目录
        "config",   # 配置目录
        "templates", # 模板目录
        "plugins",  # 插件目录
        # 可以添加更多目录
    ]
}

def add_data_dir(directory: str):
    """添加数据目录到构建配置

    Args:
        directory: 要添加的目录路径
    """
    if "data_dirs" not in BUILD_CONFIG:
        BUILD_CONFIG["data_dirs"] = []

    if directory not in BUILD_CONFIG["data_dirs"]:
        BUILD_CONFIG["data_dirs"].append(directory)
        print(f"✅ 添加数据目录: {directory}")
    else:
        print(f"⚠️  数据目录已存在: {directory}")

def remove_data_dir(directory: str):
    """从构建配置中移除数据目录

    Args:
        directory: 要移除的目录路径
    """
    if "data_dirs" in BUILD_CONFIG and directory in BUILD_CONFIG["data_dirs"]:
        BUILD_CONFIG["data_dirs"].remove(directory)
        print(f"✅ 移除数据目录: {directory}")
    else:
        print(f"⚠️  数据目录不存在: {directory}")

def list_data_dirs():
    """列出当前配置的数据目录"""
    data_dirs = BUILD_CONFIG.get("data_dirs", [])
    if data_dirs:
        print("📁 当前配置的数据目录:")
        for i, data_dir in enumerate(data_dirs, 1):
            exists = "✅" if os.path.exists(data_dir) else "❌"
            print(f"  {i}. {data_dir} {exists}")
    else:
        print("📁 未配置数据目录")

def update_build_config(**kwargs):
    """更新构建配置

    Args:
        **kwargs: 要更新的配置项，可用的键包括：
            - company_name: 公司名称
            - product_name: 产品名称
            - file_version: 文件版本
            - product_version: 产品版本
            - file_description: 文件描述
            - copyright: 版权信息
            - main_script: 主脚本文件名
            - output_dir: 输出目录
            - resources_dir: 资源目录
            - executable_name: 可执行文件名
            - data_dirs: 需要复制的额外目录列表

    Example:
        update_build_config(
            product_name="my-app",
            file_version="2.0.0",
            file_description="我的应用程序"
        )
    """
    for key, value in kwargs.items():
        if key in BUILD_CONFIG:
            BUILD_CONFIG[key] = value
            print(f"✅ 更新配置: {key} = {value}")
        else:
            print(f"⚠️  警告: 未知的配置项 '{key}'，已忽略")
            print(f"   可用的配置项: {', '.join(BUILD_CONFIG.keys())}")

def build_executable():
    """使用Nuitka构建可执行文件"""
    print("开始使用Nuitka构建可执行文件...")

    # 检查资源文件
    resources_dir = BUILD_CONFIG["resources_dir"]
    if not os.path.exists(resources_dir):
        print(f"错误: 资源目录 {resources_dir} 不存在")
        sys.exit(1)

    # 确保资源文件已编译
    print("编译资源文件...")
    try:
        if os.path.exists("resources.qrc"):
            subprocess.run(["pyside6-rcc", "resources.qrc", "-o", "resources_rc.py"], check=True)
            print("资源文件编译成功")
        else:
            print("警告: resources.qrc 不存在，跳过资源编译")
    except Exception as e:
        print(f"资源文件编译失败: {e}")
        print("继续构建，但可能缺少资源文件")

    # 创建输出目录
    output_dir = BUILD_CONFIG["output_dir"]
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 构建Nuitka命令
    cmd = [
        sys.executable, "-m", "nuitka",
        "--standalone",                # 创建独立的可执行文件
        "--enable-plugin=pyside6",     # 启用PySide6插件
        "--output-dir=" + output_dir,  # 输出目录
        f"--company-name={BUILD_CONFIG['company_name']}",        # 公司名称
        f"--product-name={BUILD_CONFIG['product_name']}",        # 产品名称
        f"--file-version={BUILD_CONFIG['file_version']}",        # 文件版本
        f"--product-version={BUILD_CONFIG['product_version']}", # 产品版本
        f"--file-description={BUILD_CONFIG['file_description']}", # 文件描述
        f"--copyright={BUILD_CONFIG['copyright']}",             # 版权信息
        BUILD_CONFIG["main_script"]                              # 主脚本
    ]

    # Windows特定选项
    if sys.platform == "win32":
        cmd.extend([
            "--windows-console-mode=disable",  # 禁用控制台窗口
        ])

        # 添加图标（如果存在）
        icon_path = os.path.join(resources_dir, "favicon.ico")
        if os.path.exists(icon_path):
            cmd.append(f"--windows-icon-from-ico={icon_path}")
            print(f"使用图标: {icon_path}")

    # 包含资源目录
    if os.path.exists(resources_dir):
        cmd.append(f"--include-data-dir={resources_dir}={resources_dir}")
        print(f"包含资源目录: {resources_dir}")

    # 包含额外的数据目录
    data_dirs = BUILD_CONFIG.get("data_dirs", [])
    if data_dirs:
        print("检查额外数据目录:")
        for data_dir in data_dirs:
            if os.path.exists(data_dir):
                cmd.append(f"--include-data-dir={data_dir}={data_dir}")
                print(f"  ✅ 包含目录: {data_dir}")
            else:
                print(f"  ⚠️  跳过不存在的目录: {data_dir}")

    # 包含配置文件（如果存在）
    if os.path.exists("config.json"):
        cmd.append("--include-data-file=config.json=config.json")
        print("包含配置文件: config.json")

    # 包含changelog（如果存在）
    if os.path.exists("CHANGELOG.md"):
        cmd.append("--include-data-file=CHANGELOG.md=CHANGELOG.md")
        print("包含CHANGELOG: CHANGELOG.md")

    # 执行构建
    print("执行Nuitka构建命令:")
    print(" ".join(cmd))
    print()

    try:
        subprocess.run(cmd, check=True)
        print("Nuitka构建成功！")
    except subprocess.CalledProcessError as e:
        print(f"Nuitka构建失败: {e}")
        sys.exit(1)

    # 重命名可执行文件
    main_script_name = os.path.splitext(BUILD_CONFIG["main_script"])[0]  # 去掉.py扩展名
    executable_name = BUILD_CONFIG["executable_name"]

    if sys.platform == "win32":
        exe_name = f"{main_script_name}.exe"
        new_exe_name = f"{executable_name}.exe"
    else:
        exe_name = main_script_name
        new_exe_name = executable_name

    exe_path = os.path.join(output_dir, f"{main_script_name}.dist", exe_name)
    new_exe_path = os.path.join(output_dir, f"{main_script_name}.dist", new_exe_name)

    if os.path.exists(exe_path):
        shutil.move(exe_path, new_exe_path)
        print(f"✅ 构建完成！可执行文件: {new_exe_path}")

        # 显示文件大小
        size = os.path.getsize(new_exe_path)
        size_mb = size / (1024 * 1024)
        print(f"📦 文件大小: {size_mb:.2f} MB")

    else:
        print(f"❌ 构建完成，但未找到可执行文件: {exe_path}")
        print(f"📁 请检查 {output_dir} 目录内容:")

        # 列出构建目录内容
        if os.path.exists(output_dir):
            for root, _, files in os.walk(output_dir):
                level = root.replace(output_dir, '').count(os.sep)
                indent = ' ' * 2 * level
                print(f"{indent}{os.path.basename(root)}/")
                subindent = ' ' * 2 * (level + 1)
                for file in files:
                    print(f"{subindent}{file}")

        sys.exit(1)

def example_custom_build():
    """示例：自定义构建配置"""
    print("📝 示例：自定义构建配置")

    # 自定义基本信息
    update_build_config(
        company_name="您的公司名称",
        product_name="your-app-name",
        file_version="1.0.0",
        product_version="1.0.0",
        file_description="您的应用程序描述",
        copyright="Copyright 2025 您的公司名称",
        executable_name="your-app"
    )

    # 添加自定义数据目录
    add_data_dir("custom_data")
    add_data_dir("user_configs")
    add_data_dir("themes")

    # 显示当前配置
    list_data_dirs()

    # 开始构建
    build_executable()

if __name__ == "__main__":
    # 示例：自定义构建配置
    # 取消注释下面的代码来使用自定义配置
    # example_custom_build()
    # return

    print("🚀 开始构建可执行文件...")
    print(f"📋 当前构建配置:")
    for key, value in BUILD_CONFIG.items():
        print(f"   {key}: {value}")
    print()

    # 显示数据目录配置
    list_data_dirs()
    print()

    build_executable()
