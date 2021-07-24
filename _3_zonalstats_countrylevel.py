####### Prepare QGIS for working#######
#########################################################################################

print('preliminary setup')
import sys
import os

 from qgis.core import (
     QgsApplication
 )

 from qgis.analysis import QgsNativeAlgorithms


 QgsApplication.setPrefixPath('C:/OSGeo4W64/apps/qgis', True)
 qgs = QgsApplication([], False)
 qgs.initQgis()

 sys.path.append('C:/OSGeo4W64/apps/qgis/python/plugins')


import processing
from processing.core.Processing import Processing
Processing.initialize()
QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())
#########################################################################################



####### Set paths to inputs and outputs#######
mainpath = "/Users/clara/Documents/MAESTRIA/HERRAMIENTAS COMPUTACIONALES/PYTHON-QGGIS 2"
outpath = "{}/_output".format(mainpath)

#######Import rasters with the information required#######
elevation = "D:/backup_school/Research/IPUMS/_GEO/elrug/elevation/alt.bil"
tpbasepath = "D:/backup_school/Research/worldclim/World"
tpath = tpbasepath + "/temperature"
ppath = tpbasepath + "/precipitation"
temp = tpath + "/TOTtmean6090.tif"
prec = ppath + "/TOTprec6090.tif"
landqual = outpath + "/landquality.tif"
popd1500 = mainpath + "/HYDE/1500ad_pop/popd_1500AD.asc"
popd1990 = mainpath + "/HYDE/1990ad_pop/popd_1990AD.asc"
popd2000 = mainpath + "/HYDE/2000ad_pop/popd_2000AD.asc"
countries = mainpath + "/ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp"

outcsv = "{}/country_level_zs.csv".format(outpath)


RASTS = [elevation, temp, prec, landqual, popd1500, popd1990, popd2000]
PREFS = ['elev_', 'temp_', 'prec_', 'lqua_', 'pd15_', 'pd19_', 'pd20_']

#######Only use last 4 rasters, due to processing time requirements#######
RASTS = RASTS[3:]
PREFS = PREFS[3:]

##################################################################
# Fix geometries
##################################################################
print('fixing geometries')
fixgeo_dict = {
    'INPUT': countries,
    'OUTPUT': 'memory:'
}
fix_geo = processing.run('native:fixgeometries', fixgeo_dict)['OUTPUT']

##################################################################
# Drop field(s)
##################################################################
print('dropping unnecessary fields')
allfields = [field.name() for field in fix_geo.fields()]
keepfields = ['ADMIN', 'ISO_A3']
dropfields = [field for field in allfields if field not in keepfields]

drop_dict = {
    'COLUMN': dropfields,
    'INPUT': fix_geo,
    'OUTPUT': 'memory:'
}
drop_fields = processing.run('qgis:deletecolumn', drop_dict)['OUTPUT']

# here we loop over the rasters
for idx, rast in enumerate(RASTS):

	pref = PREFS[idx]

	# not needed, can use rast directly as 'INPUT_RASTER' for zs
	# rlayer = QgsRasterLayer(rast, "rasterlayer", "gdal")

	###################################################################
	# Zonal statistics
	###################################################################
	print('computing zonal stats {}'.format(pref))
	zs_dict = {
	    'COLUMN_PREFIX': pref,
	    'INPUT_RASTER': rast,
	    'INPUT_VECTOR': drop_fields,
	    'RASTER_BAND': 1,
	    'STATS': [2]
	}
	processing.run('qgis:zonalstatistics', zs_dict)

###################################################################
# write to CSV
###################################################################
print('outputting the data')

with open(outcsv, 'w') as output_file:
    fieldnames = [field.name() for field in drop_fields.fields()]
    line = ','.join(name for name in fieldnames) + '\n'
    output_file.write(line)
    for f in drop_fields.getFeatures():
        line = ','.join(str(f[name]) for name in fieldnames) + '\n'
        output_file.write(line)
                                        
print('DONE!')
