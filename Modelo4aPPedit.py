#######Prepare QGIS for working#############################################################################################################################
############################################################################################################################################################

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterFeatureSink
import processing


class Modelo4a(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSink('Fixgeo_wlds', 'fixgeo_wlds', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Fixgeo_countries', 'fixgeo_countries', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Intersection', 'intersection', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback)
        feedback = QgsProcessingMultiStepFeedback(4, model_feedback)
        results = {}
        outputs = {}
############################################################################################################################################################

#######Fix geometries of shapfile imported from model 1#######
#######Use this tool to fix any polygon geometry-related problem (sometimes polygons may stack one on top of the other)#######
  
        alg_params = {
            'INPUT': '/Users/rochipodesta/Desktop/maestría/Herramientas/semana 5/output/clean.shp',
            'OUTPUT': parameters['Fixgeo_wlds']
        }
        outputs['CorregirGeometrasWlds'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fixgeo_wlds'] = outputs['CorregirGeometrasWlds']['OUTPUT']

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}
        
        
#######Fix geometries of new shapfile imported#######
#######Use this tool to fix any polygon geometry-related problem (sometimes polygons may stack one on top of the other)#######
   
        alg_params = {
            'INPUT': '/Users/rochipodesta/Desktop/maestría/Herramientas/semana 5/input/ne_10m_admin_0_countries/ne_10m_admin_0_countries.dbf',
            'OUTPUT': parameters['Fixgeo_countries']
        }
        outputs['CorregirGeometrasCountries'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fixgeo_countries'] = outputs['CorregirGeometrasCountries']['OUTPUT']

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Intersección
        alg_params = {
            'INPUT': outputs['CorregirGeometrasWlds']['OUTPUT'],
            'INPUT_FIELDS': ['GID'],
            'OVERLAY': outputs['CorregirGeometrasCountries']['OUTPUT'],
            'OVERLAY_FIELDS': ['ADMIN'],
            'OVERLAY_FIELDS_PREFIX': '',
            'OUTPUT': parameters['Intersection']
        }
        outputs['Interseccin'] = processing.run('native:intersection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Intersection'] = outputs['Interseccin']['OUTPUT']

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Estadísticas por categorías
        alg_params = {
            'CATEGORIES_FIELD_NAME': ['ADMIN'],
            'INPUT': outputs['Interseccin']['OUTPUT'],
            'OUTPUT': '/Users/rochipodesta/Desktop/maestría/Herramientas/semana 5/output/languages_by_country.gpkg',
            'VALUES_FIELD_NAME': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['EstadsticasPorCategoras'] = processing.run('qgis:statisticsbycategories', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        return results

    def name(self):
        return 'modelo4a'

    def displayName(self):
        return 'modelo4a'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Modelo4a()
