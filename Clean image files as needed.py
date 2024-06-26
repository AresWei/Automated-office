# Function: Clean low-resolution images, small files and duplicate files in the specified directory and its subdirectories.

import os
import hashlib
from tqdm import tqdm
from PIL import Image


def get_file_hash(file_path):
    """计算文件的MD5哈希值"""
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def preliminary_check(file_path):
    """获取文件的大小和前几个字节作为初步筛选条件"""
    file_size = os.path.getsize(file_path)
    with open(file_path, 'rb') as f:
        start = f.read(1024)
    return (file_size, start)


def get_image_resolution(file_path):
    """获取图片的分辨率"""
    try:
        with Image.open(file_path) as img:
            return img.size
    except:
        return None


def remove_low_resolution_images(root_dir, min_resolution):
    """删除分辨率低于指定大小的图片"""
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            resolution = get_image_resolution(file_path)
            if resolution and (resolution[0] < min_resolution[0] or resolution[1] < min_resolution[1]):
                os.remove(file_path)
                print(f"删除了分辨率低于{min_resolution[0]}x{min_resolution[1]}的图片: {file_path}")


def remove_small_files(root_dir, min_size_kb=400):
    """删除小于指定大小的文件"""
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if os.path.getsize(file_path) < min_size_kb * 1024:
                os.remove(file_path)
                print(f"删除了小于{min_size_kb}KB的文件: {file_path}")


def remove_duplicates(root_dir, check_subdirectories):
    """删除指定目录下的重复文件并显示进度条"""
    seen_hashes = {}
    preliminary_data = {}
    total_files = sum(len(files) for _, _, files in os.walk(root_dir))
    pbar = tqdm(total=total_files, desc="处理文件", unit="file")

    for dirpath, _, filenames in os.walk(root_dir):
        if not check_subdirectories and dirpath != root_dir:
            continue
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if not os.path.exists(file_path):  # 检查文件是否存在
                continue
            size_and_start = preliminary_check(file_path)
            if size_and_start in preliminary_data:
                if get_file_hash(file_path) == get_file_hash(preliminary_data[size_and_start]):
                    os.remove(file_path)
                    print(f"删除了文件: {file_path}")
            else:
                preliminary_data[size_and_start] = file_path
            pbar.update(1)
    pbar.close()


if __name__ == "__main__":
    root_directory = input("请输入要检查的根目录: ")
    choice = input("是否检查子目录及其内部文件? (y/n): ").lower()
    check_subdirs = choice == 'y'

    # 删除低分辨率图片
    resolution_threshold = tuple(map(int, input("请输入要保留的最低分辨率，格式为 宽x高（例如：800x600）: ").split('x')))
    remove_low_resolution_images(root_directory, resolution_threshold)

    # 是否删除小文件
    choice = input("是否删除低于指定文件大小的文件? (y/n): ").lower()
    if choice == 'y':
        min_size = int(input("请输入最小文件大小 (KB): "))
        remove_small_files(root_directory, min_size)

    # 删除重复文件
    remove_duplicates(root_directory, check_subdirs)
