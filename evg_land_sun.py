from functions import *
import os

land_use_raster_path = r"D:\Eco_vine_goals\Slovenia\data\raba_raster.tif"
sun_nonaligned_raster_path = r"D:\Eco_vine_goals\Slovenia\data\solar_rad_16_2-10_12.tif"
na_shp_path = r"D:\Eco_vine_goals\Slovenia\data\na_clip.shp"

sun_raster_path = r"D:\Eco_vine_goals\SLO_land_use_analysis\EVG_sun_aligned.tif"
if not os.path.isfile(sun_raster_path):
    match_two_rasters(sun_nonaligned_raster_path, land_use_raster_path, sun_raster_path)

out_raba_rast_dir = r"D:\Eco_vine_goals\SLO_land_use_analysis"

evg_id_conditions = [(9, 91), 10, 20, 21, 22, 23, 24, 30, 40, 50, 60, 70, 90]
solar_conditions = [np.nan, (0, 500000), (500000, 600000), (600000, 700000), (700000, 800000), (800000, 900000),
                    (900000, 1000000), (1000000, 1100000), (1100000, 10000000000)]
naselja = ["Brje", "Dolenje", "Gaberje", "Planina", "Šmarje", "Tevče", "Velike Žablje", "Vrtovče", "Zavino", "Dolanci",
           "Kodreti", "Branik", "Preserje", "Spodnja Branica", "Steske", "Erzelj", "Goče", "Lože", "Manče", "Orehovica",
           "Podnanos", "Podraga", "Slap"]

csv = ""
for naselje in naselja:
    out_raba_rast = os.path.join(out_raba_rast_dir, "raba_{}.tif".format(naselje))
    if not os.path.isfile(out_raba_rast):
        clip_raster_to_shape_where_att(raster_path=land_use_raster_path, shape_path=na_shp_path,
                                       attribute_name="NA_UIME",
                                       selected_att_values_list=[naselje],
                                       out_raster_path=out_raba_rast)

    out_sun_rast = os.path.join(out_raba_rast_dir, "sun_{}.tif".format(naselje))
    if not os.path.isfile(out_sun_rast):
        clip_raster_to_shape_where_att(raster_path=sun_raster_path, shape_path=na_shp_path,
                                       attribute_name="NA_UIME",
                                       selected_att_values_list=[naselje],
                                       out_raster_path=out_sun_rast)

    naselje_csv = calculate_statistics_from_rasters_where_conditions(raster1_path=out_raba_rast,
                                                                     raster2_path=out_sun_rast,
                                                                     resolution=1,
                                                                     raster1_conditions=evg_id_conditions,
                                                                     raster2_conditions=solar_conditions,
                                                                     output="csv", min2_to_nan=1000)
    csv += naselje_csv + "\n"

fp = open(os.path.join(out_raba_rast_dir, "evg_raba_solar.csv"), "w")
fp.write(csv)
fp.close()
