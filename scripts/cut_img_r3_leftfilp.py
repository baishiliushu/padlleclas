from PIL import Image
import os
# from tqdm import tqdm
import random
import shutil

"""
1. 将分拣过且有用的jpgs目录移动到新目录
2. 剪裁 
   2-1. 上下剪裁 / 左右剪裁
   2-2. 不剪切的 back:['sofa'] side:['sofa'] near
   2-3. 保守剪切的 front:['chair'] back:['chair'] side:['chair']
3. *左右翻转
   3-1. specail和nornal才翻转
*MORE: aug之后的数据集选择*

"""

MID_NAMES = ['back', 'front', 'side']
DATA_NAMES = ['normal', 'special']    
AGU_TYPES = ['cut', 'flip']
MOVEOUT_USE_TYPES = ['dark']
NO_AGU_TYPES = ['sofa', 'near']
LESS_AGU_TYPES = ['chair']

def brightness_summary(pixels, w, h):
    brightness_values = []
    is_balance = True
    for x in range(w):
        for y in range(h):
            # todo : one channel OR three channels
            r, g, b = pixels[x, y]
            _brightness = 0.299 * r + 0.587 * g + 0.114 * b
            brightness_values.append(_brightness)
    if len(brightness_values) < 10 or w*h < 10:
        return False
    too_large_counter = 0
    too_dark_counter = 0
    for b in brightness_values:
        if b < 45 :
            too_dark_counter += 1
        if b > 210:
            too_large_counter += 1
    if too_dark_counter > (len(brightness_values) * 0.68):
        is_balance = False
    return is_balance

"""
todo 剪裁之后的图像如果直方图分布 过集中 则放在left_data目录
"""
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

