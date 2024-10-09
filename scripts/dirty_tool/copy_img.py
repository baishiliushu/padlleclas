import os
import shutil

def copy_files_with_new_structure(input_file, base_output_dir, parent_dir):
    # 读取原始文件路径
    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    for line in lines:
        # 拼接父目录
        full_path = os.path.join(parent_dir, line)
        
        # 确保文件存在
        if os.path.isfile(full_path):
            path_parts = line.rsplit('/', 1)
            if len(path_parts) == 2:
                original_path, filename = path_parts
                # 创建新的目标目录结构
                new_directory = os.path.join(base_output_dir, original_path)
                os.makedirs(new_directory, exist_ok=True)  # 创建目录
                
                # 复制文件到新目录
                shutil.copy(full_path, os.path.join(new_directory, filename))
                print(f"复制 {full_path} 到 {new_directory}")

# 使用示例
copy_files_with_new_structure('solid_all2.txt', 'solid_timed', './')

