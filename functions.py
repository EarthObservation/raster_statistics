import fiona
import rasterio
import rasterio.mask
import numpy as np
import scipy.stats
import gdal


def match_two_rasters(src_raster_path, match_to_raster_path, out_raster_path):
    """
    Function that aligns two rasters, so that the left corner matches and that the cells are aligned.
    :param src_raster_path: str
        Source raster which needs to be match path.
    :param match_to_raster_path: str
        Raster to match (align) to path.
    :param out_raster_path: str
        Output result, matched (aligned) raster path.
    :return:
    """
    # Source
    src = gdal.Open(src_raster_path, gdal.gdalconst.GA_ReadOnly)
    src_proj = src.GetProjection()
    src_geotrans = src.GetGeoTransform()

    # We want a section of source that matches this:
    match_ds = gdal.Open(match_to_raster_path, gdal.gdalconst.GA_ReadOnly)
    match_proj = match_ds.GetProjection()
    match_geotrans = match_ds.GetGeoTransform()
    wide = match_ds.RasterXSize
    high = match_ds.RasterYSize

    # Output / destination
    dst = gdal.GetDriverByName('GTiff').Create(out_raster_path, wide, high, 1, gdal.gdalconst.GDT_Float32)
    dst.SetGeoTransform(match_geotrans)
    dst.SetProjection(match_proj)
    dst.GetRasterBand(1).SetNoDataValue(np.nan)

    # Do the work
    gdal.ReprojectImage(src, dst, src_proj, match_proj, gdal.gdalconst.GRA_Bilinear)

    del dst  # Flush


def clip_raster_to_shape_where_att(raster_path, out_raster_path, shape_path, attribute_name, selected_att_values_list):
    """
    Clip raster to shape on shape attribute condition.
    Selected features to clip with are the ones where attribute "attribute_name" is equal to
     "selected_att_values_list" list elements.
    :param raster_path: str
        Raster to be clipped path.
    :param out_raster_path: str
        Output raster path.
    :param shape_path: str
        Shape path.
    :param attribute_name: str
        Condition attribute name.
    :param selected_att_values_list: list
        Values list (equal to) for selection (attribute_name).
    :return: str
        Csv.
    """
    shapefile = fiona.open(shape_path, "r")
    shapes = []
    for feature in shapefile:
        if feature['properties'][attribute_name] in selected_att_values_list:
            shapes.append(feature["geometry"])
    raster = rasterio.open(raster_path)
    out_image, out_transform = rasterio.mask.mask(raster, shapes, crop=True)
    out_meta = raster.meta
    out_meta.update({"driver": "GTiff",
                     "height": out_image.shape[1],
                     "width": out_image.shape[2],
                     "transform": out_transform})
    out_raster = rasterio.open(out_raster_path, "w", **out_meta)
    out_raster.write(out_image)
    shapefile.close()
    raster.close()
    out_raster.close()


