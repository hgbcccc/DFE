import arcpy

def polygon_to_point(input_shp, output_shp, point_type="INSIDE"):
    """
    将面Shapefile转换为点Shapefile

    参数:
    input_shp (str): 输入的面Shapefile文件路径
    output_shp (str): 输出的点Shapefile文件路径
    point_type (str): 点类型，可以是 "INSIDE" 或 "CENTROID"
    """
    arcpy.env.overwriteOutput = True

    try:
        # 将面转为点
        if point_type.upper() == "INSIDE":
            arcpy.FeatureToPoint_management(input_shp, output_shp, "INSIDE")
        else:
            arcpy.FeatureToPoint_management(input_shp, output_shp)

        print(f"面Shapefile已成功转换为点Shapefile: {output_shp}")
    except Exception as e:
        print(f"转换过程中出错: {str(e)}")