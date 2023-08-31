import pydicom
import cv2
import os
import time
import logging


def logfile(info, msg):
    log_path = 'E:/MyProgramming/Python/Project/implement/heart recognize/dcm_avi_data2/report.log'
    mode = 'a+' if os.path.exists(log_path) else 'w+'
    fmt = '%(message)s'
    logging.basicConfig(
        level=logging.DEBUG,
        filename=log_path,
        filemode=mode,
        format=fmt
    )
    content = 'file info: '+info+' reason: '+msg
    logging.info(content)


# original path
start = time.time()
video_dcm_dir = 'L:/Lab_Data/dcm Data2/'
# check path
check_file = 'E:/MyProgramming/Python/Project/implement/heart recognize/dcm_avi_data2/check.txt'
# 目錄下的所有資料夾列表
video_dcm_dir_list = os.listdir(video_dcm_dir)

# 迭代每個資料夾並讀取裡面的 DCM 檔案
all_list = list()
all_files = list()
error_file = 0

for curr_dir in video_dcm_dir_list:
    curr_path = os.path.join(video_dcm_dir, curr_dir)
    curr_dir_list = os.listdir(curr_path)

    # 儲存每個 curr_dir_list 底下的所有資料夾的路徑
    reg_list = list()
    for dirs in curr_dir_list:
        if os.path.isdir(os.path.join(curr_path, dirs)):
            dir_path = curr_path + "/" + dirs
            all_list.append(dir_path)

# 已檢查底下所有檔案皆為 dcm 檔案(不做異常處理)
for dcm_dir in all_list:
    # DCM 檔案皆在 IMG001 資料夾裡
    curr_path = dcm_dir + '/IMG001/'

    dcm_files = os.listdir(curr_path)
    all_files.append(len(dcm_files))

    # 讀取每個 dcm 檔案和存取寫入的路徑
    for dcm_file in dcm_files:
        # 若寫入路徑不存在資料夾則創建
        write_dir = 'E:/MyProgramming/Python/Project/implement/heart recognize/dcm_avi_data2/'
        write_path = write_dir + curr_path[len(video_dcm_dir):]
        dcm_path = curr_path + dcm_file

        if not os.path.isdir(write_path):
            os.makedirs(write_path)
        write_path = write_path + dcm_file

        # 使用 pydicom 讀取 *.dcm 檔案
        dcm = pydicom.dcmread(dcm_path)
        # name.pixel_array.shape 可以看資料的維度(總幀數, height, width, channel)

        # 判斷 dcm 是否可以正常讀取
        try:
            dcm_data = dcm.pixel_array.shape

        except AttributeError:
            file_info = str(dcm_path[len(video_dcm_dir):]) + ' shape: None'
            string = '無法讀取該檔案資訊'
            logfile(file_info, string)
            error_file += 1
            continue

        # 資料格式分為 4 種(彩色影片、灰階影片、彩色圖片、灰階圖片)(class 1, 2, 3, 4)
        # 若資料為度 > 3 維則代表彩色影片
        if len(dcm_data) > 3:
            _class = 1
            frames, y, x, channel = dcm_data

            # 若影片的幀數小於60(2s左右), 則記錄在 logfile 裡面
            # if frames < 60:
            #     file_info = str(dcm_path[len(video_dcm_dir):]) + ' shape: ' + str(dcm_data)
            #     string = '影片的長度不足 60 幀(30 幀/秒).'
            #     logfile(file_info, string)
            #     error_file += 1
            #     continue

            # 轉成 avi 格式
            name = write_path.replace('.DCM', '.avi')

            # fourcc 為編碼格式(可以先查詢 avi 可使用的編碼)
            video_write = cv2.VideoWriter(name, cv2.VideoWriter_fourcc(*'MJPG'), 30, (x, y))

            for i in range(frames):
                bgr = cv2.cvtColor(dcm.pixel_array[i], cv2.COLOR_YUV2BGR)
                res = cv2.resize(bgr, (x, y))
                video_write.write(res)
            video_write.release()

        elif len(dcm_data) == 3:
            # 資料維度 = 3 則會有灰階影片和彩色圖片
            if dcm_data[-1] == 3:
                # 3 通道代表是彩色圖片
                _class = 3
                name = write_path.replace('.DCM', '.png')
                r, g, b = cv2.split(dcm.pixel_array)
                merge = cv2.merge([b, g, r])
                cv2.imwrite(name, merge)

            else:
                # 灰階影片
                _class = 2
                frames, y, x = dcm_data

                # if frames < 60:
                #     file_info = str(dcm_path[len(video_dcm_dir):]) + ' shape: ' + str(dcm_data)
                #     string = '影片的長度不足 60 幀(30 幀/秒).'
                #     logfile(file_info, string)
                #     error_file += 1
                #     continue

                name = write_path.replace('.DCM', '.avi')
                video_write = cv2.VideoWriter(name, cv2.VideoWriter_fourcc(*'MJPG'), 30, (x, y))
                for i in range(frames):
                    res = cv2.resize(dcm.pixel_array[i], (x, y))
                    video_write.write(res)
                video_write.release()
        else:
            # 灰階圖片
            _class = 4
            name = write_path.replace('.DCM', '.png')
            cv2.imwrite(name, dcm.pixel_array)

        check = 'path: '+dcm_path[len(video_dcm_dir):]+' shape: '+str(dcm_data)+' class: '+str(_class)+'\n'
        with open(check_file, 'a+') as f:
            f.write(check)

        print('writing {} is successfully.'.format(dcm_file))

end = time.time()
print('總檔案數量: ', sum(all_files))
print('不符合條件的影片數量: ', error_file)
print('總共花費時間: ', round(end - start, 3), '秒')
print('平均花費時間: ', round((end - start) / (sum(all_files) - error_file), 3), '秒')

