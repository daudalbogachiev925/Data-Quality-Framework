from enum import Enum

class DQDimension(str, Enum):
    COMPLETENESS = "completeness"     # нет пропусков
    ACCURACY = "accuracy"             # соответствует реальности
    CONSISTENCY = "consistency"       # согласованность между источниками
    TIMELINESS = "timeliness"         # актуальность
    UNIQUENESS = "uniqueness"         # нет дублей
    VALIDITY = "validity"             # соответствует формату/правилам
