import os
from PIL import Image

def crop_and_resize(image_path, output_path):
    # 打开图像
    image = Image.open(image_path)

    # 获取原图尺寸
    width, height = image.size

    # 设置裁剪比例为保留下方 70%
    crop_ratio = 0.7
    crop_start_height = int(height * (1 - crop_ratio))  # 从高度的 30% 开始

    # 定义裁剪区域（保留下方 70%）
    crop_area = (0, crop_start_height, width, height)

    # 裁剪图像下方区域
    cropped_image = image.crop(crop_area)

    # 将裁剪的区域重新调整为原图大小，使用抗锯齿
    resized_image = cropped_image.resize((width, height), Image.LANCZOS)

    # 保存调整后的图片
    resized_image.save(output_path)

def process_folders(base_dir):
    # 遍历 A 目录下的所有文件夹
    for root, dirs, files in os.walk(base_dir):
        # 检查 normal 文件夹
        if os.path.basename(root) == 'normal':
            # 定义 cut_normal 文件夹路径，使其位于 normal 的同级目录
            cut_normal_dir = os.path.join(os.path.dirname(root), 'cut_normal')
            os.makedirs(cut_normal_dir, exist_ok=True)

            # 遍历 normal 文件夹中的所有图像文件
            for file_name in files:
                file_path = os.path.join(root, file_name)
                output_path = os.path.join(cut_normal_dir, file_name)

                # 对图像进行裁剪并保存到 cut_normal 文件夹
                try:
                    crop_and_resize(file_path, output_path)
                    print(f"Processed {file_path} and saved to {output_path}")
                except Exception as e:
                    print(f"Failed to process {file_path}: {e}")

base_dir = '/home/indemind/nfs_1/reid_datas/reid_dataset_1104/'
process_folders(base_dir)
