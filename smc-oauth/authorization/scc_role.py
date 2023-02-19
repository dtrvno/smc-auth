import uuid
class SCCRole:
    def __init__(self,name):
        self.role_name=name
        self.uuid=str(uuid.uuid4())
    def get_role_name(self):
        return self.role_name

