import os
import shutil

firstDataDir = "E:\\MyProgramming\\Python\\Project\\implement\\heart recognize\\All Classification_avi" \
            "\\0002_Apical Four Chamber\\"

secondDataDir = "E:\\MyProgramming\\Python\\Project\\implement\\heart recognize\\All Classification2_avi" \
                "\\0002_Apical Four Chamber\\"

firstDcmDir = "L:\\Lab_Data\\dcm Data1\\"
secondDcmDir = "L:\\Lab_Data\\dcm Data2\\"

TargetDcmDir = "E:\\MyProgramming\\Python\\Project\\implement\\heart recognize\\System2\\TotalData(1+2)\\DCM Files\\"


def AllFiles(DirPath, extension_name='avi'):
    fileList = list()
    for root, dirs, files in os.walk(DirPath):
        for f in files:
            if f[-len(extension_name):].lower() == extension_name:
                fileList.append(os.path.join(root, f))

    return fileList


def selectFiles(DataPath, SearchPath, TargetDir):
    SearchFileName = [Path.split('\\')[-1] for Path in SearchPath]

    for Path in DataPath:
        FileName = Path.split('\\')[-1]
        DcmFileName = FileName.replace('.avi', '.DCM')

        if DcmFileName in SearchFileName:
            # copy DCM file to targetPath
            index = SearchFileName.index(DcmFileName)
            TargetDcmPath = TargetDir + DcmFileName
            shutil.copyfile(SearchPath[index], TargetDcmPath)
    pass


# firstDataPath = AllFiles(firstDataDir, 'avi')
# secondDataPath = AllFiles(secondDataDir, 'avi')
# firstDcmPath = AllFiles(firstDcmDir, 'dcm')
# secondDcmPath = AllFiles(secondDcmDir, 'dcm')

# selectFiles(firstDataPath, firstDcmPath, TargetDcmDir)
# selectFiles(secondDataPath, secondDcmPath, TargetDcmDir)
