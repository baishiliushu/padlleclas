path = '/mnt/sda2/dataset/pa100k/txt/train_list.txt'
new_path = '/mnt/sda2/dataset/pa100k/txt/train_label_fbs.txt'
with open(path, 'r') as file:
    # 读取所有行并存储在列表中
    lines = file.readlines()
    # 去掉每行末尾的换行符
    lines = [line.strip() for line in lines]
    new_lines = []
    for line in lines:
        new_line_0 = line.split('\t')[0]
        new_line_1 = line.split('\t')[1]
        labels = new_line_1.split(',')
        for i in range(len(labels)):
            if i == 23 or i == 24 or i == 25:
                labels[i] = labels[i]
            else:
                labels[i] = str(0)
        label = ','.join(labels)
        label = new_line_0 + '\t' + label
        new_lines.append(label)

with open(new_path, 'w') as file:
    for line in new_lines:
        file.write(line)
        file.write('\n')


# 备注：其中 output 的值索引为0表示是否佩戴帽子，索引值为1表示是否佩戴眼镜，索引值2-7表示上衣风格，索引值8-13表示下装风格，索引值14表示是否穿靴子，索引值15-17表示背的包的类型，索引值18表示正面是否持物，索引值19-21表示年龄，索引值22表示性别，索引值23-25表示朝向。详情可以查看代码。具体地，属性包含以下类型：
