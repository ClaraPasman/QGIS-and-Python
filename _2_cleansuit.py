#######Prepare QGIS for working#######
#########################################################################################################

 print('preliminary setup')
 import sys
 import os

 from qgis.core import (
     QgsApplication, 
     QgsVectorLayer,
     QgsCoordinateReferenceSystem,
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
#########################################################################################################
    
    
#######Set paths to inputs and outputs#######
mainpath = "/Users/clara/Documents/MAESTRIA/HERRAMIENTAS COMPUTACIONALES/PYTHON-QGGIS 2"
suitin = "{}/suit/suit/hdr.adf".format(mainpath)
outpath = "{}/_output/".format(mainpath)
suitout = "{}/landquality.tif".format(outpath)

####### Select a certain coordinate system#######
crs_wgs84 = QgsCoordinateReferenceSystem("epsg:4326")

####### REPROJECT#######
###Reproject an existing layer and save it as a new layer ### 

print('defining projection for the suitability data')
warp_dict = {
    'DATA_TYPE': 0,
    'EXTRA': '',
    'INPUT': suitin,
    'MULTITHREADING': False,
    'NODATA': None,
    'OPTIONS': '',
    'RESAMPLING': 0,
    'SOURCE_CRS': None,
    'TARGET_CRS': crs_wgs84,
    'TARGET_EXTENT': None,
    'TARGET_EXTENT_CRS': None,
    'TARGET_RESOLUTION': None,
    'OUTPUT': suitout
}
processing.run('gdal:warpreproject', warp_dict)


####### Extract projection: save as .tif the reprojected layer#######

print('extracting the projection for land suitability')
extpr_dict = {
    'INPUT': suitout,
    'PRJ_FILE_CREATE': True
}
processing.run('gdal:extractprojection', extpr_dict)

print('DONE!')
