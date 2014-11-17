from Singleton import Singleton
from DBConnector import DBConnector
from sqlite3 import connect

@Singleton
class LocalDBConnector():
  def __init__(self):
    self._cursor=connect('./localDB.db').cursor()
    self._cursor.execute("CREATE TABLE IF NOT EXISTS Config (CNT blob, dummy blob)")
    super().__init__()
  def executeQuery(self,query,args=()):
    if type(args) is not tuple:args=(args,)
    return self._cursor.execute(query,args)
  def commit(self):
    self._cursor.connection.commit()
  def getCounter(self):
    from Crypto.Util.number import getPrime
    return getPrime(128)