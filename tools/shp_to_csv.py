# import geopandas as gpd
# import os
# import tkinter as tk
# from tkinter import filedialog, messagebox
# from tools import find_shapefiles

# def shp_to_csv(shp_file, csv_file):
#     """
#     将Shapefile导出为CSV文件
    
#     参数:
#     shp_file (str): 输入的Shapefile文件路径。
#     csv_file (str): 输出的CSV文件路径。
#     """
#     try:
#         # 读取Shapefile
#         gdf = gpd.read_file(shp_file, encoding='utf-8')
#         # 将GeoDataFrame转换为DataFrame，并将几何列转换为WKT格式
#         df = gdf.copy()
#         df['geometry'] = df['geometry'].apply(lambda x: x.wkt)
#         # 将DataFrame导出为CSV文件
#         df.to_csv(csv_file, index=False, encoding='utf-8')
#         print(f"Shapefile 已成功导出为 CSV 文件: {csv_file}")
#     except Exception as e:
#         print(f"导出 CSV 时出错: {str(e)}")
import geopandas as gpd
import os

def shp_to_csv(shp_file, csv_file):
    """
    将Shapefile导出为CSV文件
    
    参数:
    shp_file (str): 输入的Shapefile文件路径。
    csv_file (str): 输出的CSV文件路径。
    """
    try:
        # 读取Shapefile
        gdf = gpd.read_file(shp_file, encoding='utf-8')
        # 将GeoDataFrame转换为DataFrame并移除geometry列
        df = gdf.drop(columns='geometry')
        # 将DataFrame导出为CSV文件
        df.to_csv(csv_file, index=False, encoding='utf-8')
        print(f"Shapefile 已成功导出为 CSV 文件: {csv_file}")
    except Exception as e:
        print(f"导出 CSV 时出错: {str(e)}")
