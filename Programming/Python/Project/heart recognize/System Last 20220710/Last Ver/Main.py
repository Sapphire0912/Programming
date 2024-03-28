from ProcessesCtrl import Process

InputDCMDir = "E:\\MyProgramming\\Python\\Project\\implement\\heart recognize\\System Last 20220710\\Last Ver\\Datasets" \
              "\\DCM Files\\"

InputGTDir = "E:\\MyProgramming\\Python\\Project\\implement\\heart recognize\\System Last 20220710\\Last Ver" \
             "\\GroundTruth\\"

OutputAVIDir = "E:\\MyProgramming\\Python\\Project\\implement\\heart recognize\\System Last 20220710\\Last Ver" \
               "\\Datasets\\AVI Files\\"

OutputSkeletonizeDir = "E:\\MyProgramming\\Python\\Project\\implement\\heart recognize\\System Last 20220710\\Last Ver\\" \
                       "Datasets\\Skeleton Files\\"

OutputSegmentDir = "E:\\MyProgramming\\Python\\Project\\implement\\heart recognize\\System Last 20220710\\Last Ver\\" \
                   "Datasets\\Segmentation Files\\"
OutputGLSDir = ""

Process(InputDCMDir, InputGTDir, OutputAVIDir, OutputSkeletonizeDir, OutputSegmentDir, OutputGLSDir)
