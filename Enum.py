from enum import Enum,unique

@unique
class SocketEnum(Enum):
    ERROR=0xff
    ACK,PIN,SCAN,SCAN_ANS,MASTER_LOC_IPV4,MASTER_LOC_IPV6,SHAKEHAND,SHAKE_SUCC,SYNC_FETCH,SYNC_PULL,EXCHANGE_PVG=range(11)
@unique
class IPCEnum(Enum):
    ERROR=0xff
    ACK,GET_HASH,GET,UPDATE,LIST_ALL=range(5)
class StategyEnum(Enum):
    GET,JOIN,LOGIN,CHANGE=range(4)
class TacticsEnum(Enum):
    REGEX,JSCRIPT,JSON,FORM=range(4)