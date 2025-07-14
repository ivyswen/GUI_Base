#!/usr/bin/env python3
"""
PySide6-Fluent-Widgets 构建示例

这个文件展示了如何使用build_fluent_nuitka.py脚本来构建Fluent Design版本的可执行文件。

使用方法:
1. 直接运行默认配置: python build_fluent_example.py
2. 查看不同的配置示例
3. 根据需要修改配置并构建

作者: @心福口福
日期: 2025
"""

from fluent_style.build_fluent_nuitka import update_build_config, build_executable, BUILD_CONFIG

def example_default_build():
    """示例1: 使用默认配置构建"""
    print("📋 示例1: 使用默认配置构建")
    print("=" * 40)
    
    # 显示当前配置
    print("当前配置:")
    for key, value in BUILD_CONFIG.items():
        print(f"  {key}: {value}")
    
    print("\n开始构建...")
    build_executable()

def example_custom_build():
    """示例2: 自定义配置构建"""
    print("📋 示例2: 自定义配置构建")
    print("=" * 40)
    
    # 更新配置
    update_build_config(
        company_name="我的公司",
        product_name="my-fluent-app",
        file_version="2.0.0",
        product_version="2.0.0",
        file_description="我的Fluent Design应用程序",
        copyright="Copyright 2025 我的公司",
        executable_name="my-fluent-app"
    )
    
    print("\n开始构建...")
    build_executable()

def example_enterprise_build():
    """示例3: 企业版配置构建"""
    print("📋 示例3: 企业版配置构建")
    print("=" * 40)
    
    # 企业版配置
    update_build_config(
        company_name="Enterprise Solutions Ltd.",
        product_name="enterprise-fluent-suite",
        file_version="3.1.0",
        product_version="3.1.0",
        file_description="Enterprise Fluent Design Suite - Professional Edition",
        copyright="Copyright 2025 Enterprise Solutions Ltd. All rights reserved.",
        executable_name="enterprise-fluent-suite"
    )
    
    print("\n开始构建...")
    build_executable()

def show_build_options():
    """显示所有构建选项"""
    print("🛠️  可用的构建选项:")
    print("=" * 50)
    print("1. 默认构建 - 使用预设配置")
    print("2. 自定义构建 - 个人/小团队使用")
    print("3. 企业构建 - 企业级应用")
    print("4. 仅检查依赖 - 不进行实际构建")
    print("5. 显示当前配置")
    print("0. 退出")
    print()

def check_dependencies_only():
    """仅检查依赖"""
    from fluent_style.build_fluent_nuitka import check_dependencies
    print("🔍 检查构建依赖...")
    print("=" * 30)
    check_dependencies()
    print("\n✅ 依赖检查完成！")

def show_current_config():
    """显示当前配置"""
    print("📋 当前构建配置:")
    print("=" * 30)
    for key, value in BUILD_CONFIG.items():
        print(f"  {key}: {value}")
    print()

def interactive_build():
    """交互式构建"""
    while True:
        show_build_options()
        
        try:
            choice = input("请选择构建选项 (0-5): ").strip()
            
            if choice == "0":
                print("👋 再见！")
                break
            elif choice == "1":
                example_default_build()
                break
            elif choice == "2":
                example_custom_build()
                break
            elif choice == "3":
                example_enterprise_build()
                break
            elif choice == "4":
                check_dependencies_only()
            elif choice == "5":
                show_current_config()
            else:
                print("❌ 无效选择，请输入 0-5 之间的数字")
                
        except KeyboardInterrupt:
            print("\n\n👋 用户取消操作，再见！")
            break
        except Exception as e:
            print(f"❌ 发生错误: {e}")

def main():
    """主函数"""
    print("🎨 PySide6-Fluent-Widgets 构建示例")
    print("=" * 50)
    print("这个脚本展示了如何构建Fluent Design版本的可执行文件")
    print()
    
    # 检查是否有命令行参数
    import sys
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        
        if arg == "default":
            example_default_build()
        elif arg == "custom":
            example_custom_build()
        elif arg == "enterprise":
            example_enterprise_build()
        elif arg == "check":
            check_dependencies_only()
        elif arg == "config":
            show_current_config()
        else:
            print(f"❌ 未知参数: {arg}")
            print("可用参数: default, custom, enterprise, check, config")
    else:
        # 交互式模式
        interactive_build()

if __name__ == "__main__":
    main()
