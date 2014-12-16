from Singleton import Singleton
from sqlite3 import connect,Row
from ClientSocketPool import ClientSocketPool

class DBConnector():
  def __init__(self,dbfile):
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
    self.socketPool = ClientSocketPool('', self)
  def getSettingPath(self):
    return self._settingPath
  def executeQuery(self,query,args=()):
    if type(args) is not tuple:args=(args,)
    return self._cursor.execute(query,args).fetchall()
  def commit(self):
    self._cursor.connection.commit()