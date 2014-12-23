__all__=['Tactics','FormTactics','JSTactics','JSONTactics','RegexTactics']
from Client.UserInformation import  UserInformation
# from Client.MPManager import MPManager
class Tactics:
    ''' Absctract tactics '''
    def __init__(self, order, script):
        self._order, self._script = order, script
    def format(self, uinfo):
        if type(uinfo) is UserInformation:
            for key in uinfo.uinfoDict:
                self._script.replace('{'+key+'}', uinfo.uinfoDict[key])
        elif type(uinfo) is dict:
            for key in uinfo:
                self._script.replace('{'+key+'}', uinfo[key])
    def script(self):
        return self._script

class FormTactics(Tactics):
    def __init__(self, order, script):
        super().__init__(order, script)
        self._result=None
    def getResult(self):
        return self._result
    def setResult(self,result):
        self._result=result

class JSTactics(Tactics):
    pass

class JSONTactics(Tactics):
    def __init__(self, order, script):
        super().__init__(order, script)
        self._result={}
    def getResult(self):
        return self._result

class RegexTactics(Tactics):
    def getResult(self):
        pass
    def setResult(self):
        pass