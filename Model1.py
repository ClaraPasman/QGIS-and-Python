

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterFeatureSink
import processing


class Modelo1(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSink('Autoinc_id', 'autoinc_id', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Length', 'length', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Field_calc', 'field_calc', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Output_menor_a_11', 'OUTPUT_menor_a_11', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Fix_geo', 'fix_geo', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Wldsout', 'wldsout', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(6, model_feedback)
        results = {}
        outputs = {}

############################################################################################################################################################

####### Fix geometries: use this tool to fix any polygon geometry-related problem (sometimes polygons may stack one on top of the other)#######             
       
        
        
        alg_params = {
            'INPUT': '/Users/rochipodesta/Desktop/maestría/Herramientas/semana 5/langa/langa.shp',
            'OUTPUT': parameters['Fix_geo']
        }
        outputs['CorregirGeometras'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fix_geo'] = outputs['CorregirGeometras']['OUTPUT']

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}       
        
        ####### With autoincremental tool enumerate observations per country#######
        
        alg_params = {
            'FIELD_NAME': 'GID',
            'GROUP_FIELDS': [''],
            'INPUT': outputs['CorregirGeometras']['OUTPUT'],
            'SORT_ASCENDING': True,
            'SORT_EXPRESSION': '',
            'SORT_NULLS_FIRST': False,
            'START': 1,
            'OUTPUT': parameters['Autoinc_id']
        }
        outputs['AgregarCampoQueAutoincrementa'] = processing.run('native:addautoincrementalfield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Autoinc_id'] = outputs['AgregarCampoQueAutoincrementa']['OUTPUT']
        return results

        
  #######Field calculator: length#######   
        alg_params = {
            'FIELD_LENGTH': 2,
            'FIELD_NAME': 'length',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,
            'FORMULA': 'length(NAME_PROP)',
            'INPUT': 'Incrementado_27fe8a76_6aa6_4def_8929_0f1e1ed1d2c3',
            'OUTPUT': parameters['Length']
        }
        outputs['CalculadoraDeCampos'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Length'] = outputs['CalculadoraDeCampos']['OUTPUT']

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}
  
#######Keep vaiables which length is lower than 11#######
        
   
        alg_params = {
            'INPUT': 'Calculado_4b2727ef_a5b8_48af_9cc3_438be5c0002e',
            'OUTPUT_menor_a_11': parameters['Output_menor_a_11']
        }
        outputs['FiltroDeEntidad'] = processing.run('native:filter', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Output_menor_a_11'] = outputs['FiltroDeEntidad']['OUTPUT_menor_a_11']

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}
        
        
        
   #######Copy language name into a new variable with shorter name#######     
             
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'lnm',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,
            'FORMULA': '\"NAME_PROP\"',
            'INPUT': 'menor_a_11_3baa5386_146c_4835_b5c3_37c36fe7aaba',
            'OUTPUT': parameters['Field_calc']
        }
        outputs['CalculadoraDeCamposClone'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Field_calc'] = outputs['CalculadoraDeCamposClone']['OUTPUT']

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

   
        
       #######Drop variables that you're not interested in#######
       
      
        alg_params = {
            'COLUMN': ['ID_ISO_A3','ID_ISO_A2','ID_FIPS','NAM_LABEL','NAME_PROP','NAME2','NAM_ANSI','CNT','C1','POP','LMP_POP1','G','LMP_CLASS','FAMILYPROP','FAMILY','langpc_km2','length\n'],
            'INPUT': 'Calculado_96c74cd1_8dc9_4738_8943_be3f054c5463',
            'OUTPUT': parameters['Wldsout']
        }
        outputs['QuitarCampos'] = processing.run('qgis:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Wldsout'] = outputs['QuitarCampos']['OUTPUT']

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

  
       
  
    def name(self):
        return 'Modelo1'

    def displayName(self):
        return 'Modelo1'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Modelo1()
