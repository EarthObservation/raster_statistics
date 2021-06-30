from functions import *
import os

land_use_raster_path = r"D:\Eco_vine_goals\Slovenia\data\raba_raster.tif"
terase_nonaligned_raster_path = r"D:\Eco_vine_goals\Slovenia\data\terase_rast.tif"
slope_nonaligned_raster_path = r"D:\Eco_vine_goals\Slovenia\data\slope_perc\slope_perc.tif"
aspect_raster_nonaligned_path = r"D:\Eco_vine_goals\Slovenia\data\aspect.tif"
dem_raster_nonaligned_path = r"D:\Eco_vine_goals\Slovenia\data\EVG_DEM.tif"
solar_nonaligned_raster_path = r"D:\Eco_vine_goals\Slovenia\data\solar_rad_16_2-10_12.tif"  # solar
na_shp_path = r"D:\Eco_vine_goals\Slovenia\data\na_clip.shp"

out_raba_rast_dir = r"D:\Eco_vine_goals\SLO_land_use_analysis"

# slope_raster_path = r"D:\Eco_vine_goals\SLO_land_use_analysis\EVG_slope_aligned.tif"
# if not os.path.isfile(slope_raster_path):
#     match_two_rasters(slope_nonaligned_raster_path, naravnost_raster_path, slope_raster_path)
# aspect_raster_path = r"D:\Eco_vine_goals\SLO_land_use_analysis\EVG_aspect_aligned.tif"
# if not os.path.isfile(aspect_raster_path):
#     match_two_rasters(aspect_raster_nonaligned_path, naravnost_raster_path, aspect_raster_path)
# dem_raster_path = r"D:\Eco_vine_goals\SLO_land_use_analysis\EVG_dem_aligned.tif"
# if not os.path.isfile(dem_raster_path):
#     match_two_rasters(dem_raster_nonaligned_path, naravnost_raster_path, dem_raster_path)
terase_raster_path = r"D:\Eco_vine_goals\SLO_land_use_analysis\EVG_terase_aligned.tif"
if not os.path.isfile(terase_raster_path):
    match_two_rasters(terase_nonaligned_raster_path, land_use_raster_path, terase_raster_path)
solar_raster_path = r"D:\Eco_vine_goals\SLO_land_use_analysis\EVG_solar_aligned.tif"
if not os.path.isfile(solar_raster_path):
    match_two_rasters(solar_nonaligned_raster_path, land_use_raster_path, solar_raster_path)


naselja = ["Brje", "Dolenje", "Gaberje", "Planina", "Šmarje", "Tevče", "Velike Žablje", "Vrtovče", "Zavino", "Dolanci",
           "Kodreti", "Branik", "Preserje", "Spodnja Branica", "Steske", "Erzelj", "Goče", "Lože", "Manče", "Orehovica",
           "Podnanos", "Podraga", "Slap"]
evg_id_conditions = [10, 20, 21, 22, 23, 24, 30, 40, 50, 60, 70, 90, (9, 91)]
terase_conditions = [1]
slope_conditions = [(0, 10), (10, 30), (30, 50), (50, 1000000)]
height_conditions = [(50, 100), (100, 150), (150, 200), (200, 250), (250, 300), (300, 350), (350, 1000)]
aspect_conditions = [(0, 22.5, 337.5, 360), (22.5, 67.5), (67.5, 112.5), (112.5, 157.5), (157.5, 202.5),
                     (202.5, 247.5), (247.5, 292.5), (292.5, 337.5)]
solar_conditions = [(0, 500000), (500000, 700000), (700000, 900000), (900000,1100000), (1100000, 1000000000)]

out_raba_rast = os.path.join(out_raba_rast_dir, "raba_{}.tif".format("naselja"))
if not os.path.isfile(out_raba_rast):
    clip_raster_to_shape_where_att(raster_path=land_use_raster_path, shape_path=na_shp_path,
                                   attribute_name="NA_UIME",
                                   selected_att_values_list=naselja,
                                   out_raster_path=out_raba_rast)

out_terase_rast = os.path.join(out_raba_rast_dir, "terase_{}.tif".format("naselja"))
if not os.path.isfile(out_terase_rast):
    clip_raster_to_shape_where_att(raster_path=terase_raster_path, shape_path=na_shp_path,
                                   attribute_name="NA_UIME",
                                   selected_att_values_list=naselja,
                                   out_raster_path=out_terase_rast)
