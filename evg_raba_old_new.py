from functions import *
import os

land_use_new_raster_path = r"D:\Eco_vine_goals\Slovenia\data\raba_raster.tif"
land_use_old_non_aligned_raster_path = r"D:\Eco_vine_goals\Slovenia\data\raba_raster_2002.tif"
na_shp_path = r"D:\Eco_vine_goals\Slovenia\data\na_clip.shp"
aspect_non_aligned_raster_path = r"D:\Eco_vine_goals\Slovenia\data\aspect.tif"
dem_non_aligned_raster_path = r"D:\Eco_vine_goals\Slovenia\data\EVG_DEM.tif"
soil_non_aligned_raster_path = r"D:\Eco_vine_goals\Slovenia\data\ped_k_rast.tif"
slope_non_aligned_raster_path = r"D:\Eco_vine_goals\Slovenia\data\slope_perc\slope_perc.tif"

land_use_old_raster_path = r"D:\Eco_vine_goals\SLO_land_use_analysis\raba_old_aligned.tif"
if not os.path.isfile(land_use_old_raster_path):
    match_two_rasters(land_use_old_non_aligned_raster_path, land_use_new_raster_path, land_use_old_raster_path)

aspect_raster_path = r"D:\Eco_vine_goals\SLO_land_use_analysis\aspect_aligned.tif"
if not os.path.isfile(aspect_raster_path):
    match_two_rasters(aspect_non_aligned_raster_path, land_use_new_raster_path, aspect_raster_path)

dem_raster_path = r"D:\Eco_vine_goals\SLO_land_use_analysis\dem_aligned.tif"
if not os.path.isfile(dem_raster_path):
    match_two_rasters(dem_non_aligned_raster_path, land_use_new_raster_path, dem_raster_path)

soil_raster_path = r"D:\Eco_vine_goals\SLO_land_use_analysis\soil_aligned.tif"
if not os.path.isfile(soil_raster_path):
    match_two_rasters(soil_non_aligned_raster_path, land_use_new_raster_path, soil_raster_path)

slope_raster_path = r"D:\Eco_vine_goals\SLO_land_use_analysis\slope_aligned.tif"
if not os.path.isfile(slope_raster_path):
    match_two_rasters(slope_non_aligned_raster_path, land_use_new_raster_path, slope_raster_path)

out_raba_rast_dir = r"D:\Eco_vine_goals\SLO_land_use_analysis"
evg_id_conditions = [10, 20, 21, 22, 23, 24, 30, 40, 50, 60, 70, 90]
aspect_conditions = [np.nan, (0, 22.5, 337.5, 360), (22.5, 67.5), (67.5, 112.5), (112.5, 157.5), (157.5, 202.5),
                     (202.5, 247.5), (247.5, 292.5), (292.5, 337.5)]
height_conditions = [np.nan, (50, 100), (100, 150), (150, 200), (200, 250), (250, 300), (300, 350),
                     (350, 1000)]
soil_conditions = [np.nan, 63, 139, 140, 430, 1156, 1232, 1234, 1241, 1242, 1243, 1279, 1282]
slope_conditions = [np.nan, (0, 3), (3, 7), (7, 13), (13, 21), (21, 31), (31, 46), (46, 1000)]
naselja = ["Brje", "Dolenje", "Gaberje", "Planina", "Šmarje", "Tevče", "Velike Žablje", "Vrtovče", "Zavino", "Dolanci",
           "Kodreti", "Branik", "Preserje", "Spodnja Branica", "Steske", "Erzelj", "Goče", "Lože", "Manče", "Orehovica",
           "Podnanos", "Podraga", "Slap"]

out_raba_new_rast = os.path.join(out_raba_rast_dir, "raba_new_{}.tif".format("naselja"))
if not os.path.isfile(out_raba_new_rast):
    clip_raster_to_shape_where_att(raster_path=land_use_new_raster_path, shape_path=na_shp_path,
                                   attribute_name="NA_UIME",
                                   selected_att_values_list=naselja,
                                   out_raster_path=out_raba_new_rast)

out_raba_old_rast = os.path.join(out_raba_rast_dir, "raba_old_{}.tif".format("naselja"))
if not os.path.isfile(out_raba_old_rast):
    clip_raster_to_shape_where_att(raster_path=land_use_old_raster_path, shape_path=na_shp_path,
                                   attribute_name="NA_UIME",
                                   selected_att_values_list=naselja,
                                   out_raster_path=out_raba_old_rast)

out_aspect_rast = os.path.join(out_raba_rast_dir, "aspect_{}.tif".format("naselja"))
if not os.path.isfile(out_aspect_rast):
    clip_raster_to_shape_where_att(raster_path=aspect_raster_path, shape_path=na_shp_path,
                                   attribute_name="NA_UIME",
                                   selected_att_values_list=naselja,
                                   out_raster_path=out_aspect_rast)

out_dem_rast = os.path.join(out_raba_rast_dir, "dem_{}.tif".format("naselja"))
if not os.path.isfile(out_dem_rast):
    clip_raster_to_shape_where_att(raster_path=dem_raster_path, shape_path=na_shp_path,
                                   attribute_name="NA_UIME",
                                   selected_att_values_list=naselja,
                                   out_raster_path=out_dem_rast)

