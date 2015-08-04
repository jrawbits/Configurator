# At a minimum, you'll want to import the following items to
# communicate with the NMTK.
from celery.task import task
from NMTK_apps.helpers.config_iterator import ConfigIterator
import datetime

# For this specific tool, we import the following helpers
import confighelpers as cfHelper
from collections import namedtuple
import decimal
import math
from django.core.serializers.json import DjangoJSONEncoder

import logging
logger=logging.getLogger(__name__)

@task(ignore_result=False)
def performModel(input_files,
                 tool_config,
                 client,
                 subtool_name=False):
    '''
    input_files is the set of data to analyze from the NMTK server
    tool_config is is the configuration (loaded by the tool server)
    client is an object linking back to the NMTK server
    subtool_name is provided if the tool manages multiple configurations
    '''
    logger=performModel.get_logger()
    logger.debug('Job input files are: %s', input_files)

    try:
        logger.debug("Task parameters follow:")
        logger.debug("input_files: %s"%(input_files,))
        logger.debug("tool_config"%(tool_config,))
        logger.debug("subtool_name"%(tool_config,))
        (setup,failures) = cfHelper.loadSetup(input_files)
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
            factor_iterator=ConfigIterator(input_files, 'factors', setup)
            if factor_iterator.iterable:
                raise Exception('Factors cannot be iterable')
            else:
                # Extract the parameters
                parameters=factor_iterator.data
                power = parameters.get('power')
                logger.debug("'power' is %s",power)
                power = decimal.Decimal(str(power))

            # Check that the required fields are defined for the
            # input data (based on tool_config)

            numrecs = 0
            numcomp = 0
            pyResult = setup['perfeature']['result']['value']
            for row in file_iterator: # Loop over the rows in the input file
                numrecs += 1
                fldnum = 0
                for field, value in row.iteritems():
                    logger.debug("Adding field %s"%(pyResult,))
                    value = decimal.Decimal(str(value))
                    result = value ** power
                    logger.debug("Computed result %s of value %s ** power %s"%(result,value,power))
                    file_iterator.addResult(pyResult, value ** power)    
                    fldnum += 1
                numcomp += fldnum
            client.updateStatus
            logger.debug("Done computing results.")

            client.updateStatus('Completed computations.')

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
