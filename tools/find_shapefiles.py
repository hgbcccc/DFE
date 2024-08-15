
import os
def find_shapefiles(base_folder):
    """在指定文件夹下查找所有的 .shp 文件"""
    shapefiles = []
    for root, dirs, files in os.walk(base_folder):
        for file in files:
            if file.endswith(".shp"):
                shapefiles.append(os.path.join(root, file))
    return shapefiles