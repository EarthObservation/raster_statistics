from functions import *
import os

land_use_raster_path = r"D:\Eco_vine_goals\Slovenia\data\raba_raster.tif"
solar_nonaligned_raster_path = r"D:\Eco_vine_goals\Slovenia\data\solar_rad_16_2-10_12.tif"  # solar
aspect_raster_nonaligned_path = r"D:\Eco_vine_goals\Slovenia\data\aspect.tif"
na_shp_path = r"D:\Eco_vine_goals\Slovenia\data\na_clip.shp"

out_raba_rast_dir = r"D:\Eco_vine_goals\SLO_land_use_analysis"

solar_raster_path = r"D:\Eco_vine_goals\SLO_land_use_analysis\EVG_solar_aligned.tif"
if not os.path.isfile(solar_raster_path):
    match_two_rasters(solar_nonaligned_raster_path, land_use_raster_path, solar_raster_path)
aspect_raster_path = r"D:\Eco_vine_goals\SLO_land_use_analysis\EVG_aspect_aligned.tif"
if not os.path.isfile(aspect_raster_path):
    match_two_rasters(aspect_raster_nonaligned_path, land_use_raster_path, aspect_raster_path)
dem_raster_path = r"D:\Eco_vine_goals\SLO_land_use_analysis\EVG_dem_aligned.tif"


naselja = ["Brje", "Dolenje", "Gaberje", "Planina", "Šmarje", "Tevče", "Velike Žablje", "Vrtovče", "Zavino", "Dolanci",
           "Kodreti", "Branik", "Preserje", "Spodnja Branica", "Steske", "Erzelj", "Goče", "Lože", "Manče", "Orehovica",
           "Podnanos", "Podraga", "Slap"]
evg_id_conditions = [(9, 91), 10, 20, 21, 22, 23, 24, 30, 40, 50, 60, 70, 90]
solar_conditions = [np.nan, (0, 500000), (500000, 700000), (700000, 900000), (900000,1100000), (1100000, 1000000000)]
aspect_conditions = [np.nan, (-1.1, 0), (0, 22.5, 337.5, 360), (22.5, 67.5), (67.5, 112.5), (112.5, 157.5),
                     (157.5, 202.5), (202.5, 247.5), (247.5, 292.5), (292.5, 337.5)]

out_raba_rast = os.path.join(out_raba_rast_dir, "raba_{}.tif".format("naselja"))
if not os.path.isfile(out_raba_rast):
    clip_raster_to_shape_where_att(raster_path=land_use_raster_path, shape_path=na_shp_path,
                                   attribute_name="NA_UIME",
                                   selected_att_values_list=naselja,
                                   out_raster_path=out_raba_rast)

out_solar_rast = os.path.join(out_raba_rast_dir, "solar_{}.tif".format("naselja"))
if not os.path.isfile(out_solar_rast):
    clip_raster_to_shape_where_att(raster_path=solar_raster_path, shape_path=na_shp_path,
                                   attribute_name="NA_UIME",
                                   selected_att_values_list=naselja,
                                   out_raster_path=out_solar_rast)

out_aspect_rast = os.path.join(out_raba_rast_dir, "asp_{}.tif".format("naselja"))
if not os.path.isfile(out_aspect_rast):
    clip_raster_to_shape_where_att(raster_path=aspect_raster_path, shape_path=na_shp_path,
                                   attribute_name="NA_UIME",
                                   selected_att_values_list=naselja,
                                   out_raster_path=out_aspect_rast)

# raba, terase, višinski
area_csv = calculate_statistics_from_3rasters_where_conditions(raster1_path=out_aspect_rast,
                                                               raster2_path=out_raba_rast,
                                                               raster3_path=out_solar_rast,
                                                               resolution=1,
                                                               raster1_conditions=aspect_conditions,
                                                               raster2_conditions=evg_id_conditions,
                                                               raster3_conditions=solar_conditions, output="csv")
fp = open(os.path.join(out_raba_rast_dir, "evg_raba_solar_asp.csv"), "w")
fp.write(area_csv)
fp.close()