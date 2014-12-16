from Server import *
from DBConnector import DBConnector
from ClientSocketPool import ClientSocketPool
from Enum import PortEnum

if __name__ == '__main__':
    db = DBConnector('rebauth_server.db',PortEnum.MAIN_SERVER.value)
    ipcSoc = LocalClientIPCSocket(db)
    # cliPool = ClientSocketPool(PortEnum.MAIN_SERVER.value, db)