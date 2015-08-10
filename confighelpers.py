"""
Some helpers for building and parsing configuration files.
"""
import os
import json
import logging
logger=logging.getLogger(__name__)

def loadSetup(input_files, failures=[]):
    """
    Load the magic "analysis_settings" section of the job configuration.
    input_files is the block of posted job configuration data from the NMTK server
    failures is a list of strings describing errors that might be returned
    """
    setup = ""
    try:
        setup=json.loads(open(input_files['config'][0]).read()).get('analysis settings',{})
        if (not isinstance(setup, (dict))):
            failures.append('Please provide analysis settings')
    except Exception, e:
        failures.append('JSON load of posted job configuration failed')
    else:
        logger.debug("Loaded config: %s", setup)

    return (setup,failures)

def cleanUp(input_files):
    """
    Delete the temporary files created by the tool server for this job from
    the data that was already posted.
    input_files is the original data block posted to performModel
    """
    for namespace, fileinfo in input_files.iteritems():
        os.unlink(fileinfo[0])        
