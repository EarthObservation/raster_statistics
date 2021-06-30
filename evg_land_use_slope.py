from functions import *
import os
import json

land_use_raster_path = r"D:\Eco_vine_goals\Slovenia\data\raba_raster.tif"
slope_nonaligned_raster_path = r"D:\Eco_vine_goals\Slovenia\data\slope_perc\slope_perc.tif"
na_shp_path = r"D:\Eco_vine_goals\Slovenia\NA\NA.shp"

slope_raster_path = r"D:\Eco_vine_goals\SLO_land_use_analysis\EVG_slope_aligned.tif"
if not os.path.isfile(slope_raster_path):
    match_two_rasters(slope_nonaligned_raster_path, land_use_raster_path, slope_raster_path)

out_raba_rast_dir = r"D:\Eco_vine_goals\SLO_land_use_analysis"

naselja = ["Brje", "Dolenje", "Gaberje", "Planina", "Šmarje", "Tevče", "Velike Žablje", "Vrtovče", "Zavino", "Dolanci",
           "Kodreti", "Branik", "Preserje", "Spodnja Branica", "Steske", "Erzelj", "Goče", "Lože", "Manče", "Orehovica",
           "Podnanos", "Podraga", "Slap"]
evg_id_conditions = [(0, 100), 10, 20, 21, 22, 23, 24, 30, 40, 50, 60, 70, 90]
slope_conditions = [np.nan, (0, 3), (3, 7), (7, 13), (13, 21), (21, 31), (31, 46), (46, 1000)]

result_dict = {}
csv = ""
for naselje in naselja:
    print(naselje)
    out_raba_rast = os.path.join(out_raba_rast_dir, "raba_{}.tif".format(naselje))
    if not os.path.isfile(out_raba_rast):
        clip_raster_to_shape_where_att(raster_path=land_use_raster_path, shape_path=na_shp_path,
                                       attribute_name="NA_UIME",
                                       selected_att_values_list=[naselje],
                                       out_raster_path=out_raba_rast)

    out_slope_rast = os.path.join(out_raba_rast_dir, "slope_{}.tif".format(naselje))
    if not os.path.isfile(out_slope_rast):
        clip_raster_to_shape_where_att(raster_path=slope_raster_path, shape_path=na_shp_path,
                                       attribute_name="NA_UIME",
                                       selected_att_values_list=[naselje],
                                       out_raster_path=out_slope_rast)

    area_csv = calculate_statistics_from_rasters_where_conditions(raster1_path=out_raba_rast,
                                                                  raster2_path=out_slope_rast,
                                                                  resolution=1,
                                                                  raster1_conditions=evg_id_conditions,
                                                                  raster2_conditions=slope_conditions, output="csv",
                                                                  condition_comparison="<=x<",
                                                                  min2_to_nan=0.0001,
                                                                  max2_to_nan=999)
    csv += area_csv + "\n"
    # # no conditions pearson
    # no_conditions_csv = calculate_statistics_from_rasters_where_conditions(raster1_path=out_vin_rast,
    #                                                                        raster2_path=out_slope_rast,
    #                                                                        resolution=1,
    #                                                                        raster1_conditions=[None],
    #                                                                        raster2_conditions=[None],
    #                                                                        output="csv",
    #                                                                        statistic=["pearson"])
    # print(no_conditions_csv)

    print("area: {}".format(
        calculate_statistics_from_raster_where_condition(raster1_path=out_raba_rast, resolution=1, output="csv",
                                                         raster1_conditions=[(0, 100)])))

out_raba_rast = os.path.join(out_raba_rast_dir, "raba_{}.tif".format("naselja"))
if not os.path.isfile(out_raba_rast):
    clip_raster_to_shape_where_att(raster_path=land_use_raster_path, shape_path=na_shp_path,
                                   attribute_name="NA_UIME",
                                   selected_att_values_list=naselja,
                                   out_raster_path=out_raba_rast)
print(calculate_statistics_from_raster_where_condition(raster1_path=out_raba_rast, resolution=1, output="csv",
                                                       raster1_conditions=[(0, 100)]))

fp = open(os.path.join(out_raba_rast_dir, "evg_land_use_slope.csv"), "w")
fp.write(csv)
fp.close()
