import os
import random

"""
root_path:待标注路径
    /home/spring/dataset/person_0813
    该路径下需要有front、side、back三个文件夹
    这三个文件夹下放各批次数据例如：
        /home/spring/dataset/person_0813/front/front_1/img
生成的标注文件在
    /home/spring/dataset/person_0813
"""
def split_list_randomly(input_list):
    # 随机打乱列表
    random.shuffle(input_list)

    # 计算中间位置
    mid_index = len(input_list) // 5

    # 将列表分为两部分
    part1 = input_list[:mid_index]
    part2 = input_list[mid_index:]

    return part1, part2
root_path = "/home/leon/mount_point_d/test-result-moved/peson-attr-train-test-data/datasets/train/person_19_20_0920_cut_0929picked" # input("data_path:")
label_path = os.path.join(root_path, 'labels.txt')
train_path = os.path.join(root_path, 'train.txt')
test_path = os.path.join(root_path, 'test.txt')
other = '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,'
front = '1,0,0'
side = '0,1,0'
back = '0,0,1'
labels = []
for root, dirs, files in os.walk(root_path):
    for file in files:
        if(file.lower().endswith(('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff'))):
            print(file)
        else:
           continue

        file_path = os.path.join(root, file)
        file_path = file_path.replace(root_path + '/', '')
        if 'front' in file_path:
            label = file_path + '\t' + other + front
        elif 'back' in file_path:
            label = file_path + '\t' + other + back
        elif 'side' in file_path:
            label = file_path + '\t' + other + side
        else:
            print(os.path.join(root, file))
            continue
        labels.append(label)
test,train = split_list_randomly(labels)
print(len(labels))
print(len(test))
print(len(train))
with open(label_path, 'w') as file:
    for line in labels:
        file.write(line)
        file.write('\n')
with open(train_path, 'w') as file:
    for line in train:
        file.write(line)
        file.write('\n')
with open(test_path, 'w') as file:
    for line in test:
        file.write(line)
        file.write('\n')
