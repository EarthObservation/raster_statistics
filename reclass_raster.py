from functions import *

in_rast_path = r"D:\Eco_vine_goals\Slovenia\data\raba_raster.tif"
out_rast_path = r"D:\Eco_vine_goals\SLO_land_use_analysis\raba_raster_reclass.tif"
reclass_val = [(30, 1), (60, 1), (70, 1), (40, 2), (50, 2), (24, 3), (23, 3), (20, 4), (21, 4), (22, 4), (10, 5), (90,0)]
no_data = np.nan
reclas_raster(src_raster_path=in_rast_path, out_raster_path=out_rast_path,
              reclas_values=reclass_val, e_type=6)
