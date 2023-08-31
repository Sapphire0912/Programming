import os


def Allfiles(dir_path, extension_name):
    result = list()
    for root, dirs, files in os.walk(dir_path):
        for f in files:
            if f[-len(extension_name):] == extension_name:
                result.append(os.path.join(root, f))

    return result
