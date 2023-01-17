from typing import Union

import random

from .dao import LoversDAO, NiuziDAO
from .entiry import Lovers, NiuZi
from .Msg import msg
from .utils.Sex import Sex

class BaseService:

    def __init__(self) -> None:
        self.niuzi_dao = NiuziDAO()
        self.lovers_dao = LoversDAO()


class ChangeSexService(BaseService):
    
    def change2Woman(self, qq: str, length: int) -> str:
        niuzi: Union[NiuZi, None] = self.niuzi_dao.findNiuziByQQ(qq)
        if niuzi == None:
            return msg['change_sex']['no_niuzi']

        if niuzi.sex == Sex.FEMALE:
            return msg['change_sex']['already_woman']
        else:
            niuzi.length -= length 
            niuzi.sex = Sex.FEMALE
            self.niuzi_dao.update(niuzi) 

            return msg['change_sex']['success'].format(length)


    def change2Man(self, qq: str) -> str:
        assert False


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
 

class InfoService(BaseService):
    
    def getNiuziInfo(self, qq) -> str:
        niuzi: Union[NiuZi, None]= self.niuzi_dao.findNiuziByQQ(qq)
        if niuzi == None:
            return msg['info']['no_niuzi']

        return msg['info']['niuzi_info']


