import os
import logging
import time
from joblib import Parallel, delayed
from tools.calculate_density import calculate_density
import arcpy
def compute_densitys(input_folder, output_tif_dir, extent_shp, size=50, radii=[200, 1000, 2000], name="NONE", n_jobs=1):
    """
    计算点或线文件的核密度，并保存为多个 TIFF 文件，每个文件对应一个不同的搜索半径
    
    参数:
    input_folder (str): 输入文件夹的路径
    output_tif_dir (str): 输出 TIFF 文件夹的路径
    extent_shp (str): 用于设置处理范围的 shapefile 文件路径
    size (int): 像元大小
    radii (list): 搜索半径的列表
    name (str): 数值字段名称
    n_jobs (int): 并行工作的线程数
    
    返回:
    list: 输出 TIFF 文件的路径列表
    """
    logging.info(f"利用 {name} 计算核密度 tif...")

    # 允许覆盖输出
    arcpy.env.overwriteOutput = True

    # 检查输出文件夹是否存在，不存在则创建
    if not os.path.exists(output_tif_dir):
        os.makedirs(output_tif_dir)

    # 获取输入文件夹中的所有 shapefile 文件
    input_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith(".shp")]
    
    if not input_files:
        logging.error(f"在文件夹 {input_folder} 中没有找到 .shp 文件。")
        return []

    def process_file(input_file):
        output_files = []
        for R in radii:
            logging.info(f"计算 {input_file} 的搜索半径为 {R} 的核密度 tif...")
            output_tif = os.path.join(output_tif_dir, f"{os.path.splitext(os.path.basename(input_file))[0]}_R{R}.tif")
            
            try:
                result = calculate_density(input_file, output_tif, extent_shp, size, R, name)
                output_files.append(result)
            except Exception as e:
                logging.error(f"处理文件 {input_file} 时出错: {str(e)}")
        return output_files

    # 使用 Parallel 和 delayed 进行并行处理
    start_time = time.time()
    results = Parallel(n_jobs=n_jobs)(delayed(process_file)(input_file) for input_file in input_files)
    end_time = time.time()

    # 展平结果列表
    flattened_results = [item for sublist in results for item in sublist]

    logging.info(f"所有文件处理完成，总运行时间: {end_time - start_time:.2f} 秒")

    return flattened_results