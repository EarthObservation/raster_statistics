# Remove geotiff reference

import os
import gdal

rasters_dir = r"D:\test_remove_geo\in"
out_rasters_dir = r"D:\test_remove_geo\out"

def remove_raster_geodata(raster_path, out_raster_path):
    dataset = gdal.Open(raster_path)
    dataset = gdal.Translate(out_raster_path, dataset, creationOptions=['PROFILE=BASELINE'])
    dataset = None
    os.remove(out_raster_path+".aux.xml")

dir_in_dir = os.listdir(rasters_dir)
for dir_in_dir_name in dir_in_dir:
    dir_in_dir_path = os.path.join(rasters_dir, dir_in_dir_name)
    if os.path.isdir(dir_in_dir_path):
        if not os.path.isdir(os.path.join(out_rasters_dir, dir_in_dir_name)):
            os.mkdir(os.path.join(out_rasters_dir, dir_in_dir_name))
        dir_in_dir_path = os.path.join(rasters_dir, dir_in_dir_name)
        dir_in_dir_raster_names = os.listdir(dir_in_dir_path)
        for raster_name in dir_in_dir_raster_names:
            raster_path = os.path.join(rasters_dir, dir_in_dir_name, raster_name)
            out_raster_path = os.path.join(out_rasters_dir, dir_in_dir_name, raster_name)
            remove_raster_geodata(raster_path, out_raster_path)
