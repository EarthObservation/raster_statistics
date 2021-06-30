from functions import *
import os

land_use_new_raster_path = r"D:\Eco_vine_goals\Slovenia\data\raba_raster.tif"
land_use_old_non_aligned_raster_path = r"D:\Eco_vine_goals\Slovenia\data\raba_raster_2002.tif"
eko_vin_non_aligned_path = r"D:\Eco_vine_goals\Slovenia\data\vin_eko_rast.tif"
na_shp_path = r"D:\Eco_vine_goals\Slovenia\data\na_clip.shp"

land_use_old_raster_path = r"D:\Eco_vine_goals\SLO_land_use_analysis\raba_old_aligned.tif"
if not os.path.isfile(land_use_old_raster_path):
    match_two_rasters(land_use_old_non_aligned_raster_path, land_use_new_raster_path, land_use_old_raster_path)

eko_vin_path = r"D:\Eco_vine_goals\SLO_land_use_analysis\eko_vin_aligned.tif"
if not os.path.isfile(eko_vin_path):
    match_two_rasters(eko_vin_non_aligned_path, land_use_new_raster_path, eko_vin_path)

out_raba_rast_dir = r"D:\Eco_vine_goals\SLO_land_use_analysis"
evg_id_conditions = [np.nan, 10, 20, 21, 22, 23, 24, 30, 40, 50, 60, 70, 90]
vineyard_condition = [21]
eko_vin_condition = [1]
naselja = ["Brje", "Dolenje", "Gaberje", "Planina", "Šmarje", "Tevče", "Velike Žablje", "Vrtovče", "Zavino", "Dolanci",
           "Kodreti", "Branik", "Preserje", "Spodnja Branica", "Steske", "Erzelj", "Goče", "Lože", "Manče", "Orehovica",
           "Podnanos", "Podraga", "Slap"]

csv_1 = ""
csv_2 = ""
csv_3 = ""
csv_4 = ""
for naselje in naselja:
    print(naselje)
    out_land_use_rast = os.path.join(out_raba_rast_dir, "raba_{}.tif".format(naselje))
    if not os.path.isfile(out_land_use_rast):
        clip_raster_to_shape_where_att(raster_path=land_use_new_raster_path, shape_path=na_shp_path,
                                       attribute_name="NA_UIME",
                                       selected_att_values_list=[naselje],
                                       out_raster_path=out_land_use_rast)

    out_land_use_old_rast = os.path.join(out_raba_rast_dir, "raba_old_{}.tif".format(naselje))
    if not os.path.isfile(out_land_use_old_rast):
        clip_raster_to_shape_where_att(raster_path=land_use_old_raster_path, shape_path=na_shp_path,
                                       attribute_name="NA_UIME",
                                       selected_att_values_list=[naselje],
                                       out_raster_path=out_land_use_old_rast)

    out_eko_vin_rast = os.path.join(out_raba_rast_dir, "eko_vin_{}.tif".format(naselje))
    if not os.path.isfile(out_eko_vin_rast):
        clip_raster_to_shape_where_att(raster_path=eko_vin_path, shape_path=na_shp_path,
                                       attribute_name="NA_UIME",
                                       selected_att_values_list=[naselje],
                                       out_raster_path=out_eko_vin_rast)

    # sedanja raba na starih vinogradih
    naselje_csv_1 = calculate_statistics_from_rasters_where_conditions(raster1_path=out_land_use_rast,
                                                                       raster2_path=out_land_use_old_rast,
                                                                       resolution=1,
                                                                       raster1_conditions=evg_id_conditions,
                                                                       raster2_conditions=vineyard_condition,
                                                                       output="csv")
    csv_1 += naselje_csv_1 + "\n"

    # stara raba na sedanjih vinogradih
    naselje_csv_2 = calculate_statistics_from_rasters_where_conditions(raster1_path=out_land_use_rast,
                                                                       raster2_path=out_land_use_old_rast,
                                                                       resolution=1,
                                                                       raster1_conditions=vineyard_condition,
                                                                       raster2_conditions=evg_id_conditions,
                                                                       output="csv")
    csv_2 += naselje_csv_2 + "\n"

    # sedanja raba na eko_vin
    naselje_csv_3 = calculate_statistics_from_rasters_where_conditions(raster1_path=out_land_use_rast,
                                                                       raster2_path=out_eko_vin_rast,
                                                                       resolution=1,
                                                                       raster1_conditions=evg_id_conditions,
                                                                       raster2_conditions=eko_vin_condition,
                                                                       output="csv")
    csv_3 += naselje_csv_3 + "\n"

    # stara raba na eko_vin
    naselje_csv_4 = calculate_statistics_from_rasters_where_conditions(raster1_path=out_land_use_old_rast,
                                                                       raster2_path=out_eko_vin_rast,
                                                                       resolution=1,
                                                                       raster1_conditions=evg_id_conditions,
                                                                       raster2_conditions=eko_vin_condition,
                                                                       output="csv")
    csv_4 += naselje_csv_4 + "\n"

fp = open(os.path.join(out_raba_rast_dir, "sedanja_raba_stari_vin.csv"), "w")
fp.write(csv_1)
fp.close()

fp = open(os.path.join(out_raba_rast_dir, "stara_raba_sedanji_vin.csv"), "w")
fp.write(csv_2)
fp.close()

fp = open(os.path.join(out_raba_rast_dir, "sedanja_raba_eko_vin.csv"), "w")
fp.write(csv_3)
fp.close()

fp = open(os.path.join(out_raba_rast_dir, "stara_raba_eko_vin.csv"), "w")
fp.write(csv_4)
fp.close()