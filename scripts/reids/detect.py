import onnxruntime
import numpy as np
from scipy.spatial import distance
import cv2
import os

'''
 mean:
- 123.675
        - 116.28
        - 103.53
        scale:
        - 58.395
        - 57.12
        - 57.375
'''


MODEL_TYPE_IS_OSNET = True

def infer_img(img, onnx_model):
    # 读入测试图像
    img = cv2.imread(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (128, 256))
    img = img.astype(np.float32)
    img = (img / 255.0 - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]  # 图像归一化

    # 转换输入数据为ONNX模型的输入格式
    input_data = img.transpose((2, 0, 1)).reshape(1, 3, 256, 128)
    input_data = input_data.astype(np.float32)
    # 进行推理
    outputs = None
    if MODEL_TYPE_IS_OSNET :
        outputs = onnx_model.run(None, {"images": input_data})
    else:
        outputs = onnx_model.run(None, {"image": input_data})
    outputs = np.squeeze(outputs)
    return outputs
    
# 加载ONNX模型
model_path = "./osnet_x1_0_market_256x128_amsgrad_ep150_stp60_lr0.0015_b64_fb10_softmax_labelsmooth_flip.onnx"
if not MODEL_TYPE_IS_OSNET:
    model_path = './resnet18_128x256.onnx'
#"./osnet_x1_0_market_256x128_amsgrad_ep150_stp60_lr0.0015_b64_fb10_softmax_labelsmooth_flip.onnx"
#"./osnet_x1_0_msmt17_256x128_amsgrad_ep150_stp60_lr0.0015_b64_fb10_softmax_labelsmooth_flip.onnx"

onnx_model = onnxruntime.InferenceSession(model_path)

img_path = '/home/leon/mount_point_d/test-result-moved/reid_datas/20241025_model_compare/'
#'/home/leon/mount_point_d/test-result-moved/psl_off_testes/1104-new-models-2/kpts' 
#'/home/leon/mount_point_d/test-result-moved/reid_datas/20241025_model_compare/'

test_couple = [] #[['b1-3.jpg', 'e1-3.jpg'], ['b1-3.jpg', 'e1-3.jpg'] ,['b1-3.jpg', 'e1-3.jpg'] ]
outputs_couple = []

imgs_input = ['b1-3.jpg', 'e1-3.jpg'] 
# ['1730724752468.png', '1730724764071.png']  0.6
# ['1730724753439.png', '1730724765193.png'] 0.7
# '20_1714492880428949-1.jpg', '41_1714492901321631-2.jpg' (half v.s. body   -> 0.48 17.3 )
# '20_1714492880428949-1.jpg', '59_1714492859899564-1.jpg'
# '41_1714492901321631-1.jpg', '59_1714492859899564-1.jpg' (different people -> 0.52 16.0 )

outputs = list()

for i in imgs_input:
    o = infer_img(os.path.join(img_path, i), onnx_model)
    outputs.append(o)

if len(outputs) > 1:
    # 计算两个特征向量的余弦相似度
    dot_product = np.dot(outputs[0], outputs[1])
    norm_product = np.linalg.norm(outputs[0]) * np.linalg.norm(outputs[1])
    cosine_similarity = dot_product / norm_product
    ouler_distance = np.linalg.norm(outputs[0] - outputs[1])

    print("outputs0:{}\n{}".format(len(outputs[0]), outputs[0]))

    #print("outputs1:{}\n{}".format(len(outputs[1]), outputs[1]))

    print("Cosine similarity:{} ({} v.s. {})".format(cosine_similarity, imgs_input[0], imgs_input[1]))
    print("ouler distance:{} ({} v.s. {})".format(ouler_distance, imgs_input[0], imgs_input[1]))
    
print("Test on {}".format(model_path))


