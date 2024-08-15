import geopandas as gpd

def rename_field_values(shp_file, field_name, value_mapping, output_file):
    """
    将Shapefile中的某个字段下的值进行重命名

    参数:
    shp_file (str): 输入的Shapefile文件路径
    field_name (str): 要进行重命名操作的字段名称
    value_mapping (dict): 一个字典，其中键是旧值，值是新值
    output_file (str): 输出的Shapefile文件路径
    """
    try:
        # 读取Shapefile
        gdf = gpd.read_file(shp_file, encoding='utf-8')

        # 进行值重命名
        gdf[field_name] = gdf[field_name].apply(lambda x: value_mapping.get(x, x))

        # 保存为新的Shapefile
        gdf.to_file(output_file, encoding='utf-8')
        print(f"Shapefile 已成功保存为: {output_file}")
    except Exception as e:
        print(f"处理Shapefile时出错: {str(e)}")

# if __name__ == "__main__":
#     # 示例文件路径
#     shp_file = "pri_data\shp\DJ_add.shp"
#     output_file = "output.shp"
    
#     # 要进行重命名操作的字段名称
#     field_name = "class"
    
#     # 定义值重命名的映射关系
#     value_mapping = {
#         "商业": "商",
#         "商场": "商",
#         "娱乐": "乐",
    
#     }
    
#     # 调用函数进行处理
#     rename_field_values(shp_file, field_name, value_mapping, output_file)
