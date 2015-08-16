# At a minimum, you'll want to import the following items to
# communicate with the NMTK.
from celery.task import task
from NMTK_apps.helpers.config_iterator import ConfigIterator
import datetime

# For this specific tool, we import the following helpers
import confighelpers as cfHelper
import decimal
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

    failures = []
    try:
        logger.debug("Task parameters follow:")
        logger.debug("input_files: %s"%(input_files,))
        logger.debug("tool_config\n%s\n"%(tool_config,))
        (setup,failures) = cfHelper.loadSetup(input_files)
        logger.debug("setup\n%s\n"%(setup,))
        file_iterator=ConfigIterator(input_files, 'data', setup)
    except:
        logger.exception('Failed to parse config file or data file.')
        failures.append('Invalid job configuration')

    if failures:
        for f in failures:
            logger.debug("Failure: %s",f)
        client.updateResults(payload={'errors': failures },
                             failure=True)
    else:    
        client.updateStatus('Parameter & data file validation complete.')
        summ_text = ''
        try:
            client.updateStatus('Starting R Server')
            R = pyRserve.connect()
            factor_iterator=ConfigIterator(input_files, 'factors', setup)
            if factor_iterator.iterable:
                raise Exception('Factors cannot be iterable')
            else:
                # Extract the parameters
                parameters=factor_iterator.data
                power = parameters.get('power')
                logger.debug("'power' is %s",power)

            # Check that the required fields are defined for the
            # input data (based on tool_config)

            numrecs = 0
            numcomp = 0

            pyResultField = setup['perfeature']['python_result']['value']
            RResultField = setup['perfeature']['r_result']['value']

            pyPower = decimal.Decimal(str(power))
            R.r.rpower = power # Warning: everyting arrives in the tool as a string

            client.updateStatus('Setup complete, starting calculations')

            for row in file_iterator: # Loop over the rows in the input file
                numrecs += 1
                fldnum = 0
                for field, value in row.iteritems():
                    logger.debug("Adding Python field %s"%(pyResultField,))
                    try:
                        pyValue = decimal.Decimal(str(value))
                    except:
                        pyValue = decimal.Decimal.from_float(float('nan'))
                    if not pyValue.is_nan():
                        pyResult = pyValue ** pyPower
                    else:
                        pyResult = "NaN-Python"
                    logger.debug("Computed Python result %s of value %s ** power %s"%(pyResult,pyValue,pyPower))
                    file_iterator.addResult(pyResultField+"_"+field, pyResult)    
                    fldnum += 1

                    logger.debug("Adding R field %s"%(RResultField,))
                    R.r.value = value
                    # The JSON parser (used in displaying NMTK results) chokes on a NaN returned directly from R
                    # becauce is doesn't recognize an unquoted NaN as numeric and sses it as a string without quotes
                    R.voidEval('''
result <- as.numeric(value) ** as.numeric(rpower)
if (is.nan(result)||is.na(result)) result<-"Nan-R"
''')
                    logger.debug("Computed R result %s of value %s ** power %s"%(R.r.result,R.r.value,R.r.power))
                    file_iterator.addResult(RResultField+"_"+field,R.r.result)    
                    fldnum += 1
                numcomp += fldnum

            client.updateStatus('Done with calculations')
            logger.debug("Done computing results.")

            #Write out a summary file for the run
            #Number of records processed, string comparison between the
            #different styles out to ten decimal places
            summ_text = 'Description,Value'
            summ_text += '\r\n' + 'Number of records,' + str(numrecs)
            summ_text += '\r\n' + 'Number of computations,' + str(numcomp)
            logger.debug("Summary text %s"%(summ_text,))
                
        except Exception, e:
            # if anything goes wrong we'll send over a failure status.
            print e
            logger.exception('Job Failed with Exception!')
            client.updateResults(payload={'errors': [str(e),] },
                                 failure=True)
        finally:
            del R

        # Since we are updating the data as we go along, we just need to return
        # the data with the new column (results) which contains the result of the 
        # model.
        #result_field=setup['results']['chk_bin_hhsize']['value']
        #units='HH size bins total check'

        client.updateResults(result_field=None,
                         units=None,
                         result_file='data',
                         files={'data': ('data.{0}'.format(file_iterator.extension),
                                         file_iterator.getDataFile(), 
                                         file_iterator.content_type),
                                'summary': ('summary.csv',
                                        summ_text, 
                                        'text/csv')
                                })
            
        
    cfHelper.cleanUp(input_files)
