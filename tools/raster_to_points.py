import logging
import fiona
import geopandas as gpd
import numpy as np
from scipy.ndimage import map_coordinates
from osgeo import gdal
import os
import arcpy
# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_raster_files_from_folder(folder_path):
    """
    获取文件夹下的所有 .tif 文件路径
    """
    raster_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.tif')]
    return raster_files

def raster_to_points(input_point, raster_folder):
    """
    将栅格对应区域数值作为点要素的属性。
    
    参数:
    input_point (str): 输入的点shapefile文件路径。
    raster_folder (str): 包含栅格文件的文件夹路径。
    """
    logging.info("栅格数据导入属性表...")
    
    try:
        # 读取点要素数据
        with fiona.open(input_point, 'r', encoding='utf-8') as points_shp:
            crs = points_shp.crs
            schema = points_shp.schema
            features = list(points_shp)
        
        if not features:
            logging.warning(f"文件 {input_point} 中没有任何要素，跳过处理...")
            return
        
        # 从 features 创建 GeoDataFrame，自动识别几何信息
        points_gdf = gpd.GeoDataFrame.from_features(features, crs=crs)
        
        # 获取文件夹下的所有栅格文件路径
        raster_files = get_raster_files_from_folder(raster_folder)

        for raster_file in raster_files:
            logging.info(f"提取 {raster_file} 的值到点要素属性表...")
            
            # 读取栅格数据
            raster_dataset = gdal.Open(raster_file)
            if raster_dataset is None:
                logging.error(f"无法打开栅格文件 {raster_file}")
                continue
            
            raster_band = raster_dataset.GetRasterBand(1)
            raster_array = raster_band.ReadAsArray()
            transform = raster_dataset.GetGeoTransform()
            
            # 将点要素坐标转换为栅格坐标
            cols = np.floor((points_gdf.geometry.x - transform[0]) / transform[1]).astype(int)
            rows = np.floor((points_gdf.geometry.y - transform[3]) / transform[5]).astype(int)
            
            # 将栅格坐标限制在合法范围内
            cols = np.clip(cols, 0, raster_array.shape[1] - 1)
            rows = np.clip(rows, 0, raster_array.shape[0] - 1)
            
            # 使用 map_coordinates 函数获取栅格值
            values = map_coordinates(raster_array, [rows, cols], order=1)
            
            # 获取栅格文件名（不含扩展名），并转换为ASCII字符
            raster_name = os.path.splitext(os.path.basename(raster_file))[0]
            ascii_safe_name = ''.join(c for c in raster_name if ord(c) < 128)
            
            # 添加栅格值到点要素属性表
            points_gdf[ascii_safe_name] = values
        
        # 保存更新后的点要素数据
        points_gdf.to_file(input_point, driver='ESRI Shapefile', encoding='utf-8')
        
        logging.info("栅格值已导入点要素属性表")
    
    except fiona.errors.DriverError:
        logging.error(f"无法打开 {input_point} 文件。")
    except Exception as e:
        logging.error(f"处理 {input_point} 文件时发生异常：{str(e)}")

if __name__ == "__main__":
    input_point = "./shp_dir/DJ.shp"  # 注意路径分隔符的方向
    raster_folder = "./pri_data/tif"  # 确保这是一个包含 .tif 文件的文件夹路径
    dem2table(input_point, raster_folder)