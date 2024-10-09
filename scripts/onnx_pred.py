import os
import onnxruntime
import numpy as np
import cv2
from tqdm import tqdm
import math
"""
onnx_path:onnx路径
dataset_path:测试集的路径
save_path:图片结果保存路径
save_img_res:是否保存图片结果
thr:置信度阈值
"""
# onnx_path = "/mnt/sda2/code/tools/onnx/person_attentive_122.onnx"
# dataset_path = '/home/spring/dataset/person_0906_test_near'
# save_path = '/mnt/sda3/persson_test_onnx'
onnx_path = ''
dataset_path = ''
save_path = ''
save_img_res = True
thr = 0
save_path = os.path.join(save_path, dataset_path.split('/')[-1] + '_' + os.path.split(onnx_path)[-1].replace('.onnx','') + '_thr_' + str(thr))
session = onnxruntime.InferenceSession(onnx_path)

class_names = ['front', 'side','back']
# 准备输入数据，这里需要根据你的模型来准备

def save_res(image,id,label,save_path,res,thr,all_res_path):
    # 获取置信度
    # res = np.round(res, decimals=2)
    conf_z = 'z:' + str(res[0])
    conf_c = 'c:' + str(res[1])
    conf_b = 'b:' + str(res[2])
    # image hwc

    if id == 0:
        id = "Z"
        if res[0]  < thr:
            return False
    elif id == 1:
        id = "C"
        if res[1] < thr:
            return False
    elif id == 2:
        id = "B"
        if res[2] < thr:
            return False
    if label == 0:
        label = "Z"
    elif label == 1:
        label = "C"
    elif label == 2:
        label = "B"
    if id != label:
        font_color = (0, 64, 215)
        root,name = os.path.split(save_path)
        os.makedirs(os.path.join(root,"bad"), exist_ok=True)
        save_path = os.path.join(root,"bad",name)
    elif id == label:
        font_color = (170, 178, 32)
        root,name = os.path.split(save_path)
        os.makedirs(os.path.join(root,"good"), exist_ok=True)
        save_path = os.path.join(root,"good",name)
    id = id
    height, width, _ = image.shape
    center_x = width // 2
    center_y = height // 2# 添加序号
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 2

    thickness = 8
    image = (image - image.min()) / (image.max() - image.min())
    image = (image * 255).astype("uint8")
    image = np.ascontiguousarray(image)


    cv2.putText(image, id, (center_x, center_y), font, font_scale, font_color, thickness, cv2.LINE_AA)# 显示或保存图像
    cv2.putText(image, conf_z, (10, 20), font, 0.5, font_color, 1, cv2.LINE_AA)
    cv2.putText(image, conf_c, (10, 35), font, 0.5, font_color, 1, cv2.LINE_AA)
    cv2.putText(image, conf_b, (10, 50), font, 0.5, font_color, 1, cv2.LINE_AA)
    # cv2.imshow('Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # os.makedirs(all_res_path, exist_ok=True)
    if save_img_res:
        cv2.imwrite(all_res_path, image)
        cv2.imwrite(save_path, image)
    return True
def num(num):
    if 'e-0' in num:
        a,b = num.split('e-0')
        a1,a2 = a.split('.')
        num = '0.' + '0' * (int(b) - 1) + a1 + a2
    return num
def transform_image(image):
    mean = [0.485, 0.456, 0.406]
    std = [0.229, 0.224, 0.225]
    mean = np.array(mean)
    std = np.array(std)
    image = image / 255.0
    image = np.transpose(image, (1, 2, 0))
    image = (image - mean) / std
    image = np.transpose(image, (2, 0, 1))
    return image
def softmax(x) -> int:
  if x.ndim == 2:
    x = x-x.max(axis=1, keepdims=True)
    x = np.exp(x)
    x /= x.sum(axis=1, keepdims=True)
  elif x.ndim == 1:
    x = x-np.max(x)
    x = np.exp(x) / np.sum(np.exp(x))
  return x
# 创建会话并加载ONNX模型

tp = 0
fp = 0
save_txt = False
np.set_printoptions(suppress=True)
recall = []
for root, dirs, files in os.walk(dataset_path):
    good = 0
    bad = 0
    for file in tqdm(files):

        lines = []
        if not file.endswith(".jpg"):
            continue
        # print(os.path.join(root, file))
        input_data = cv2.imread(os.path.join(root, file))
        input_data = np.transpose(input_data, (2, 0, 1))
        input_data = transform_image(input_data)
        input_data = np.expand_dims(input_data, axis=0)
        input_data = input_data.astype(np.float32)
        # 运行模型进行推理
        output = session.run([], {"x": input_data})
        for r in output[0][0]:
            # r = np.around(r, decimals=7)
            # r = math.ldexp(r, 0)
            r = str(r)
            r = num(r)
            lines.append(r)

        # 输出结果
        res = output[0][:,-3:][0]
        # print(os.path.join(root, file))
        pred = class_names[np.argmax(res)]
        save_img = True
        if "front" in root:
            label = 0
        elif "side" in root:
            label = 1
        elif "back" in root:
            label = 2
        if save_img:
            img_save = input_data.reshape(3, 256, 192)
            # 更改通道顺序从 (channels, height, width) 到 (height, width, channels)
            img_save = img_save.transpose(1, 2, 0)
            dir_path_img = root.replace(dataset_path, '').replace('img','')
            img_path = os.path.join(save_path,dir_path_img[1:-1])
            img_path = os.path.join(img_path,file)
            all_save_path = os.path.join(save_path,'all')
            # 是否大于阈值
            os.makedirs(all_save_path, exist_ok=True)
            all_save_path = os.path.join(all_save_path,file)
            save_if = save_res(img_save, np.argmax(res), label, img_path,res,thr,all_save_path)
            # print(img_path)
        if save_if:
            if pred in os.path.join(root, file):
                tp += 1
                good += 1
            else:
                fp += 1
                bad += 1
        if save_txt:
            with open(os.path.join('./res',file.replace('.jpg', '.txt')), 'w') as file1:
                for line in lines:
                    file1.write(line)
                    file1.write('\n')
        if file.endswith(".jpg") and file == files[-1]:
            recall.append('-------------------------------------------------------')
            recall.append(img_path.split('/')[-2])
            if good + bad != 0:
                recall.append(good/(good+bad))
            else:
                recall.append("未检出")
print(tp, fp)
print(tp/(tp + fp))
for r in recall:
    print(r)
# with open(result_path, 'w') as file:
#     for line in lines:
#         file.write(line)
#         file.write('\n')