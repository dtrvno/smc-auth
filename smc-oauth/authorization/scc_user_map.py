import smc_utils.smc_constants
from smc_utils.smc_exception import SMCException
import logging
class SCCUserMap:
    user_roles={}
    logger = logging.getLogger(smc_utils.smc_constants.LOGGER_NAME)
    def __init__(self):
        pass

    @staticmethod
    def add_role_to_user(user_id, role_name):
        if user_id not in SCCUserMap.user_roles:
           SCCUserMap.user_roles[user_id]=[role_name]
        else:
           SCCUserMap.user_roles[user_id].append(role_name)

    @staticmethod
    def get_user_roles(user_id):
        if user_id not in SCCUserMap.user_roles:
           message="User {0} is not supported"
           SCCUserMap.logger.error(message)
           raise SMCException(message)
        roles_obj={"roles": SCCUserMap.user_roles[user_id]}
        return roles_obj


