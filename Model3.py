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

####### Fix geometries: use this tool to fix any polygon geometry-related problem (sometimes polygons may stack one on top of the other)####### 
print('fixing geometries')
fixgeo_dict = {
    'INPUT': countries,
    'OUTPUT': 'memory:'
}
geomfixed= processing.run('native:fixgeometries', fixgeo_dict)['OUTPUT']

#######Drop variables that you're not interested in and save as a new layer#######
print('dropping unnecessary fields')
allfields = [field.name() for field in geomfixed.fields()]
keepfields = ['ADMIN', 'ISO_A3']
drop_fields = [field for field in allfields if field not in keepfields]

drop_dict = {
    'COLUMN': dropped,
    'INPUT': geomfixed,
    'OUTPUT': 'memory:'
}
dropped = processing.run('qgis:deletecolumn', drop_dict)['OUTPUT']

######## Select the zonal satatistics for each country for each raster (mean of land quality and population), calculate mean and save as new layer#######
####### Instead of doing one by one we loop over the rasters #######
for idx, rast in enumerate(RASTS):

	pref = PREFS[idx]

	print('computing zonal stats {}'.format(pref))
	zs_dict = {
	    'COLUMN_PREFIX': pref,
	    'INPUT_RASTER': rast,
	    'INPUT_VECTOR': dropped,
	    'RASTER_BAND': 1,
	    'STATS': [2]
	}
	processing.run('qgis:zonalstatistics', zs_dict)

#######Export attribute table as csv#######
print('outputting the data')

with open(outcsv, 'w') as output_file:
    fieldnames = [field.name() for field in dropped.fields()]
    line = ','.join(name for name in fieldnames) + '\n'
    output_file.write(line)
    for f in dropped.getFeatures():
        line = ','.join(str(f[name]) for name in fieldnames) + '\n'
        output_file.write(line)
                                        
print('DONE!')
