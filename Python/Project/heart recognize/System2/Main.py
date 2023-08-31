from ProcessesCtrl import Process

InputDCMDir = "E:\\MyProgramming\\Python\\Project\\implement\\heart recognize\\System2\\TotalData(1+2)\\DCM Files\\"
InputGTDir = "E:\\MyProgramming\\Python\\Project\\implement\\heart recognize\\System2\\Ground Truth\\"
OutputAVIDir = "E:\\MyProgramming\\Python\\Project\\implement\\heart recognize\\System2\\TotalData(1+2)\\AVI Files\\"
OutputSkeletonizeDir = "E:\\MyProgramming\\Python\\Project\\implement\\heart recognize\\System2\\TotalData(1+2)" \
                       "\\Skeletonize Files\\"
OutputSegmentDir = "E:\\MyProgramming\\Python\\Project\\implement\\heart recognize\\System2\\TotalData(1+2)" \
                   "\\Segmentation Files\\"
OutputGLSDir = "E:\\MyProgramming\\Python\\Project\\implement\\heart recognize\\System2\\Unit GLS\\"

Process(InputDCMDir, InputGTDir, OutputAVIDir, OutputSkeletonizeDir, OutputSegmentDir, OutputGLSDir)
