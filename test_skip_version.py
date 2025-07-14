"""
测试跳过版本功能
"""

import time
from datetime import datetime
from updater.config import app_config


def test_skip_version_functionality():
    """测试跳过版本功能"""
    print("=== 测试跳过版本功能 ===")
    
    # 清除现有的跳过版本
    print("\n1. 清除现有跳过版本")
    app_config.clear_skipped_versions()
    print("✅ 已清除所有跳过版本")
    
    # 测试跳过版本
    print("\n2. 测试跳过版本")
    test_versions = ["2.0.0", "2.1.0", "3.0.0"]
    
    for version in test_versions:
        app_config.skip_version(version, duration_days=7)  # 跳过7天
        print(f"✅ 跳过版本: {version}")
    
    # 检查跳过状态
    print("\n3. 检查跳过状态")
    for version in test_versions:
        is_skipped = app_config.is_version_skipped(version)
        print(f"版本 {version} 是否被跳过: {is_skipped}")
    
    # 检查未跳过的版本
    print("\n4. 检查未跳过的版本")
    not_skipped_versions = ["1.0.0", "1.5.0", "4.0.0"]
    for version in not_skipped_versions:
        is_skipped = app_config.is_version_skipped(version)
        print(f"版本 {version} 是否被跳过: {is_skipped}")
    
    # 获取跳过版本详细信息
    print("\n5. 跳过版本详细信息")
    skipped_info = app_config.get_skipped_versions_info()
    for version, info in skipped_info.items():
        print(f"版本 {version}:")
        print(f"  过期时间: {info['expire_date']}")
        print(f"  剩余天数: {info['days_remaining']}")
        print(f"  是否过期: {info['is_expired']}")
    
    # 测试移除单个跳过版本
    print("\n6. 测试移除单个跳过版本")
    removed = app_config.remove_skipped_version("2.1.0")
    print(f"移除版本 2.1.0: {removed}")
    
    # 再次检查状态
    print("\n7. 移除后的状态检查")
    is_skipped = app_config.is_version_skipped("2.1.0")
    print(f"版本 2.1.0 是否被跳过: {is_skipped}")


def test_version_expiry():
    """测试版本过期功能"""
    print("\n=== 测试版本过期功能 ===")
    
    # 清除现有跳过版本
    app_config.clear_skipped_versions()
    
    # 跳过一个版本，设置很短的过期时间（用于测试）
    print("\n1. 跳过版本（短期过期测试）")
    
    # 手动设置一个即将过期的版本
    import time
    skipped = app_config.get("skipped_versions", {})
    skipped["test-version"] = time.time() + 2  # 2秒后过期
    app_config.set("skipped_versions", skipped)
    app_config.save_config()
    
    print("✅ 设置测试版本，2秒后过期")
    
    # 立即检查（应该被跳过）
    print("\n2. 立即检查跳过状态")
    is_skipped = app_config.is_version_skipped("test-version")
    print(f"版本 test-version 是否被跳过: {is_skipped}")
    
    # 等待过期
    print("\n3. 等待版本过期...")
    time.sleep(3)
    
    # 再次检查（应该不再被跳过）
    print("\n4. 过期后检查跳过状态")
    is_skipped = app_config.is_version_skipped("test-version")
    print(f"版本 test-version 是否被跳过: {is_skipped}")
    
    # 检查是否自动清理
    print("\n5. 检查自动清理")
    skipped_info = app_config.get_skipped_versions_info()
    if "test-version" in skipped_info:
        print("❌ 过期版本未被自动清理")
    else:
        print("✅ 过期版本已被自动清理")


def test_configuration_persistence():
    """测试配置持久化"""
    print("\n=== 测试配置持久化 ===")
    
    # 清除并添加测试数据
    app_config.clear_skipped_versions()
    app_config.skip_version("persist-test-1.0.0", duration_days=30)
    app_config.skip_version("persist-test-2.0.0", duration_days=60)
    
    print("✅ 添加测试跳过版本")
    
    # 重新加载配置
    app_config.load_config()
    
    # 检查数据是否持久化
    print("\n检查配置持久化:")
    is_skipped_1 = app_config.is_version_skipped("persist-test-1.0.0")
    is_skipped_2 = app_config.is_version_skipped("persist-test-2.0.0")
    
    print(f"版本 persist-test-1.0.0 是否被跳过: {is_skipped_1}")
    print(f"版本 persist-test-2.0.0 是否被跳过: {is_skipped_2}")
    
    if is_skipped_1 and is_skipped_2:
        print("✅ 配置持久化测试通过")
    else:
        print("❌ 配置持久化测试失败")


def main():
    """主测试函数"""
    print("跳过版本功能测试开始")
    print("=" * 50)
    
    try:
        # 运行各项测试
        test_skip_version_functionality()
        test_version_expiry()
        test_configuration_persistence()
        
        print("\n" + "=" * 50)
        print("✅ 所有测试完成！")
        
        # 清理测试数据
        print("\n🧹 清理测试数据...")
        app_config.clear_skipped_versions()
        print("✅ 测试数据已清理")
        
    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
