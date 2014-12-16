from Server import *
from DBConnector import DBConnector
from ClientSocketPool import ClientSocketPool
from Enum import PortEnum

if __name__ == '__main__':
    db = DBConnector('rebauth_server.db')
    def initDB():
        dbInitialQueries=(('Cert', 'ipaddr text', 'port int')
                          ,('Tactics', 'ID int NOT NULL', 'exec_order int NOT NULL', 'type int NOT NULL', 'script text')
                          ,('Strategy', 'URL text NOT NULL', 'type integer NOT NULL'))
        for q in dbInitialQueries:
            db.executeQuery('CREATE TABLE IF NOT EXISTS '+q[0]+'('+','.join(q[1:])+')')
        db.commit()
    initDB()
    ipcSoc = LocalClientIPCSocket(db)
    cliPool = ClientSocketPool(PortEnum.MAIN_SERVER.value, db)