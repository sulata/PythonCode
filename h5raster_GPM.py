import h5py
import numpy
import rio


X_MIN = -180.0
Y_MIN = -90.0
L_X = 0.1
L_Y = 0.1
NO_DATA = -9999.9
SR = 4326 #wgs84


f = open("list.txt", "r")  ###
LIST = []
for l in f:
	LIST.append(l[:-1])
f.close()

for fi in LIST:
	s = fi.split(".")[3]
	f = h5py.File(fi, "r")
	sm = f["Grid"]["precipitationCal"][:]
	
	sm = sm.transpose()
	sm = numpy.flipud(sm)
	
	f.close()
	rio.DefineSpatialReferenceAndSave(sm, "C:\\Research\\SMAP\\" + s, X_MIN, Y_MIN, L_X, L_Y, NO_DATA, SR)
