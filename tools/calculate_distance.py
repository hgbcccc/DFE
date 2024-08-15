# import geopandas as gpd
# import os
# import logging
# import time
# from joblib import Parallel, delayed

# # Setup logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# def calculate_distance(shp_file1, shp_file2):
#     """
#     计算 shp_file1 与 shp_file2 之间的距离，并返回带有距离字段的数据框
    
#     参数:
#     shp_file1 (str): 输入的 Shapefile 文件路径
#     shp_file2 (str): 用于计算距离的 Shapefile 文件路径
    
#     返回:
#     tuple: 包含新的字段名和距离计算结果的数据框
#     """
#     logging.info(f"计算 {shp_file1} 与 {shp_file2} 的距离...")

#     # 读取第一个 shapefile 文件
#     gdf1 = gpd.read_file(shp_file1, encoding="utf8")
    
#     # 读取第二个 shapefile 文件
#     gdf2 = gpd.read_file(shp_file2, encoding="utf8")
    
#     # 计算距离
#     distances = gdf1.geometry.apply(lambda geom: geom.distance(gdf2.unary_union))
    
#     # 获取第二个 shapefile 文件的文件名，不包括扩展名
#     shp_file2_name = os.path.splitext(os.path.basename(shp_file2))[0]
    
#     # 创建新的字段名
#     field_name = f"dis_{shp_file2_name}"
    
#     # 添加距离到新的字段
#     gdf1[field_name] = distances
    
#     return field_name, gdf1

# def process1(shp_file1, shp_folder, n_jobs=-1):
#     """
#     计算 shp_file1 与 shp_folder 中的每个 shp 文件之间的距离，并更新 shp_file1
    
#     参数:
#     shp_file1 (str): 输入的 Shapefile 文件路径
#     shp_folder (str): 存放第二个 shapefile 文件的文件夹路径
#     n_jobs (int): 并行工作的线程数
    
#     返回:
#     list: 处理后的数据框列表
#     """
#     logging.info(f"开始处理 {shp_file1} 与 {shp_folder} 中的 shapefiles 的距离...")
    
#     # 获取 shp_folder 中所有的 shapefile 文件
#     shp_files = [os.path.join(shp_folder, f) for f in os.listdir(shp_folder) if f.endswith(".shp")]

#     # 使用 Parallel 和 delayed 进行并行计算
#     results = Parallel(n_jobs=n_jobs)(delayed(calculate_distance)(shp_file1, shp_file) for shp_file in shp_files)

#     # 读取原始的 shapefile 文件
#     gdf1 = gpd.read_file(shp_file1, encoding="utf8")

#     # 将所有计算的字段添加到原始的 DataFrame
#     for field_name, gdf in results:
#         if field_name not in gdf1.columns:
#             gdf1[field_name] = gdf[field_name]
#         else:
#             logging.warning(f"字段 {field_name} 已存在于 {shp_file1} 中，跳过添加")

#     # 保存更新后的结果到原始 shapefile 文件
#     gdf1.to_file(shp_file1, driver="ESRI Shapefile", encoding="utf-8")
#     logging.info(f"更新后的结果已保存到 {shp_file1}")

#     return results

# if __name__ == "__main__":
#     start_time = time.time()
#     shp_file1 = "data\建设用地\工业用地\工业用地.shp"
#     shp_folder = "pri_data\shp"
    
#     try:
#         results = process1(shp_file1, shp_folder, n_jobs=1)
#         logging.info("所有文件处理完成")
#     except Exception as e:
#         logging.error(f"运行时发生错误: {str(e)}")

#     end_time = time.time()
#     logging.info(f"总运行时间: {end_time - start_time:.2f} 秒")
# tools/calculate_distance.py

import geopandas as gpd
import os
import arcpy

def calculate_distance(shp_file1, shp_file2):
    """
    计算 shp_file1 与 shp_file2 之间的距离，并返回带有距离字段的数据框
    
    参数:
    shp_file1 (str): 输入的 Shapefile 文件路径
    shp_file2 (str): 用于计算距离的 Shapefile 文件路径
    
    返回:
    tuple: 包含新的字段名和距离计算结果的数据框
    """
    # 读取第一个 shapefile 文件
    gdf1 = gpd.read_file(shp_file1, encoding="utf8")
    
    # 读取第二个 shapefile 文件
    gdf2 = gpd.read_file(shp_file2, encoding="utf8")
    
    # 计算距离
    distances = gdf1.geometry.apply(lambda geom: geom.distance(gdf2.unary_union))
    
    # 获取第二个 shapefile 文件的文件名，不包括扩展名
    shp_file2_name = os.path.splitext(os.path.basename(shp_file2))[0]
    
    # 创建新的字段名
    field_name = f"s_{shp_file2_name}"
    
    # 添加距离到新的字段
    gdf1[field_name] = distances
    
    return field_name, gdf1