def calculate_statistics_from_raster_where_condition(raster1_path, resolution, raster1_conditions,
                                                     output="dict", statistic="area"):
    """
    Calculate statistics from raster on condition.
    :param raster1_path: str
        Raster path.
    :param resolution: float or int
        Raster resolution.
    :param raster1_conditions: dict, tuple, list, int, float, None
        If tuple(min_range, max_range), if list all elements in list, if None all, else (int, float) equal that value.
    :param output: str
        "csv" or "dict"
    :param statistic: str
        possible val = "area", "max", "min", "mean", "quantile_5" (5 is percent you can change number). Statistics that
        are not area are for second raster.
    :return: str
        Csv.
    """

    if not isinstance(statistic, list):
        statistic = [statistic]

    raster1 = rasterio.open(raster1_path)
    raster1_arr = raster1.read(1)
    pixel1SizeX, pixel1SizeY = raster1.res
    raster1.close()

    out_dict = {}
    print_output = ""
    out_csv = ""
    for raster1_condition in raster1_conditions:
        key = ""
        if isinstance(raster1_condition, tuple):
            if len(raster1_condition) == 2:
                key += "{}-{}".format(raster1_condition[0], raster1_condition[1])
                rast1_bool_arr = np.logical_and(raster1_condition[0] < raster1_arr, raster1_arr <= raster1_condition[1])
            elif len(raster1_condition) == 4:
                key += "{}-{}--{}-{}".format(raster1_condition[0], raster1_condition[1], raster1_condition[2],
                                             raster1_condition[3])
                rast1_bool_arr1 = np.logical_and(raster1_condition[0] < raster1_arr,
                                                 raster1_arr <= raster1_condition[1])
                rast1_bool_arr2 = np.logical_and(raster1_condition[2] < raster1_arr,
                                                 raster1_arr <= raster1_condition[3])
                rast1_bool_arr = np.logical_or(rast1_bool_arr1, rast1_bool_arr2)
        elif isinstance(raster1_condition, list):
            key += "and".join([str(elem) for elem in raster1_condition])
            rast1_bool_arr = np.isin(raster1_arr, raster1_condition)
        elif raster1_condition is None:
            key += "None"
            rast1_bool_arr = np.ones(raster1_arr.shape, dtype=bool)
        elif np.isnan(raster1_condition):
            rast1_bool_arr = np.isnan(raster1_arr)
        else:
            key += "{}".format(raster1_condition)
            rast1_bool_arr = raster1_condition == raster1_arr

        rast_both_bool_arr = rast1_bool_arr
        for stat in statistic:
            value = None
            if stat == "area":
                key += "_area"
                area = np.count_nonzero(rast_both_bool_arr) * (resolution ** 2)
                value = area
            elif stat == "min":
                key += "_min"
                # select values from raster2_arr where mask True to calc stat
                val_where_true_arr = np.ma.masked_array(raster1_arr, mask=np.invert(rast_both_bool_arr))
                min = np.nanmin(val_where_true_arr)
                value = min
            elif stat == "max":
                key += "_max"
                # select values from raster2_arr where mask True to calc stat
                val_where_true_arr = np.ma.masked_array(raster1_arr, mask=np.invert(rast_both_bool_arr))
                max = np.nanmax(val_where_true_arr)
                value = max
            elif stat == "mean":
                key += "_mean"
                # select values from raster2_arr where mask True to calc stat
                val_where_true_arr = np.ma.masked_array(raster1_arr, mask=np.invert(rast_both_bool_arr))
                try:
                    mean = np.nanmean(val_where_true_arr)
                except:
                    mean = "--"
                value = mean
            elif "quantile_" in stat:
                key += "_{}".format(stat)
                quatile_perc = float(stat.split("_")[1])
                val_where_true_arr = np.ma.masked_array(raster1_arr, mask=np.invert(rast_both_bool_arr))
                val_where_true_arr = np.ma.filled(val_where_true_arr, np.nan)  # fill with nan
                quantile = np.nanpercentile(val_where_true_arr, quatile_perc)
                if np.isnan(quantile):
                    quantile = "--"
                value = quantile
            else:
                raise Exception("Wrong statistics!")
            # print(value)
            out_dict[key] = str(value).replace(".", ",")
            print_output += "\t" + str(value).replace(".", ",")
            out_csv += str(value).replace(".", ",") + ";"

    # print(print_output)
    if output == "dict":
        return out_dict
    elif output == "csv":
        return out_csv


