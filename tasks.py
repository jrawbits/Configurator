# At a minimum, you'll want to import the following items to
# communicate with the NMTK.
from celery.task import task
from NMTK_apps.helpers.config_iterator import ConfigIterator
import datetime

# For this specific tool, we import the following helpers
from django.conf import settings
import confighelpers as cfHelper
import decimal
import os
import pyRserve

import logging
logger=logging.getLogger(__name__)

def getPythonValue(value,power):
    pass
def getRValue(value,power):
    pass

@task(ignore_result=False)
def performModel(input_files,
                 tool_config,
                 client,
                 subtool_name=False):
    '''
    input_files is the set of data to analyze from the NMTK server
    tool_config is the "header" part of the input
    client is an object of type NMTK_apps.helpers.server_api.NMTKClient
    subtool_name is provided if the tool manages multiple configurations
    '''
    logger=performModel.get_logger()
    logger.debug('Job input files are: %s', input_files)

    # Set up a master directory of error conditions and parameters
    failures = []
    parameters = {}
    compute = parameters["compute"] = {}
    raster = parameters["raster"] = {}
    image = parameters["image"] = {}

    try:
#         logger.debug("Task parameters follow:")
#         logger.debug("input_files: %s"%(input_files,))
#         logger.debug("tool_config\n%s\n"%(tool_config,))
        (setup,failures) = cfHelper.loadSetup(input_files)
        logger.debug("setup\n%s\n"%(setup,))

        ########################################
        # Computation (Python/R)
        compute_factors = ConfigIterator(input_files,'computation_params',setup)

        #   Determine specific computational engines to use, if any
        computetype    = compute["type"] = compute_factors.data.get('computetype',"None")

        #   Notify the user via a status update
        if computetype != 'None':
            compute_R      = compute["with_R"] = computetype in ['R','Both']
            compute_Python = compute["with_Python"] = computetype in ['Python','Both']

            computemsg = "Computation will occur using"
            if compute_R:
                computemsg += " R"
                if compute_Python:
                    computemsg += " and"
            if compute_Python:
                computemsg += " Python"

            #   Determine parameter; default is to square it same as /tool_config
            compute["raisetopower"] = compute_factors.data.get('raisetopower',2)

            #   Determine input (file/constant data) / we'll iterate later
            compute_file = ConfigIterator(input_files,'computation',setup)
            if (compute_R or compute_Python) and not ( compute_file.iterable or compute_file.data ):
                raise Exception("Cannot perform computations without input data")

            #   Determine what to return (result file)
            compute_output = ConfigIterator(input_files,'computation_output',setup)
            compute["PythonName"] = compute_output.data.get('python_result','PowerOfPython')
            compute["RName"] = compute_output.data.get('r_result','PowerOfR')
        else:
            computemsg = "Computation was not requested."

        client.updateStatus(computemsg)

#         ########################################
#         # Rasterization (desired, input file provided, default to use instead)
#         raster_factors = ConfigIterator(input_files,'rasterization_params',setup)
# 
#         #   Check if rasterization was requested
#         dorasterize = raster["do"] = raster_factors.data.get('dorasterize',0)
# 
#         # We're setting up rasterization manually (rather than via ConfigIterator)
#         # because we just need the 'value' property name and the file name for R
#         default_vector_name = os.path.join(settings.STATIC_ROOT, "ALX_roads.json")
#         if dorasterize: # don't bother setting up unless rasterization requested
# 
#             # Get the filename to rasterize, substituting in a default if no file is
#             # provided.  We won't load the file data since we're just going to hand
#             # the file path to R for processing.
#             try:
#                 raster["vectorname"] = input_files['rasterize'][0] # the file name
#             except:  # No file provided, so we'll pull out the default
#                 raster["vectorname"] = default_vector_name
# 
#             # Pull the rastervalue from the job configuration.  We don't care if it's
#             # a literal numeric value or a property name.  The R function to
#             # rasterize the file will use the value as a constant if provided, or
#             # will use a string as the name of a feature attribute to provide the
#             # raster value for that feature.
#             raster["value"] = 1
#             for key, value in setup['rasterize'].iteritems():
#                 if key == 'rastervalue':
#                     raster["value"] = value.get('value', 1)
#                 # Note that we don't care if raster["value"] is a string/fieldname or
#                 # a number because R can handle either one, and we can pass it
#                 # transparently
# 
#             #   Set output format (Rdata, Erdas IMAGINE, geoTIFF)
#             raster_output = ConfigIterator(input_files,'rasterization_output',setup)
#             raster["returnraster"] = raster_output.data.get('return_raster',0) # text of the format requested
#             raster["returnvector"] = raster_output.data.get('return_vector',0)
#             raster["rastername"] = raster_output.data.get('raster_basename',"raster")
# 
#             client.updateStatus('Rasterization configured.')
#         else:
#             client.updateStatus('Rasterization was not requested')
# 
#         ########################################
#         # Image Generation (desired, output format)
#         image_selection = ConfigIterator(input_files,'imaging_params',setup)
#         image["vector"] = image_selection.data.get('imagevector',0)
#         image["raster"] = image_selection.data.get('imageraster',0)
# 
#         image_output = ConfigIterator(input_files,'imaging_output',setup)
#         image["format"] = image_output.data.get('imageformat','PNG')
#         if image_vector or image_raster:
#             client.updateStatus("Imaging successfully configured.")
#         else:
#             client.updateStatus("Imaging was not requested.")

    except Exception as e:
        logger.exception('Failed to parse configuration file or data file.')
        failures.append('Invalid job configuration')
        logger.exception(str(e))
        failures.append(str(e))

    if failures:
        for f in failures:
            logger.debug("Failure: %s",f)
        client.updateResults(payload={'errors': failures },
                             failure=True,
                             files={}
                            )
    else:    
        client.updateStatus('Parameter & data file validation complete.')
        parameter_summary = [("Description","Value")]
        logger.debug("Parameter dictionary")
        logger.debug(str(parameters))
        for section in ["compute","raster","image"]:
            if section in parameters:
                logger.debug("Section ",section,str(parameters[section]))
                parameter_summary.append( ("Section",section) )
                for k,v in parameters[section].iteritems():
                    parameter_summary.append( ("Parameter-%s-%s"%(section,k,),str(v)) )
        summ_text = "\n".join( [ ",".join((str(a),str(b))) for (a,b) in parameter_summary ] )

        client.updateResults(result_field=None,
                             units=None,
                             result_file='summary',
                             files={'summary': ('summary.csv',
                                            summ_text, 
                                            'text/csv')
                                    })

