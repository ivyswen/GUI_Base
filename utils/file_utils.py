"""
文件操作工具集
提供常用的文件和目录操作功能
"""

import os
import shutil
import hashlib
from pathlib import Path
from typing import Optional, List, Tuple
from utils.logger import get_logger

logger = get_logger(__name__)


def ensure_dir(directory: str) -> bool:
    """确保目录存在，如果不存在则创建
    
    Args:
        directory: 目录路径
        
    Returns:
        bool: 操作是否成功
    """
    try:
        os.makedirs(directory, exist_ok=True)
        logger.debug(f"目录已确保存在: {directory}")
        return True
    except Exception as e:
        logger.error(f"创建目录失败 {directory}: {e}")
        return False


def file_exists(file_path: str) -> bool:
    """检查文件是否存在
    
    Args:
        file_path: 文件路径
        
    Returns:
        bool: 文件是否存在
    """
    return os.path.isfile(file_path)


def dir_exists(directory: str) -> bool:
    """检查目录是否存在
    
    Args:
        directory: 目录路径
        
    Returns:
        bool: 目录是否存在
    """
    return os.path.isdir(directory)


def get_file_size(file_path: str) -> int:
    """获取文件大小（字节）
    
    Args:
        file_path: 文件路径
        
    Returns:
        int: 文件大小，如果文件不存在返回0
    """
    try:
        return os.path.getsize(file_path)
    except Exception as e:
        logger.error(f"获取文件大小失败 {file_path}: {e}")
        return 0


