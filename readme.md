## Livox Detection-simu V1.0: Trained on Simulated Data, Tested in the Real World [\[Livox Simu-dataset\]](https://livox-wiki-en.readthedocs.io/en/latest/data_summary/dataset.html#livox-simu-dataset-v1-0-cn)
## Introduction
Livox Detection-simu is a robust and real-time detection package trained on [Livox Simu-dataset](https://livox-wiki-en.readthedocs.io/en/latest/data_summary/dataset.html#livox-simu-dataset-v1-0-cn). It only uses 14k frames of simulated data for training, and performs effective detection in the real world. The inference time is about 50ms on 2080Ti for 200m*100m range detection.   
We hope this project can help you make better use of [Livox Simu-dataset](https://livox-wiki-en.readthedocs.io/en/latest/data_summary/dataset.html#livox-simu-dataset-v1-0-cn). In order to improve the performance of the detector, data augmentation such as object insertion and background mix-up is necessary. 

## Demo
<div align="center"><img src="./res/demo1.gif" width=90% /></div>



## Dependencies
- `python3.6+`
- `tensorflow1.13+` (tested on 1.13.0)
- `pybind11`
- `ros`

## Installation

1. Clone this repository.
2. Clone `pybind11` from [pybind11](https://github.com/pybind/pybind11).
```bash
$ cd utils/lib_cpp
$ git clone https://github.com/pybind/pybind11.git
```
3. Compile C++ module in utils/lib_cpp by running the following command.
```bash
$ mkdir build && cd build
$ cmake -DCMAKE_BUILD_TYPE=Release ..
$ make
```
4. copy the `lib_cpp.so` to root directory:
```bash
$ cp lib_cpp.so ../../../
```

5. Download the [pre_trained model](https://terra-1-g.djicdn.com/65c028cd298f4669a7f0e40e50ba1131/Download/dataset/livox_detection_simu_model.zip) and unzip it to the root directory.

## Run

### For sequence frame detection

Download the provided rosbags : [rosbag](https://terra-1-g.djicdn.com/65c028cd298f4669a7f0e40e50ba1131/github/livox_detection_v1.1_data.zip) and then

```bash
$ roscore

$ rviz -d ./config/show.rviz

$ python livox_detection_simu.py

$ rosbag play *.bag -r 0.1
```
The network inference time is around `25ms`, but the point cloud data preprocessing module takes a lot of time based on python. If you want to get a faster real time detection demo, you can modify the point cloud data preprocessing module with c++.

To play with your own rosbag, please change your rosbag topic to `/livox/lidar`.

## Support
You can get support from Livox with the following methods :
- Send email to dev@livoxtech.com with a clear description of your problem and your setup
- Report issue on github
