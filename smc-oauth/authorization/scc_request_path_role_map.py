class SCCRequestPathRoleMap:
    #we need to setup it from config
    request_role_map={
            "/v1/execute1":
                {
                    "admin_role": ["GET"]
                },
            "/v1/execute2":
                {
                    "regular_role": ["GET"],
                    "admin_role": ["GET"]
                }
        }

    def __init__(self):
        pass

    @staticmethod
    def get_role_map():
        return SCCRequestPathRoleMap.request_role_map

    @staticmethod
    def is_role_supported(roles,path,method):
        if path not in SCCRequestPathRoleMap.request_role_map:
           return False
        path_obj=SCCRequestPathRoleMap.request_role_map[path]
        for role_name in roles:
            if role_name in path_obj:
               return True
        return False
