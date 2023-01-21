from typing import Union

import random
import datetime
import time

from .dao import LoversDAO, NiuziDAO
from .entiry import CoolDown, Lovers, NiuZi
from .msg import Msg, setting 
from .event import *
from .utils.Sex import Sex

msg = Msg(**setting) 

class BaseService:

    def __init__(self) -> None:
        self.niuzi_dao = NiuziDAO()
        self.lovers_dao = LoversDAO()
        self.cd_dao = CoolDownDAO()


class ChangeSexService(BaseService):
    
    def change2Woman(self, qq: str, length: int = 50) -> str:
        niuzi: Union[NiuZi, None] = self.niuzi_dao.findNiuziByQQ(qq)
        if niuzi == None:
            return msg.change_sex.no_niuzi

        if niuzi.sex == Sex.FEMALE:
            return msg.change_sex.already_woman
        else:
            niuzi.length -= length 
            niuzi.sex = Sex.FEMALE
            self.niuzi_dao.update(niuzi) 

            return msg.change_sex.success.format(length)


    def change2Man(self, qq: str) -> str:
        assert False


class GetService(BaseService):
        
    def getNewNiuzi(self, qq: str, name: str) -> str:
        if self.niuzi_dao.findNiuziByQQ(qq) != None:
            return msg.get.has_niuzi

        niuzi = self.__createNiuzi(qq, name)
        self.niuzi_dao.insert(niuzi)
        return msg.get.success

    def __createNiuzi(self, qq, name: str) -> NiuZi:
        values = {
                "qq": qq,
                "name": name,
                "length": random.randint(0, 10),
                "sex": random.randint(Sex.getMin(), Sex.getMax()),
                "level": 0,
                "points": 0
                }
        return NiuZi(**values)
 

class InfoService(BaseService):
    
    def getNiuziInfo(self, qq, qq_name) -> str:
        """
        Note: The str return include qq, name, sex end length
        """
        niuzi: Union[NiuZi, None]= self.niuzi_dao.findNiuziByQQ(qq)
        if niuzi == None:
            return msg.info.no_niuzi

        res = msg.info.niuzi_info.format(
                qq = niuzi.qq,
                name = niuzi.name,
                sex =  '女' if niuzi.sex == Sex.FEMALE else '男',
                length = niuzi.length,
                qq_name = qq_name
                )

        return  res

class NameService(BaseService):

    def changeName(self, qq: str, new_name: str) -> str:
        if len(new_name) == 0:
            return msg.no_arg
        
        if len(new_name) > 10:
            return msg.name.name_too_long

        niuzi: Union[NiuZi, None] = self.niuzi_dao.findNiuziByQQ(qq)
        if niuzi == None:
            return msg.no_niuzi

        niuzi.name = new_name
        self.niuzi_dao.update(niuzi)
        return msg.name.success

# TODO
class PKService(BaseService):

    def __init__(self) -> None:
        super().__init__()
        self.events = [
                    PKLost,
                    PKWin,
                    PKAllLost
                ]

    def __getCd(self, qq: str) -> datetime.timedelta:
        cool_down: Union[CoolDown, None] = self.cd_dao.findCoolDownByQQ(qq)
        if cool_down == None:
            return datetime.timedelta(seconds=99999999)
        old = datetime.datetime.fromtimestamp(cool_down.timestampe)
        return datetime.datetime.now() - old

    def __targetEvent(self, 
                      niuzi: NiuZi, 
                      qq_name: str, 
                      target_niuzi: NiuZi, 
                      qq_name_target: str) -> str:

        event: PKEvent = random.choice(self.events)
        return event().execute(niuzi, qq_name, target_niuzi, qq_name_target)
            
    def pk(self, 
           sender_qq: str, 
           sender_name: str, 
           target_qq: Union[str, None], 
           name_target: Union[str, None],
           cd: int) -> str:

        niuzi: Union[NiuZi, None] = self.niuzi_dao.findNiuziByQQ(sender_qq)
        if niuzi == None:
            return msg.no_niuzi

        if target_qq == None:
            return msg.pk.no_args

        if sender_qq == target_qq:
            return msg.pk.same

        time: datetime.timedelta = self.__getCd(sender_qq)
        if time.seconds < cd:
            return msg.pk.source_in_cd.format(cd - time.seconds)
        print(time.seconds)

        target_niuzi: Union[NiuZi, None] = self.niuzi_dao.findNiuziByQQ(target_qq)
        if target_niuzi == None:
            return msg.pk.target_no_niuzi

        time: datetime.timedelta = self.__getCd(target_qq)
        if time.seconds < cd:
            return msg.pk.target_in_cd.format(cd - time.seconds)

        self.cd_dao.deleteByQQ(sender_qq)
        self.cd_dao.deleteByQQ(target_qq)
        self.cd_dao.insert(CoolDown.parse_obj({
                "qq": sender_qq,
                "timestampe": datetime.datetime.now().timestamp()
            }))

        self.cd_dao.insert(CoolDown.parse_obj({
                "qq": target_qq,
                "timestampe": datetime.datetime.now().timestamp()
            }))

        return self.__targetEvent(niuzi, sender_name, target_niuzi, name_target)         

class LoveService(BaseService):
    pass


class AmdinService(BaseService):
    pass



        
