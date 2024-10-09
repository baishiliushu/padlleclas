import os
import shutil
from tqdm import tqdm

path = '/home/spring/nfs_client/postest_res/0906_test_near'
out_path = '/home/spring/dataset/person_0906_test_near'
def copy_img(src, dest):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.copy(src, dest)
for root, dirs, files in os.walk(path):
    for dir in dirs:
        if 'input_imgs' in dir:
            print(root)
            dir_list = os.listdir(os.path.join(root, dir))
            for img in tqdm(dir_list):

                name_path = root.replace(path,'').split('/')[-2]
                if 'front' in name_path:
                    copy_path = os.path.join(out_path,'front',name_path,'img',img)
                    copy_img(os.path.join(root, dir,img), os.path.join(out_path,'front',name_path,'img',img))
                    # print(copy_path)
                elif 'back' in name_path:
                    copy_path = os.path.join(out_path,'back',name_path,'img',img)
                    copy_img(os.path.join(root, dir,img), os.path.join(out_path,'back',name_path,'img',img))
                    # print(copy_path)
                elif 'side' in name_path:
                    copy_path = os.path.join(out_path,'side',name_path,'img',img)
                    copy_img(os.path.join(root, dir,img), os.path.join(out_path,'side',name_path,'img',img))
                    # print(copy_path)
            # src = os.path.join(root, dir)
            # dest = os.path.join(root, "output",dir,"img")
            # for root1, dirs1, files1 in os.walk(src):
            #     for file1 in files1:
            #         if "/cam0" in os.path.join(root1, file1) and "/ORIGIN" not in os.path.join(root1, file1):
            #             copy_img(os.path.join(root1, file1), os.path.join(dest, root1.split('/')[-2] + "_" + file1))