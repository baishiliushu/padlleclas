import os
from collections import defaultdict

def extract_filenames(input_file, output_file, x):
    # 读取原始文件名和时间戳
    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    # 打印原TXT文件中的文件数量
    original_count = len(lines)

    # 按子目录分组
    grouped_files = defaultdict(list)
    
    for line in lines:
        path_parts = line.rsplit('/', 1)  # 分离路径和文件名
        if len(path_parts) == 2:
            path, filename = path_parts
            try:
                timestamp = int(filename.split('.')[0])  # 提取时间戳
                second = timestamp // 1_000_000  # 微秒转换为秒
                
                # 将文件名按子目录和秒分组
                grouped_files[(path, second)].append(line)
            except ValueError:
                print(f"跳过无法解析的文件名: {path} {filename}")  # 打印出无法解析的文件名

    # 准备待抽取的数据
    extracted_filenames = []
    for (path, second), files in grouped_files.items():
        extracted_filenames.extend(files[:x])  # 只取前x个文件名

    # 写入新的TXT文件
    with open(output_file, 'w') as f:
        for name in extracted_filenames:
            f.write(f"{name}\n")  # 保持原路径结构

    # 打印新TXT文件中的文件数量
    new_count = len(extracted_filenames)
    print(f"原TXT文件中的文件数量: {original_count}")
    print(f"新TXT文件中的文件数量: {new_count}")

# 使用示例
extract_filenames('solid_all.txt', 'solid_all2.txt', 2)  # 每个子目录每秒抽取2个文件名

