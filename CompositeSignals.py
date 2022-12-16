import numpy as np
import os
import argparse
from tqdm import tqdm
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False #用来正常显示负号
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

def CompositeSignals(MobileEmg, MobileImu, StationaryEmg, StationaryImu):
    return MobileEmg + StationaryEmg, MobileImu + StationaryImu



if __name__ == "__main__":
    DataStretch = Stretch(4)
    DataNormalization = Normalization()

    with open("D:/张江涛/GitHub/Mobile-Scenarios-SLR/Config/" + opt.Mobile + "StationaryDataNames.txt", "r") as StationaryFile:
        StationaryDataNames = eval(StationaryFile.readline())

    MobileDataPath = 'D:/张江涛/手势数据集/移动场景下的手语翻译数据集/' + opt.Mobile + '/emg/'
    StationaryDataPath = 'D:/张江涛/手势数据集/移动场景下的手语翻译数据集/stationary/emg/'
    MobileFilenames = os.listdir(MobileDataPath)
    MobileDataNmaes = []
    for MobileFilename in MobileFilenames:
        if "0000" in MobileFilename:
            MobileDataNmaes.append(MobileFilename)
    
    for StationaryDataName, _ in zip(StationaryDataNames, tqdm(range(len(StationaryDataNames)))):
        StationaryEmgPath = StationaryDataPath + StationaryDataName
        StationaryImuPath = StationaryEmgPath.replace('emg', "imu")
        StationaryEmg = ReadFile(StationaryEmgPath, DataType= "int")
        StationaryImu = ReadFile(StationaryImuPath, DataType= "float")
        StationaryEmgCut, StationaryImuCut = cut_data(StationaryEmg, StationaryImu)
        StationaryEmgStretch, StationaryImuStretch =  DataStretch.stretch(StationaryEmgCut, StationaryImuCut)

        for MobileDataName in MobileDataNmaes:
            if MobileDataName.split('_')[-3] == StationaryDataName.split('_')[-3]:
                MobileEmgPath = MobileDataPath + MobileDataName
                MobileImuPath = MobileEmgPath.replace('emg', "imu")
                MobileEmg = ReadFile(MobileEmgPath, DataType= "int")
                MobileImu = ReadFile(MobileImuPath, DataType= "float")
                MobileEmgCut, MobileImuCut = cut_data(MobileEmg, MobileImu)
                MobileEmgStretch, MobileImuStretch =  DataStretch.stretch(MobileEmgCut, MobileImuCut)
                CompositeEmg, CompositeImu = CompositeSignals(MobileEmgStretch, MobileImuStretch, StationaryEmgStretch, StationaryImuStretch)
                CompositeEmgNorm, CompositeImuNorm = DataNormalization.MaxMinNorm(CompositeEmg, CompositeImu)
                FigurePath = 'D:/张江涛/GitHub/Mobile-Scenarios-SLR/Result/composite/' + opt.Mobile + '/' + StationaryDataName.split('_')[0] + \
                 '_' +  StationaryDataName.split('_')[-3] + '_S' + StationaryDataName.split('_')[-2] + '_M' + MobileDataName.split('_')[-2]
                FigureShow(CompositeEmgNorm, CompositeImuNorm, FigurePath)