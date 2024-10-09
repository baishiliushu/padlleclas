from PIL import Image
import os
from tqdm import tqdm
import random

def crop_and_resize(image_path, output_path):
    # 打开图像
    image = Image.open(image_path)

    # 获取原图尺寸
    width, height = image.size

    # 计算下半部分的区域（左，上，右，下）
    random_int = random.randint(2, 10)
    crop_area = (0, height // random_int, width, height)

    # 裁剪下半部分
    bottom_half = image.crop(crop_area)

    # 将裁剪的下半部分重新调整为原图大小
    resized_image = bottom_half.resize((width, height))

    # 保存调整后的图片
    resized_image.save(output_path)


# 使用示例
if __name__ == '__main__':
    data_path = '/mnt/sda3/cut_img/person_19_20_0902'
    save_dir_path = data_path + '_cut_random'
    os.makedirs(save_dir_path, exist_ok=True)
    for root, dirs, files in os.walk(data_path):
        for file in tqdm(files):
            if '.jpg' in file:
                os.makedirs(root.replace(data_path,save_dir_path),exist_ok=True)
                save_img_path = os.path.join(root, file).replace(data_path, save_dir_path)
                crop_and_resize(os.path.join(root, file), save_img_path)
