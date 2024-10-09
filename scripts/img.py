import os
import shutil
"""
/mnt/sda2/0902/20240902_data_0
path:采集的源数据路径
    /mnt/sda2/0902
word：采集数据时设置的保存路径
    20240902_data_
output:输出文件夹，与 20240902_data_ 同级，如果是多批次会生成多个output
    
"""
def copy_img(src, dest):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.copy(src, dest)
path = input("Enter the image path: ")
word = input("Enter the word to search for: ")
for root, dirs, files in os.walk(path):
    for dir in dirs:
        if word in dir:
            src = os.path.join(root, dir)
            dest = os.path.join(root, "output",dir,"img")
            for root1, dirs1, files1 in os.walk(src):
                for file1 in files1:
                    if "/cam0" in os.path.join(root1, file1) and "/ORIGIN" not in os.path.join(root1, file1):
                        copy_img(os.path.join(root1, file1), os.path.join(dest, root1.split('/')[-2] + "_" + file1))