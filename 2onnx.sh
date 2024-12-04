#!/bin/bash
if [ $# -lt 1 ]; then
    echo "Usage: $0 <model_name> "
    exit 1
fi
command0="conda activate pulc"
command1="python tools/export_model.py \
   -c /mnt/sda2/code/PaddleClas/ppcls/configs/PULC/person_attribute/PPLCNet_x1_0_rubby.yaml \
   -o Global.pretrained_model=/mnt/sda2/code/PaddleClas/tools/$1/best_model/model.pdparams  \
   -o Global.save_inference_dir=/mnt/sda2/code/PaddleClas/deploy/models/$1"
command2="paddle2onnx --model_dir /mnt/sda2/code/PaddleClas/deploy/models/$1 \
          --model_filename /mnt/sda2/code/PaddleClas/deploy/models//$1/inference.pdmodel \
         --params_filename /mnt/sda2/code/PaddleClas/deploy/models/$1/inference.pdiparams \
	--save_file /mnt/sda2/code/PaddleClas/deploy/models/$1/$1.onnx"
command3="python onnx_input_size.py --onnx_path /mnt/sda2/code/PaddleClas/deploy/models/$1/$1.onnx"
echo $command0
eval $command0
echo $command1
eval $command1
echo $command2
eval $command2
echo $command3
eval $command3