out_soil_rast = os.path.join(out_raba_rast_dir, "soil_{}.tif".format("naselja"))
if not os.path.isfile(out_soil_rast):
    clip_raster_to_shape_where_att(raster_path=soil_raster_path, shape_path=na_shp_path,
                                   attribute_name="NA_UIME",
                                   selected_att_values_list=naselja,
                                   out_raster_path=out_soil_rast)

out_slope_rast = os.path.join(out_raba_rast_dir, "slope_{}.tif".format("naselja"))
if not os.path.isfile(out_slope_rast):
    clip_raster_to_shape_where_att(raster_path=slope_raster_path, shape_path=na_shp_path,
                                   attribute_name="NA_UIME",
                                   selected_att_values_list=naselja,
                                   out_raster_path=out_slope_rast)

# csv = calculate_statistics_from_rasters_where_conditions(raster1_path=out_raba_old_rast,
#                                                          raster2_path=out_raba_new_rast,
#                                                          resolution=1,
#                                                          raster1_conditions=naravnost_conditions,
#                                                          raster2_conditions=naravnost_conditions,
#                                                          output="csv")
#
# fp = open(os.path.join(out_raba_rast_dir, "evg_raba_old_new.csv"), "w")
# fp.write(csv)
# fp.close()

# csv_aspect = ""
# csv_aspect += calculate_statistics_from_rasters_where_conditions(raster1_path=out_raba_old_rast,
#                                                                  raster2_path=out_aspect_rast,
#                                                                  resolution=1,
#                                                                  raster1_conditions=naravnost_conditions,
#                                                                  raster2_conditions=aspect_conditions,
#                                                                  output="csv", min2_to_nan=0.001, max2_to_nan=360)
# csv_aspect += "\n"
# csv_aspect += calculate_statistics_from_rasters_where_conditions(raster1_path=out_raba_new_rast,
#                                                                  raster2_path=out_aspect_rast,
#                                                                  resolution=1,
#                                                                  raster1_conditions=naravnost_conditions,
#                                                                  raster2_conditions=aspect_conditions,
#                                                                  output="csv", min2_to_nan=0.001, max2_to_nan=360)
# csv_aspect += "\n"
# print("Aspect\n")
# print(csv_aspect)
#
#
# csv_height = ""
# csv_height += calculate_statistics_from_rasters_where_conditions(raster1_path=out_raba_old_rast,
#                                                                  raster2_path=out_dem_rast,
#                                                                  resolution=1,
#                                                                  raster1_conditions=naravnost_conditions,
#                                                                  raster2_conditions=height_conditions,
#                                                                  output="csv", min2_to_nan=0.001)
# csv_height += "\n"
# csv_height += calculate_statistics_from_rasters_where_conditions(raster1_path=out_raba_new_rast,
#                                                                  raster2_path=out_dem_rast,
#                                                                  resolution=1,
#                                                                  raster1_conditions=naravnost_conditions,
#                                                                  raster2_conditions=height_conditions,
#                                                                  output="csv", min2_to_nan=0.001)
# csv_height += "\n"
# print("Height\n")
# print(csv_height)
#
# csv_soil = ""
# csv_soil += calculate_statistics_from_rasters_where_conditions(raster1_path=out_raba_old_rast,
#                                                                raster2_path=out_land_use_old_rast,
#                                                                resolution=1,
#                                                                raster1_conditions=naravnost_conditions,
#                                                                raster2_conditions=soil_conditions,
#                                                                output="csv")
# csv_soil += "\n"
# csv_soil += calculate_statistics_from_rasters_where_conditions(raster1_path=out_raba_new_rast,
#                                                                raster2_path=out_land_use_old_rast,
#                                                                resolution=1,
#                                                                raster1_conditions=naravnost_conditions,
#                                                                raster2_conditions=soil_conditions,
#                                                                output="csv")
# csv_soil += "\n"
# print("Soil\n")
# print(csv_soil)
#

csv_slope = ""
csv_slope += calculate_statistics_from_rasters_where_conditions(raster1_path=out_raba_old_rast,
                                                                raster2_path=out_slope_rast,
                                                                resolution=1,
                                                                raster1_conditions=evg_id_conditions,
                                                                raster2_conditions=slope_conditions,
                                                                output="csv",
                                                                condition_comparison="<=x<",
                                                                  min2_to_nan=0.0001,
                                                                  max2_to_nan=999)
csv_slope += "\n"
csv_slope += calculate_statistics_from_rasters_where_conditions(raster1_path=out_raba_new_rast,
                                                                raster2_path=out_slope_rast,
                                                                resolution=1,
                                                                raster1_conditions=evg_id_conditions,
                                                                raster2_conditions=slope_conditions,
                                                                output="csv",
                                                                condition_comparison="<=x<",
                                                                  min2_to_nan=0.0001,
                                                                  max2_to_nan=999)
csv_slope += "\n"
print("Slope\n")
print(csv_slope)