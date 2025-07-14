#!/usr/bin/env python3
"""
构建脚本使用示例

这个文件展示了如何使用灵活的build_nuitka.py脚本来构建不同的应用程序。
"""

from build_nuitka import update_build_config, build_executable, add_data_dir, remove_data_dir, list_data_dirs

def build_my_app():
    """构建自定义应用程序示例 - 包含自定义数据目录"""
    print("🎯 构建示例：自定义应用程序")

    # 更新构建配置
    update_build_config(
        company_name="我的公司",
        product_name="my-awesome-app",
        file_version="2.1.0",
        product_version="2.1.0",
        file_description="我的超棒应用程序 - 基于GUI Base Template",
        copyright="Copyright 2025 我的公司",
        executable_name="my-awesome-app"
    )

    # 添加自定义数据目录
    print("\n📁 配置数据目录:")
    add_data_dir("user_data")      # 用户数据目录
    add_data_dir("app_configs")    # 应用配置目录
    add_data_dir("custom_themes")  # 自定义主题目录

    # 显示当前数据目录配置
    print()
    list_data_dirs()
    print()

    # 执行构建
    build_executable()

def build_demo_app():
    """构建演示应用程序示例 - 包含演示数据"""
    print("🎯 构建示例：演示应用程序")

    # 更新构建配置
    update_build_config(
        company_name="Demo Corp",
        product_name="demo-gui",
        file_version="0.9.0",
        product_version="0.9.0-beta",
        file_description="GUI Demo Application - 演示程序",
        copyright="Copyright 2025 Demo Corp",
        executable_name="demo-gui"
    )

    # 添加演示相关的数据目录
    print("\n📁 配置演示数据目录:")
    add_data_dir("demo_data")      # 演示数据
    add_data_dir("sample_files")   # 示例文件
    add_data_dir("tutorials")      # 教程文件

    # 移除不需要的目录（如果存在）
    remove_data_dir("plugins")     # 演示版本不需要插件

    # 显示当前数据目录配置
    print()
    list_data_dirs()
    print()

    # 执行构建
    build_executable()

def build_production_app():
    """构建生产环境应用程序示例 - 完整功能版本"""
    print("🎯 构建示例：生产环境应用程序")

    # 更新构建配置
    update_build_config(
        company_name="Production Inc.",
        product_name="production-tool",
        file_version="3.0.1",
        product_version="3.0.1",
        file_description="Production Tool - 生产环境工具",
        copyright="Copyright 2025 Production Inc.",
        executable_name="production-tool"
    )

    # 添加生产环境需要的数据目录
    print("\n📁 配置生产环境数据目录:")
    add_data_dir("production_data")  # 生产数据
    add_data_dir("config_templates") # 配置模板
    add_data_dir("plugins")          # 插件目录
    add_data_dir("logs")             # 日志目录
    add_data_dir("backups")          # 备份目录

    # 显示当前数据目录配置
    print()
    list_data_dirs()
    print()

    # 执行构建
    build_executable()

def build_with_data_dirs_demo():
    """数据目录功能演示"""
    print("🎯 构建示例：数据目录功能演示")

    # 基本配置
    update_build_config(
        company_name="Data Demo Corp",
        product_name="data-dirs-demo",
        file_version="1.0.0",
        product_version="1.0.0",
        file_description="数据目录功能演示程序",
        copyright="Copyright 2025 Data Demo Corp",
        executable_name="data-dirs-demo"
    )

    print("\n📁 数据目录管理演示:")

    # 显示默认配置
    print("1. 默认数据目录配置:")
    list_data_dirs()

    # 添加新目录
    print("\n2. 添加自定义数据目录:")
    add_data_dir("custom_data")
    add_data_dir("user_profiles")
    add_data_dir("export_files")

    # 尝试添加重复目录
    print("\n3. 尝试添加重复目录:")
    add_data_dir("docs")  # 这个目录已经在默认配置中

    # 移除不需要的目录
    print("\n4. 移除不需要的目录:")
    remove_data_dir("templates")  # 移除模板目录

    # 显示最终配置
    print("\n5. 最终数据目录配置:")
    list_data_dirs()

    print("\n🚀 开始构建...")
    build_executable()

if __name__ == "__main__":
    print("🚀 构建脚本使用示例")
    print("请选择要构建的应用程序类型：")
    print("1. 自定义应用程序（包含自定义数据目录）")
    print("2. 演示应用程序（包含演示数据）")
    print("3. 生产环境应用程序（完整功能版本）")
    print("4. 数据目录功能演示")
    print("5. 使用默认配置构建")

    choice = input("\n请输入选择 (1-5): ").strip()

    if choice == "1":
        build_my_app()
    elif choice == "2":
        build_demo_app()
    elif choice == "3":
        build_production_app()
    elif choice == "4":
        build_with_data_dirs_demo()
    elif choice == "5":
        print("🎯 使用默认配置构建")
        build_executable()
    else:
        print("❌ 无效选择，使用默认配置构建")
        build_executable()
