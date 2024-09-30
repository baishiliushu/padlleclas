# Copyright (c) 2021 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os
import time
import platform

import numpy as np
import paddle
import cv2
from ppcls.utils.misc import AverageMeter
from ppcls.utils import logger
# from save_img import save_res
def save_res(image,id,label,save_path):
    # image hwc
    id = id.numpy()
    id = np.argmax(id)
    if id == 0:
        id = "Z"
    elif id == 1:
        id = "C"
    elif id == 2:
        id = "B"
    label = label.numpy()
    label = np.argmax(label)
    if label == 0:
        label = "Z"
    elif label == 1:
        label = "C"
    elif label == 2:
        label = "B"
    if id != label:

        root,name = os.path.split(save_path)
        os.makedirs(os.path.join(root,"bad"), exist_ok=True)
        save_path = os.path.join(root,"bad",name)
    elif id == label:
        root,name = os.path.split(save_path)
        os.makedirs(os.path.join(root,"good"), exist_ok=True)
        save_path = os.path.join(root,"good",name)
    id = id + label
    height, width, _ = image.shape
    center_x = width // 2
    center_y = height // 2# 添加序号
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 2
    font_color = (255, 255, 255)
    thickness = 8
    image = (image - image.min()) / (image.max() - image.min())
    image = (image * 255).astype("uint8")
    image = np.ascontiguousarray(image)
    cv2.putText(image, id, (center_x, center_y), font, font_scale, font_color, thickness, cv2.LINE_AA)# 显示或保存图像
    # cv2.imshow('Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    cv2.imwrite(save_path, image)
def denormalize(tensor_normalized, mean, std):
    # 将归一化的张量恢复成原始像素值
    tensor_original = (tensor_normalized * std[:, None, None]) + mean[:, None, None]
    return tensor_original





