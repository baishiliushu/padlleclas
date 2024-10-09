import os
import shutil
from pathlib import Path

def copy_files_from_txt(txt_path, source_dir, target_dir):
    # 创建目标目录
    os.makedirs(target_dir, exist_ok=True)

    # 读取txt文件
    with open(txt_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 处理每一行，将相对路径的文件从source_dir复制到target_dir
    for line in lines:
        # 去除行末的换行符和空白符
        relative_path = line.strip()

        # 构建完整的源文件路径和目标文件路径
        source_path = Path(source_dir) / relative_path
        target_path = Path(target_dir) / relative_path

        # 确保目标文件所在的目录存在
        os.makedirs(target_path.parent, exist_ok=True)  # 自动创建类似的目录结构

        try:
            # 复制文件
            shutil.copy2(source_path, target_path)
            print(f"Copied {source_path} to {target_path}")
        except FileNotFoundError:
            print(f"File not found: {source_path}")
        except Exception as e:
            print(f"Error copying {source_path}: {e}")

# 示例用法
txt_file = '/home/leon/mount_point_d/test-result-moved/dirty_data/20241009/20241007_dirty_dongdong/all1.guti.txt'  # txt文件路径
source_directory = '/home/leon/mount_point_d/test-result-moved/dirty_data/20241009/20241007_dirty_dongdong'  # 源目录
target_directory = '/home/leon/mount_point_d/test-result-moved/dirty_data/20241009/20241007_dirty_dongdong_solid_annos'  # 目标目录

copy_files_from_txt(txt_file, source_directory, target_directory)

