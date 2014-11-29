from Singleton import Singleton
from DBConnector import DBConnector
from sqlite3 import connect,Row

__all__=['LocalDBConnector']
@Singleton
class LocalDBConnector(DBConnector):
  def __init__(self):
    from PyQt5.QtCore import QSettings
    from os import sep
    from os.path import dirname, join, exists
    print('db init')
    setting = QSettings(QSettings.IniFormat, QSettings.UserScope,'KonkukUniv','rebauth')
    setting.isWritable() #it makes setting folder if doesn't exist
    self._cursor=connect(join(dirname(setting.fileName().replace('/',sep)),'rebauth_local.db'))
    self._cursor.row_factory=Row
    self._cursor=self._cursor.cursor()
    self._cursor.execute('CREATE TABLE IF NOT EXISTS Config (CNT blob, dummy blob, MPexpire integer)')
    self._cursor.connection.commit()
    self._config = self._cursor.execute('SELECT * FROM Config LIMIT 1').fetchone()
    if self._config :
      self._config=dict(self._config)
      self._config['CNT']=int.from_bytes(self._config['CNT'],'big')
    super().__init__()
  def executeQuery(self,query,args=()):
    if type(args) is not tuple:args=(args,)
    return self._cursor.execute(query,args).fetchall()
  def commit(self):
    self._cursor.connection.commit()
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
# localDBConnector=LocalDBConnector()