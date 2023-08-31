from DCMToAVI_v2 import DCMInit
from VideoInformation import VideoInit
from Segmentation import Segment
import Matching_v2
import Matching

import os
import time
import cv2

# 對應 information.py 裡面的內容


def _TotalFiles(InputDCMDir):
    DCMList = list()
    for root, dirs, files in os.walk(InputDCMDir):
        for f in files:
            if f[-3:].lower() == 'dcm':
                DCMList.append(os.path.join(root, f))
    return DCMList


def CtrlProcess(InputDCMDir, OutputAVIDir, OutputSkeletonizeDir, OutputSegmentDir, OutputMatchingDir):
    """
    function:
        CtrlProcess(InputDCMDir, OutputAVIDir, OutputSkeletonizeDir, OutputSegmentDir)
        處理到目前為止的系統模組流程

    parameters:
        InputDCMDir: DCM 檔案的資料夾路徑, str
        OutputAVIDir: 輸出存放 avi 檔案的資料夾路徑, str
        OutputSkeletonizeDir: 輸出存放骨架圖檔案的資料夾路徑, str
        OutputSegmentDir: 輸出存放定義完瓣膜和腔室的影片資料夾路徑, str
        OutputMatchingDir: 輸出存放定 matching 的影片資料夾路徑, str
    """

    # 1. DCMToAVI OK
    TotalProcessTimeStart = time.time()
    DCMTimeStart = time.time()

    DCMFiles = _TotalFiles(InputDCMDir)
    FileCount = 0

    for DCMPath in DCMFiles:
        CurrProcessTimeStart = time.time()
        DCMTimeStart = time.time()
        DCMInfo = DCMInit(
            FilePath=DCMPath,
            OutputDir=OutputAVIDir
        )

        # 病人資訊
        PatientInfo = DCMInfo.TotalPatientInfo
        DCMTimeEnd = time.time()

        # print(f'PatientInfo: {PatientInfo}')
        print(f'===== DCM 轉檔花費時間: {round(DCMTimeEnd - DCMTimeStart, 2)} 秒 =====')

        # 2. 使用 AVI 檔案做影像處理
        FileCount += 1
        print(f'FileCount: {FileCount}')
        Path = DCMInfo.AVIPath
        FileName = str(Path.split('\\')[-1]).replace('DCM', 'avi')

        # 處理 2-1.A, 2-1.B, 2-1.D; Doppler 之後處理
        VideoInitTimeStart = time.time()
        Video = VideoInit(
            VideoPath=Path,
            OutputSkeletonDir=OutputSkeletonizeDir
        )

        # if PatientInfo[FileName]["BPM"] == 0:
        #     PatientInfo[FileName]["BPM"] = Video.UnitBPM
        # PatientInfo[FileName]["CM"] = Video.UnitCM
        VideoInitTimeEnd = time.time()
        print(f'===== 完成 {FileName} VideoInformation 所需時間: {round(VideoInitTimeEnd - VideoInitTimeStart, 2)} 秒 =====')

        # 骨架圖
        SegmentTimeStart = time.time()
        SkeletonizePath = Video.OutputSkeletonDir + FileName + '.png'
        try:
            skeleton = cv2.imread(SkeletonizePath)

        except cv2.error:
            print(f'{SkeletonizePath}, 沒有找到該檔案的骨架圖')
            continue

        try:
            segment = Segment(
                VideoPath=Path,
                ROI=Video.roi,
                OutputSegDir=OutputSegmentDir
            )
            segment.HandleHeartBound(skeleton)

        except ValueError:
            print(f'{SkeletonizePath}, 該骨架圖可能為全黑的')
            continue

        # Segment: Semantic 腔室位置 & 二尖瓣位置
        try:
            segment.Semantic_FindValve(isOutputValveVideo=False, isOutputSegVideo=False)

        except (IndexError, ValueError):
            print(f'{Path}, 統計腔室中心點有問題, 檢查該影片 distance transform 的過程')
            continue

        SegmentTimeEnd = time.time()
        print(f'===== 完成 {FileName} Segment 所需時間: {round(SegmentTimeEnd - SegmentTimeStart, 2)} 秒 =====')

        # Matching LV Muscle
        matchingTimeStart = time.time()
        try:
            matchLV = Matching.MatchModel(
                Path=Path,
                roi=Video.roi,
                roi_center=(Video.ox, Video.oy),
                OutputMatchingDir=OutputMatchingDir
            )

            LeftValve, RightValve = segment.LeftPivotList, segment.RightPivotList
            matchLV.MuscleMatching(LeftValve, RightValve, isOutputVideo=True)

        except:
            print(f'{Path} Matching 到 Fitting 過程有狀況')
            continue

        matchingTimeEnd = time.time()
        print(f'===== 完成 {FileName} Matching 所需時間: {round(matchingTimeEnd - matchingTimeStart, 2)} 秒 =====')

        CurrProcessTimeEnd = time.time()
        print(f'===== 處理 {FileName} 所需時間: {round(CurrProcessTimeEnd - CurrProcessTimeStart, 2)} 秒 =====')

    print('\n')
    TotalProcessTimeEnd = time.time()
    print(f'處理所有資料集所需時間: {round(TotalProcessTimeEnd - TotalProcessTimeStart, 2)} 秒')

