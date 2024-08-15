import os
import logging
import argparse
import geopandas as gpd
from tools import find_shapefiles, compute_densitys, compute_distances, raster_to_points,shp_to_csv

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def feature_extraction(data_folder, pri_data_folder, shp2tif_file, output_tif_dir, extent_shp, output_csv_dir, size=50, radii=[200, 1000, 2000], name="NONE"):
    """
    处理所有的 .shp 文件

    计算每个数据文件夹中的 .shp 文件与 pri_data_folder 中 shp 文件夹下的 .shp 文件的距离，
    并计算核密度，将结果保存为 TIFF 文件，并将栅格值提取到原始 .shp 文件的属性表中。

    参数:
    data_folder (str): 包含数据 .shp 文件的文件夹路径，在实例中应填写【A】流程化_准备数据.ipynb给定的包含10类的shp文件夹
    pri_data_folder (str): 包含用于计算距离和核密度的文件夹路径
    shp2tif_file (str): 用于计算核密度的输入文件夹路径
    output_tif_dir (str): 输出 TIFF 文件的文件夹路径
    extent_shp (str): 用于设置处理范围的 shapefile 文件路径
    output_csv_dir (str): 输出 CSV 文件的文件夹路径
    size (int): 像元大小，默认为50
    radii (list): 搜索半径列表，默认为 [200, 1000, 2000]
    name (str): 数值字段名称，默认为 "NONE"

    返回:
    None
    """
    # 查找所有的数据文件夹下的 .shp 文件
    data_shapefiles = find_shapefiles(data_folder)

    # 查找用于计算距离的 shapefiles
    shp_folder = os.path.join(pri_data_folder, "shp")
    shp_files = find_shapefiles(shp_folder)

    # 计算距离
    for data_shapefile in data_shapefiles:
        logging.info(f"Processing distance for {data_shapefile}...")
        results = compute_distances(data_shapefile, shp_folder, n_jobs=1)

    # 计算核密度
    output_files = compute_densitys(shp2tif_file, output_tif_dir, extent_shp, size=size, radii=radii, name=name, n_jobs=1)

    # 提取栅格值添加到shp属性表
    for data_shapefile in data_shapefiles:
        raster_to_points(data_shapefile, output_tif_dir)  # raster_folder = output_tif_dir

    # 创建输出CSV文件夹（如果不存在）
    if not os.path.exists(output_csv_dir):
        os.makedirs(output_csv_dir)

    # 将shp文件保存为csv文件
    for data_shapefile in data_shapefiles:
        # 获取文件名（不含扩展名）
        base_name = os.path.splitext(os.path.basename(data_shapefile))[0]
        # 构建输出CSV文件路径
        csv_file = os.path.join(output_csv_dir, f"{base_name}.csv")
        # 将Shapefile转换为CSV
        shp_to_csv(data_shapefile, csv_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='进行特征提取和核密度计算')

    parser.add_argument('--data_folder', type=str, required=True, help='包含数据 .shp 文件的文件夹路径')
    parser.add_argument('--pri_data_folder', type=str, required=True, help='包含用于计算距离和核密度的文件夹路径')
    parser.add_argument('--shp2tif_file', type=str, required=True, help='用于计算核密度的输入文件夹路径')
    parser.add_argument('--output_tif_dir', type=str, required=True, help='输出 TIFF 文件的文件夹路径')
    parser.add_argument('--extent_shp', type=str, required=True, help='用于设置处理范围的 shapefile 文件路径')
    parser.add_argument('--output_csv_dir', type=str, required=True, help='输出 CSV 文件的文件夹路径')
    parser.add_argument('--size', type=int, default=50, help='像元大小，默认为50')
    parser.add_argument('--radii', type=int, nargs='+', default=[200, 1000, 2000], help='搜索半径列表，默认为 [200, 1000, 2000]')
    parser.add_argument('--name', type=str, default='NONE', help='数值字段名称，默认为 "NONE"')

    args = parser.parse_args()
    
    # 开始进行处理
    try:
        feature_extraction(args.data_folder, 
                           args.pri_data_folder, 
                           args.shp2tif_file, 
                           args.output_tif_dir, 
                           args.extent_shp, 
                           args.output_csv_dir,
                           args.size, 
                           args.radii, 
                           args.name)
        logging.info("---------------------------------")
        logging.info("---------征提取已经完成-----------")
        logging.info("---------------------------------")
    except Exception as e:
        logging.error(f"!!!错误!!!: {str(e)}")
