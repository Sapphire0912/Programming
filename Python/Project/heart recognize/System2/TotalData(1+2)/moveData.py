import os
import shutil


segDir = "E:\\MyProgramming\\Python\\Project\\implement\\heart recognize\\System2\\TotalData(1+2)\\1+2 Data OK" \
         "\\Segmentation Files\\"

TargetDCMDir = "E:\\MyProgramming\\Python\\Project\\implement\\heart recognize\\System2\\TotalData(1+2)\\1+2 Data OK" \
               "\\DCM Files\\"

TargetSkeDir = "E:\\MyProgramming\\Python\\Project\\implement\\heart recognize\\System2\\TotalData(1+2)\\1+2 Data OK" \
               "\\Skeleton Files\\"

TargetAVIDir = "E:\\MyProgramming\\Python\\Project\\implement\\heart recognize\\System2\\TotalData(1+2)\\1+2 Data OK" \
               "\\AVI Files\\"

OriDCMDir = "E:\\MyProgramming\\Python\\Project\\implement\\heart recognize\\System2\\TotalData(1+2)\\DCM Files\\"
OriAVIDir = "E:\\MyProgramming\\Python\\Project\\implement\\heart recognize\\System2\\TotalData(1+2)\\AVI Files\\"
OriSkeDir = "E:\\MyProgramming\\Python\\Project\\implement\\heart recognize\\System2\\TotalData(1+2)\\" \
            "Skeletonize Files\\"


def AllFiles(DirPath, extension_name='avi'):
    fileList = list()
    for root, dirs, files in os.walk(DirPath):
        for f in files:
            if f[-len(extension_name):].lower() == extension_name:
                fileList.append(os.path.join(root, f))

    return fileList


segPath = AllFiles(segDir)
FileNameList = [path.split('\\')[-1][15:] for path in segPath]

for filename in FileNameList:
    DCMName = str(filename).replace('avi', 'DCM')
    skeName = str(filename) + '.png'

    shutil.copyfile(OriDCMDir + DCMName, TargetDCMDir + DCMName)
    shutil.copyfile(OriAVIDir + str(filename), TargetAVIDir + str(filename))
    shutil.copyfile(OriSkeDir + skeName, TargetSkeDir + skeName)





