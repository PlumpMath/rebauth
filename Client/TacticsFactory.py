
from Client.Tactics import *

def createTactics(type,script):
    ''' translates human readable type name to create new instance of it
    :param type: <string> language type of tactics script
    :param script: <string> tactics script body
    :return: created tactics object    '''
    if type=='form':
        return FormTactics(script)
    elif type=='js':
        return JSTactics(script)
    elif type=='json':
        return JSONTactics(script)
    elif type=='regex':
        return RegexTactics(script)
    return Tactics(script)