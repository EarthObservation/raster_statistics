from functions import *
import os
import json

land_use_raster_path = r"D:\Eco_vine_goals\Slovenia\data\raba_raster.tif"
na_shp_path = r"D:\Eco_vine_goals\Slovenia\data\na_clip.shp"

out_raba_rast_dir = r"D:\Eco_vine_goals\SLO_land_use_analysis"

naselja = ["Brje", "Dolenje", "Gaberje", "Planina", "Šmarje", "Tevče", "Velike Žablje", "Vrtovče", "Zavino", "Dolanci",
           "Kodreti", "Branik", "Preserje", "Spodnja Branica", "Steske", "Erzelj", "Goče", "Lože", "Manče", "Orehovica",
           "Podnanos", "Podraga", "Slap"]
evg_id_conditions = [10, 20, 21, 22, 23, 24, 30, 40, 50, 60, 70, 90]
statistics = ["area"]

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

    area_csv = calculate_statistics_from_raster_where_condition(raster1_path=out_raba_rast, resolution=1,
                                                                raster1_conditions=evg_id_conditions,
                                                                output="csv", statistic=statistics)
    csv += area_csv + "\n"

fp = open(os.path.join(out_raba_rast_dir, "evg_land_use.csv"), "w")
fp.write(csv)
fp.close()

print(calculate_statistics_from_raster_where_condition(raster1_path=land_use_raster_path, resolution=1,
                                                       raster1_conditions=evg_id_conditions,
                                                       output="csv", statistic=statistics))

print(calculate_statistics_from_raster_where_condition(raster1_path=land_use_raster_path, resolution=1,
                                                       raster1_conditions=[(0,100)],
                                                       output="csv", statistic=statistics))
