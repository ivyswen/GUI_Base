#!/usr/bin/env python3
"""
构建脚本使用示例

这个文件展示了如何使用灵活的build_nuitka.py脚本来构建不同的应用程序。
"""

from build_nuitka import update_build_config, build_executable

def build_my_app():
    """构建自定义应用程序示例"""
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
    
    # 执行构建
    build_executable()

def build_demo_app():
    """构建演示应用程序示例"""
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
    
    # 执行构建
    build_executable()

def build_production_app():
    """构建生产环境应用程序示例"""
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
    
    # 执行构建
    build_executable()

if __name__ == "__main__":
    print("🚀 构建脚本使用示例")
    print("请选择要构建的应用程序类型：")
    print("1. 自定义应用程序")
    print("2. 演示应用程序")
    print("3. 生产环境应用程序")
    print("4. 使用默认配置构建")
    
    choice = input("\n请输入选择 (1-4): ").strip()
    
    if choice == "1":
        build_my_app()
    elif choice == "2":
        build_demo_app()
    elif choice == "3":
        build_production_app()
    elif choice == "4":
        print("🎯 使用默认配置构建")
        build_executable()
    else:
        print("❌ 无效选择，使用默认配置构建")
        build_executable()
