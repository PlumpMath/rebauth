#-*-coding:utf-8
from pipes import Template
from os.path import dirname, join
from DBConnector import DBConnector
from Crypto.Hash import SHA256
from Enum import IPCEnum
from threading import Thread

class LocalClientIPCSocket(Template):
    def __init__(self,db):
        super().__init__()
        self._path=db.getSettingPath()
        self._IPCRecvPath,self._IPCSendPath=map(join,(self._path,)*2,('cToSPipe','sToCPipe'))
        self._codeLst=((self._shakeHand,),(self._getStrategyHash,1,4),(self._getStrategy,1,4),(self._updateStrategy,1,4),(self._listAllStrategy,))
        self.db=db
        self.send('')
        Thread(target=self._servLocalClient).start()
    def send(self,msg):
        super().open_w(self._IPCSendPath).write(msg)
    def _clearRecv(self):
        super().open_w(self._IPCRecvPath).write('')
    def recv(self):
        ''' read and clear the reading pipe
        :return:None on no pipe, str on pipe read '''
        try:
            msg=super().open_r(self._IPCRecvPath).read()
            self._clearRecv()
            return msg
        except FileNotFoundError : return None
    def _servLocalClient(self):
        '''  acts like socketserver.BaseServer.serv_forever '''
        from time import sleep
        while True:
            msg=self.recv()
            if msg and len(msg)>=1 and msg[0].isdigit():
                fnNum=int(msg[0])
                if 0 <= fnNum < len(self._codeLst):
                    code=self._codeLst[fnNum]
                    fn,arg,ind=code[0],[],1
                    for i in range(1,len(code)):
                        if ind+code[i]>=len(msg) : break
                        arg.append(msg[ind:ind+code[i]])
                        ind+=code[i]
                    if len(msg) > ind:
                        arg.append(msg[ind:])
                    fn(*arg)
            sleep(0.5)
    def _updateStrategy(self,type,urlLen,body):
        if not type.isdecimal() or not urlLen.isdecimal() or len(body)<int(urlLen)+2: return
        type,urlLen=map(int,(type,urlLen))
        url,body=body[:urlLen],body[urlLen:]
        ID=self.db.executeQuery('select rowid from Strategy where URL=? and type=?',(url,type))
        if not ID:
            self.db.executeQuery('insert into Strategy(URL,type) values(?,?)',(url,type))
            ID=self.db.executeQuery('select rowid from Strategy where URL=? and type=?',(url,type))
        ID=ID[0]
        order=0
        for script in body.split('\x1f'): #0x1f=US=Unit Seperator
            strategyType,script=int.from_bytes(script[0].encode(),'big'),script[1:]
            rowid=self.db.executeQuery('select rowid from Tactics where ID=? and exec_order=?',(ID,order))
            if rowid:
                self.db.executeQuery('update Tactics set exec_order=?,type=?,script=? where rowid=?',(order,strategyType,script,rowid[0]))
            else:
                self.db.executeQuery('insert into Tactics(ID,exec_order,type,script) values(?,?,?,?)',(ID,order,strategyType,script))
            order+=1
        # rst=self.db.executeQuery('select order from Tactics where ID=? order by order',ID)
        # if rst:
        #     self.db.executeQuery('insert into Strategy')
        self.send(str(IPCEnum.ACK.value)+str(order))
        # self.write(int.to_bytes(IPCEnum.ERROR,1,'big'))
    def _shakeHand(self):
        print('IPC shakeHand')
        # if msg<36 or msg[0]!=str(IPCEnum.ACK.value): return
        self.send(str(IPCEnum.ACK.value))
    def _getStrategyHash(self,type,urlLen,url):
        if not type.isdecimal() or not urlLen.isdecimal() or len(url)!=int(urlLen): return
        hash = self.db.getStrategyHash(url,int(type))
        self.send(hash.hexdigest if hash else str(IPCEnum.ERROR.value))
    def _getStrategy(self,type,urlLen,url):
        if not type.isdecimal() or not urlLen.isdecimal() or len(url)!=int(urlLen): return
        s=self.db.getStrategy(url, int(type))
        self.send('\x1f'.join([tup[0] for tup in s]) if s else str(IPCEnum.ERROR.value))
    def _listAllStrategy(self):
        rst=self.db.executeQuery('select * from Strategy')
        self.send('\x1f'.join([tup[0] for tup in rst]))