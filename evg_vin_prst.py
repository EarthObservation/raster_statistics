from functions import *
import os

soil_non_aligned_raster_path = r"D:\Eco_vine_goals\Slovenia\data\ped_k_rast.tif"
vin_raster_path = r"D:\Eco_vine_goals\Slovenia\data\vin_rast.tif"
eko_vin_non_aligned_raster_path = r"D:\Eco_vine_goals\Slovenia\data\vin_eko_rast.tif"
na_shp_path = r"D:\Eco_vine_goals\Slovenia\data\na_clip.shp"

soil_raster_path = r"D:\Eco_vine_goals\SLO_land_use_analysis\soil_aligned.tif"
if not os.path.isfile(soil_raster_path):
    match_two_rasters(soil_non_aligned_raster_path, vin_raster_path, soil_raster_path)

eko_vin_raster_path = r"D:\Eco_vine_goals\SLO_land_use_analysis\eko_vin_aligned.tif"
if not os.path.isfile(eko_vin_raster_path):
    match_two_rasters(eko_vin_non_aligned_raster_path, vin_raster_path, eko_vin_raster_path)

out_raba_rast_dir = r"D:\Eco_vine_goals\SLO_land_use_analysis"

naselja = ["Brje", "Dolenje", "Gaberje", "Planina", "Šmarje", "Tevče", "Velike Žablje", "Vrtovče", "Zavino", "Dolanci",
           "Kodreti", "Branik", "Preserje", "Spodnja Branica", "Steske", "Erzelj", "Goče", "Lože", "Manče", "Orehovica",
           "Podnanos", "Podraga", "Slap"]

vin_conditions = [1]
soil_conditions = [np.nan, 63, 139, 140, 430, 1156, 1232, 1234, 1241, 1242, 1243, 1279, 1282]

csv_1 = ""
csv_2 = ""
for naselje in naselja:
    print(naselje)
    out_vin_rast = os.path.join(out_raba_rast_dir, "vin_{}.tif".format(naselje))
    if not os.path.isfile(out_vin_rast):
        clip_raster_to_shape_where_att(raster_path=vin_raster_path, shape_path=na_shp_path,
                                       attribute_name="NA_UIME",
                                       selected_att_values_list=[naselje],
                                       out_raster_path=out_vin_rast)

    out_eco_vin_rast = os.path.join(out_raba_rast_dir, "eko_vin_{}.tif".format(naselje))
    if not os.path.isfile(out_eco_vin_rast):
        clip_raster_to_shape_where_att(raster_path=eko_vin_raster_path, shape_path=na_shp_path,
                                       attribute_name="NA_UIME",
                                       selected_att_values_list=[naselje],
                                       out_raster_path=out_eco_vin_rast)

    out_soil_rast = os.path.join(out_raba_rast_dir, "soil_{}.tif".format(naselje))
    if not os.path.isfile(out_soil_rast):
        clip_raster_to_shape_where_att(raster_path=soil_raster_path, shape_path=na_shp_path,
                                       attribute_name="NA_UIME",
                                       selected_att_values_list=[naselje],
                                       out_raster_path=out_soil_rast)

    naselje_csv_1 = calculate_statistics_from_rasters_where_conditions(raster1_path=out_vin_rast,
                                                                       raster2_path=out_soil_rast,
                                                                       resolution=1,
                                                                       raster1_conditions=vin_conditions,
                                                                       raster2_conditions=soil_conditions,
                                                                       output="csv")
    csv_1 += naselje_csv_1 + "\n"
    naselje_csv_2 = calculate_statistics_from_rasters_where_conditions(raster1_path=out_eco_vin_rast,
                                                                       raster2_path=out_soil_rast,
                                                                       resolution=1,
                                                                       raster1_conditions=vin_conditions,
                                                                       raster2_conditions=soil_conditions,
                                                                       output="csv")
    csv_2 += naselje_csv_2 + "\n"

out_vin_rast = os.path.join(out_raba_rast_dir, "vin_{}.tif".format("naselja"))
if not os.path.isfile(out_vin_rast):
    clip_raster_to_shape_where_att(raster_path=vin_raster_path, shape_path=na_shp_path,
                                   attribute_name="NA_UIME",
                                   selected_att_values_list=naselja,
                                   out_raster_path=out_vin_rast)

out_eco_vin_rast = os.path.join(out_raba_rast_dir, "eko_vin_{}.tif".format("naselja"))
if not os.path.isfile(out_eco_vin_rast):
    clip_raster_to_shape_where_att(raster_path=eko_vin_raster_path, shape_path=na_shp_path,
                                   attribute_name="NA_UIME",
                                   selected_att_values_list=naselja,
                                   out_raster_path=out_eco_vin_rast)
print(calculate_statistics_from_raster_where_condition(raster1_path=out_vin_rast, resolution=1,
                                                       raster1_conditions=vin_conditions))
print(calculate_statistics_from_raster_where_condition(raster1_path=out_eco_vin_rast, resolution=1,
                                                       raster1_conditions=vin_conditions))

fp = open(os.path.join(out_raba_rast_dir, "evg_vin_soil.csv"), "w")
fp.write(csv_1)
fp.close()

fp = open(os.path.join(out_raba_rast_dir, "evg_eco_vin_soil.csv"), "w")
fp.write(csv_2)
fp.close()
