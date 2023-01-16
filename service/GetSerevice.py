
import random

from ..entiry.Niuzi import NiuZi
from .BaseService import BaseService
from ..utils.Sex import Sex
from ..Msg import msg

class GetService(BaseService):
        
    def getNewNiuzi(self, qq: str, name: str) -> str:
        if self.niuzi_dao.findNiuziByQQ(qq) != None:
            return msg['get']['hash_niuzi']

        self.__createNiuzi(qq, name)
        return msg['get']['success']

    def __createNiuzi(self, qq, name: str) -> NiuZi:
        values = {
                "owner": qq,
                "name": name,
                "length": random.randint(0, 10),
                "sex": random.randint(Sex.getMin(), Sex.getMax()) 
                }
        return NiuZi(**values)
        
