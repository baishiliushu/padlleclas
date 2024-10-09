import os
import shutil
import glob

# 设置主文件夹路径
base_folder = '/home/leon/mount_point_two/rubby-data-track/nfs_label_work/dataset/train/person_19_20_0902_cut/'
middle_folders = [] # 'side' 'back' 'front' 


white_names = ['front_1', 'front_2', 'front_2_2','front_3', 'front_4', 'front_5', 'front_6', 'front_7', 'front_8', 'front__3',
               'back_1', 'back_2', 'back_3', 'back_4', 'back_5', 'back_6', 'back_7', 'back_8']
todo_names = ['front_chair_3_2']

name_kinds = {1:'normal', 2:'special', 3:'unuseful'}

for m in middle_folders:
    _common = name_kinds[1]
    _clear_agein = name_kinds[2]
    _err = name_kinds[3]
    dir_to_process = os.path.join(base_folder, m)
    for d in os.listdir(dir_to_process):
        # d : side_1
        # if d in white_names:
        if d not in todo_names:
            print("{} in white names".format(d))
            continue
        deep_path = os.path.join(dir_to_process, d)
        
        img_jpg_counter = 0
        special_jpg_counter = 0
        common_jpg_counter = 0
        if os.path.isdir(deep_path):
            handdle_txt_name = "{}.txt".format(d)
            txt_path = os.path.join(deep_path, handdle_txt_name)
            print("{} under {}".format(handdle_txt_name, deep_path))
            folder_common = os.path.join(deep_path, _common)
            folder_clear_agein = os.path.join(deep_path, _clear_agein)
            folder_err = os.path.join(deep_path, _err)
            os.makedirs(folder_common, exist_ok=True)
            os.makedirs(folder_clear_agein, exist_ok=True)
            os.makedirs(folder_err, exist_ok=True)
            files_by_txt = list()
            if handdle_txt_name in os.listdir(deep_path):
                with open(txt_path, 'r') as f:
                    files_by_txt = [line.strip() for line in f]
            jpg_path = os.path.join(deep_path, 'img')
            jpg_files = os.listdir(jpg_path)
            img_jpg_counter = len(jpg_files) 
            for j in jpg_files:
                source_path = os.path.join(jpg_path, j)
                folder_target = os.path.join(folder_common, j)
                if j in files_by_txt:
                    folder_target = os.path.join(folder_clear_agein, j)
                shutil.copy(source_path, folder_target)
                print("copy {} TO {}".format(source_path, folder_target))    
            special_jpg_counter = len(os.listdir(folder_clear_agein))  
            common_jpg_counter = len(os.listdir(folder_common))         
                
        check_info = "=="
        if img_jpg_counter != (special_jpg_counter + common_jpg_counter):
            check_info = "!="
        print("-----------------------FINISHED {} : jpgs {} {} {} + {}-----------------------".format(deep_path, img_jpg_counter, check_info, special_jpg_counter, common_jpg_counter))
            
print("文件复制完成！")
