
import os
def get_raster_files_from_folder(folder_path):
    """
    获取文件夹下的所有 .tif 文件路径
    """
    raster_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.tif')]
    return raster_files