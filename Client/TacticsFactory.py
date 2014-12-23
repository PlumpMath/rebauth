
from Client.Tactics import *
from Enum import TacticsEnum
def createTactics(ttype,order,script):
    ''' translates human readable type name to create new instance of it
    :param type: <string> language type of tactics script
    :param script: <string> tactics script body
    :return: created tactics object    '''
    if type(ttype) is str:
        if ttype=='form':
            return FormTactics(order,script)
        elif ttype=='js':
            return JSTactics(order,script)
        elif ttype=='json':
            return JSONTactics(order,script)
        elif ttype=='regex':
            return RegexTactics(order,script)
    elif type(ttype) is int:
        if ttype == TacticsEnum.FORM.value:
            return FormTactics(order,script)
        elif ttype == TacticsEnum.JSCRIPT.value:
            return JSTactics(order,script)
        elif ttype == TacticsEnum.JSON.value:
            return JSONTactics(order,script)
        elif ttype == TacticsEnum.REGEX.value:
            return RegexTactics(order,script)
    return Tactics(order,script)