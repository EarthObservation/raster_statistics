from functions import *
import os

land_use_raster_path = r"D:\Eco_vine_goals\Slovenia\data\raba_raster.tif"
soil_non_aligned_raster_path = r"D:\Eco_vine_goals\Slovenia\data\ped_k_rast.tif"
na_shp_path = r"D:\Eco_vine_goals\Slovenia\data\na_clip.shp"

soil_raster_path = r"D:\Eco_vine_goals\SLO_land_use_analysis\EVG_soil_aligned.tif"
if not os.path.isfile(soil_raster_path):
    match_two_rasters(soil_non_aligned_raster_path, land_use_raster_path, soil_raster_path)

out_raba_rast_dir = r"D:\Eco_vine_goals\SLO_land_use_analysis"

evg_id_conditions = [(9, 91), 10, 20, 21, 22, 23, 24, 30, 40, 50, 60, 70, 90]
soil_conditions = [np.nan, 63, 139, 140, 430, 1156, 1232, 1234, 1241, 1242, 1243, 1279, 1282]
naselja = ["Brje", "Dolenje", "Gaberje", "Planina", "Šmarje", "Tevče", "Velike Žablje", "Vrtovče", "Zavino", "Dolanci",
           "Kodreti", "Branik", "Preserje", "Spodnja Branica", "Steske", "Erzelj", "Goče", "Lože", "Manče", "Orehovica",
           "Podnanos", "Podraga", "Slap"]

csv = ""
for naselje in naselja:
    print(naselje)
    out_land_use_rast = os.path.join(out_raba_rast_dir, "raba_{}.tif".format(naselje))
    if not os.path.isfile(out_land_use_rast):
        clip_raster_to_shape_where_att(raster_path=land_use_raster_path, shape_path=na_shp_path,
                                       attribute_name="NA_UIME",
                                       selected_att_values_list=[naselje],
                                       out_raster_path=out_land_use_rast)

    out_soil_rast = os.path.join(out_raba_rast_dir, "soil_{}.tif".format(naselje))
    if not os.path.isfile(out_soil_rast):
        clip_raster_to_shape_where_att(raster_path=soil_raster_path, shape_path=na_shp_path,
                                       attribute_name="NA_UIME",
                                       selected_att_values_list=[naselje],
                                       out_raster_path=out_soil_rast)

    naselje_csv = calculate_statistics_from_rasters_where_conditions(raster1_path=out_land_use_rast,
                                                                     raster2_path=out_soil_rast,
                                                                     resolution=1,
                                                                     raster1_conditions=evg_id_conditions,
                                                                     raster2_conditions=soil_conditions,
                                                                     output="csv")
    csv += naselje_csv + "\n"

fp = open(os.path.join(out_raba_rast_dir, "evg_raba_soil.csv"), "w")
fp.write(csv)
fp.close()