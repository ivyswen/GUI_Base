"""
示例更新程序
这是一个简单的更新程序示例，用于演示自动更新功能
实际项目中需要根据具体需求实现更复杂的更新逻辑
"""

import sys
import os
import zipfile
import shutil
import time
import argparse
from pathlib import Path


def extract_update_package(package_path: str, target_dir: str) -> bool:
    """
    解压更新包
    
    Args:
        package_path: 更新包路径
        target_dir: 目标目录
        
    Returns:
        是否成功
    """
    try:
        with zipfile.ZipFile(package_path, 'r') as zip_ref:
            zip_ref.extractall(target_dir)
        return True
    except Exception as e:
        print(f"解压更新包失败: {e}")
        return False


def backup_current_version(target_dir: str) -> bool:
    """
    备份当前版本
    
    Args:
        target_dir: 目标目录
        
    Returns:
        是否成功
    """
    try:
        backup_dir = Path(target_dir).parent / "backup"
        backup_dir.mkdir(exist_ok=True)
        
        # 备份主要文件
        for file_path in Path(target_dir).iterdir():
            if file_path.is_file() and file_path.suffix in ['.exe', '.py']:
                shutil.copy2(file_path, backup_dir / file_path.name)
        
        return True
    except Exception as e:
        print(f"备份当前版本失败: {e}")
        return False


def apply_update(package_path: str, target_dir: str) -> bool:
    """
    应用更新
    
    Args:
        package_path: 更新包路径
        target_dir: 目标目录
        
    Returns:
        是否成功
    """
    try:
        # 创建临时目录
        temp_dir = Path(target_dir).parent / "temp_update"
        temp_dir.mkdir(exist_ok=True)
        
        # 解压更新包到临时目录
        if not extract_update_package(package_path, str(temp_dir)):
            return False
        
        # 备份当前版本
        if not backup_current_version(target_dir):
            print("警告: 备份失败，继续更新")
        
        # 复制新文件到目标目录
        for file_path in temp_dir.rglob('*'):
            if file_path.is_file():
                relative_path = file_path.relative_to(temp_dir)
                target_file = Path(target_dir) / relative_path
                
                # 创建目标目录
                target_file.parent.mkdir(parents=True, exist_ok=True)
                
                # 复制文件
                shutil.copy2(file_path, target_file)
        
        # 清理临时目录
        shutil.rmtree(temp_dir, ignore_errors=True)
        
        return True
        
    except Exception as e:
        print(f"应用更新失败: {e}")
        return False


def restart_application(app_path: str) -> None:
    """
    重启应用程序
    
    Args:
        app_path: 应用程序路径
    """
    try:
        # 等待一段时间确保原程序完全退出
        time.sleep(2)
        
        # 启动新版本
        if app_path.endswith('.exe'):
            os.startfile(app_path)
        else:
            # Python脚本
            os.system(f'start "" "{app_path}"')
            
    except Exception as e:
        print(f"重启应用程序失败: {e}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='应用程序更新工具')
    parser.add_argument('--target-dir', required=True, help='目标目录')
    parser.add_argument('--update-package', required=True, help='更新包路径')
    parser.add_argument('--app-exe', required=True, help='应用程序可执行文件名')

    args = parser.parse_args()

    print("开始更新...")
    print(f"目标目录: {args.target_dir}")
    print(f"更新包: {args.update_package}")
    print(f"应用程序: {args.app_exe}")

    # 检查文件是否存在
    if not Path(args.update_package).exists():
        print(f"错误: 更新包不存在: {args.update_package}")
        return 1

    if not Path(args.target_dir).exists():
        print(f"错误: 目标目录不存在: {args.target_dir}")
        return 1

    # 构建完整的应用程序路径
    app_path = Path(args.target_dir) / args.app_exe

    # 应用更新
    if apply_update(args.update_package, args.target_dir):
        print("更新成功!")

        # 清理更新包
        try:
            os.remove(args.update_package)
        except:
            pass

        # 重启应用程序
        restart_application(str(app_path))

        return 0
    else:
        print("更新失败!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