def calculate_statistics_from_rasters_where_conditions(raster1_path, raster2_path, resolution,
                                                       raster1_conditions, raster2_conditions, output="dict",
                                                       statistic="area", condition_comparison="<x<=", min1_to_nan=None,
                                                       max1_to_nan=None, min2_to_nan=None,
                                                       max2_to_nan=None):
    """
    :param raster1_path: str
        First raster path.
    :param raster2_path: str
        Second raster path.
    :param resolution: int or float
        Rasters resolution.
    :param raster1_conditions: str
        First raster conditions.
        If tuple(min_range, max_range), if list all elements in list, if None all, else (int, float) equal that value.
    :param raster2_conditions: str
        Second raster conditions.
        If tuple(min_range, max_range), if list all elements in list, if None all, else (int, float) equal that value.
    :param output: str
        "csv" or "dict"
    :param statistic: str
        possible val = "area", "max", "min", "mean", "quantile_5" (5 is percent you can change number). Statistics that
        are not area are for second raster.
    :param condition_comparison: str
        If condition is tuple, possible val = "<x<=" or "<=x<".
    :param min1_to_nan: int or float
        Values smaller than this value of first raster are set to np.nan (not a number).
    :param max1_to_nan: int or float
        Values bigger than this value of first raster are set to np.nan (not a number).
    :param min2_to_nan: int or float
        Values smaller than this value of second raster are set to np.nan (not a number).
    :param max2_to_nan: int or float
        Values bigger than this value of second raster are set to np.nan (not a number).
    :return: str
        Csv.
    """

    if not isinstance(statistic, list):
        statistic = [statistic]

    raster1 = rasterio.open(raster1_path)
    raster1_arr = raster1.read(1)
    pixel1SizeX, pixel1SizeY = raster1.res
    raster1.close()
    raster2 = rasterio.open(raster2_path)
    raster2_arr = raster2.read(1)
    pixel2SizeX, pixel2SizeY = raster2.res
    raster2.close()
    if pixel1SizeX != pixel2SizeX:
        raise Exception("Not equal pixel size in X direction: {}, {}".format(pixel1SizeX, pixel2SizeX))
    if pixel1SizeY != pixel2SizeY:
        raise Exception("Not equal pixel size in Y direction: {}, {}".format(pixel1SizeY, pixel2SizeY))

    # if raster1_arr.shape != raster2_arr.shape:
    #     if raster2_arr.shape[0] < raster1_arr.shape[0]:
    #         row_shape = raster2_arr.shape[0]
    #     else:
    #         row_shape = raster1_arr.shape[0]
    #     if raster2_arr.shape[1] < raster1_arr.shape[1]:
    #         col_shape = raster2_arr.shape[1]
    #     else:
    #         col_shape = raster1_arr.shape[1]
    #     raster1_arr = raster1_arr[0:row_shape, 0:col_shape]
    #     raster2_arr = raster2_arr[0:row_shape, 0:col_shape]

    raster2_arr = np.floor(raster2_arr)
    mask = np.isin(raster2_arr, raster2_conditions)
    raster2_arr[~mask] = np.nan

    if min1_to_nan is not None:
        raster1_arr[raster1_arr < min1_to_nan] = np.nan
    if max1_to_nan is not None:
        raster1_arr[raster1_arr > max1_to_nan] = np.nan
    if min2_to_nan is not None:
        raster2_arr[raster2_arr < min2_to_nan] = np.nan
    if max2_to_nan is not None:
        raster2_arr[raster2_arr > max2_to_nan] = np.nan

    out_dict = {}
    print_output = ""
    out_csv = ""
    for raster1_condition in raster1_conditions:
        for raster2_condition in raster2_conditions:
            key = ""
            if isinstance(raster1_condition, tuple):
                if len(raster1_condition) == 2:
                    key += "{}-{}".format(raster1_condition[0], raster1_condition[1])
                    if condition_comparison == "<x<=":
                        rast1_bool_arr = np.logical_and(raster1_condition[0] < raster1_arr,
                                                        raster1_arr <= raster1_condition[1])
                    elif condition_comparison == "<=x<":
                        rast1_bool_arr = np.logical_and(raster1_condition[0] <= raster1_arr,
                                                        raster1_arr < raster1_condition[1])
                elif len(raster1_condition) == 4:
                    key += "{}-{}--{}-{}".format(raster1_condition[0], raster1_condition[1], raster1_condition[2],
                                                 raster1_condition[3])
                    if condition_comparison == "<x<=":
                        rast1_bool_arr1 = np.logical_and(raster1_condition[0] < raster1_arr,
                                                         raster1_arr <= raster1_condition[1])
                        rast1_bool_arr2 = np.logical_and(raster1_condition[2] < raster1_arr,
                                                         raster1_arr <= raster1_condition[3])
                        rast1_bool_arr = np.logical_or(rast1_bool_arr1, rast1_bool_arr2)
                    elif condition_comparison == "<=x<":
                        rast1_bool_arr1 = np.logical_and(raster1_condition[0] <= raster1_arr,
                                                         raster1_arr < raster1_condition[1])
                        rast1_bool_arr2 = np.logical_and(raster1_condition[2] <= raster1_arr,
                                                         raster1_arr < raster1_condition[3])
                        rast1_bool_arr = np.logical_or(rast1_bool_arr1, rast1_bool_arr2)
            elif isinstance(raster1_condition, list):
                key += "and".join([str(elem) for elem in raster1_condition])
                rast1_bool_arr = np.isin(raster1_arr, raster1_condition)
            elif raster1_condition is None:
                key += "None"
                rast1_bool_arr = np.ones(raster1_arr.shape, dtype=bool)
            elif np.isnan(raster1_condition):
                rast1_bool_arr = np.isnan(raster1_arr)
            else:
                key += "{}".format(raster1_condition)
                rast1_bool_arr = raster1_condition == raster1_arr

            if isinstance(raster2_condition, tuple):
                if len(raster2_condition) == 2:
                    key += "_{}-{}".format(raster2_condition[0], raster2_condition[1])
                    if condition_comparison == "<x<=":
                        rast2_bool_arr = np.logical_and(raster2_condition[0] < raster2_arr,
                                                        raster2_arr <= raster2_condition[1])
                    elif condition_comparison == "<=x<":
                        rast2_bool_arr = np.logical_and(raster2_condition[0] <= raster2_arr,
                                                        raster2_arr < raster2_condition[1])
                elif len(raster2_condition) == 4:
                    key += "_{}-{}--{}-{}".format(raster2_condition[0], raster2_condition[1], raster2_condition[2],
                                                  raster2_condition[3])
                    if condition_comparison == "<x<=":
                        rast2_bool_arr1 = np.logical_and(raster2_condition[0] < raster2_arr,
                                                         raster2_arr <= raster2_condition[1])
                        rast2_bool_arr2 = np.logical_and(raster2_condition[2] < raster2_arr,
                                                         raster2_arr <= raster2_condition[3])
                        rast2_bool_arr = np.logical_or(rast2_bool_arr1, rast2_bool_arr2)
                    elif condition_comparison == "<=x<":
                        rast2_bool_arr1 = np.logical_and(raster2_condition[0] <= raster2_arr,
                                                         raster2_arr < raster2_condition[1])
                        rast2_bool_arr2 = np.logical_and(raster2_condition[2] <= raster2_arr,
                                                         raster2_arr < raster2_condition[3])
                        rast2_bool_arr = np.logical_or(rast2_bool_arr1, rast2_bool_arr2)
            elif isinstance(raster2_condition, list):
                key += "_" + "and".join([str(elem) for elem in raster2_condition])
                rast2_bool_arr = np.isin(raster2_arr, raster2_condition)
            elif raster2_condition is None:
                key += "_None"
                rast2_bool_arr = np.ones(raster2_arr.shape, dtype=bool)
            elif np.isnan(raster2_condition):
                rast2_bool_arr = np.isnan(raster2_arr)
            else:
                key += "_{}".format(raster2_condition)
                rast2_bool_arr = raster2_condition == raster2_arr

            rast_both_bool_arr = np.logical_and(rast1_bool_arr, rast2_bool_arr)
            for stat in statistic:
                value = None
                if stat == "area":
                    key += "_area"
                    area = np.count_nonzero(rast_both_bool_arr) * (resolution ** 2)
                    value = area
                elif stat == "min":
                    key += "_min"
                    # select values from raster2_arr where mask True to calc stat
                    val_where_true_arr = np.ma.masked_array(raster2_arr, mask=np.invert(rast_both_bool_arr))
                    min = np.nanmin(val_where_true_arr)
                    value = min
                elif stat == "max":
                    key += "_max"
                    # select values from raster2_arr where mask True to calc stat
                    val_where_true_arr = np.ma.masked_array(raster2_arr, mask=np.invert(rast_both_bool_arr))
                    max = np.nanmax(val_where_true_arr)
                    value = max
                elif stat == "mean":
                    key += "_mean"
                    # select values from raster2_arr where mask True to calc stat
                    val_where_true_arr = np.ma.masked_array(raster2_arr, mask=np.invert(rast_both_bool_arr))
                    try:
                        mean = np.nanmean(val_where_true_arr)
                    except:
                        mean = "--"
                    value = mean
                elif "quantile_" in stat:
                    key += "_{}".format(stat)
                    quatile_perc = float(stat.split("_")[1])
                    val_where_true_arr = np.ma.masked_array(raster2_arr, mask=np.invert(rast_both_bool_arr))
                    val_where_true_arr = np.ma.filled(val_where_true_arr, np.nan)  # fill with nan
                    quantile = np.nanpercentile(val_where_true_arr, quatile_perc)
                    if np.isnan(quantile):
                        quantile = "--"
                    value = quantile
                elif "pearson" in stat:
                    val_where_true_rast1_arr = np.ma.masked_array(raster1_arr, mask=np.invert(rast_both_bool_arr),
                                                                  dtype=float)
                    val_where_true_rast1_arr = np.ma.filled(val_where_true_rast1_arr, np.nan)
                    val_where_true_rast1_arr.astype(float)
                    val_where_true_rast2_arr = np.ma.masked_array(raster2_arr, mask=np.invert(rast_both_bool_arr),
                                                                  dtype=float)
                    val_where_true_rast2_arr = np.ma.filled(val_where_true_rast2_arr, np.nan)
                    val_where_true_rast2_arr.astype(float)
                    key += "_pearson"
                    nas = np.logical_or(np.isnan(val_where_true_rast1_arr), np.isnan(val_where_true_rast2_arr))
                    if np.all(nas):
                        r = "--"
                        p = "--"
                    else:
                        r, p = scipy.stats.pearsonr(x=val_where_true_rast1_arr[~nas], y=val_where_true_rast2_arr[~nas])
                        r = round(r, 6)
                        p = round(p, 6)
                    value = r

                else:
                    raise Exception("Wrong statistics!")
                # print(value)
                out_dict[key] = str(value).replace(".", ",")
                print_output += "\t" + str(value).replace(".", ",")
                out_csv += str(value).replace(".", ",") + ";"
        # out_csv += "\n"
    # print(print_output)
    if output == "dict":
        return out_dict
    elif output == "csv":
        return out_csv


