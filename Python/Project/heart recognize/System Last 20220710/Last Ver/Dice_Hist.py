import os
import cv2
import numpy as np
import matplotlib.pyplot as plt


def AllFiles(DirPath, ext):
    targetList = list()
    for root, dirs, files in os.walk(DirPath):
        for f in files:
            if f[-len(ext):] == ext:
                targetList.append(os.path.join(f))

    return targetList


def Dice_coef(src, GT, mode):
    if mode == 'All':
        src = cv2.imread(".\\TargetDir\\frames\\" + src, 0)

    if mode == 'EDV':
        src = cv2.imread(".\\TargetDir\\EDV\\" + src, 0)

    if mode == 'ESV':
        src = cv2.imread(".\\TargetDir\\ESV\\" + src, 0)

    GT = cv2.imread('.\\TargetDir\\GT\\' + GT, 0)
    mask_GT = np.zeros(GT.shape, np.uint8)
    cnt_GT, _ = cv2.findContours(GT, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(cnt_GT) != 1:
        areaList = list()
        for c in cnt_GT:
            areaList.append(cv2.contourArea(c))
        cnt_index = areaList.index(max(areaList))
        cnt_target = cnt_GT[cnt_index]
    else:
        cnt_target = cnt_GT[0]
    cv2.drawContours(mask_GT, [cnt_target], -1, (255, 255, 255), -1)

    intersection = cv2.bitwise_and(src, mask_GT)
    intersection = np.unique(intersection, return_counts=True)[1][1]
    A = np.unique(src, return_counts=True)[1][1]
    B = np.unique(mask_GT, return_counts=True)[1][1]
    dice = int(round(2 * intersection / (A + B), 2) * 100)

    return dice


GTDir = ".\\TargetDir\\GT\\"
Frames = ".\\TargetDir\\frames\\"  # total image
EDVFrames = ".\\TargetDir\\EDV\\"  # EDV image
ESVFrames = ".\\TargetDir\\ESV\\"  # ESV image

GTPath = AllFiles(GTDir, 'png')
FPath = AllFiles(Frames, 'png')
EDVPath = AllFiles(EDVFrames, 'png')
ESVPath = AllFiles(ESVFrames, 'png')


total = np.zeros(101, np.int)
EDVScore = np.zeros(101, np.int)
ESVScore = np.zeros(101, np.int)
score = 0

for i, path in enumerate(GTPath):
    if path in FPath:
        score = Dice_coef(path, path, mode='All')  # path -> filename
        total[score] += 1

    if path in EDVPath:
        score = Dice_coef(path, path, mode='EDV')  # path -> filename
        EDVScore[score] += 1

    if path in ESVPath:
        score = Dice_coef(path, path, mode='ESV')  # path -> filename
        ESVScore[score] += 1

# print(np.sum(total), np.sum(EDVScore), np.sum(ESVScore))
w = np.arange(0, 101)

print(np.sum(w * total) / np.sum(total))
print(np.sum(w * EDVScore) / np.sum(EDVScore))
print(np.sum(w * ESVScore) / np.sum(ESVScore))

# draw
xaxis = np.arange(0, 101)
fig, ax = plt.subplots(3)

ax[0].set_facecolor('gray')
ax[0].bar(xaxis, total, color='blue')
ax[0].set_ylabel("Count")
ax[0].axes.yaxis.set_ticks([])
# ax[0].get_yaxis().set_visible(False)
# ax[0].set_xlabel("Dice Similarity Coefficient (%)")

ax[1].set_facecolor('gray')
ax[1].bar(xaxis, EDVScore, color='blue')
ax[1].set_ylabel("Count")
ax[1].axes.yaxis.set_ticks([])
# ax[1].get_yaxis().set_visible(False)
# ax[1].set_xlabel("Dice Similarity Coefficient (%)")

ax[2].set_facecolor('gray')
ax[2].bar(xaxis, ESVScore, color='blue')
ax[2].set_ylabel("Count")
ax[2].axes.yaxis.set_ticks([])
ax[2].set_xlabel("Dice Similarity Coefficient (%)")
# ax[2].get_yaxis().set_visible(False)

plt.show()
