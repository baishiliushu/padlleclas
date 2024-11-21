# 添加多文件labeling
import os
import random


def split_list_randomly(input_list):
    # 随机打乱列表
    random.shuffle(input_list)

    # 计算中间位置
    mid_index = len(input_list) // 5

    # 将列表分为两部分
    part1 = input_list[:mid_index]
    part2 = input_list[mid_index:]

    return part1, part2


# 获取多个数据路径
root_paths = [
    '/home/indemind/nfs_1/peson-attr-train-test-data/0920-skirt',
    '/home/indemind/nfs_1/peson-attr-train-test-data/0923-skirt',
    '/home/mount_point_one/dataset/train/person_19_20_0920_cut_0929picked'
]

label_path = '/home/mount_point_one/dataset/train_label_addfolder/labels.txt'
train_path = '/home/mount_point_one/dataset/train_label_addfolder/train.txt'
test_path = '/home/mount_point_one/dataset/train_label_addfolder/test.txt'

other = '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,'
front = '1,0,0'
side = '0,1,0'
back = '0,0,1'
labels = []

for root_path in root_paths:
    dataset_name = os.path.basename(root_path)  # 获取文件夹名称作为前缀
    for root, dirs, files in os.walk(root_path):
        for file in files:
            file_path = os.path.join(root, file)
            # 生成以数据集文件夹名称为前缀的相对路径
            relative_path = os.path.join(dataset_name, file_path.replace(root_path + '/', ''))

            if 'front' in file_path:
                label = relative_path + '\t' + other + front
            elif 'back' in file_path:
                label = relative_path + '\t' + other + back
            elif 'side' in file_path:
                label = relative_path + '\t' + other + side
            else:
                print(f"Skipping {os.path.join(root, file)}")
                continue
            labels.append(label)

# 随机分割标签列表为训练集和测试集
test, train = split_list_randomly(labels)
print(f"Total labels: {len(labels)}")
print(f"Test set size: {len(test)}")
print(f"Train set size: {len(train)}")

# 将标签保存到文件
with open(label_path, 'w') as file:
    for line in labels:
        file.write(line + '\n')
with open(train_path, 'w') as file:
    for line in train:
        file.write(line + '\n')
with open(test_path, 'w') as file:
    for line in test:
        file.write(line + '\n')