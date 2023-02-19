import shutil
import os
import sys

from smc_utils.smc_exception import SMCException
import logging

logger = logging.getLogger("smc-orchestrator")
def remove_file(file_name,throw_exception=True):
    try:
        os.remove(file_name)
    except OSError as e:
        if throw_exception:
            message = "Cannot remove file {0}.{1}".format(file_name, e.strerror)
            logger.error(message)
            raise SMCException(message)
def remove_dir(folder):
    try:
       shutil.rmtree(folder,False)
    except (OSError) as e:
       message="Cannot delete folder {0}.{1}:{2}".format(folder,e.strerror,e.filename)
       logger.error(message)
       raise SMCException(message)
    except(Exception) as e:
       message="Cannot delete folder {0}".format(folder)
       logger.error(message)
       raise SMCException(message)
def create_dir(folder,throw=True):

    if os.path.exists(folder):
        if not throw:
           return folder
        message = "Directory {0} already exist".format(folder)
        logger.error(message)
        raise SMCException(message)
    try:
       os.makedirs(folder)
       return folder
    except (OSError) as e:
       message="Cannot create folder {0}.{1}:{2}".format(folder,e.strerror,e.filename)
       logger.error(message)
       raise SMCException(message)
    except(Exception) as e:
       message="Cannot create folder {0}".format(folder)
       logger.error(message)
       raise SMCException(message)

def copy_file(source, target):
    try:
      shutil.copy(source, target)
    except (Exception) as e:
      message="Cannot copy task template from {0} to {1}.{2}:{3}".format(source,target,e.strerror,e.filename)
      logger.error(message)
      raise  SMCException(message)
def get_base_dir():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    base_dir=os.path.dirname(dir_path)
    return base_dir
def load_file(file_name):
    try:
       with open(file_name,'rb') as f:
         s=f.read()
       return s.decode("utf-8")
    except OSError as e:
       message="Cannot open file {0}.{1}.{2}".format(file_name,e.filename,e.strerror)
       logger.error(message)
       raise SMCException(message)
    except FileNotFoundError as e:
        message = "Cannot open file {0}.{1}.{2}".format(file_name, e.filename, e.strerror)
        logger.error(message)
        raise SMCException(message)
    finally:
        if f:
           f.close()
def is_file_exist(file_name):
    if os.path.exists(file_name):
       return True
    return False
def save_file(s,file_name):
    try:
       with open(file_name,"w") as f:
          f.write(s)
       f.close()
    except OSError as e:
        message = "Cannot open file {0}.{1}.{2}".format(file_name, e.filename, e.strerror)
        logger.error(message)
        raise SMCException(message)
def is_windows():
    if sys.platform.startswith("win"):
       return True
    return False


def is_folder_exist(folder):
    if os.path.exists(folder):
        return True
    return False


