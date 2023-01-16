from typing import Union 

from .BaseService import BaseService
from ..entiry.Niuzi import NiuZi
from ..Msg import msg


class InfoService(BaseService):
    
    def getNiuziInfo(self, qq) -> str:
        niuzi: Union[NiuZi, None]= self.niuzi_dao.findNiuziByQQ(qq)
        if niuzi == None:
            return msg['info']['no_niuzi']

        return msg['info']['niuzi_info']


    

