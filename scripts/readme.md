## 一、数据集制作

​    1、运行img.py将图片提取出来
​    2、将文件夹根据朝向重命名，并放入front、back、side三个文件夹当中
​    3、将文件夹放到nfs上(sudo mount -t nfs 192.168.50.222:/home/leon/mount_point_two/rubby-data-track/nfs_label_work ~/nfs_client
)
​    放到  ~/nfs_client/postest_img （最好放到这里别随便改）
​    4、sh root@192.168.50.198
​        连接198服务器，进入 /root/liang/tcl_pedestrian
​        运行 ./run_batch_test.sh <input_dir>
​        如：./run_batch_test.sh /mnt/nfs_data/postest_img/dark
​        <input_dir> 为数据集在服务器上的路径
​        如果输入的数据集为 ~/nfs_client/postest_img/<input_dir> 输出结果在 ~/nfs_client/postest_res/<input_dir>
​    5、运行 generate_label.py 将第4步中的人体图片提取出来
​    6、运行 labeling.py 生成标注文件 生成的文件为 train.txt test.txt labels.txt 均保存在数据集的路径下
​        训练时使用 labels.txt 即可
​    （最好将数据放到固态里面，不然训练会很慢）

## 二、pdparams转onnx

​    运行 2onnx.sh <pdparams路径>
​    例如：
​        模型位置：/mnt/sda2/code/PaddleClas/tools/0902/best_model/model.pdparams
​        2onnx.sh 0902

## 三、onnx测试

​    运行 onnx_pred.py

## 四、onnx转nb

​    1、进入nfs路径 (sudo mount -t nfs 192.168.50.222:/home/leon/mount_point_d/test-result-moved ~/nfs_1 )
​        cd ~/nfs_1/acuity-toolkit-binary-6.24.7/person_towards
​    2、将person_attentive.onnx 放到 ~/nfs_1/acuity-toolkit-binary-6.24.7/person_towards/person_attentive.onnx
​    3、运行t=~/nfs_1/acuity-toolkit-binary-6.24.7
​        m=person_attentive
​    4、运行 ./0_import_model.sh $t $m
​        （在 ~/nfs_1/acuity-toolkit-binary-6.24.7/person_towards 下）
​    5、修改 person_attentive_inputmeta.yml 中的归一化参数，修改为：

```json
        mean:
        - 123.675
        - 116.28
        - 103.53
        scale:
        - 0.017124754
        - 0.017507003
        - 0.0174291940
```

​		add_preproc_node: true
​    6、运行 ./1_quantize_model_u16.sh $t $m
​    7、修改 person_attentive_postprocess_file.yml
​        add_preproc_node: true
​    8、运行 ./2_export_model.sh $t $m
​        结果会保存为 network_binary.nb

## 五、nb测试

​    1、将nb文件传到198服务器 root@192.168.50.198:/root/liang/tcl_pedestrian
​    2、将nb文件重命名为 person_attr.nb
​    3、运行 ./run_batch_test.sh <input_dir>
​    4、将 root@192.168.50.198:/root/liang/tcl_pedestrian 复制到本地
​    5、运行 res.py 结果保存为 .xls （tcl_pedestrian 文件夹 需要与 res.py 在同级目录下）
​        .xls 文件中会有3个sheet分别存放3个类别的测试结果