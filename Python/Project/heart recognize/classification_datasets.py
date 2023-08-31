import os
import shutil

img_path = 'L:/Lab_Data/model_anchor/Model_anchor/'
datasets_path = 'E:/MyProgramming/Python/Project/implement/heart recognize/All Classification/'
write_path = 'E:/MyProgramming/Python/Project/implement/heart recognize/classified data/'

# 列出 img_path 底下的所有檔案
all_img = os.listdir(img_path)
list_img = list()

for file in all_img:
    list_img.append(file[0:len(file)-4])

# 讀取分類的資較夾
all_datasets_dir = os.listdir(datasets_path)
classification_dir = list()  # 存放分類資料夾
for dirs in all_datasets_dir:
    if os.path.isdir(os.path.join(datasets_path, dirs)):
        classification_dir.append(dirs)

# 迭代每個資料夾裡面的檔案去比對未分類的資料圖片列表
for index in range(0, len(classification_dir)):
    print("正在處理第 %d 類的資料夾..." % (index + 1))

    curr_file_list = os.listdir(os.path.join(datasets_path, classification_dir[index]))

    # 讀取當前資料夾底下的檔案
    for file in curr_file_list:
        if file in list_img:
            target_dir_name = os.path.join(write_path, classification_dir[index]) + '/'

            # 若不存在則創建新的資料夾
            if not os.path.exists(target_dir_name):
                os.mkdir(target_dir_name)

            # 移動檔案到目標資料夾底下
            fill_name = file + '.png'
            target_path = img_path + fill_name
            shutil.move(target_path, target_dir_name)