#         try:
#             client.updateStatus('Starting R Server')
#             R = pyRserve.connect()
#             factor_iterator=ConfigIterator(input_files, 'factors', setup)
#             if factor_iterator.iterable:
#                 raise Exception('Factors cannot be iterable')
#             else:
#                 # Extract the parameters
#                 parameters=factor_iterator.data
#                 power = parameters.get('power')
#                 logger.debug("'power' is %s",power)
# 
#             # Check that the required fields are defined for the
#             # input data (based on tool_config)
# 
#             numrecs = 0
#             numcomp = 0
# 
#             pyResultField = setup['perfeature']['python_result']['value']
#             RResultField = setup['perfeature']['r_result']['value']
# 
#             pyPower = decimal.Decimal(str(power))
#             R.r.rpower = power # Warning: everyting arrives in the tool as a string
# 
#             client.updateStatus('Setup complete, starting calculations')
# 
#             for row in file_iterator: # Loop over the rows in the input file
#                 numrecs += 1
#                 fldnum = 0
#                 for field, value in row.iteritems():
#                     logger.debug("Adding Python field %s"%(pyResultField,))
#                     try:
#                         pyValue = decimal.Decimal(str(value))
#                     except:
#                         pyValue = decimal.Decimal.from_float(float('nan'))
#                     if not pyValue.is_nan():
#                         pyResult = pyValue ** pyPower
#                     else:
#                         pyResult = "NaN-Python"
#                     logger.debug("Computed Python result %s of value %s ** power %s"%(pyResult,pyValue,pyPower))
#                     file_iterator.addResult(pyResultField+"_"+field, pyResult)    
#                     fldnum += 1
# 
#                     logger.debug("Adding R field %s"%(RResultField,))
#                     R.r.value = value
#                     # The JSON parser (used in displaying NMTK results) chokes on a NaN returned directly from R
#                     # becauce is doesn't recognize an unquoted NaN as numeric and sses it as a string without quotes
#                     R.voidEval('''
# result <- as.numeric(value) ** as.numeric(rpower)
# if (is.nan(result)||is.na(result)) result<-"Nan-R"
# ''')
#                     logger.debug("Computed R result %s of value %s ** power %s"%(R.r.result,R.r.value,R.r.power))
#                     file_iterator.addResult(RResultField+"_"+field,R.r.result)    
#                     fldnum += 1
#                 numcomp += fldnum
# 
#             client.updateStatus('Done with calculations')
#             logger.debug("Done computing results.")
# 
#         except Exception, e:
#             # if anything goes wrong we'll send over a failure status.
#             print e
#             logger.exception('Job Failed with Exception!')
#             client.updateResults(payload={'errors': [str(e),] },
#                                  failure=True)
#         finally:
#             del R
# 
#         # Since we are updating the data as we go along, we just need to return
#         # the data with the new column (results) which contains the result of the 
#         # model.
#         #result_field=setup['results']['chk_bin_hhsize']['value']
#         #units='HH size bins total check'
# 
#         client.updateResults(result_field=None,
#                          units=None,
#                          result_file='data',
#                          files={'data': ('data.{0}'.format(file_iterator.extension),
#                                          file_iterator.getDataFile(), 
#                                          file_iterator.content_type),
#                                 'summary': ('summary.csv',
#                                         summ_text, 
#                                         'text/csv')
#                                 })

    cfHelper.cleanUp(input_files)
