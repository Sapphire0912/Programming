import FileIO
import DCMToAVI
import Preprocessing
import MultiThreshold as Mt
import A4CSegmentation
import A4CCardiacCycle
import A4CGLS
import IOUScore

import time
import cv2
import os


def Process(
        InputDCMDir,
        InputGTDir,
        OutputAVIDir,
        OutputSkeletonizeDir,
        OutputSegmentDir,
        OutputGLSDir
):

    """
    function:
        process(
            InputDCMDir,
            InputGTDir,
            OutputAVIDir,
            OutputSkeletonizeDir,
            OutputSegmentDir,
            OutputGLSDir
        ):
        控制系統的流程

    parameters:
        InputDCMDir: DCM 檔案的資料夾路徑, str
        InputGTDir: Ground Truth 的資料夾路徑, str
        OutputAVIDir: 輸出存放 avi 檔案的資料夾路徑, str
        OutputSkeletonizeDir: 輸出存放骨架圖檔案的資料夾路徑, str
        OutputSegmentDir: 輸出存放定義完瓣膜和腔室的影片資料夾路徑, str
        OutputGLSDir: 輸出存放 DLS 的影片資料夾路徑, str
    """

    # 1. DCMToAVI
    ProcessTime = time.time()
    DCMFiles = FileIO.AllFiles(InputDCMDir, 'dcm')
    if len(DCMFiles) == 0:
        raise ValueError(f"{InputDCMDir} 該路徑底下找不到有 DCM 的檔案.")

    FileCount = 0
    for DCMPath in DCMFiles:
        FileCount += 1

        print(f'FileCount: {FileCount}')
        print(f'----- 正在進行 {DCMPath} DCM 轉檔 -----')
        DCMStartTime = time.time()

        ConvertAVI = DCMToAVI.DCMInit(
            FilePath=DCMPath,
            OutputDir=OutputAVIDir
        )

        # 讀取 DCM 裡面的 cine rate & bpm
        CineRate, HeartRate = ConvertAVI.fps, ConvertAVI.bpm
        if CineRate is None:
            print(f'{DCMPath}, DCM 資訊裡沒有 Cine Rate 數值\n')
        if HeartRate is None:
            print(f'{DCMPath}, DCM 資訊裡沒有 Heart Rate 數值\n')

        DCMEndTime = time.time()
        print(f'===== DCM 轉檔花費時間: {round(DCMEndTime - DCMStartTime, 2)} 秒 =====\n')

        # 2. AVI 影片的預處理 (ROI & Skeletonize)
        PreStartTime = time.time()
        VideoPath = ConvertAVI.AVIPath
        FileName = str(VideoPath.split('\\')[-1]).replace('DCM', 'avi')
        CaseName = FileName[:-4]
        GTDir = os.path.join(InputGTDir, CaseName)
        print(f'----- 正在進行 {VideoPath} AVI 影像的預處理 -----')

        ROI = Preprocessing.ROI(VideoPath)  # return: roi, (ox, oy), radius
        Preprocessing.Skeletonize(VideoPath, OutputSkeletonizeDir)

        PreEndTime = time.time()
        print(f'===== 完成 {VideoPath} Preprocessing 所需時間: {round(PreEndTime - PreStartTime, 2)} 秒 =====\n')
        # 2. AVI 影片的預處理 (ROI & Skeletonize) End.

        # 3. A4C Segmentation
        SegmentStartTime = time.time()
        SkeletonPath = OutputSkeletonizeDir + FileName + '.png'
        try:
            skeleton = cv2.imread(SkeletonPath)

        except cv2.error:
            print(f'{SkeletonPath}, 沒有找到該檔案的骨架圖')
            continue

        try:
            Segment = A4CSegmentation.Segment(
                VideoPath=VideoPath,
                ROI=ROI,
                OutputSegDir=OutputSegmentDir
            )
            Segment.HandleHeartBound(skeleton)

        except ValueError:
            print(f'{SkeletonPath}, 該骨架圖可能為全黑的')
            continue

        try:
            Segment.Semantic_FindValve(isOutputSegVideo=False)

        except (IndexError, ValueError, ZeroDivisionError):
            print(f'{VideoPath}, 統計腔室中心點有問題, 檢查該影片 distance transform 的過程')
            continue

        SegmentEndTime = time.time()
        print(f'===== 完成 {FileName} Segment 所需時間: {round(SegmentEndTime - SegmentStartTime, 2)} 秒 =====\n')
        # 3. A4C Segmentation End.

        # 4. E/A Ratio <- current cardiac cycle
        # period = A4CCardiacCycle.CardiacCycle(
        #     VideoPath=VideoPath,
        #     ROI=ROI,
        #     LeftValvePos=Segment.LeftPivotList,
        #     RightValvePos=Segment.RightPivotList
        # )
        # period.Wave()

        # 4. Global Longitudinal Strain
        # MatchingStartTime = time.time()
        # print(f'----- 正在進行 {VideoPath} Global Longitudinal Strain 的 Muscle Semantic 處理 -----')
        #
        # try:
        #     MatchLV = A4CGLS.MatchModel(
        #         Path=VideoPath,
        #         ROI=ROI,
        #         OutputMatchingDir=OutputGLSDir
        #     )
        #     LeftValve, RightValve = Segment.LeftPivotList, Segment.RightPivotList
        #     MatchLV.MuscleMatching(LeftValve, RightValve, isOutputVideo=True)
        #
        # except:  # 通常是 fitting 會有狀況
        #     print(f'{VideoPath} Matching 到 Fitting 過程有狀況 (未處理)')
        #     continue
        #
        # MatchingEndTime = time.time()
        # print(f'===== 完成 {FileName} Muscle Semantic 所需時間: {round(MatchingEndTime - MatchingStartTime, 2)} 秒 =====\n')

        # 4. 計算 LVEF
        pass  # any code

        # 5. 計算 IOU
        # score, frame = IOUScore.HandleIOU(
        #     src=curr_frame,
        #     FrameCount=curr_frame_count,
        #     mask=binary_mask,
        #     GroundTruthDir=GTDir
        # )
