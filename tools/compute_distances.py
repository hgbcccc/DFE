# process1.py
import arcpy
import os
import logging
import geopandas as gpd
from joblib import Parallel, delayed
from tools.calculate_distance import calculate_distance

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def compute_distances(shp_file1, shp_folder, n_jobs=-1):
    """
    计算 shp_file1 与 shp_folder 中的每个 shp 文件之间的距离，并更新 shp_file1
    
    参数:
    shp_file1 (str): 输入的 Shapefile 文件路径
    shp_folder (str): 存放第二个 shapefile 文件的文件夹路径
    n_jobs (int): 并行工作的线程数
    
    返回:
    list: 处理后的数据框列表
    """
    logging.info(f"开始处理 {shp_file1} 与 {shp_folder} 中的 shapefiles 的距离...")
    
    # 获取 shp_folder 中所有的 shapefile 文件
    shp_files = [os.path.join(shp_folder, f) for f in os.listdir(shp_folder) if f.endswith(".shp")]

    # 使用 Parallel 和 delayed 进行并行计算
    results = Parallel(n_jobs=n_jobs)(delayed(calculate_distance)(shp_file1, shp_file) for shp_file in shp_files)

    # 读取原始的 shapefile 文件
    gdf1 = gpd.read_file(shp_file1, encoding="utf8")

    # 将所有计算的字段添加到原始的 DataFrame
    for field_name, gdf in results:
        if field_name not in gdf1.columns:
            gdf1[field_name] = gdf[field_name]
        else:
            logging.warning(f"字段 {field_name} 已存在于 {shp_file1} 中，跳过添加")

    # 保存更新后的结果到原始 shapefile 文件
    gdf1.to_file(shp_file1, driver="ESRI Shapefile", encoding="utf-8")
    logging.info(f"更新后的结果已保存到 {shp_file1}")

    return results
