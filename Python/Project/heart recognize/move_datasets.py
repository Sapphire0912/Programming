import os
import shutil

skePath = "E:\\MyProgramming\\Python\\Project\\implement\\heart recognize\\data2_classifier\\all_img\\"
targetPath = "E:\\MyProgramming\\Python\\Project\\implement\\heart recognize\\classified data2_png\\"
classifierPath = "E:\\MyProgramming\\Python\\Project\\implement\\heart recognize\\All Classification2_avi\\"

each_category = os.listdir(classifierPath)
each_categoryPath = [os.path.join(classifierPath, p) + "\\" for p in each_category]

for i, Path in enumerate(each_categoryPath):
    category = each_category[i]
    move_targetDir = os.path.join(targetPath, category) + "\\"

    Videos = os.listdir(Path)
    for video in Videos:
        Filename = video + '.png'
        move_targetPath = move_targetDir + Filename
        skeImg = os.path.join(skePath, Filename)
        shutil.move(skeImg, move_targetPath)