def format_file_size(size_bytes: int) -> str:
    """格式化文件大小为人类可读格式
    
    Args:
        size_bytes: 文件大小（字节）
        
    Returns:
        str: 格式化后的文件大小
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def calculate_file_hash(file_path: str, algorithm: str = 'sha256') -> Optional[str]:
    """计算文件哈希值
    
    Args:
        file_path: 文件路径
        algorithm: 哈希算法（md5, sha1, sha256等）
        
    Returns:
        Optional[str]: 哈希值，失败返回None
    """
    try:
        hash_obj = hashlib.new(algorithm)
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()
    except Exception as e:
        logger.error(f"计算文件哈希失败 {file_path}: {e}")
        return None


def copy_file(src: str, dst: str, overwrite: bool = False) -> bool:
    """复制文件
    
    Args:
        src: 源文件路径
        dst: 目标文件路径
        overwrite: 是否覆盖已存在的文件
        
    Returns:
        bool: 操作是否成功
    """
    try:
        if not overwrite and file_exists(dst):
            logger.warning(f"目标文件已存在: {dst}")
            return False
        
        # 确保目标目录存在
        dst_dir = os.path.dirname(dst)
        if dst_dir:
            ensure_dir(dst_dir)
        
        shutil.copy2(src, dst)
        logger.info(f"文件已复制: {src} -> {dst}")
        return True
    except Exception as e:
        logger.error(f"复制文件失败 {src} -> {dst}: {e}")
        return False


def move_file(src: str, dst: str, overwrite: bool = False) -> bool:
    """移动文件
    
    Args:
        src: 源文件路径
        dst: 目标文件路径
        overwrite: 是否覆盖已存在的文件
        
    Returns:
        bool: 操作是否成功
    """
    try:
        if not overwrite and file_exists(dst):
            logger.warning(f"目标文件已存在: {dst}")
            return False
        
        # 确保目标目录存在
        dst_dir = os.path.dirname(dst)
        if dst_dir:
            ensure_dir(dst_dir)
        
        shutil.move(src, dst)
        logger.info(f"文件已移动: {src} -> {dst}")
        return True
    except Exception as e:
        logger.error(f"移动文件失败 {src} -> {dst}: {e}")
        return False


def delete_file(file_path: str) -> bool:
    """删除文件
    
    Args:
        file_path: 文件路径
        
    Returns:
        bool: 操作是否成功
    """
    try:
        if file_exists(file_path):
            os.remove(file_path)
            logger.info(f"文件已删除: {file_path}")
            return True
        else:
            logger.warning(f"文件不存在: {file_path}")
            return False
    except Exception as e:
        logger.error(f"删除文件失败 {file_path}: {e}")
        return False


def delete_directory(directory: str, recursive: bool = False) -> bool:
    """删除目录
    
    Args:
        directory: 目录路径
        recursive: 是否递归删除（包括所有内容）
        
    Returns:
        bool: 操作是否成功
    """
    try:
        if not dir_exists(directory):
            logger.warning(f"目录不存在: {directory}")
            return False
        
        if recursive:
            shutil.rmtree(directory)
            logger.info(f"目录已递归删除: {directory}")
        else:
            os.rmdir(directory)
            logger.info(f"目录已删除: {directory}")
        return True
    except Exception as e:
        logger.error(f"删除目录失败 {directory}: {e}")
        return False


def list_files(directory: str, pattern: str = "*", recursive: bool = False) -> List[str]:
    """列出目录中的文件
    
    Args:
        directory: 目录路径
        pattern: 文件名模式（支持通配符）
        recursive: 是否递归搜索子目录
        
    Returns:
        List[str]: 文件路径列表
    """
    try:
        path = Path(directory)
        if recursive:
            files = [str(f) for f in path.rglob(pattern) if f.is_file()]
        else:
            files = [str(f) for f in path.glob(pattern) if f.is_file()]
        logger.debug(f"在 {directory} 中找到 {len(files)} 个文件")
        return files
    except Exception as e:
        logger.error(f"列出文件失败 {directory}: {e}")
        return []


def list_directories(directory: str, recursive: bool = False) -> List[str]:
    """列出目录中的子目录
    
    Args:
        directory: 目录路径
        recursive: 是否递归搜索
        
    Returns:
        List[str]: 目录路径列表
    """
    try:
        path = Path(directory)
        if recursive:
            dirs = [str(d) for d in path.rglob("*") if d.is_dir()]
        else:
            dirs = [str(d) for d in path.glob("*") if d.is_dir()]
        logger.debug(f"在 {directory} 中找到 {len(dirs)} 个目录")
        return dirs
    except Exception as e:
        logger.error(f"列出目录失败 {directory}: {e}")
        return []


def get_file_extension(file_path: str) -> str:
    """获取文件扩展名
    
    Args:
        file_path: 文件路径
        
    Returns:
        str: 文件扩展名（包含点号，如 '.txt'）
    """
    return os.path.splitext(file_path)[1]


def get_file_name(file_path: str, with_extension: bool = True) -> str:
    """获取文件名
    
    Args:
        file_path: 文件路径
        with_extension: 是否包含扩展名
        
    Returns:
        str: 文件名
    """
    name = os.path.basename(file_path)
    if not with_extension:
        name = os.path.splitext(name)[0]
    return name


def read_text_file(file_path: str, encoding: str = 'utf-8') -> Optional[str]:
    """读取文本文件
    
    Args:
        file_path: 文件路径
        encoding: 文件编码
        
    Returns:
        Optional[str]: 文件内容，失败返回None
    """
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            content = f.read()
        logger.debug(f"文件已读取: {file_path}")
        return content
    except Exception as e:
        logger.error(f"读取文件失败 {file_path}: {e}")
        return None


def write_text_file(file_path: str, content: str, encoding: str = 'utf-8') -> bool:
    """写入文本文件
    
    Args:
        file_path: 文件路径
        content: 文件内容
        encoding: 文件编码
        
    Returns:
        bool: 操作是否成功
    """
    try:
        # 确保目录存在
        directory = os.path.dirname(file_path)
        if directory:
            ensure_dir(directory)
        
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(content)
        logger.info(f"文件已写入: {file_path}")
        return True
    except Exception as e:
        logger.error(f"写入文件失败 {file_path}: {e}")
        return False

