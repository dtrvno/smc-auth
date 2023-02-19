class SMCException(Exception):
    def __init__(self,message):
        self.message = message
        return
def get_common_exception_message(e):
    if len(e.args)==0:
       return "Error in orchestrator"
    s=""
    for numb in range(len(e.args)):
        item=e.args[numb]
        if numb!=0:
           item=":"+str(item)
        s+=str(item)
    return s    
        
        

      
