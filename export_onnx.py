import paddle2onnx
from paddle.inference import Config, Predictor
import os
# 模型路径
model_dir = 'path/to/your/model'  # 例如'inference_model'
# Paddle模型参数文件
model_file = os.path.join(model_dir, 'model.pdmodel')
# Paddle参数权重文件
params_file = os.path.join(model_dir, 'model.pdiparams')
# 导出的ONNX模型文件
onnx_file = 'model.onnx'

# 创建Paddle预测器
config = Config(model_file, params_file)
config.enable_int8 = True
# 设置int8的calibraion数据
config.set_int8_calibrator(your_calibrator)  # 替换为你的校准器
predictor = create_predictor(config)

# 导出ONNX模型
paddle2onnx.command_line.main(
    [
        "--model_dir", model_dir,
        "--model_filename", "model.pdmodel",
        "--params_filename", "model.pdiparams",
        "--save_file", onnx_file,
        "--opset_version", "10",  # 根据需要选择合适的opset版本
        "--enable_int8", "True",
        "--int8_calib_dataset", "path/to/calibration/dataset",  # 校准数据集路径
        "--int8_scale_range", "127.0",  # 可以是'max'或具体的数值
    ]
)