#######Prepare QGIS for working#############################################################################################################################
############################################################################################################################################################


from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterVectorDestination
from qgis.core import QgsProcessingParameterFeatureSink
import processing


class Modelo4b(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorDestination('Distout', 'distout', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorDestination('Nearout', 'nearout', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Country_centroids', 'country_centroids', type=QgsProcessing.TypeVectorPoint, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Extract_by_attribute', 'extract_by_attribute', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Extract_vertices', 'extract_vertices', type=QgsProcessing.TypeVectorPoint, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Nearest_cat_adjust', 'nearest_cat_adjust', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Added_field_cent_lat', 'added_field_cent_lat', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Added_field_cent_lon', 'added_field_cent_lon', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Added_field_coast_lat', 'added_field_coast_lat', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Added_field_coast_lon', 'added_field_coast_lon', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Fixgeo_coast', 'fixgeo_coast', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Fixgeo_countries', 'fixgeo_countries', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Centroids_nearest_coast_joined', 'centroids_nearest_coast_joined', optional=True, type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Centroids_nearest_distance_joined', 'centroids_nearest_distance_joined', optional=True, type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Coastout', 'coastout', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Centroidout', 'centroidout', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Nearest_cat_adjust_dropfields', 'nearest_cat_adjust_dropfields', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Centroids_nearest_coast_joined_dropfields', 'centroids_nearest_coast_joined_dropfields', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Centroids_lat_lon_drop_fields', 'centroids_lat_lon_drop_fields', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Centroids_w_coord', 'centroids_w_coord', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Add_geo_coast', 'add_geo_coast', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        
        feedback = QgsProcessingMultiStepFeedback(21, model_feedback)
        results = {}
        outputs = {}
        
############################################################################################################################################################


        alg_params = {
            'INPUT': '/Users/rochipodesta/Desktop/maestría/Herramientas/semana 5/input/ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp',
            'OUTPUT': parameters['Fixgeo_countries']
        }
        outputs['CorregirGeometrasContries'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fixgeo_countries'] = outputs['CorregirGeometrasContries']['OUTPUT']

        feedback.setCurrentStep(14)
        if feedback.isCanceled():
            return {}
        



        alg_params = {
            'INPUT': '/Users/rochipodesta/Desktop/maestría/Herramientas/semana 5/input/ne_10m_coastline/ne_10m_coastline.shp',
            'OUTPUT': parameters['Fixgeo_coast']
        }
        outputs['CorregirGeometrasCoast'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fixgeo_coast'] = outputs['CorregirGeometrasCoast']['OUTPUT']

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}        
        

####### Add centroid to each country#######
        alg_params = {
            'ALL_PARTS': False,
            'INPUT': outputs['CorregirGeometrasContries']['OUTPUT'],
            'OUTPUT': parameters['Country_centroids']
        }
        outputs['Centroides'] = processing.run('native:centroids', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Country_centroids'] = outputs['Centroides']['OUTPUT']

        feedback.setCurrentStep(15)
        if feedback.isCanceled():
            return {}   
        
####### Add coordinates to centroids by "adding geometry attributes"  #######
        alg_params = {
            'CALC_METHOD': 0,
            'INPUT': outputs['Centroides']['OUTPUT'],
            'OUTPUT': parameters['Centroids_w_coord']
        }
        outputs['AgregarAtributosDeGeometra'] = processing.run('qgis:exportaddgeometrycolumns', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroids_w_coord'] = outputs['AgregarAtributosDeGeometra']['OUTPUT']

        feedback.setCurrentStep(19)
        if feedback.isCanceled():
            return {}     
     
#######Drop variables that you're not interested in:fixgeo_coast#######
        alg_params = {
            'COLUMN': ['scalerank'],
            'INPUT': 'Geometrías_corregidas_307b078f_b077_44e6_856e_8d7d7875593d',
            'OUTPUT': parameters['Coastout']
        }
        outputs['QuitarCamposFixgeo_coast'] = processing.run('qgis:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Coastout'] = outputs['QuitarCamposFixgeo_coast']['OUTPUT']

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}
    

        alg_params = {
            'COLUMN': ['featurecla','scalerank','LABELRANK','SOVEREIGNT','SOV_A3','ADM0_DIF','LEVEL','TYPE','ADM0_A3','GEOU_DIF','GEOUNIT','GU_A3','SU_DIF','SUBUNIT','SU_A3','BRK_DIFF','NAME','NAME_LONG','BRK_A3','BRK_NAME','BRK_GROUP','ABBREV','POSTAL','FORMAL_EN','FORMAL_FR','NAME_CIAWF','NOTE_ADM0','NOTE_BRK','NAME_SORT','NAME_ALT','MAPCOLOR7','MAPCOLOR8','APCOLOR9','MAPCOLOR13','POP_EST','POP_RANK','GDP_MD_EST','POP_YEAR','LASTCENSUS','GDP_YEAR','ECONOMY','INCOME_GRP','WIKIPEDIA','FIPS_10_','ISO_A2','ISO_A3_EH','ISO_N3','UN_A3','WB_A2','WB_A3','WOE_ID','WOE_ID_EH','WOE_NOTE','ADM0_A3_IS','ADM0_A3_US','ADM0_A3_UN','ADM0_A3_WB','CONTINENT','REGION_UN','SUBREGION','REGION_WB','NAME_LEN','LONG_LEN','ABBREV_LEN','TINY','HOMEPART','MIN_ZOOM','MIN_LABEL','MAX_LABEL','NE_ID','WIKIDATAID','NAME_AR','NAME_BN','NAME_DE','NAME_EN','NAME_ES','NAME_FR','NAME_EL','NAME_HI','NAME_HU','NAME_ID','NAME_IT','NAME_JA','NAME_KO','NAME_NL','NAME_PL','NAME_PT','NAME_RU','NAME_SV','NAME_TR','NAME_VI','NAME_ZH','MAPCOLOR9'],
            'INPUT': 'Información_de_geometría_añadida_028a0ab0_2033_4655_a86f_3f5fdd2a8316',
            'OUTPUT': parameters['Centroidout']
        }
        outputs['QuitarCamposCentroids_w_coast'] = processing.run('qgis:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroidout'] = outputs['QuitarCamposCentroids_w_coast']['OUTPUT']

        feedback.setCurrentStep(20)
        if feedback.isCanceled():
            return {}
  
    
####### Calculate distance from centroid to coast#######
        alg_params = {
            'GRASS_MIN_AREA_PARAMETER': 0.0001,
            'GRASS_OUTPUT_TYPE_PARAMETER': 0,
            'GRASS_REGION_PARAMETER': None,
            'GRASS_SNAP_TOLERANCE_PARAMETER': -1,
            'GRASS_VECTOR_DSCO': '',
            'GRASS_VECTOR_EXPORT_NOCAT': False,
            'GRASS_VECTOR_LCO': '',
            'column': ['xcoord'],
            'dmax': -1,
            'dmin': -1,
            'from': 'Información_de_geometría_añadida_028a0ab0_2033_4655_a86f_3f5fdd2a8316',
            'from_type': [0,1,3],
            'to': 'Campos_restantes_a7592147_e50d_4b32_a53b_a2f4da978543',
            'to_column': '',
            'to_type': [0,1,3],
            'upload': [0],
            'from_output': parameters['Nearout'],
            'output': parameters['Distout']
        }
        outputs['Vdistance'] = processing.run('grass7:v.distance', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Distout'] = outputs['Vdistance']['output']
        results['Nearout'] = outputs['Vdistance']['from_output']

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}
   
#######Field Calculator: adjust "cat" to merge with distance lines#######
        alg_params = {
            'FIELD_LENGTH': 4,
            'FIELD_NAME': 'cat',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 1,
            'FORMULA': 'attribute($currentfeature, \'cat\')-1',
            'INPUT': 'from_output_0399f750_16b3_49de_a382_27311a70fce1',
            'OUTPUT': parameters['Nearest_cat_adjust']
        }
        outputs['CalculadoraDeCamposCatAdjust'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Nearest_cat_adjust'] = outputs['CalculadoraDeCamposCatAdjust']['OUTPUT']

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

   
#######Drop variables that you're not interested in: cat_adjust#######
        alg_params = {
            'COLUMN': ['xcoord','ycoord'],
            'INPUT': 'Calculado_22fbfe03_1b02_426e_a2f9_13a666786ccf',
            'OUTPUT': parameters['Nearest_cat_adjust_dropfields']
        }
        outputs['QuitarCamposCat_adjust'] = processing.run('qgis:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Nearest_cat_adjust_dropfields'] = outputs['QuitarCamposCat_adjust']['OUTPUT']

        feedback.setCurrentStep(12)
        if feedback.isCanceled():
            return {}
 
    


        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'ISO_A3',
            'FIELDS_TO_COPY': [''],
            'FIELD_2': 'ISO_A3',
            'INPUT': 'Campos_restantes_e358711e_8428_4fe2_a5c5_d768323ba885',
            'INPUT_2': 'Campos_restantes_cd95ff82_b829_4f83_a233_7b72da1b09d1',
            'METHOD': 1,
            'PREFIX': '',
            'OUTPUT': parameters['Centroids_nearest_coast_joined']
        }
        outputs['UnirAtributosPorValorDeCampo'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroids_nearest_coast_joined'] = outputs['UnirAtributosPorValorDeCampo']['OUTPUT']

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

    

        alg_params = {
            'COLUMN': ['featurecla','scalerank','LABELRANK','SOVEREIGNT','SOV_A3','ADM0_DIF','LEVEL','TYPE','ADM0_A3','GEOU_DIF','GEOUNIT','GU_A3','SU_DIF','SUBUNIT','SU_A3','BRK_DIFF','NAME','NAME_LONG','BRK_A3','BRK_NAME','BRK_GROUP','ABBREV','POSTAL','FORMAL_EN','FORMAL_FR','NAME_CIAWF','NOTE_ADM0','NOTE_BRK','NAME_SORT','NAME_ALT','MAPCOLOR7','MAPCOLOR8','APCOLOR9','MAPCOLOR13','POP_EST','POP_RANK','GDP_MD_EST','POP_YEAR','LASTCENSUS','GDP_YEAR','ECONOMY','INCOME_GRP','WIKIPEDIA','FIPS_10_','ISO_A2','ISO_A3_EH','ISO_N3','UN_A3','WB_A2','WB_A3','WOE_ID','WOE_ID_EH','WOE_NOTE','ADM0_A3_IS','ADM0_A3_US','ADM0_A3_UN','ADM0_A3_WB','CONTINENT','REGION_UN','SUBREGION','REGION_WB','NAME_LEN','LONG_LEN','ABBREV_LEN','TINY','HOMEPART','MIN_ZOOM','MIN_LABEL','MAX_LABEL','NE_ID','WIKIDATAID','NAME_AR','NAME_BN','NAME_DE','NAME_EN','NAME_ES','NAME_FR','NAME_EL','NAME_HI','NAME_HU','NAME_ID','NAME_IT','NAME_JA','NAME_KO','NAME_NL','NAME_PL','NAME_PT','NAME_RU','NAME_SV','NAME_TR','NAME_VI','NAME_ZH','MAPCOLOR9','ADMIN_2','ISO_A3_2'],
            'INPUT': 'Capa_unida_6cf146ea_9ec6_4efc_940e_616907d88a77',
            'OUTPUT': parameters['Centroids_nearest_coast_joined_dropfields']
        }
        outputs['QuitarCamposCentroids_coast_joined'] = processing.run('qgis:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroids_nearest_coast_joined_dropfields'] = outputs['QuitarCamposCentroids_coast_joined']['OUTPUT']

        feedback.setCurrentStep(18)
        if feedback.isCanceled():
            return {}

       
####### Join attributes by field value: merge both tables nearest and distance#######
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'cat',
            'FIELDS_TO_COPY': [''],
            'FIELD_2': 'cat',
            'INPUT': 'output_68c79c5e_cdc5_4b50_b2e1_65fc6eaedbca',
            'INPUT_2': 'Campos_restantes_05b99d00_cbc4_4535_9ef4_20de63712a66',
            'METHOD': 1,
            'PREFIX': '',
            'OUTPUT': parameters['Centroids_nearest_distance_joined']
        }
        outputs['UnirAtributosPorValorDeCampo'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroids_nearest_distance_joined'] = outputs['UnirAtributosPorValorDeCampo']['OUTPUT']

        feedback.setCurrentStep(16)
        if feedback.isCanceled():
            return {}
        
        
####### Extract vertices#######
        alg_params = {
            'INPUT': 'Capa_unida_14fda893_f44e_41f2_9296_c306c31a37ca',
            'OUTPUT': parameters['Extract_vertices']
        }
        outputs['ExtraerVrtices'] = processing.run('native:extractvertices', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Extract_vertices'] = outputs['ExtraerVrtices']['OUTPUT']

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}
    
        
####### Extract by attribute #######
        alg_params = {
            'FIELD': 'distance',
            'INPUT': 'Vértices_b8cbf0ec_902d_42f6_8cf4_4ecc539ae562',
            'OPERATOR': 2,
            'VALUE': '0',
            'OUTPUT': parameters['Extract_by_attribute']
        }
        outputs['ExtraerPorAtributo'] = processing.run('native:extractbyattribute', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Extract_by_attribute'] = outputs['ExtraerPorAtributo']['OUTPUT']

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}
  
        

        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'cent_lat',
            'FIELD_PRECISION': 10,
            'FIELD_TYPE': 0,
            'FORMULA': 'attribute($currentfeature, \'ycoord\')',
            'INPUT': 'Extraído__atributo__20c5dffb_8c9c_43b4_82b5_7bef65f572b5',
            'OUTPUT': parameters['Added_field_cent_lat']
        }
        outputs['CalculadoraDeCamposCent_lat'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Added_field_cent_lat'] = outputs['CalculadoraDeCamposCent_lat']['OUTPUT']

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}
     
 #######Field Calculator: create new field containing the longitude of the centroid#######
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'cent_lon',
            'FIELD_PRECISION': 10,
            'FIELD_TYPE': 0,
            'FORMULA': 'attribute($currentfeature, \'xcoord\')',
            'INPUT': 'Calculado_7de0a7b2_d5b3_4090_b93c_90732a2bfe01',
            'OUTPUT': parameters['Added_field_cent_lon']
        }
        outputs['CalculadoraDeCamposCent_lon'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Added_field_cent_lon'] = outputs['CalculadoraDeCamposCent_lon']['OUTPUT']

        feedback.setCurrentStep(13)
        if feedback.isCanceled():
            return {}

        
#######Drop variables that you're not interested in: cent_lat_lon#######
        alg_params = {
            'COLUMN': ['fid','cat','xcoord','ycoord','fid_2','cat_2','vertex_index','vertex_part','vertex_part','_index','angle'],
            'INPUT': 'Calculado_1d5469fb_ee3c_408f_a792_e4964bd8200f',
            'OUTPUT': parameters['Centroids_lat_lon_drop_fields']
        }
        outputs['QuitarCamposCent_lat_lon'] = processing.run('qgis:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroids_lat_lon_drop_fields'] = outputs['QuitarCamposCent_lat_lon']['OUTPUT']
        return results   
     
####### Add geometry attributes  #######
        alg_params = {
            'CALC_METHOD': 0,
            'INPUT': 'Campos_restantes_82b5304d_11ed_4cc9_8333_cca4d684f08e',
            'OUTPUT': parameters['Add_geo_coast']
        }
        outputs['AgregarAtributosDeGeometra'] = processing.run('qgis:exportaddgeometrycolumns', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Add_geo_coast'] = outputs['AgregarAtributosDeGeometra']['OUTPUT']

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}    
        
     

        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'coast_lat',
            'FIELD_PRECISION': 10,
            'FIELD_TYPE': 0,
            'FORMULA': 'attribute($currentfeature, \'ycoord\')',
            'INPUT': 'Información_de_geometría_añadida_9ac859f4_820a_48d3_ad32_8d56c4a47d95',
            'OUTPUT': parameters['Added_field_coast_lat']
        }
        outputs['CalculadoraDeCampos'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Added_field_coast_lat'] = outputs['CalculadoraDeCampos']['OUTPUT']

        feedback.setCurrentStep(17)
        if feedback.isCanceled():
            return {}
       
#######Field Calculator: create new field containing the longitude of the coast centroid#######
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'coast_lon',
            'FIELD_PRECISION': 10,
            'FIELD_TYPE': 0,
            'FORMULA': 'attribute($currentfeature, \'xcoord\')',
            'INPUT': 'Calculado_867f6c18_7cb6_478c_ba9b_3e8dd208c133',
            'OUTPUT': parameters['Added_field_coast_lon']
        }
        outputs['CalculadoraDeCampos'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Added_field_coast_lon'] = outputs['CalculadoraDeCampos']['OUTPUT']

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        

#######Drop variables that you're not interested in: coast_lon#######
        alg_params = {
            'COLUMN': ['xcoord','ycoord\n'],
            'INPUT': 'Calculado_3c69fec3_1786_4950_af43_2cb9cce6990d',
            'OUTPUT': '/Users/rochipodesta/Desktop/maestría/Herramientas/semana 5/output/csvout.gpkg',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['QuitarCamposCoast_lon'] = processing.run('qgis:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

    def name(self):
        return 'modelo4b '

    def displayName(self):
        return 'modelo4b '

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Modelo4b()
