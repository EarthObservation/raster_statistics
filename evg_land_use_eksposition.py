from functions import *
import os
import json

land_use_raster_path = r"D:\Eco_vine_goals\Slovenia\data\raba_raster.tif"
aspect_reclass_nonaligned_raster_path = r"D:\Eco_vine_goals\Slovenia\data\aspect.tif"
na_shp_path = r"D:\Eco_vine_goals\Slovenia\NA\NA.shp"

aspect_reclass_raster_path = r"D:\Eco_vine_goals\SLO_land_use_analysis\EVG_asp_aligned.tif"
if not os.path.isfile(aspect_reclass_raster_path):
    match_two_rasters(aspect_reclass_nonaligned_raster_path, land_use_raster_path, aspect_reclass_raster_path)

out_raba_rast_dir = r"D:\Eco_vine_goals\SLO_land_use_analysis"

naselja = ["Brje", "Dolenje", "Gaberje", "Planina", "Šmarje", "Tevče", "Velike Žablje", "Vrtovče", "Zavino", "Dolanci",
           "Kodreti", "Branik", "Preserje", "Spodnja Branica", "Steske", "Erzelj", "Goče", "Lože", "Manče", "Orehovica",
           "Podnanos", "Podraga", "Slap"]
evg_id_conditions = [10, 20, 21, 22, 23, 24, 30, 40, 50, 60, 70, 90]
aspect_conditions = [np.nan, (-1.1, 0), (0, 22.5, 337.5, 360), (22.5, 67.5), (67.5, 112.5), (112.5, 157.5), (157.5, 202.5),
                     (202.5, 247.5), (247.5, 292.5), (292.5, 337.5)]

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

    out_asp_rast = os.path.join(out_raba_rast_dir, "asp_recl_{}.tif".format(naselje))
    if not os.path.isfile(out_asp_rast):
        clip_raster_to_shape_where_att(raster_path=aspect_reclass_raster_path, shape_path=na_shp_path,
                                       attribute_name="NA_UIME",
                                       selected_att_values_list=[naselje],
                                       out_raster_path=out_asp_rast)

    area_csv = calculate_statistics_from_rasters_where_conditions(raster1_path=out_raba_rast, raster2_path=out_asp_rast,
                                                                  resolution=1,
                                                                  raster1_conditions=evg_id_conditions,
                                                                  raster2_conditions=aspect_conditions, output="csv")
    csv += area_csv+"\n"
    # # no conditions pearson
    # no_conditions_csv = calculate_statistics_from_rasters_where_conditions(raster1_path=out_vin_rast,
    #                                                                        raster2_path=out_asp_rast,
    #                                                                        resolution=1,
    #                                                                        raster1_conditions=[None],
    #                                                                        raster2_conditions=[None],
    #                                                                        output="csv",
    #                                                                        statistic=["pearson"])
    # print(no_conditions_csv)


fp = open(os.path.join(out_raba_rast_dir, "evg_land_use_aspect.csv"), "w")
fp.write(csv)
fp.close()