def calculate_statistics_from_3rasters_where_conditions(raster1_path, raster2_path, raster3_path, resolution,
                                                        raster1_conditions, raster2_conditions, raster3_conditions,
                                                        output="dict", statistic="area"):
    """

    :param raster1_path: str
        First raster path.
    :param raster2_path: str
        Second raster path.
    :param raster3_path: str
        Third raster path.
    :param resolution: int or float
        Rasters resolution.
    :param raster1_conditions: str
        First  raster conditions.
        If tuple(min_range, max_range), if list all elements in list, if None all, else (int, float) equal that value.
    :param raster2_conditions: str
        Second raster conditions.
        If tuple(min_range, max_range), if list all elements in list, if None all, else (int, float) equal that value.
    :param raster3_conditions: str
        Third raster conditions.
        If tuple(min_range, max_range), if list all elements in list, if None all, else (int, float) equal that value.
    :param output: str
        "csv" or "dict"
    :param statistic:
        possible val = "area", "max", "min", "mean", "quantile_5" (5 is percent you can change number). Statistics that
        are not area are for second raster.
    :return: str
        Csv.
    """

    if not isinstance(statistic, list):
        statistic = [statistic]

    raster1 = rasterio.open(raster1_path)
    raster1_arr = raster1.read(1)
    pixel1SizeX, pixel1SizeY = raster1.res
    raster1.close()
    raster2 = rasterio.open(raster2_path)
    raster2_arr = raster2.read(1)
    pixel2SizeX, pixel2SizeY = raster2.res
    raster2.close()
    raster3 = rasterio.open(raster3_path)
    raster3_arr = raster3.read(1)
    pixel3SizeX, pixel3SizeY = raster3.res
    raster3.close()

    if pixel1SizeX != pixel2SizeX != pixel3SizeX:
        raise Exception("Not equal pixel size in X direction: {}, {}, {}".format(pixel1SizeX, pixel2SizeX, pixel3SizeX))
    if pixel1SizeY != pixel2SizeY != pixel3SizeY:
        raise Exception("Not equal pixel size in Y direction: {}, {}, {}".format(pixel1SizeY, pixel2SizeY, pixel3SizeY))

    if raster1_arr.shape != raster2_arr.shape != raster3_arr.shape:
        raise Exception("Rasters don't align!")

    #
    # raster1_arr[raster1_arr < -1] = np.nan
    # raster2_arr[raster2_arr < 1000] = np.nan

    out_dict = {}
    print_output = ""
    out_csv = ""
    for raster1_condition in raster1_conditions:
        for raster2_condition in raster2_conditions:
            for raster3_condition in raster3_conditions:
                key = ""
                # rast 1
                if isinstance(raster1_condition, tuple):
                    if len(raster1_condition) == 2:
                        key += "{}-{}".format(raster1_condition[0], raster1_condition[1])
                        rast1_bool_arr = np.logical_and(raster1_condition[0] < raster1_arr,
                                                        raster1_arr <= raster1_condition[1])
                    elif len(raster1_condition) == 4:
                        key += "{}-{}--{}-{}".format(raster1_condition[0], raster1_condition[1], raster1_condition[2],
                                                     raster1_condition[3])
                        rast1_bool_arr1 = np.logical_and(raster1_condition[0] < raster1_arr,
                                                         raster1_arr <= raster1_condition[1])
                        rast1_bool_arr2 = np.logical_and(raster1_condition[2] < raster1_arr,
                                                         raster1_arr <= raster1_condition[3])
                        rast1_bool_arr = np.logical_or(rast1_bool_arr1, rast1_bool_arr2)
                elif isinstance(raster1_condition, list):
                    key += "and".join([str(elem) for elem in raster1_condition])
                    rast1_bool_arr = np.isin(raster1_arr, raster1_condition)
                elif raster1_condition is None:
                    key += "None"
                    rast1_bool_arr = np.ones(raster1_arr.shape, dtype=bool)
                elif np.isnan(raster1_condition):
                    rast1_bool_arr = np.isnan(raster1_arr)
                else:
                    key += "{}".format(raster1_condition)
                    rast1_bool_arr = raster1_condition == raster1_arr
                # rast 2
                if isinstance(raster2_condition, tuple):
                    if len(raster2_condition) == 2:
                        key += "_{}-{}".format(raster2_condition[0], raster2_condition[1])
                        rast2_bool_arr = np.logical_and(raster2_condition[0] < raster2_arr,
                                                        raster2_arr <= raster2_condition[1])
                    elif len(raster2_condition) == 4:
                        key += "_{}-{}--{}-{}".format(raster2_condition[0], raster2_condition[1], raster2_condition[2],
                                                      raster2_condition[3])
                        rast2_bool_arr1 = np.logical_and(raster2_condition[0] < raster2_arr,
                                                         raster2_arr <= raster2_condition[1])
                        rast2_bool_arr2 = np.logical_and(raster2_condition[2] < raster2_arr,
                                                         raster2_arr <= raster2_condition[3])
                        rast2_bool_arr = np.logical_or(rast2_bool_arr1, rast2_bool_arr2)
                elif isinstance(raster2_condition, list):
                    key += "_" + "and".join([str(elem) for elem in raster2_condition])
                    rast2_bool_arr = np.isin(raster2_arr, raster2_condition)
                elif raster2_condition is None:
                    key += "_None"
                    rast2_bool_arr = np.ones(raster2_arr.shape, dtype=bool)
                elif np.isnan(raster2_condition):
                    rast2_bool_arr = np.isnan(raster2_arr)
                else:
                    key += "_{}".format(raster2_condition)
                    rast2_bool_arr = raster2_condition == raster2_arr
                # rast 3
                if isinstance(raster3_condition, tuple):
                    if len(raster3_condition) == 2:
                        key += "_{}-{}".format(raster3_condition[0], raster3_condition[1])
                        rast3_bool_arr = np.logical_and(raster3_condition[0] < raster3_arr,
                                                        raster3_arr <= raster3_condition[1])
                    elif len(raster3_condition) == 4:
                        key += "_{}-{}--{}-{}".format(raster3_condition[0], raster3_condition[1], raster3_condition[2],
                                                      raster3_condition[3])
                        rast3_bool_arr1 = np.logical_and(raster3_condition[0] < raster3_arr,
                                                         raster3_arr <= raster3_condition[1])
                        rast3_bool_arr2 = np.logical_and(raster3_condition[2] < raster3_arr,
                                                         raster3_arr <= raster3_condition[3])
                        rast3_bool_arr = np.logical_or(rast3_bool_arr1, rast3_bool_arr2)
                elif isinstance(raster3_condition, list):
                    key += "_" + "and".join([str(elem) for elem in raster3_condition])
                    rast3_bool_arr = np.isin(raster3_arr, raster3_condition)
                elif raster3_condition is None:
                    key += "_None"
                    rast3_bool_arr = np.ones(raster3_arr.shape, dtype=bool)
                elif np.isnan(raster3_condition):
                    rast3_bool_arr = np.isnan(raster3_arr)
                else:
                    key += "_{}".format(raster3_condition)
                    rast3_bool_arr = raster3_condition == raster3_arr

                rast_both_bool_arr = np.logical_and(np.logical_and(rast1_bool_arr, rast2_bool_arr), rast3_bool_arr)
                for stat in statistic:
                    value = None
                    if stat == "area":
                        key += "_area"
                        area = np.count_nonzero(rast_both_bool_arr) * (resolution ** 2)
                        value = area
                    elif stat == "min":
                        key += "_min"
                        # select values from raster3_arr where mask True to calc stat
                        val_where_true_arr = np.ma.masked_array(raster3_arr, mask=np.invert(rast_both_bool_arr))
                        min = np.nanmin(val_where_true_arr)
                        value = min
                    elif stat == "max":
                        key += "_max"
                        # select values from raster3_arr where mask True to calc stat
                        val_where_true_arr = np.ma.masked_array(raster3_arr, mask=np.invert(rast_both_bool_arr))
                        max = np.nanmax(val_where_true_arr)
                        value = max
                    elif stat == "mean":
                        key += "_mean"
                        # select values from raster3_arr where mask True to calc stat
                        val_where_true_arr = np.ma.masked_array(raster3_arr, mask=np.invert(rast_both_bool_arr))
                        try:
                            mean = np.nanmean(val_where_true_arr)
                        except:
                            mean = "--"
                        value = mean
                    elif "quantile_" in stat:
                        key += "_{}".format(stat)
                        quatile_perc = float(stat.split("_")[1])
                        val_where_true_arr = np.ma.masked_array(raster3_arr, mask=np.invert(rast_both_bool_arr))
                        val_where_true_arr = np.ma.filled(val_where_true_arr, np.nan)  # fill with nan
                        quantile = np.nanpercentile(val_where_true_arr, quatile_perc)
                        if np.isnan(quantile):
                            quantile = "--"
                        value = quantile
                    else:
                        raise Exception("Wrong statistics!")
                    print(value)
                    out_dict[key] = str(value).replace(".", ",")
                    print_output += "\t" + str(value).replace(".", ",")
                    out_csv += str(value).replace(".", ",") + ";"
        out_csv += "\n"
    # print(print_output)
    if output == "dict":
        return out_dict
    elif output == "csv":
        return out_csv


