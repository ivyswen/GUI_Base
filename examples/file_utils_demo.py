"""
文件操作工具集演示
展示 utils.file_utils 模块的各种功能
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import file_utils


def demo_basic_operations():
    """演示基本文件操作"""
    print("=" * 60)
    print("基本文件操作演示")
    print("=" * 60)
    
    # 创建测试目录
    test_dir = "test_files"
    print(f"\n1. 创建目录: {test_dir}")
    file_utils.ensure_dir(test_dir)
    print(f"   目录是否存在: {file_utils.dir_exists(test_dir)}")
    
    # 创建测试文件
    test_file = os.path.join(test_dir, "test.txt")
    print(f"\n2. 创建文件: {test_file}")
    content = "这是一个测试文件\n包含多行文本\n用于演示文件操作"
    file_utils.write_text_file(test_file, content)
    print(f"   文件是否存在: {file_utils.file_exists(test_file)}")
    
    # 读取文件
    print(f"\n3. 读取文件: {test_file}")
    read_content = file_utils.read_text_file(test_file)
    print(f"   文件内容:\n{read_content}")
    
    # 获取文件信息
    print(f"\n4. 文件信息:")
    size = file_utils.get_file_size(test_file)
    print(f"   文件大小: {size} 字节 ({file_utils.format_file_size(size)})")
    print(f"   文件名: {file_utils.get_file_name(test_file)}")
    print(f"   文件名（无扩展名）: {file_utils.get_file_name(test_file, with_extension=False)}")
    print(f"   文件扩展名: {file_utils.get_file_extension(test_file)}")
    
    # 计算哈希
    print(f"\n5. 计算文件哈希:")
    md5_hash = file_utils.calculate_file_hash(test_file, 'md5')
    sha256_hash = file_utils.calculate_file_hash(test_file, 'sha256')
    print(f"   MD5: {md5_hash}")
    print(f"   SHA256: {sha256_hash}")


def demo_file_operations():
    """演示文件复制、移动、删除"""
    print("\n" + "=" * 60)
    print("文件复制、移动、删除演示")
    print("=" * 60)
    
    test_dir = "test_files"
    src_file = os.path.join(test_dir, "test.txt")
    
    # 复制文件
    copy_file = os.path.join(test_dir, "test_copy.txt")
    print(f"\n1. 复制文件: {src_file} -> {copy_file}")
    file_utils.copy_file(src_file, copy_file)
    print(f"   复制成功: {file_utils.file_exists(copy_file)}")
    
    # 移动文件
    move_file = os.path.join(test_dir, "test_moved.txt")
    print(f"\n2. 移动文件: {copy_file} -> {move_file}")
    file_utils.move_file(copy_file, move_file)
    print(f"   移动成功: {file_utils.file_exists(move_file)}")
    print(f"   原文件已删除: {not file_utils.file_exists(copy_file)}")
    
    # 删除文件
    print(f"\n3. 删除文件: {move_file}")
    file_utils.delete_file(move_file)
    print(f"   删除成功: {not file_utils.file_exists(move_file)}")


def demo_directory_operations():
    """演示目录操作"""
    print("\n" + "=" * 60)
    print("目录操作演示")
    print("=" * 60)
    
    test_dir = "test_files"
    
    # 创建多个文件
    print(f"\n1. 创建多个测试文件")
    for i in range(5):
        file_path = os.path.join(test_dir, f"file_{i}.txt")
        file_utils.write_text_file(file_path, f"这是文件 {i}")
    
    # 创建子目录和文件
    sub_dir = os.path.join(test_dir, "subdir")
    file_utils.ensure_dir(sub_dir)
    for i in range(3):
        file_path = os.path.join(sub_dir, f"subfile_{i}.txt")
        file_utils.write_text_file(file_path, f"这是子目录文件 {i}")
    
    # 列出文件
    print(f"\n2. 列出目录中的文件:")
    files = file_utils.list_files(test_dir)
    for f in files:
        print(f"   - {f}")
    
    print(f"\n3. 递归列出所有文件:")
    all_files = file_utils.list_files(test_dir, recursive=True)
    for f in all_files:
        print(f"   - {f}")
    
    print(f"\n4. 列出 .txt 文件:")
    txt_files = file_utils.list_files(test_dir, pattern="*.txt", recursive=True)
    for f in txt_files:
        print(f"   - {f}")
    
    print(f"\n5. 列出子目录:")
    dirs = file_utils.list_directories(test_dir)
    for d in dirs:
        print(f"   - {d}")


def cleanup():
    """清理测试文件"""
    print("\n" + "=" * 60)
    print("清理测试文件")
    print("=" * 60)
    
    test_dir = "test_files"
    print(f"\n删除测试目录: {test_dir}")
    file_utils.delete_directory(test_dir, recursive=True)
    print(f"清理完成: {not file_utils.dir_exists(test_dir)}")


def main():
    """主函数"""
    print("\n文件操作工具集演示")
    print("=" * 60)
    
    try:
        demo_basic_operations()
        demo_file_operations()
        demo_directory_operations()
    finally:
        cleanup()
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()

