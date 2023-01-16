from typing import Union

from ..entiry.Niuzi import NiuZi
from .BaseService import BaseService

from ..Msg import msg
from ..utils.Sex import Sex

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

