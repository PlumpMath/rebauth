from Singleton import Singleton
from sqlite3 import connect,Row
from ClientSocketPool import ClientSocketPool
from Enum import PortEnum
from Crypto.Hash import SHA256
class DBConnector():
  def __init__(self,dbfile,port):
    self._con=connect(dbfile)
    from PyQt5.QtCore import QSettings
    from os import sep
    from os.path import dirname, join, exists
    setting = QSettings(QSettings.IniFormat, QSettings.UserScope, 'KonkukUniv', 'rebauth')
    setting.isWritable() #it makes setting folder if doesn't exist
    self._settingPath=dirname(setting.fileName().replace('/',sep))
    self._cursor=connect(join(self._settingPath,dbfile))
    self._cursor.row_factory=Row
    self._cursor=self._cursor.cursor()
    dbInitialQueries=(('Cert', 'PIN int default 0', 'ipaddr text not null', 'port int not null','key blob not null','cnt blob not null')
                      ,('Tactics', 'ID int NOT NULL', 'exec_order int default 0', 'type int NOT NULL', 'script text')
                      ,('Strategy', 'URL text NOT NULL', 'type integer NOT NULL','hash blob', 'valid int default 0'))
    for q in dbInitialQueries:
      self.executeQuery('CREATE TABLE IF NOT EXISTS '+q[0]+'('+','.join(q[1:])+')')
    self._cursor.connection.commit()
    self.socketPool = ClientSocketPool(port, self)
  def getStrategy(self,url,type):
    ''' get transferable type of strategy '''
    ID = self.executeQuery('select rowid from Strategy where URL=? and type=?', (url, type))
    if ID and ID[0]:
      rst=self.executeQuery('select type,script from Tactics where ID=? order by exec_order', ID[0][0])
      return [int.to_bytes(tup['type'],1,'big')+tup['script'].decode() for tup in rst]
    return ()
  def getStrategyHash(self,url,type):
    hash = SHA256.new()
    s = self.getStrategy(url, type)
    for script in s: hash.update(script)
    return hash
  def updateStrategy(self,url,type,strategy):
    ID = self.executeQuery('select rowid from Strategy where URL=? and type=?', (url, type))
    tacticsLst=strategy.getTacticsList()
    if not ID or not ID[0]:
      hash = SHA256.new()
      for tactics in tacticsLst:
        hash.update(tactics.script().encode())
      self.executeQuery('insert into Strategy values(?,?,?,?)',(url,type,hash.digest(),0))
      ID = self.executeQuery('select rowid from Strategy where URL=? and type=?', (url, type))
    rst = self.executeQuery('select rowid from Tactics where ID=? order by exec_order', ID[0]['rowid'])
    for order,s in enumerate(rst):
      self.executeQuery('update Tactics set ID=?,exec_order=?,type=?,script=? where rowid=?',ID[0]['rowid'],(order,type,tacticsLst[order].script(),s['rowid']))
    if len(tacticsLst)<len(rst):
      for i in range(len(tacticsLst), len(rst)):
        self.executeQuery('delete from Tactics where rowid=?',rst[i]['rowid'])
    else:
      for i in range(len(rst), len(tacticsLst)):
        self.executeQuery('insert into Tactics values(?,?,?,?)',(ID[0]['rowid'],i,type,tacticsLst[i].script()))

  def getSettingPath(self):
    return self._settingPath
  def executeQuery(self,query,args=()):
    if type(args) is not tuple:args=(args,)
    return self._cursor.execute(query,args).fetchall()
  def commit(self):
    self._cursor.connection.commit()