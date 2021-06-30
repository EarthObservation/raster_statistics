from functions import *
import os

land_use_raster_path = r"D:\Eco_vine_goals\Slovenia\data\raba_raster.tif"
terase_nonaligned_raster_path = r"D:\Eco_vine_goals\Slovenia\data\terase_rast.tif"
na_shp_path = r"D:\Eco_vine_goals\Slovenia\data\na_clip.shp"

out_raba_rast_dir = r"D:\Eco_vine_goals\SLO_land_use_analysis"

terase_raster_path = r"D:\Eco_vine_goals\SLO_land_use_analysis\EVG_terase_aligned.tif"
if not os.path.isfile(terase_raster_path):
    match_two_rasters(terase_nonaligned_raster_path, land_use_raster_path, terase_raster_path)

naselja = ["Brje", "Dolenje", "Gaberje", "Planina", "Šmarje", "Tevče", "Velike Žablje", "Vrtovče", "Zavino", "Dolanci",
           "Kodreti", "Branik", "Preserje", "Spodnja Branica", "Steske", "Erzelj", "Goče", "Lože", "Manče", "Orehovica",
           "Podnanos", "Podraga", "Slap"]
evg_id_conditions = [(9, 91), 10, 20, 21, 22, 23, 24, 30, 40, 50, 60, 70, 90]
terase_conditions = [1]

csv = ""
for naselje in naselja:
    out_raba_rast = os.path.join(out_raba_rast_dir, "raba_{}.tif".format(naselje))
    if not os.path.isfile(out_raba_rast):
        clip_raster_to_shape_where_att(raster_path=land_use_raster_path, shape_path=na_shp_path,
                                       attribute_name="NA_UIME",
                                       selected_att_values_list=[naselje],
                                       out_raster_path=out_raba_rast)

    out_terase_rast = os.path.join(out_raba_rast_dir, "terase_{}.tif".format(naselje))
    if not os.path.isfile(out_terase_rast):
        clip_raster_to_shape_where_att(raster_path=terase_raster_path, shape_path=na_shp_path,
                                       attribute_name="NA_UIME",
                                       selected_att_values_list=[naselje],
                                       out_raster_path=out_terase_rast)

    area_csv = calculate_statistics_from_rasters_where_conditions(raster1_path=out_raba_rast,
                                                                  raster2_path=out_terase_rast,
                                                                  resolution=1,
                                                                  raster1_conditions=evg_id_conditions,
                                                                  raster2_conditions=terase_conditions, output="csv")
    csv += area_csv + "\n"

fp = open(os.path.join(out_raba_rast_dir, "evg_land_use_terase.csv"), "w")
fp.write(csv)
fp.close()