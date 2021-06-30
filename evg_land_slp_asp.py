from functions import *
import os

land_use_raster_path = r"D:\Eco_vine_goals\Slovenia\data\raba_raster.tif"
slope_nonaligned_raster_path = r"D:\Eco_vine_goals\Slovenia\data\slope_perc\slope_perc.tif"
aspect_raster_nonaligned_path = r"D:\Eco_vine_goals\Slovenia\data\aspect.tif"
na_shp_path = r"D:\Eco_vine_goals\Slovenia\data\na_clip.shp"

slope_raster_path = r"D:\Eco_vine_goals\SLO_land_use_analysis\EVG_slope_aligned.tif"
if not os.path.isfile(slope_raster_path):
    match_two_rasters(slope_nonaligned_raster_path, land_use_raster_path, slope_raster_path)
aspect_raster_path = r"D:\Eco_vine_goals\SLO_land_use_analysis\EVG_aspect_aligned.tif"
if not os.path.isfile(aspect_raster_path):
    match_two_rasters(aspect_raster_nonaligned_path, land_use_raster_path, aspect_raster_path)

out_raba_rast_dir = r"D:\Eco_vine_goals\SLO_land_use_analysis"

aspect_conditions = [np.nan, (-1.1, 0), (0, 22.5, 337.5, 360), (22.5, 67.5), (67.5, 112.5), (112.5, 157.5), (157.5, 202.5),
                     (202.5, 247.5), (247.5, 292.5), (292.5, 337.5)]
evg_id_conditions = [(9, 91), 10, 20, 21, 22, 23, 24, 30, 40, 50, 60, 70, 90]
slope_conditions = [np.nan, (0, 10), (10, 30), (30, 50), (50, 1000000)]
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

out_aspect_rast = os.path.join(out_raba_rast_dir, "asp_{}.tif".format("naselja"))
if not os.path.isfile(out_aspect_rast):
    clip_raster_to_shape_where_att(raster_path=aspect_raster_path, shape_path=na_shp_path,
                                   attribute_name="NA_UIME",
                                   selected_att_values_list=naselja,
                                   out_raster_path=out_aspect_rast)

area_csv = calculate_statistics_from_3rasters_where_conditions(raster1_path=out_aspect_rast,
                                                               raster2_path=out_raba_rast,
                                                               raster3_path=out_slope_rast,
                                                               resolution=1,
                                                               raster1_conditions=aspect_conditions,
                                                               raster2_conditions=evg_id_conditions,
                                                               raster3_conditions=slope_conditions, output="csv")

fp = open(os.path.join(out_raba_rast_dir, "evg_asp_landuse_slope.csv"), "w")
fp.write(area_csv)
fp.close()