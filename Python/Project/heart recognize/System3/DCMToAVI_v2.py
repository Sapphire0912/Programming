import pydicom
import json
import time
import cv2
import re
import os


class DCMInit(object):
    """
    class name:
        DCMInit(FilePath, OutputDir=None):
        DCM 轉 avi 或 png，並讀取病人資訊

    parameters:
        FilePath:  輸入當前檔案的絕對路徑
        OutputDir: 輸出 AVI or png 的路徑位置
    """

    def __init__(self, FilePath, OutputDir=None):
        """
        initialization attributes:

        self.DCMFilePath: DCM 檔案的絕對路徑, str
        self.OutputDir: 輸出資料夾的位置, str
        self.OutputDirPath: 存放輸出資料夾存在的檔案路徑, list
        self.TotalPatientInfo: 存放病人資訊, dict
        """

        self.DCMFilePath = FilePath
        self.OutputDir = OutputDir
        self.OutputDirPath = self._AllFiles(OutputDir)

        self.TotalPatientInfo = {}
        CheckAVI = FilePath.split("\\")[-1].replace('DCM', 'avi')
        CheckAVI = self.OutputDir + CheckAVI

        if CheckAVI in self.OutputDirPath:
            print(f'{FilePath}, 該 DCM 檔案已轉成 avi or png 在輸出資料夾裡. (可忽略此訊息)')
            self._DCMInformation(FilePath)
        else:
            self._ConvDCMToAVI()

        self.AVIPath = CheckAVI

    def _AllFiles(self, InputDir):
        """
        method name:
            _AllFiles():
            讀取 FileDir 資料夾下的 DCM 及 AVI 檔案

        return:
            file_list: 回傳所有 DCM 和 AVI 檔案的列表
        """
        file_list = list()
        for root, dirs, files in os.walk(InputDir):
            for f in files:
                if f[-3:].lower() == "avi":
                    file_list.append(os.path.join(root, f))
        return file_list

    def _DCMInformation(self, CurrentDCMFilePath):
        DCMData = pydicom.dcmread(CurrentDCMFilePath)
        FileName = CurrentDCMFilePath.replace('.DCM', '.avi')

        CaseInfoDict = dict()

        # 基本當前資訊的 DCM 屬性
        year = int(DCMData.PatientBirthDate[:4])
        month = int(DCMData.PatientBirthDate[4:6])
        day = int(DCMData.PatientBirthDate[6:])

        LocalTime = time.localtime()
        LocalYear, LocalMonth, LocalDay = int(LocalTime[0]), int(LocalTime[1]), int(LocalTime[2])

        Age = LocalYear - year
        if LocalMonth < month:
            Age = Age - 1
        elif LocalMonth == month and LocalDay < day:
            Age = Age - 1

        fps = 30
        bpm = None
        for key in DCMData.keys():
            str_key = '%s' % DCMData[key]
            key = str(key)

            CaseInfoDict[key] = str_key[len(key) + 1:]

            pattern = r"\D"
            if key == '(0018, 1088)':
                bpm_info = CaseInfoDict[key]
                if bpm_info != '':
                    bpm = int(re.split(pattern, bpm_info)[-2])

            if key == '(0018, 0040)':
                fps_info = CaseInfoDict[key]
                if fps_info != '':
                    fps = int(re.split(pattern, fps_info)[-2])

        if bpm is None:
            bpm = 0

        self.TotalPatientInfo[FileName] = {
            "FileName": FileName,
            "ID": DCMData.PatientID,
            "Name": str(DCMData.PatientName),
            "Birth": DCMData.PatientBirthDate,
            "Age": Age,
            "Gender": DCMData.PatientSex,
            "StudyDate": DCMData.StudyDate,
            "StudyTime": DCMData.StudyTime,
            "FPS": fps,
            "BPM": bpm
        }

    def _ConvDCMToAVI(self):
        """
        method name:
            _ConvDCMToAVI():
            將 DCM 檔轉成 avi 或 png 檔
        """

        CurrDCMPath = self.DCMFilePath
        DCMFileName = CurrDCMPath.split('\\')[-1]

        self._DCMInformation(CurrDCMPath)

        if not os.path.isdir(self.OutputDir):
            os.makedirs(self.OutputDir)

        print(f'----- 正在進行 {CurrDCMPath} 轉檔 -----')
        OutputConvPath = self.OutputDir + DCMFileName

        DCMFile = pydicom.dcmread(CurrDCMPath)

        try:
            DCMData = DCMFile.pixel_array.shape

        except AttributeError:
            raise AttributeError(f'AttributeError: {CurrDCMPath} 該路徑的 DCM 檔無法被正確讀取')

        if len(DCMData) > 3:
            frames, y, x, channel = DCMData

            OutputConvPath = OutputConvPath.replace('.DCM', '.avi')
            video_write = cv2.VideoWriter(OutputConvPath, cv2.VideoWriter_fourcc(*'MJPG'), 30, (x, y))

            for i in range(frames):
                bgr = cv2.cvtColor(DCMFile.pixel_array[i], cv2.COLOR_YUV2BGR)
                res = cv2.resize(bgr, (x, y))
                video_write.write(res)
            video_write.release()

        elif len(DCMData) == 3:
            if DCMData[-1] == 3:
                OutputConvPath = OutputConvPath.replace('.DCM', '.png')
                r, g, b = cv2.split(DCMFile.pixel_array)
                merge = cv2.merge([b, g, r])
                cv2.imwrite(OutputConvPath, merge)

            else:
                frames, y, x = DCMData

                OutputConvPath = OutputConvPath.replace('.DCM', '.avi')
                video_write = cv2.VideoWriter(OutputConvPath, cv2.VideoWriter_fourcc(*'MJPG'), 30, (x, y))

                for i in range(frames):
                    res = cv2.resize(DCMFile.pixel_array[i], (x, y))
                    video_write.write(res)
                video_write.release()

        else:
            OutputConvPath = OutputConvPath.replace('.DCM', '.png')
            cv2.imwrite(OutputConvPath, DCMFile.pixel_array)

