import json
from smc_utils.smc_exception import SMCException
import logging
logger = logging.getLogger("smc-orchestrator")
def has_attribute(data, attribute):
    return attribute in data and data[attribute] is not None
def save_json(fileName,jsonObj):
    try:
        with open(fileName, 'w') as outfile:
            json.dump(jsonObj, outfile,indent=4)
    except Exception as e:
        message = "Can not create output file:{0}.{1}".format(fileName,e.args[0])
        logger.error(message)
        raise SMCException(message)