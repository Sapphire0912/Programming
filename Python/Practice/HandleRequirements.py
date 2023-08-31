requirementsFilePath = "E:\\MyProgramming\\Python\\requirements2.txt"
requirementsFileOutput = "E:\\MyProgramming\\Python\\requirement_v2.txt"

with open(requirementsFilePath, 'r') as file:
    _packages = file.readlines()
    for pack in _packages:
        line = pack.split(' ')
        module_name = line[0]
        version = line[-1].replace("\n", '')
        _format = module_name + "==" + version

        with open(requirementsFileOutput, 'a+') as requirements:
            requirements.write(_format)
            requirements.write("\n")
