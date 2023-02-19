import logging
import os

import smc_utils.smc_constants
from smc_utils.smc_jsonutil import has_attribute
from smc_utils.smc_dirutil import create_dir
from smc_utils.smc_exception import SMCException

class LoggingConfiguration:
    def __init__(self,config=None):

        self.logger=logging.getLogger(smc_utils.smc_constants.LOGGER_NAME)
        self.flask_log = logging.getLogger('werkzeug')
        self.flask_log.disabled = True
        self.init_config()

    def init_config(self):
        consoleHandler = logging.StreamHandler();
        infoFormatter = logging.Formatter('%(asctime)s - %(module)s - %(levelname)s - %(message)s')
        debugFormatter = logging.Formatter(
            '%(asctime)s - %(module)s - %(levelname)s - [%(filename)s:%(lineno)d] -%(message)s')
        consoleHandler.setFormatter(SpecialFormatter())


        dirorig = 'c:\smc'

        dir = os.path.expandvars(dirorig)
        if os.path.isabs(dir) is False:
            dir = os.path.join(os.path.abspath('.'),dir)
        create_dir(dir,False)
        if not os.path.isdir(dir):
            message="SMC Error:logging directory {0} does not exist".format(dir)
            raise SMCException(message)

        log_file_name = os.path.join(dir,"auth.log")
        fileHandler = logging.FileHandler(log_file_name)
        fileHandler.setFormatter(SpecialFormatter())

        self.logger.addHandler(consoleHandler)
        self.logger.addHandler(fileHandler)
        self.flask_log.addHandler(consoleHandler)
        self.flask_log.addHandler(fileHandler)

        self.logger.setLevel(logging.DEBUG)
        consoleHandler.setLevel(logging.DEBUG)
        fileHandler.setLevel(logging.DEBUG)


        self.logger.info("Logging configuration has been setup.Logging file:'{0}'.".format(log_file_name))
class SpecialFormatter(logging.Formatter):
    FORMATS = {
        logging.DEBUG: "[%(process)d] %(asctime)s - %(module)s - %(levelname)s - [%(filename)s:%(lineno)d] -%(message)s",
        logging.ERROR: "[%(process)d] %(asctime)s - %(module)s - %(levelname)s - [%(filename)s:%(lineno)d] -%(message)s",
        logging.INFO: "%(asctime)s -%(levelname)s -%(message)s",
        logging.WARNING: "[%(process)d] %(asctime)s - %(module)s - %(levelname)s - [%(filename)s:%(lineno)d] -%(message)s",
        'DEFAULT': "%(levelname)s: %(message)s"}

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt,"%Y-%m-%d %H:%M:%S")
        return formatter.format(record)