#
# out_slope_rast = os.path.join(out_raba_rast_dir, "slope_{}.tif".format("naselja"))
# if not os.path.isfile(out_slope_rast):
#     clip_raster_to_shape_where_att(raster_path=slope_raster_path, shape_path=na_shp_path,
#                                    attribute_name="NA_UIME",
#                                    selected_att_values_list=naselja,
#                                    out_raster_path=out_slope_rast)
#
# out_eco_vin_rast = os.path.join(out_raba_rast_dir, "dem_{}.tif".format("naselja"))
# if not os.path.isfile(out_eco_vin_rast):
#     clip_raster_to_shape_where_att(raster_path=dem_raster_path, shape_path=na_shp_path,
#                                    attribute_name="NA_UIME",
#                                    selected_att_values_list=naselja,
#                                    out_raster_path=out_eco_vin_rast)
#
# out_aspect_rast = os.path.join(out_raba_rast_dir, "asp_{}.tif".format("naselja"))
# if not os.path.isfile(out_aspect_rast):
#     clip_raster_to_shape_where_att(raster_path=aspect_raster_path, shape_path=na_shp_path,
#                                    attribute_name="NA_UIME",
#                                    selected_att_values_list=naselja,
#                                    out_raster_path=out_aspect_rast)
out_solar_rast = os.path.join(out_raba_rast_dir, "solar_{}.tif".format("naselja"))
if not os.path.isfile(out_solar_rast):
    clip_raster_to_shape_where_att(raster_path=solar_raster_path, shape_path=na_shp_path,
                                   attribute_name="NA_UIME",
                                   selected_att_values_list=naselja,
                                   out_raster_path=out_solar_rast)

# # raba, terase, višinski
# area_csv = calculate_statistics_from_3rasters_where_conditions(raster1_path=out_vin_rast,
#                                                                raster2_path=out_eco_vin_rast,
#                                                                raster3_path=terase_raster_path,
#                                                                resolution=1,
#                                                                raster1_conditions=naravnost_conditions,
#                                                                raster2_conditions=height_conditions,
#                                                                raster3_conditions=terase_conditions, output="csv")
# fp = open(os.path.join(out_raba_rast_dir, "evg_raba_vis_terase.csv"), "w")
# fp.write(area_csv)
# fp.close()
# # raba terase naklon
# area_csv = calculate_statistics_from_3rasters_where_conditions(raster1_path=out_vin_rast,
#                                                                raster2_path=out_slope_rast,
#                                                                raster3_path=terase_raster_path,
#                                                                resolution=1,
#                                                                raster1_conditions=naravnost_conditions,
#                                                                raster2_conditions=slope_conditions,
#                                                                raster3_conditions=terase_conditions, output="csv")
# fp = open(os.path.join(out_raba_rast_dir, "evg_raba_naklon_terase.csv"), "w")
# fp.write(area_csv)
# fp.close()
# # raba terase ekspozicija
# area_csv = calculate_statistics_from_3rasters_where_conditions(raster1_path=out_vin_rast,
#                                                                raster2_path=out_aspect_rast,
#                                                                raster3_path=terase_raster_path,
#                                                                resolution=1,
#                                                                raster1_conditions=naravnost_conditions,
#                                                                raster2_conditions=aspect_conditions,
#                                                                raster3_conditions=terase_conditions, output="csv")
# fp = open(os.path.join(out_raba_rast_dir, "raba_ekspozicija_terase.csv"), "w")
# fp.write(area_csv)
# fp.close()

# raba terase solar
area_csv = calculate_statistics_from_3rasters_where_conditions(raster1_path=out_raba_rast,
                                                               raster2_path=out_solar_rast,
                                                               raster3_path=terase_raster_path,
                                                               resolution=1,
                                                               raster1_conditions=evg_id_conditions,
                                                               raster2_conditions=solar_conditions,
                                                               raster3_conditions=terase_conditions, output="csv")
fp = open(os.path.join(out_raba_rast_dir, "raba_solar_terase.csv"), "w")
fp.write(area_csv)
fp.close()
