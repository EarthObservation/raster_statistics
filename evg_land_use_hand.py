from functions import *
import os
import json

land_use_raster_path = r"D:\Eco_vine_goals\Slovenia\data\raba_raster.tif"
hand_nonaligned_raster_path = r"D:\Eco_vine_goals\Slovenia\data\hand_index.tif"
na_shp_path = r"D:\Eco_vine_goals\Slovenia\NA\NA.shp"

# resample hand
hand_resample_raster_path = r"D:\Eco_vine_goals\SLO_land_use_analysis\hand_resample.tif"
kwargs = {"xRes": 1, "yRes": 1, "resampleAlg": "bilinear", "format": 'GTiff'}
ds = gdal.Translate(hand_resample_raster_path, hand_nonaligned_raster_path, **kwargs)

hand_raster_path = r"D:\Eco_vine_goals\SLO_land_use_analysis\EVG_hand_aligned.tif"
if not os.path.isfile(hand_raster_path):
    match_two_rasters(hand_resample_raster_path, land_use_raster_path, hand_raster_path)

out_raba_rast_dir = r"D:\Eco_vine_goals\SLO_land_use_analysis"

naselja = ["Brje", "Dolenje", "Gaberje", "Planina", "Šmarje", "Tevče", "Velike Žablje", "Vrtovče", "Zavino", "Dolanci",
           "Kodreti", "Branik", "Preserje", "Spodnja Branica", "Steske", "Erzelj", "Goče", "Lože", "Manče", "Orehovica",
           "Podnanos", "Podraga", "Slap"]
evg_id_conditions = [10, 20, 21, 22, 23, 24, 30, 40, 50, 60, 70, 90]
statistics = ["mean", "max", "min", "quantile_5", "quantile_95"]
hand_conditions = [None]

result_dict = {}
csv = ""
# for naselje in naselja:
#     print(naselje)
#     out_vin_rast = os.path.join(out_raba_rast_dir, "raba_{}.tif".format(naselje))
#     if not os.path.isfile(out_vin_rast):
#         clip_raster_to_shape_where_att(raster_path=naravnost_raster_path, shape_path=na_shp_path,
#                                        attribute_name="NA_UIME",
#                                        selected_att_values_list=[naselje],
#                                        out_raster_path=out_vin_rast)
#
#     out_hand_rast = os.path.join(out_raba_rast_dir, "hand_{}.tif".format(naselje))
#     if not os.path.isfile(out_hand_rast):
#         clip_raster_to_shape_where_att(raster_path=hand_raster_path, shape_path=na_shp_path,
#                                        attribute_name="NA_UIME",
#                                        selected_att_values_list=[naselje],
#                                        out_raster_path=out_hand_rast)
#
#     area_csv = calculate_statistics_from_rasters_where_conditions(raster1_path=out_vin_rast,
#                                                                   raster2_path=out_hand_rast,
#                                                                   resolution=1,
#                                                                   raster1_conditions=naravnost_conditions,
#                                                                   raster2_conditions=hand_conditions, output="csv",
#                                                                   statistic=statistics)
#     csv += area_csv + "\n"
#
# fp = open(os.path.join(out_raba_rast_dir, "evg_land_use_hand.csv"), "w")
# fp.write(csv)
# fp.close()


clip_shp_path = r"D:\Eco_vine_goals\Slovenia\data\EVG_obmocje_new.shp"
raba_all_path = os.path.join(out_raba_rast_dir, "raba_{}.tif".format("all"))
if not os.path.isfile(raba_all_path):
    clip_raster_to_shape_where_att(raster_path=land_use_raster_path, shape_path=clip_shp_path,
                                   attribute_name="ENOTA",
                                   selected_att_values_list=["NA"],
                                   out_raster_path=raba_all_path)


hand_all_path = os.path.join(out_raba_rast_dir, "hand_{}.tif".format("all"))
if not os.path.isfile(hand_all_path):
    clip_raster_to_shape_where_att(raster_path=hand_raster_path, shape_path=clip_shp_path,
                                   attribute_name="ENOTA",
                                   selected_att_values_list=["NA"],
                                   out_raster_path=hand_all_path)

all_no_cond_csv = calculate_statistics_from_rasters_where_conditions(raster1_path=raba_all_path,
                                                                     raster2_path=hand_all_path,
                                                                     resolution=1,
                                                                     raster1_conditions=evg_id_conditions,
                                                                     raster2_conditions=hand_conditions, output="csv",
                                                                     statistic=statistics)
print(all_no_cond_csv)