def calculate_pearson_with_codition(condition_raster_path, raster_conditions, raster1_path, raster2_path,
                                    output="csv"):
    raster1 = rasterio.open(raster1_path)
    raster1_arr = raster1.read(1)
    pixel1SizeX, pixel1SizeY = raster1.res
    raster1.close()
    raster2 = rasterio.open(raster2_path)
    raster2_arr = raster2.read(1)
    pixel2SizeX, pixel2SizeY = raster2.res
    raster2.close()
    condition_raster = rasterio.open(condition_raster_path)
    cond_raster_arr = condition_raster.read(1)
    pixel3SizeX, pixel3SizeY = condition_raster.res
    condition_raster.close()

    if pixel1SizeX != pixel2SizeX != pixel3SizeX:
        raise Exception("Not equal pixel size in X direction: {}, {}, {}".format(pixel1SizeX, pixel2SizeX, pixel3SizeX))
    if pixel1SizeY != pixel2SizeY != pixel3SizeY:
        raise Exception("Not equal pixel size in Y direction: {}, {}, {}".format(pixel1SizeY, pixel2SizeY, pixel3SizeY))
    raster1_arr = raster1_arr[0:11845, 0:17017]
    raster2_arr = raster2_arr[0:11845, 0:17017]
    cond_raster_arr = cond_raster_arr[0:11845, 0:17017]

    if raster1_arr.shape != raster2_arr.shape != condition_raster.shape:
        raise Exception("Rasters don't align!")

    out_dict = {}
    print_output = ""
    out_csv = ""
    for raster_condition in raster_conditions:
        key = ""
        if isinstance(raster_condition, tuple):
            if len(raster_condition) == 2:
                key += "{}-{}".format(raster_condition[0], raster_condition[1])
                cond_rast_bool_arr = np.logical_and(raster_condition[0] < cond_raster_arr,
                                                    cond_raster_arr <= raster_condition[1])
            elif len(raster_condition) == 4:
                key += "{}-{}--{}-{}".format(raster_condition[0], raster_condition[1], raster_condition[2],
                                             raster_condition[3])
                rast1_bool_arr1 = np.logical_and(raster_condition[0] < cond_raster_arr,
                                                 cond_raster_arr <= raster_condition[1])
                rast1_bool_arr2 = np.logical_and(raster_condition[2] < cond_raster_arr,
                                                 cond_raster_arr <= raster_condition[3])
                cond_rast_bool_arr = np.logical_or(rast1_bool_arr1, rast1_bool_arr2)
        elif isinstance(raster_condition, list):
            key += "and".join([str(elem) for elem in raster_condition])
            cond_rast_bool_arr = np.isin(cond_raster_arr, raster_condition)
        elif raster_condition is None:
            key += "None"
            cond_rast_bool_arr = np.ones(cond_raster_arr.shape, dtype=bool)
        elif np.isnan(raster_condition):
            cond_rast_bool_arr = np.isnan(cond_raster_arr)
        else:
            key += "{}".format(raster_condition)
            cond_rast_bool_arr = raster_condition == cond_raster_arr

        val_where_true_rast1_arr = np.ma.masked_array(raster1_arr, mask=np.invert(cond_rast_bool_arr),
                                                      dtype=float)
        val_where_true_rast1_arr = np.ma.filled(val_where_true_rast1_arr, np.nan)
        val_where_true_rast1_arr.astype(float)
        val_where_true_rast2_arr = np.ma.masked_array(raster2_arr, mask=np.invert(cond_rast_bool_arr),
                                                      dtype=float)
        val_where_true_rast2_arr = np.ma.filled(val_where_true_rast2_arr, np.nan)
        val_where_true_rast2_arr.astype(float)
        key += "_pearson"
        nas = np.logical_or(np.isnan(val_where_true_rast1_arr), np.isnan(val_where_true_rast2_arr))
        if np.all(nas):
            r = "--"
            p = "--"
        else:
            r, p = scipy.stats.pearsonr(x=val_where_true_rast1_arr[~nas], y=val_where_true_rast2_arr[~nas])
            r = round(r, 6)
            p = round(p, 6)
        value = r
        print(value)
        out_dict[key] = str(value).replace(".", ",")
        print_output += "\t" + str(value).replace(".", ",")
        out_csv += str(value).replace(".", ",") + ";"

    out_csv += "\n"
    # print(print_output)
    if output == "dict":
        return out_dict
    elif output == "csv":
        return out_csv


