import FileIO

import cv2
import numpy as np


def HandleIOU(src, FrameCount, mask, GroundTruthDir):
    """
    parameters:
        src: 當前的原始三通道圖象, np.ndarray
        FrameCount: 當前影像的幀數, int
        mask: 計算好結果的 mask 區域 (封閉實心 mask), 二值圖
        GroundTruthDir: 當前病例的 GroundTruthDir 路徑, str

    return:
        Score: IOU 的分數, float
        src: 繪製後的圖像, np.ndarray
    """
    GTPath = FileIO.AllFiles(GroundTruthDir, '.png')

    # 以每幀都畫 Ground Truth 的情況設計
    GTCountList = list()
    for path in GTPath:
        filename = path.split('\\')[-1][:-4]  # 去除副檔名
        count = int(filename.split('_')[-1])
        GTCountList.append(count)
        # print(count)

    # 找出對應幀的 Ground Truth
    index = GTCountList.index(FrameCount)
    GroundTruth = cv2.imread(GTPath[index], 0)  # 灰階讀取

    # 計算 IOU
    IOUMask = np.zeros(mask.shape, np.uint8)
    cnt_GT, _ = cv2.findContours(GroundTruth, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(cnt_GT) != 1:
        areaList = list()
        for cnt in cnt_GT:
            areaList.append(cv2.contourArea(cnt))
        cnt_index = areaList.index(max(areaList))
        cv2.drawContours(IOUMask, [cnt_GT[cnt_index]], -1, (255, 255, 255), -1)

    else:
        cv2.drawContours(IOUMask, cnt_GT, -1, (255, 255, 255), -1)

    intersection = cv2.bitwise_and(IOUMask, mask)
    union = cv2.bitwise_or(IOUMask, mask)

    cnt_intersection, _ = cv2.findContours(intersection, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnt_union, _ = cv2.findContours(union, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    UnionArea = cv2.contourArea(cnt_union[0])
    InterSectionArea = cv2.contourArea(cnt_intersection[0])
    Score = round(InterSectionArea / UnionArea, 3)

    # 將 IOU & 結果 繪製在 frame 上面
    drawIOU = np.zeros(src.shape, np.uint8)
    cnt_draw, _ = cv2.findContours(IOUMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(drawIOU, cnt_draw, -1, (255, 255, 0), -1)
    src = cv2.addWeighted(src, 1, drawIOU, 0.3, 1)

    # 判斷結果好壞
    if Score > 0.85:
        cv2.putText(
            src,
            f'IoU score: {Score}, Excellent.',
            (70, 100),
            cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 1
        )
    elif Score > 0.65:
        cv2.putText(
            src,
            f'IoU score: {Score}, Good.',
            (70, 100),
            cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 0), 1
        )
    else:
        cv2.putText(
            src,
            f'IoU score: {Score}, Poor.',
            (70, 100),
            cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 1
        )

    return Score, src


# # use
# GTDir = "D:\\System_combine\\Ground Truth\\"
# score, frame = HandleIOU(
#     src=curr_frame,
#     FrameCount=curr_frame_count,
#     mask=binary_mask,
#     GroundTruthDir=GTDir
# )
