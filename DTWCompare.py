from dtaidistance import dtw
from dtaidistance import dtw_visualisation as dtwvis
import linecache
import time
import argparse
from tqdm import tqdm
import os
import numpy as np
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
from Analysis import DataPrePro
## 参数
parser=argparse.ArgumentParser()
parser.add_argument("--Mobile",type=str,default="down-the-stairs")
opt=parser.parse_args()


def CompareDim(Data):
    DataSort = sorted(Data,reverse =True)
    DimIndex = []
    for i in DataSort:
        DimIndex.append(list(Data).index(i)+1)
    return DimIndex
    


if __name__ == "__main__":
    ## 选取相同人的静态文件
    MobileDataPath = 'D:/张江涛/手势数据集/移动场景下的手语翻译数据集/' + opt.Mobile + '/emg/'
    StationaryDataPath = 'D:/张江涛/手势数据集/移动场景下的手语翻译数据集/stationary/emg/'
    CompareFilePath = "D:/张江涛/GitHub/Mobile-Scenarios-SLR/Config/" + opt.Mobile + "StationaryCompare.txt"
    CompareDimFilePath = "D:/张江涛/GitHub/Mobile-Scenarios-SLR/Config/" + opt.Mobile + "StationaryCompareDim.txt"
    MobileFilenames = os.listdir(MobileDataPath)

    with open("D:/张江涛/GitHub/Mobile-Scenarios-SLR/Config/" + opt.Mobile + "StationaryDataNames.txt", "r") as StationaryFile:
        StationaryFileNames = eval(StationaryFile.readline())

    StationaryDataNames = []
    Scales = []
    
    # with open(CompareFilePath, "w") as CompareFile:
    for StationaryFileName, _ in zip(StationaryFileNames, tqdm(range(len(StationaryFileNames)))):
        # StationaryEmgPath = StationaryDataPath + StationaryFileName
        # StationaryImuPath = StationaryEmgPath.replace('emg', "imu")
        # StationaryEmg = ReadFile(StationaryEmgPath, DataType= "int")
        # StationaryImu = ReadFile(StationaryImuPath, DataType= "float")
        StationaryDataNames.append(StationaryFileName.split('_')[0])
        Scales.append(StationaryFileName.split('_')[-3])
        # StationaryEmgNorm, StationaryImuNorm = DataPrePro(StationaryEmg, StationaryImu)
            
            # for MobileFilename in MobileFilenames:
            #     if MobileFilename.split('_')[-3] == StationaryFileName.split('_')[-3] and MobileFilename.split('_')[0] == StationaryFileName.split('_')[0]:
            #         MobileEmgPath = MobileDataPath + MobileFilename
            #         MobileImuPath = MobileEmgPath.replace('emg', "imu")
            #         MobileEmg = ReadFile(MobileEmgPath, DataType= "int")
            #         MobileImu = ReadFile(MobileImuPath, DataType= "float")
            #         MobileEmgNorm, MobileImuNorm = DataPrePro(MobileEmg, MobileImu)
            #         ## 按通道进行DTW对比
            #         emg_compare = []
            #         imu_compare = []

            #         for i in range(StationaryEmgNorm.shape[1]):
            #             distance, path = dtw.warping_paths(StationaryEmgNorm[:,i], MobileEmgNorm[:,i])
            #             emg_compare.append(distance)
            #         for i in range(StationaryImuNorm.shape[1]):
            #             distance, path = dtw.warping_paths(StationaryImuNorm[:,i], MobileImuNorm[:,i])
            #             imu_compare.append(distance)  
            #         print(StationaryFileName, " VS ", MobileFilename, file=CompareFile)
            #         print("emg_compare:\n", emg_compare, file=CompareFile)
            #         print("imu_compare:\n", imu_compare, file=CompareFile)

    # print(StationaryDataNames)
    # print(Scales)
    with open(CompareFilePath, "r") as CompareFile:
        CompareFileLen = len(CompareFile.readlines())

    with open(CompareDimFilePath, "w") as CompareDimFile:
        StationaryDataNames = list(set(StationaryDataNames))
        Scales = list(set(Scales))
        for StationaryDataName in StationaryDataNames:
            # print(StationaryDataName)
            for Scale in Scales:
                # print(Scale)
                emg_compares = np.zeros(8)
                imu_compares = np.zeros(10)
                count = 0
                for i in range(CompareFileLen):
                    if StationaryDataName in linecache.getline(CompareFilePath, i) and Scale in linecache.getline(CompareFilePath, i):
                        emg_compares = emg_compares + np.array(eval(linecache.getline(CompareFilePath, i+2)))
                        imu_compares = imu_compares + np.array(eval(linecache.getline(CompareFilePath, i+4)))
                        count += 1
                # print(count)
                # print(emg_compares)
                emgComapreDim = CompareDim(emg_compares)
                imuComapreDim = CompareDim(imu_compares)
                
                Fig = plt.figure()
                plt.plot(np.arange(8), emg_compares/count)
                plt.title(StationaryDataName + '_' + Scale + '_emg')
                plt.savefig("D:/张江涛/GitHub/Mobile-Scenarios-SLR/Result/"+ opt.Mobile + "/" + StationaryDataName + '_' + Scale + '_emg.png')

                Fig = plt.figure()
                plt.plot(np.arange(10), imu_compares/count)
                plt.title(StationaryDataName + '_' + Scale + '_imu')
                plt.savefig("D:/张江涛/GitHub/Mobile-Scenarios-SLR/Result/" + opt.Mobile + "/" + StationaryDataName + '_' + Scale + '_imu.png')

                print(StationaryDataName + '_' + Scale + '_emg:\n', emgComapreDim, file= CompareDimFile)
                print(StationaryDataName + '_' + Scale + '_imu:\n', imuComapreDim, file= CompareDimFile)



            



