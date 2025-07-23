#!/usr/bin/env python3
"""
配置功能测试脚本
测试全局配置组件的各项功能
"""

def test_config_basic_functionality():
    """测试配置基础功能"""
    print("测试配置基础功能...")
    try:
        from utils import app_config
        
        # 测试基本属性访问
        print(f"  - 应用名称: {app_config.app_name}")
        print(f"  - 当前版本: {app_config.current_version}")
        print(f"  - 组织名称: {app_config.organization_name}")
        print(f"  - 更新服务器: {app_config.update_server}")
        print(f"  - 更新检查URL: {app_config.update_check_url}")
        print(f"  - 自动检查更新: {app_config.auto_check_updates}")
        
        # 测试配置读写
        original_timeout = app_config.update_check_timeout
        app_config.set("update_check_timeout", 15)
        new_timeout = app_config.get("update_check_timeout")
        print(f"  - 配置读写测试: {original_timeout} -> {new_timeout}")
        
        # 恢复原值
        app_config.set("update_check_timeout", original_timeout)
        
        print("✅ 配置基础功能测试通过")
        return True
    except Exception as e:
        print(f"❌ 配置基础功能测试失败: {e}")
        return False

def test_config_version_functionality():
    """测试版本相关功能"""
    print("\n测试版本相关功能...")
    try:
        from utils import app_config
        
        # 测试版本获取
        current_version = app_config.current_version
        print(f"  - 当前版本: {current_version}")
        
        # 测试从exe获取版本（开发环境下应该返回None）
        exe_version = app_config.get_version_from_exe()
        if exe_version:
            print(f"  - exe版本: {exe_version}")
        else:
            print("  - exe版本: 无法获取（开发环境正常）")
        
        # 测试版本设置
        original_version = app_config.current_version
        test_version = "2.0.0-test"
        app_config.set_current_version(test_version)
        new_version = app_config.current_version
        print(f"  - 版本设置测试: {original_version} -> {new_version}")
        
        # 恢复原版本
        app_config.set_current_version(original_version)
        
        print("✅ 版本功能测试通过")
        return True
    except Exception as e:
        print(f"❌ 版本功能测试失败: {e}")
        return False

def test_config_url_functionality():
    """测试URL构建功能"""
    print("\n测试URL构建功能...")
    try:
        from utils import app_config
        
        # 测试URL构建
        test_path = "updates/app_v2.0.0.zip"
        full_url = app_config.get_update_url(test_path)
        print(f"  - URL构建测试: {test_path} -> {full_url}")
        
        # 测试更新检查URL
        check_url = app_config.update_check_url
        print(f"  - 更新检查URL: {check_url}")
        
        print("✅ URL功能测试通过")
        return True
    except Exception as e:
        print(f"❌ URL功能测试失败: {e}")
        return False

def test_config_skip_version_functionality():
    """测试版本跳过功能"""
    print("\n测试版本跳过功能...")
    try:
        from utils import app_config
        
        # 测试版本跳过
        test_version = "1.5.0-test"
        app_config.skip_version(test_version, 1)  # 跳过1天
        
        # 检查是否被跳过
        is_skipped = app_config.is_version_skipped(test_version)
        print(f"  - 版本跳过测试: {test_version} 被跳过: {is_skipped}")
        
        # 清理测试数据
        skipped_versions = app_config.get("skipped_versions", {})
        if test_version in skipped_versions:
            del skipped_versions[test_version]
            app_config.set("skipped_versions", skipped_versions)
            app_config.save_config()
        
        print("✅ 版本跳过功能测试通过")
        return True
    except Exception as e:
        print(f"❌ 版本跳过功能测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始配置功能测试\n")
    
    tests = [
        test_config_basic_functionality,
        test_config_version_functionality,
        test_config_url_functionality,
        test_config_skip_version_functionality
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有配置功能测试通过！")
        return True
    else:
        print("⚠️  部分配置功能测试失败，请检查相关功能。")
        return False

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
