from Singleton import Singleton
from DBConnector import DBConnector
from Client.ServerSocket import ServerSocket
from Enum import PortEnum
__all__=['LocalDBConnector']

@Singleton
class LocalDBConnector(DBConnector):
  def __init__(self):
    super().__init__('rebauth_local.db', PortEnum.MASTER_CLIENT.value)
    self.executeQuery('CREATE TABLE IF NOT EXISTS Config (CNT blob, dummy blob, MPexpire int default 5, lastPIN int default 0)')
    self.executeQuery('CREATE TABLE IF NOT EXISTS UserInformation (uID blob, firstname blob, lastname blob, middlename blob, gender blob, birthday blob, hom_country blob, hom_city blob, hom_address1 blob, hom_address2 blob, hom_address3 blob, hom_postal blob, com_country blob, com_city blob, email blob, phone_mobile blob, phone_home blob, phone_work blob)')
    self.executeQuery('CREATE TABLE IF NOT EXISTS AuthInformation (url string, uID blob, uPW blob, cnt blob, lastUpdate blob)')
    self.commit()
    self._config = self._cursor.execute('SELECT * FROM Config LIMIT 1').fetchone()
    self.socket = ServerSocket(self)
    if self._config :
      self._config=dict(self._config)
      self._config['CNT']=int.from_bytes(self._config['CNT'],'big')
  def getUserInfo(self):
    return self.executeQuery('select * from UserInformation limit 1')
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