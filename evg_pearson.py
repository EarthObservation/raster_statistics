from functions import *
import os

land_use_raster_path = r"D:\Eco_vine_goals\Slovenia\data\raba_raster.tif"
slope_nonaligned_raster_path = r"D:\Eco_vine_goals\Slovenia\data\slope_perc\slope_perc.tif"
aspect_raster_nonaligned_path = r"D:\Eco_vine_goals\Slovenia\data\aspect.tif"
dem_raster_nonaligned_path = r"D:\Eco_vine_goals\Slovenia\data\EVG_DEM.tif"
solar_nonaligned_raster_path = r"D:\Eco_vine_goals\Slovenia\data\solar_rad_16_2-10_12.tif"  # solar
na_shp_path = r"D:\Eco_vine_goals\Slovenia\data\na_clip.shp"

out_raba_rast_dir = r"D:\Eco_vine_goals\SLO_land_use_analysis"

slope_raster_path = r"D:\Eco_vine_goals\SLO_land_use_analysis\EVG_slope_aligned.tif"
if not os.path.isfile(slope_raster_path):
    match_two_rasters(slope_nonaligned_raster_path, land_use_raster_path, slope_raster_path)
aspect_raster_path = r"D:\Eco_vine_goals\SLO_land_use_analysis\EVG_aspect_aligned.tif"
if not os.path.isfile(aspect_raster_path):
    match_two_rasters(aspect_raster_nonaligned_path, land_use_raster_path, aspect_raster_path)
dem_raster_path = r"D:\Eco_vine_goals\SLO_land_use_analysis\EVG_dem_aligned.tif"
if not os.path.isfile(dem_raster_path):
    match_two_rasters(dem_raster_nonaligned_path, land_use_raster_path, dem_raster_path)
terase_raster_path = r"D:\Eco_vine_goals\SLO_land_use_analysis\EVG_terase_aligned.tif"
solar_raster_path = r"D:\Eco_vine_goals\SLO_land_use_analysis\EVG_solar_aligned.tif"
if not os.path.isfile(solar_raster_path):
    match_two_rasters(solar_nonaligned_raster_path, land_use_raster_path, solar_raster_path)

naselja = ["Brje", "Dolenje", "Gaberje", "Planina", "Šmarje", "Tevče", "Velike Žablje", "Vrtovče", "Zavino", "Dolanci",
           "Kodreti", "Branik", "Preserje", "Spodnja Branica", "Steske", "Erzelj", "Goče", "Lože", "Manče", "Orehovica",
           "Podnanos", "Podraga", "Slap"]

out_raba_rast = os.path.join(out_raba_rast_dir, "raba_{}.tif".format("naselja"))
if not os.path.isfile(out_raba_rast):
    clip_raster_to_shape_where_att(raster_path=land_use_raster_path, shape_path=na_shp_path,
                                   attribute_name="NA_UIME",
                                   selected_att_values_list=naselja,
                                   out_raster_path=out_raba_rast)

out_slope_rast = os.path.join(out_raba_rast_dir, "slope_{}.tif".format("naselja"))
if not os.path.isfile(out_slope_rast):
    clip_raster_to_shape_where_att(raster_path=slope_raster_path, shape_path=na_shp_path,
                                   attribute_name="NA_UIME",
                                   selected_att_values_list=naselja,
                                   out_raster_path=out_slope_rast)

out_dem_rast = os.path.join(out_raba_rast_dir, "dem_{}.tif".format("naselja"))
if not os.path.isfile(out_dem_rast):
    clip_raster_to_shape_where_att(raster_path=dem_raster_path, shape_path=na_shp_path,
                                   attribute_name="NA_UIME",
                                   selected_att_values_list=naselja,
                                   out_raster_path=out_dem_rast)

out_aspect_rast = os.path.join(out_raba_rast_dir, "asp_{}.tif".format("naselja"))
if not os.path.isfile(out_aspect_rast):
    clip_raster_to_shape_where_att(raster_path=aspect_raster_path, shape_path=na_shp_path,
                                   attribute_name="NA_UIME",
                                   selected_att_values_list=naselja,
                                   out_raster_path=out_aspect_rast)
out_solar_rast = os.path.join(out_raba_rast_dir, "solar_{}.tif".format("naselja"))
if not os.path.isfile(out_solar_rast):
    clip_raster_to_shape_where_att(raster_path=solar_raster_path, shape_path=na_shp_path,
                                   attribute_name="NA_UIME",
                                   selected_att_values_list=naselja,
                                   out_raster_path=out_solar_rast)

evg_id_conditions = [10, 20, 21, 22, 23, 24, 30, 40, 50, 60, 70, 90]
for condition in evg_id_conditions:
    print(condition)
    csv = ""
    csv += calculate_pearson_with_codition(condition_raster_path=out_raba_rast, raster_conditions=[condition],
                                           raster1_path=out_dem_rast, raster2_path=slope_raster_path)
    csv += calculate_pearson_with_codition(condition_raster_path=out_raba_rast, raster_conditions=[condition],
                                           raster1_path=out_dem_rast, raster2_path=out_solar_rast)
    csv += calculate_pearson_with_codition(condition_raster_path=out_raba_rast, raster_conditions=[condition],
                                           raster1_path=slope_raster_path, raster2_path=solar_raster_path)
    print(csv)
