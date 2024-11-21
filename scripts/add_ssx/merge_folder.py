import os
import shutil
import argparse
from tqdm import tqdm  # 用于显示进度条

def merge_res_folders(source_directory, destination_directory):
    # 确保目标目录存在
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    # 用于统计文件总数
    total_files = 0

    # 首先遍历所有符合条件的文件夹，统计文件数量
    for folder_name in os.listdir(source_directory):
        if folder_name.startswith('20241111_wangjing_'):
            res_folder_path = os.path.join(source_directory, folder_name, 'res')
            if os.path.exists(res_folder_path) and os.path.isdir(res_folder_path):
                for root, dirs, files in os.walk(res_folder_path):
                    total_files += len(files)

    # 开始复制文件并显示进度
    copied_files = 0
    for folder_name in os.listdir(source_directory):
        if folder_name.startswith('20241111_wangjing_'):
            res_folder_path = os.path.join(source_directory, folder_name, 'res')
            if os.path.exists(res_folder_path) and os.path.isdir(res_folder_path):
                for root, dirs, files in os.walk(res_folder_path):
                    # 计算当前相对路径
                    relative_path = os.path.relpath(root, res_folder_path)
                    target_folder = os.path.join(destination_directory, relative_path)

                    # 创建对应的目标子文件夹
                    if not os.path.exists(target_folder):
                        os.makedirs(target_folder)

                    # 使用 tqdm 显示进度条
                    for file in tqdm(files, desc='Copying files', unit='file', total=total_files):
                        source_file = os.path.join(root, file)
                        target_file = os.path.join(target_folder, file)

                        # 如果目标文件已存在，重命名文件
                        if os.path.exists(target_file):
                            base, ext = os.path.splitext(file)
                            counter = 1
                            while os.path.exists(target_file):
                                target_file = os.path.join(target_folder, f"{base}_{counter}{ext}")
                                counter += 1

                        shutil.copy2(source_file, target_file)
                        copied_files += 1

if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--source_directory', type=str, required=True, help='Path to the source directory containing folders.')
    # parser.add_argument('--destination_directory', type=str, required=True, help='Path to the destination directory to merge res folders.')
    # opt = parser.parse_args()

    # 指定目标目录的路径
    source_directory = '/home/indemind/nfs_1/reid_datas/reid_datas_pick/20241111_data_wangjing/output'
    destination_directory = '/home/indemind/nfs_1/reid_datas/reid_datas_pick/20241111_data_wangjing/output/20241111_data_wangjing_all'
    all_res_directory = os.path.join(destination_directory, 'res')
    merge_res_folders(source_directory, all_res_directory)



