from functions import *
import os
import json

land_use_raster_path = r"D:\Eco_vine_goals\Slovenia\data\raba_raster.tif"
dem_raster_nonaligned_path = r"D:\Eco_vine_goals\Slovenia\data\EVG_DEM.tif"
na_shp_path = r"D:\Eco_vine_goals\Slovenia\NA\NA.shp"

dem_raster_path = r"D:\Eco_vine_goals\SLO_land_use_analysis\EVG_DEM_aligned.tif"
if not os.path.isfile(dem_raster_path):
    match_two_rasters(dem_raster_nonaligned_path, land_use_raster_path, dem_raster_path)

out_raba_rast_dir = r"D:\Eco_vine_goals\SLO_land_use_analysis"

naselja = ["Brje", "Dolenje", "Gaberje", "Planina", "Šmarje", "Tevče", "Velike Žablje", "Vrtovče", "Zavino", "Dolanci",
           "Kodreti", "Branik", "Preserje", "Spodnja Branica", "Steske", "Erzelj", "Goče", "Lože", "Manče", "Orehovica",
           "Podnanos", "Podraga", "Slap"]
evg_id_conditions = [10, 20, 21, 22, 23, 24, 30, 40, 50, 60, 70, 90]
statistics = ["mean", "max", "min"]
height_conditions = [None]

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

    out_dem_rast = os.path.join(out_raba_rast_dir, "dem_{}.tif".format(naselje))
    if not os.path.isfile(out_dem_rast):
        clip_raster_to_shape_where_att(raster_path=dem_raster_path, shape_path=na_shp_path,
                                       attribute_name="NA_UIME",
                                       selected_att_values_list=[naselje],
                                       out_raster_path=out_dem_rast)

    naselje_csv = calculate_statistics_from_rasters_where_conditions(raster1_path=out_raba_rast,
                                                                     raster2_path=out_dem_rast,
                                                                     resolution=1,
                                                                     raster1_conditions=evg_id_conditions,
                                                                     raster2_conditions=height_conditions, output="csv",
                                                                     statistic=statistics)
    csv += naselje_csv + "\n"
    # # no conditions pearson
    # no_conditions_csv = calculate_statistics_from_rasters_where_conditions(raster1_path=out_vin_rast,
    #                                                                        raster2_path=out_eco_vin_rast,
    #                                                                        resolution=1,
    #                                                                        raster1_conditions=[None],
    #                                                                        raster2_conditions=[None],
    #                                                                        output="csv",
    #                                                                        statistic="pearson")
    # print(no_conditions_csv)


fp = open(os.path.join(out_raba_rast_dir, "evg_land_use_height.csv"), "w")
fp.write(csv)
fp.close()


# clip_shp_path = r"D:\Eco_vine_goals\Slovenia\data\EVG_obmocje_new.shp"
# raba_all_path = os.path.join(out_raba_rast_dir, "raba_{}.tif".format("all"))
# if not os.path.isfile(raba_all_path):
#     clip_raster_to_shape_where_att(raster_path=naravnost_raster_path, shape_path=clip_shp_path,
#                                    attribute_name="ENOTA",
#                                    selected_att_values_list=["NA"],
#                                    out_raster_path=raba_all_path)
#
#
# dem_all_path = os.path.join(out_raba_rast_dir, "dem_{}.tif".format("all"))
# if not os.path.isfile(dem_all_path):
#     clip_raster_to_shape_where_att(raster_path=dem_raster_path, shape_path=clip_shp_path,
#                                    attribute_name="ENOTA",
#                                    selected_att_values_list=["NA"],
#                                    out_raster_path=dem_all_path)
#
# all_no_cond_csv = calculate_statistics_from_rasters_where_conditions(raster1_path=raba_all_path,
#                                                                      raster2_path=dem_all_path,
#                                                                      resolution=1,
#                                                                      raster1_conditions=naravnost_conditions,
#                                                                      raster2_conditions=height_conditions, output="csv",
#                                                                      statistic=statistics)
# print(all_no_cond_csv)