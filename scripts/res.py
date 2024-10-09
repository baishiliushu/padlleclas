import os
import xlwt
def export_excell(data_list,excell_save_path):
    # data : [name,front_num, back_num, side_num]
    # 创建一个Excel工作簿
    workbook = xlwt.Workbook()
    # 创建一个工作表
    sheet_front = workbook.add_sheet('sheet_front')
    sheet_front.write(0, 1, 'front_num')
    sheet_front.write(0, 2, 'back_num')
    sheet_front.write(0, 3, 'side_num')
    sheet_front.write(0, 4, 'img_num')
    sheet_front.write(0, 5, 'recall')
    sheet_side = workbook.add_sheet('sheet_side')
    sheet_side.write(0, 1, 'front_num')
    sheet_side.write(0, 2, 'back_num')
    sheet_side.write(0, 3, 'side_num')
    sheet_side.write(0, 4, 'img_num')
    sheet_side.write(0, 5, 'recall')
    sheet_back = workbook.add_sheet('sheet_back')
    sheet_back.write(0, 1, 'front_num')
    sheet_back.write(0, 2, 'back_num')
    sheet_back.write(0, 3, 'side_num')
    sheet_back.write(0, 4, 'img_num')
    sheet_back.write(0, 5, 'recall')

    # 写入数据
    for i in range(len(data_list)):
        name = data_list[i][0]
        if 'front' in name:
            sheet = sheet_front
        elif 'side' in name:
            sheet = sheet_side
        elif 'back' in name:
            sheet = sheet_back
        else:
            sheet = sheet_front
        for j in range(len(data_list[i])):
            sheet.write(i + 1, j, data_list[i][j])
        # sheet.write(i+1, 0, data_list[i][0])
        # sheet.write(i+1, 1, data_list[i][1])
        # sheet.write(i+1, 2, data_list[i][2])
        # sheet.write(i+1, 3, data_list[i][3])
        # sheet.write(i+1, 4, data_list[i][4])


    # 保存Excel文件
    workbook.save(excell_save_path)

def res(path):
    res = []
    res_num = []
    # 打开文件
    with open(path, 'r') as file:
        # 读取所有行并存储在列表中
        lines = file.readlines()
        # 去掉每行末尾的换行符
        lines = [line.strip() for line in lines]
        res_img = []
        is_save = False
        for line in lines:
            if ">>>>>> outputBoxes.size()" in line:
                if len(res_img) > 0 and is_save:
                    res.append(res_img)
                res_img = []
                is_save = True
            else:
                res_img.append(line)
    for r in res:
        side = 0
        front = 0
        back = 0
        for i in r:
            if "Side" in i:
                side = side + 1
            elif "Front" in i:
                front = front + 1
            elif "Back" in i:
                back = back + 1
            if "imageName =" in i:
                name = i.split("=")[1].split("<")[0]
        res_num.append({"front": front, "back": back, "side": side, "name": name})
    front_num = 0
    back_num = 0
    side_num = 0
    for r in res_num:
        front_num += r["front"]
        back_num += r["back"]
        side_num += r["side"]
        # print(r)
    name = os.path.basename(path).replace('.txt', '')
    img_num = len(res_num)
    print('----------------------------------------')
    print(name)
    print("front_num: ", front_num)
    print("back_num: ", back_num)
    print("side_num: ", side_num)
    print(img_num)
    return name,front_num, back_num, side_num,img_num
if __name__ == '__main__':
    dir_path = "./tcl_pedestrian"
    excell_save_path = dir_path.replace('./tcl_pedestrian','') + '-res.xls'
    excell_save_path = excell_save_path.replace('_','')
    data_list = []
    # res("/home/spring/PycharmProjects/pythonProject/tcl_pedestrian/side_1_near.txt")
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith(".txt"):
                name,front_num, back_num, side_num,img_num = res(os.path.join(root, file))
                person_num = (front_num + side_num + back_num)
                person_num = max(person_num,0.001)  # 防止0作为除数
                if 'front' in name:
                    recall = front_num / person_num
                elif 'side' in name:
                    recall = side_num / person_num
                elif 'back' in name:
                    recall = back_num / person_num
                else:
                    recall = max(front_num, side_num, back_num) / person_num
                data_list.append([name,front_num, back_num, side_num,img_num,recall])
    export_excell(data_list,excell_save_path)