def crop_and_resize_x(image_path, output_path):
    # 打开图像
    image = Image.open(image_path)

    # 获取原图尺寸
    width, height = image.size

    # 计算右半部分的区域（左，上，右，下）
    random_int = 2 #random.randint(2, 3)
    
    crop_areas = [(width // random_int, 0, width, height), (0, 0, width // random_int, height)]
    crop_area = random.choice(crop_areas)  
    # 裁剪右半部分
    bottom_half = image.crop(crop_area)

    # 将裁剪的右半部分重新调整为原图大小
    resized_image = bottom_half.resize((width, height))

    # 保存调整后的图片
    resized_image.save(output_path)

def filp_img(image_path, output_path):
    img = Image.open(image_path)
    out = img.transpose(Image.FLIP_LEFT_RIGHT)     #水平翻转
    out.save(output_path)

def subitems(father_path_abs):
    sub_items = os.listdir(father_path_abs)
    dirs = list()
    files = list()
    for s in sub_items:
        if os.path.isdir(os.path.join(father_path_abs, s)):
            dirs.append(s)
        if os.path.isfile(os.path.join(father_path_abs, s)):
            files.append(s)
    print("sub dirs : {}".format(dirs))
    print("sub files: {}".format(len(files)))
    return dirs, files
    

# 使用示例
if __name__ == '__main__':   
    data_path = "/home/leon/mount_point_d/test-result-moved/peson-attr-train-test-data/datasets/train/person_19_20_0920_cut_0929picked" #'/mnt/sda3/cut_img/person_19_20_0902'    
    # scene_paths os.listdir('back') os.path.isdir(deep_path)
    
    new_path = "/home/leon/mount_point_d/test-result-moved/peson-attr-train-test-data/datasets/train_iter/person_clean_0929_base"
    
    do_normal_specail_copy = True
    data_op_endless = "1007"
    # os.makedirs(save_dir_path, exist_ok=True)
    # if '.jpg' in f:
    # crop_and_resize(os.path.join(root, f), save_img_path)
    
    """
    MID_NAMES = ['back', 'front', 'side']
    DATA_NAMES = ['normal', 'special']    
    AGU_TYPES = ['cut', 'flip']
    MOVEOUT_USE_TYPES = ['dark']
    NO_AGU_TYPES = ['sofa', 'near']
    LESS_AGU_TYPES = ['chair']
    """
    for m in MID_NAMES:
        # 1. 不管cut目录， back
        middle_path = os.path.join(data_path, m)
        print("Enter: {}".format(middle_path))
        if not os.path.exists(middle_path):
            print("WARNING: NOT exist {}".format(middle_path))
            continue
        middle_path_new = os.path.join(new_path, m)
        os.makedirs(middle_path_new, exist_ok=True)

        scene_names, _ = subitems(middle_path)
        # 2. back_1
        for s in scene_names:
            scene_path = os.path.join(middle_path, s)
            scene_path_new = os.path.join(middle_path_new, s)
            os.makedirs(scene_path_new, exist_ok=True)
            # 3. normal / specail
            for n in DATA_NAMES:
                data_name_path = os.path.join(scene_path, n)
                if not os.path.exists(data_name_path):
                    print("WARNING: NOT exist data_type {}".format(data_name_path))
                    continue
                data_name_path_new = os.path.join(scene_path_new, n)
                os.makedirs(data_name_path_new, exist_ok=True)
                # 4. move
                _, fs = subitems(data_name_path)
                if do_normal_specail_copy is True:
                    for f in fs:
                        source_path = os.path.join(data_name_path, f)   
                        folder_target = os.path.join(data_name_path_new, f)        
                        shutil.copy(source_path, folder_target)
                    _, new_fs = subitems(data_name_path_new)
                    print("copy {} ({}) TO {} ({})".format(data_name_path, len(fs), data_name_path_new, len(new_fs)))  
                    
                # 5. agu {scene_path_new/cut; scene_path_new/filp}
                do_agu = True
                for a in NO_AGU_TYPES:
                    if a in s:
                        do_agu = False
                        break
                if not do_agu:
                    continue
                if n == 'normal':
                    data_father_location = scene_path_new
                    allowed_optional_data_path = data_name_path_new
                    class_type = m # back 
                    do_all_agu = True
                    for c in LESS_AGU_TYPES:
                        if c in s:
                            do_all_agu = False
                            break
                    # do agu
                    path_cut = os.path.join(scene_path_new, 'cut.y.{}'.format(data_op_endless))
                    os.makedirs(path_cut, exist_ok=True)
                    for f in new_fs:
                        src_file_path = os.path.join(data_name_path_new, f)
                        cut_file_path = os.path.join(path_cut, f)
                        crop_and_resize(src_file_path, cut_file_path)
                    print("CUT.Y {} TO {}".format(data_name_path_new, path_cut))
                    path_cut = os.path.join(scene_path_new, 'cut.x.{}'.format(data_op_endless))
                    os.makedirs(path_cut, exist_ok=True)                    
                    for f in new_fs:
                        src_file_path = os.path.join(data_name_path_new, f)
                        cut_file_path = os.path.join(path_cut, f)
                        crop_and_resize_x(src_file_path, cut_file_path)
                
                path_filp = os.path.join(scene_path_new, 'flip_{}.{}'.format(n, data_op_endless))
                os.makedirs(path_filp, exist_ok=True)
                for f in new_fs:
                    src_file_path = os.path.join(data_name_path_new, f)
                    flip_file_path = os.path.join(path_filp, f)
                    filp_img(src_file_path, flip_file_path)
                print("FLIP {} TO {}".format(data_name_path_new, path_filp))
    """
    for m in MID_NAMES:
        middle_path_new = os.path.join(new_path, m)
        scene_names, _ = subitems(middle_path_new)
        # 2. back_1
        for s in scene_names:
            scene_path_new = os.path.join(middle_path_new, s)
            ns, _ = subitems(scene_path_new)
            for n in ns:
                path_filp = os.path.join(scene_path_new, 'flip_{}.{}'.format(n, data_op_endless))
                os.makedirs(path_filp, exist_ok=True)
                _, _ = subitems(scene_path_new)
                for f in new_fs:
                    src_file_path = os.path.join(data_name_path_new, f)
                    flip_file_path = os.path.join(path_filp, f)
                    filp_img(src_file_path, flip_file_path)
            print("FLIP {} TO {}".format(data_name_path_new, path_filp))
    """  






 
                
