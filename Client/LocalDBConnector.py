from Singleton import Singleton
from DBConnector import DBConnector
from Client.ServerSocket import ServerSocket
from Enum import PortEnum
__all__=['LocalDBConnector']

@Singleton
class LocalDBConnector(DBConnector):
  def __init__(self):
    super().__init__('rebauth_local.db',PortEnum.MASTER_CLIENT.value)
    self.executeQuery('CREATE TABLE IF NOT EXISTS Config (CNT blob, dummy blob, MPexpire int default 5, lastPIN int default 0)')
    self.commit()
    self._config = self._cursor.execute('SELECT * FROM Config LIMIT 1').fetchone()
    self.socket = ServerSocket(self)
    if self._config :
      self._config=dict(self._config)
      self._config['CNT']=int.from_bytes(self._config['CNT'],'big')
  def getConfig(self):
    return self._config
  def updateConfig(self,dict=None):
    qry=''
    if self._config:
      if dict:self._config.update(dict)
      qry='UPDATE Config SET ' + ','.join(key+'=?' for key in self._config)
    else:
      self._config = dict
      qry='INSERT INTO Config ('+','.join(self._config)+') VALUES('+','.join('?'*len(self._config))+')'
    intBackup=self._config['CNT']
    self._config['CNT']=self._config['CNT'].to_bytes(128//8,'big')
    self._cursor.execute(qry,tuple(self._config.values()))
    self.commit()
    self._config['CNT']=intBackup
    return self._config