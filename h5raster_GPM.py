#This code will open GPM H5 files and create ArcGIS Rasters

import h5py
import numpy
import arcpy

# contants and envitonments
arcpy.env.overwriteOutput = True

def DefineSpatialReferenceAndSave(in_array, path, x_min, y_min, cell_x, cell_y, no_data, spatial_ref, silent = False):
	"""DefineSpatialReferenceAndSave(in_array, path, x_min, y_min, cell_x, cell_y{, no_data = None}{, spatial_ref = None}{, silent = False})
convert input array to raster, define coordinate system and projection, then save to a file.
arguments
in_array: array to convert. (NumPy ndarray)
path: save path. (string)
x_min: left edge coordinate. (number)
y_min: bottom edge coordinate. (number)
cell_x: horizontal length of a pixel. (number)
cell_y: vertical length of a pixel. (number)
no_data: 'no data' value of created raster. (value)
spatial_ref: path of a raster for spatial references. (arcpy spatialReference)
silent: quiet mode. (boolean)"""
	if not silent: print "DEFINING COORD SYSTEM & SAVING:", path
	raster = arcpy.NumPyArrayToRaster(in_array, arcpy.Point(x_min, y_min), cell_x, cell_y, no_data)
	arcpy.DefineProjection_management(raster, arcpy.SpatialReference(spatial_ref))
	raster.save(path)

# Extent, cell size, no data and ArcGIS coordinate system for GPM data file
X_MIN = -180.0
Y_MIN = -90.0
L_X = 0.1
L_Y = 0.1
NO_DATA = -9999.9
SR = 4326 #wgs84

f = open("list.txt", "r")  #list.txt contains all .H5 file names
LIST = []
for l in f:
	LIST.append(l[:-1])
f.close()

for fi in LIST:
	s = fi.split(".")[3]
	f = h5py.File(fi, "r")
	sm = f["Grid"]["precipitationCal"][:] #calibrated precip values from GPM-IMERG H5 files
	
	#needed to re-orient GPM data for ArcGIS mapping
	sm = sm.transpose()
	sm = numpy.flipud(sm)
	
	f.close()
	
	#Create and save the ArcGIS Raster
	DefineSpatialReferenceAndSave(sm, "C:\\Research\\GPM\\" + s, X_MIN, Y_MIN, L_X, L_Y, NO_DATA, SR)