def classification_eval(engine, epoch_id=0):
    if hasattr(engine.eval_metric_func, "reset"):
        engine.eval_metric_func.reset()
    output_info = dict()
    time_info = {
        "batch_cost": AverageMeter(
            "batch_cost", '.5f', postfix=" s,"),
        "reader_cost": AverageMeter(
            "reader_cost", ".5f", postfix=" s,"),
    }
    print_batch_step = engine.config["Global"]["print_batch_step"]

    tic = time.time()
    accum_samples = 0
    total_samples = len(
        engine.eval_dataloader.
        dataset) if not engine.use_dali else engine.eval_dataloader.size
    max_iter = len(engine.eval_dataloader) - 1 if platform.system(
    ) == "Windows" else len(engine.eval_dataloader)
    for iter_id, batch in enumerate(engine.eval_dataloader):
        if iter_id >= max_iter:
            break
        if iter_id == 5:
            for key in time_info:
                time_info[key].reset()

        time_info["reader_cost"].update(time.time() - tic)
        batch_size = batch[0].shape[0]
        batch[0] = paddle.to_tensor(batch[0])
        if not engine.config["Global"].get("use_multilabel", False):
            batch[1] = batch[1].reshape([-1, 1]).astype("int64")

        # image input
        with engine.auto_cast(is_eval=True):
            out = engine.model(batch[0])

        # just for DistributedBatchSampler issue: repeat sampling
        current_samples = batch_size * paddle.distributed.get_world_size()
        accum_samples += current_samples

        if isinstance(out, dict) and "Student" in out:
            out = out["Student"]
        if isinstance(out, dict) and "logits" in out:
            out = out["logits"]

        # gather Tensor when distributed
        if paddle.distributed.get_world_size() > 1:
            label_list = []
            device_id = paddle.distributed.ParallelEnv().device_id
            label = batch[1].cuda(device_id) if engine.config["Global"][
                "device"] == "gpu" else batch[1]
            paddle.distributed.all_gather(label_list, label)
            labels = paddle.concat(label_list, 0)

            if isinstance(out, list):
                preds = []
                for x in out:
                    pred_list = []
                    paddle.distributed.all_gather(pred_list, x)
                    pred_x = paddle.concat(pred_list, 0)
                    preds.append(pred_x)
            else:
                pred_list = []
                paddle.distributed.all_gather(pred_list, out)
                preds = paddle.concat(pred_list, 0)

            if accum_samples > total_samples and not engine.use_dali:
                if isinstance(preds, list):
                    preds = [
                        pred[:total_samples + current_samples - accum_samples]
                        for pred in preds
                    ]
                else:
                    preds = preds[:total_samples + current_samples -
                                  accum_samples]
                labels = labels[:total_samples + current_samples -
                                accum_samples]
                current_samples = total_samples + current_samples - accum_samples
        else:
            labels = batch[1]
            preds = out
            # 人体朝向
            labels = labels[:,:,23:]
            preds = preds[:,23:]
        save_img = True
        if save_img:
            save_path = '/mnt/sda3/persson_test/person_test_0819_20(0813)/'
            img_id = 0
            for img_save,pred,label in zip(batch[0], preds,labels):
                mean = np.array([0.485, 0.456, 0.406])
                std = np.array([0.229, 0.224, 0.225])
                # img_save = denormalize(img_save, mean, std)
                img_save = img_save.numpy()

                # 更改通道顺序从 (channels, height, width) 到 (height, width, channels)
                img_save = img_save.transpose(1, 2, 0)
                img_path = os.path.join(save_path, str(iter_id)+"_"+str(img_id) + '.jpg')
                save_res(img_save,pred,label,img_path)
                # print(img_path)
                img_id += 1

        # calc loss
        if engine.eval_loss_func is not None:
            with engine.auto_cast(is_eval=True):
                loss_dict = engine.eval_loss_func(preds, labels)

            for key in loss_dict:
                if key not in output_info:
                    output_info[key] = AverageMeter(key, '7.5f')
                output_info[key].update(float(loss_dict[key]), current_samples)

        #  calc metric
        if engine.eval_metric_func is not None:
            engine.eval_metric_func(preds, labels)
        time_info["batch_cost"].update(time.time() - tic)

        if iter_id % print_batch_step == 0:
            time_msg = "s, ".join([
                "{}: {:.5f}".format(key, time_info[key].avg)
                for key in time_info
            ])

            ips_msg = "ips: {:.5f} images/sec".format(
                batch_size / time_info["batch_cost"].avg)

            if "ATTRMetric" in engine.config["Metric"]["Eval"][0]:
                metric_msg = ""
            else:
                metric_msg = ", ".join([
                    "{}: {:.5f}".format(key, output_info[key].val)
                    for key in output_info
                ])
                if "MultiLabelMAP" not in engine.config["Metric"]["Eval"][0]:
                    metric_msg += ", {}".format(engine.eval_metric_func.avg_info)
            logger.info("[Eval][Epoch {}][Iter: {}/{}]{}, {}, {}".format(
                epoch_id, iter_id,
                len(engine.eval_dataloader), metric_msg, time_msg, ips_msg))

        tic = time.time()
    if engine.use_dali:
        engine.eval_dataloader.reset()

    if "ATTRMetric" in engine.config["Metric"]["Eval"][0]:
        metric_msg = ", ".join([
            "evalres: ma: {:.5f} label_f1: {:.5f} label_pos_recall: {:.5f} label_neg_recall: {:.5f} instance_f1: {:.5f} instance_acc: {:.5f} instance_prec: {:.5f} instance_recall: {:.5f}".
            format(*engine.eval_metric_func.attr_res())
        ])
        logger.info("[Eval][Epoch {}][Avg]{}".format(epoch_id, metric_msg))

        # do not try to save best eval.model
        if engine.eval_metric_func is None:
            return -1
        # return 1st metric in the dict
        return engine.eval_metric_func.attr_res()[0]
    else:
        metric_msg = ", ".join([
            "{}: {:.5f}".format(key, output_info[key].avg)
            for key in output_info
        ])
        metric_msg += ", {}".format(engine.eval_metric_func.avg_info)
        logger.info("[Eval][Epoch {}][Avg]{}".format(epoch_id, metric_msg))

        # do not try to save best eval.model
        if engine.eval_metric_func is None:
            return -1
        # return 1st metric in the dict
        return engine.eval_metric_func.avg
