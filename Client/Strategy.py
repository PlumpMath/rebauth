from Crypto.Hash import SHA256

class Strategy:
    def __init__(self,url,type,tacticsList=[]):
        self._targetUrl,self._type=url,type
        self._tacticsList=tacticsList
        self._result,self._rstAssertCode,self._maxPassLen=None,None,0
    def getHash(self):
        ''' :return: a new SHA256 instance which holds hash of all tactics in order '''
        hash=SHA256.new()
        for tactics in self._tacticsList:
            hash.update(tactics.script())
        return hash
    def getTacticsList(self):
        return self._tacticsList
    def addTactics(self,tactics):
        self._tacticsList.append(tactics)
    def assertResult(self,document):
        ''' :param document: web HTML document
            :return: is assert succeed        '''
        self._isWork=self.rstAssertCode in document
        return self._isWork
    def updateTactics(self,index,tactics):
        self._tacticsList[index]=tactics