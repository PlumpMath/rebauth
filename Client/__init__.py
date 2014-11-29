# import Client.Client
# from Client import Client, MainWindow

from .MainWindow import MainWindow
from .LocalDBConnector import LocalDBConnector
from .MPManager import MPManager
# mainWindow=MainWindow.Instance()
# localDBConnector=LocalDBConnector.Instance()
# mpManager=MPManager.Instance()
from .Cryptor import Cryptor
from .encryptedLineEdit import EncryptedLineEdit

__all__=['MainWindow','LocalDBConnector','MPManager','Cryptor','EncryptedLineEdit']