def reclas_raster(src_raster_path, out_raster_path, reclas_values, no_data_values=None, e_type=6, no_data=None):
    """
    Reclass raster.
    :param src_raster_path: str
        Source raster path.
    :param out_raster_path: str
        Output raster path.
    :param reclas_values: tuple
        Example:
        [(30, 1), (60, 1), (10, 2)], where 30 set to 1, where 60 set to 1, where 10 set to 2
    :param no_data_values: list of tuples
        List of tuple(min, max) values to set to no_data value.
    :param e_type: int or str
        gdal e_type
    :param no_data:
        No data value.
    :return:
    """
    src_data_set = gdal.Open(src_raster_path)
    gt = src_data_set.GetGeoTransform()
    x_res = abs(gt[1])
    y_res = abs(-gt[5])
    src_no_data = src_data_set.GetRasterBand(1).GetNoDataValue()  # we assume that all the bands have same no_data val
    input_raster_arr = np.array(src_data_set.GetRasterBand(1).ReadAsArray())

    out_raster_arr = input_raster_arr.copy()
    for reclas_value in reclas_values:
        if isinstance(reclas_value, tuple):
            if isinstance(reclas_value[0], tuple):  # prvi je range
                out_raster_arr[(out_raster_arr >= reclas_value[0][0]) &
                               (out_raster_arr <= reclas_value[0][1])] = reclas_value[1]
            else:
                out_raster_arr[out_raster_arr == reclas_value[0]] = reclas_value[1]
        else:
            raise Exception("Input reclass value as list of tuples where first value is src val and other reclass val!")

    if no_data_values is not None and no_data is not None:
        for nd_val in no_data_values:
            if isinstance(nd_val, tuple):
                out_raster_arr[(out_raster_arr >= nd_val[0]) &
                               (out_raster_arr <= nd_val[1])] = no_data
            else:
                out_raster_arr[out_raster_arr == nd_val] = no_data

    if no_data is not None:
        out_raster_arr[out_raster_arr == src_no_data] = no_data

    gtiff_driver = gdal.GetDriverByName("GTiff")
    if len(out_raster_arr.shape) == 2:  # 2D array, one band
        out_data_set = gtiff_driver.Create(out_raster_path, xsize=out_raster_arr.shape[1],
                                           ysize=out_raster_arr.shape[0],
                                           bands=1,
                                           eType=e_type,  # eType: 6 = GDT_Float32
                                           options=['COMPRESS=LZW'])
        out_data_set.SetProjection(src_data_set.GetProjection())
        out_data_set.SetGeoTransform(src_data_set.GetGeoTransform())
        out_data_set.GetRasterBand(1).WriteArray(out_raster_arr)
        if no_data is not None:
            out_data_set.GetRasterBand(1).SetNoDataValue(no_data)
        else:
            out_data_set.GetRasterBand(1).SetNoDataValue(src_no_data)

    else:
        raise Exception("You have to input 2D numpy array!")
    out_data_set.FlushCache()
    src_data_set = None  # Close source data set
    out_data_set = None  # Close output data set
