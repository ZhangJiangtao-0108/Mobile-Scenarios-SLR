import numpy as np
import os
import argparse
from tqdm import tqdm
import sys
sys.path.append('../')
sys.path.append("D:/张江涛/GitHub/DataPreProcess_packages/DataPostProce")
sys.path.append("D:/张江涛/GitHub/DataPreProcess_packages/DataPreProce")
sys.path.append("D:/张江涛/GitHub/DataPreProcess_packages/DataStatistics")
sys.path.append("D:/张江涛/GitHub/Mobile-Scenarios-SLR")
from utils.ReadFile import ReadFile
from algorithm.cutting_algorithm import cut_data, Stretch
from algorithm.Normalization import Normalization
from Result.FigureShow import FigureShow
## 参数
parser=argparse.ArgumentParser()
parser.add_argument("--Mobile",type=str,default="walk")
opt=parser.parse_args()

def DataPrePro(emg, imu):
    DataStretch = Stretch(4)
    DataNormalization = Normalization()
    ## 将数据裁剪和拉伸
    emg_cut, imu_cut = cut_data(emg, imu)
    emg_stretch, imu_stretch = DataStretch.stretch(emg_cut, imu_cut)
    ## 将数据按照列归一化
    emg_norm, imu_norm = DataNormalization.MaxMinNorm(emg_stretch, imu_stretch)
    return emg_norm, imu_norm


if __name__ == "__main__":
    ## 选取相同人的静态文件
    MobileDataPath = 'D:/张江涛/手势数据集/移动场景下的手语翻译数据集/' + opt.Mobile + '/emg/'
    StationaryDataPath = 'D:/张江涛/手势数据集/移动场景下的手语翻译数据集/stationary/emg/'
    MobileFilenames = os.listdir(MobileDataPath)
    StationaryFilenames = os.listdir(StationaryDataPath)
    StationaryDataNames = []

    for MobileFilename, _ in zip(MobileFilenames, tqdm(range(len(MobileFilenames)))):
        sentence = MobileFilename.split('_')[0]
        scale = MobileFilename.split('_')[-3]
        for StationaryFilename in StationaryFilenames:
            if sentence in StationaryFilename and scale in StationaryFilename:
                StationaryDataNames.append(StationaryFilename)
    StationaryDataNames = list(set(StationaryDataNames))

    with open("D:/张江涛/GitHub/Mobile-Scenarios-SLR/Config/" + opt.Mobile + 'StationaryDataNames.txt', 'w') as SentenceFile:
        print(list(set(StationaryDataNames)), file= SentenceFile)

    ## 读取文件并画图展示
    for MobileFilename, _ in zip(MobileFilenames, tqdm(range(len(MobileFilenames)))):
        EmgPath = MobileDataPath + MobileFilename
        ImuPath = EmgPath.replace('emg', "imu")
        emg = ReadFile(EmgPath, DataType= "int")
        imu = ReadFile(ImuPath, DataType= "float")
        
        emg_norm, imu_norm = DataPrePro(emg, imu)
        ## 画图展示
        FigurePath = 'D:/张江涛/GitHub/Mobile-Scenarios-SLR/Result/' + opt.Mobile + "/" + MobileFilename.split('_')[0] \
                     + '_' +  MobileFilename.split('_')[-3] + '_' + MobileFilename.split('_')[-2]
        FigureShow(emg_norm, imu_norm, FigurePath)

    for StationaryFilename, _ in zip(StationaryDataNames, tqdm(range(len(StationaryDataNames)))):
        EmgPath = StationaryDataPath + StationaryFilename
        ImuPath = EmgPath.replace('emg', "imu")
        emg = ReadFile(EmgPath, DataType= "int")
        imu = ReadFile(ImuPath, DataType= "float")
        
        emg_norm, imu_norm = DataPrePro(emg, imu)
        ## 画图展示
        FigurePath = 'D:/张江涛/GitHub/Mobile-Scenarios-SLR/Result/stationary/' + StationaryFilename.split('_')[0] + \
                    '_' +  StationaryFilename.split('_')[-3] + '_' + StationaryFilename.split('_')[-2]
        FigureShow(emg_norm, imu_norm, FigurePath)










