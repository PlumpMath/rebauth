__all__=['Tactics','FormTactics','JSTactics','JSONTactics','RegexTactics']

# from Client.MPManager import MPManager
class Tactics:
    ''' Absctract tactics '''
    def __init__(self,script):
        self._script=script
    def format(self, uinfo):
        for key in uinfo.uinfoDict:
            self._script.replace('{'+key+'}', uinfo.uinfoDict[key])
    def script(self):
        return self._script

class FormTactics(Tactics):
    def __init__(self):
        super.__init__()
        self._result=None
    def getResult(self):
        return self._result
    def setResult(self,result):
        self._result=result

class JSTactics(Tactics):
    pass

class JSONTactics(Tactics):
    def __init__(self):
        super.__init__()
        self._result={}
    def getResult(self):
        return self._result

class RegexTactics(Tactics):
    def getResult(self):
        pass
    def setResult(self):
        pass