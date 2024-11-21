import os
import onnxruntime
import numpy as np
import cv2
import shutil
import math


def infer_similar_between_two_rois():
    
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


#单张图片的推理朝向
def infer_roi_towards(input_data, session):
    res = 0
    input_data = np.transpose(input_data, (2, 0, 1))
    input_data = transform_image(input_data)
    input_data = np.expand_dims(input_data, axis=0)
    input_data = input_data.astype(np.float32)
    # 运行模型进行推理
    output = session.run([], {"x": input_data})
    # 输出结果
    res = output[0][:,-3:][0]
    return res


if __name__ == '__main__':
    
    ONNX_FILE_PATH = "../model-release/2.1/person_attentive.onnx"
    DATA_SOURCE_PATH_FORMAT = "res/input_imgs"

    #当前源数据集的output目录
    DATA_SOURCE_BASE_PATH = "/home/leon/mount_point_d/test-result-moved/reid_datas/reid_datas_pick/20241025_tck_datas/output"
    #指定目录
    DATA_SOURCE_MID_PATHS = ['20241025_tck_lxy_0'] 
    #全部子目录 DATA_SOURCE_MID_PATHS = next(os.walk(DATA_SOURCE_BASE_PATH))[1]

    if len(DATA_SOURCE_MID_PATHS) < 1:
        print("data sub-paths not exists. {}".format(DATA_SOURCE_BASE_PATH))
        exit(-1)

    #当前朝向分类数据集保存的顶层目录
    ANNO_DATA_BASE_PATH = "/home/leon/mount_point_d/test-result-moved/peson-attr-train-test-data/datasets/train_iter/person_towards_reid_cap_reuse1112"
    
    if not os.path.exists(ANNO_DATA_BASE_PATH):
        print("save path not exists. {}".format(ANNO_DATA_BASE_PATH))
        exit(-1)
    
    np.set_printoptions(suppress=True)
    session = onnxruntime.InferenceSession(ONNX_FILE_PATH)
    print("onnx loaded: {}".format(ONNX_FILE_PATH))

    class_names = ['front', 'side','back']
    target_classes_path = list()
    
    for c in class_names:
        c_path = os.path.join(ANNO_DATA_BASE_PATH,c)
        target_classes_path.append(c_path)
        
    for c in target_classes_path:
        if not os.path.exists(c):
            os.makedirs(c)
        print("save path prepared. {}".format(c))

    for m in DATA_SOURCE_MID_PATHS:
        
        current_directory = os.path.join(DATA_SOURCE_BASE_PATH, m, DATA_SOURCE_PATH_FORMAT)
        files_and_dirs = os.listdir(current_directory)
        jpg_files = [f for f in files_and_dirs if f.endswith('.jpg')]
        cped_number = 0
        front_counter = 0
        side_conter = 0
        back_conter = 0
        for j in jpg_files:
            source_path = os.path.join(current_directory, j)

            input_data_src_size = cv2.imread(source_path)
            width, height = 192, 256
            resize_dim = (width, height)
            input_data = cv2.resize(input_data_src_size, resize_dim)
            cls_index = infer_roi_towards(input_data, session)
            cls_index = np.argmax(cls_index)
            
            pred_cls_path = target_classes_path[cls_index]
            if cls_index == 0:
                front_counter = front_counter + 1
            if cls_index == 1:
                side_conter = side_conter + 1
            if cls_index == 2:
                back_conter = back_conter + 1
            towards_mid_path = os.path.join(pred_cls_path, m)
            if not os.path.exists(towards_mid_path):
                os.makedirs(towards_mid_path)
            for q_type in ['normal', 'special']:
                if not os.path.exists(os.path.join(towards_mid_path, q_type)): 
                    os.makedirs(os.path.join(towards_mid_path, q_type))
            towards_mid_path = os.path.join(towards_mid_path, 'normal')

            destination_path = os.path.join(towards_mid_path, j)
            # shutil.copy2(source_path, destination_path)
            cv2.imwrite(destination_path, input_data)
            cped_number = cped_number + 1
        
        print("processed path {}; {} v.s. {}".format(current_directory, len(jpg_files), cped_number))
        print("front {} ; side {} ; back {} = {} ".format(front_counter, side_conter, back_conter, (back_conter+side_conter+front_counter)))
        
    print("Finished towards classify.")


