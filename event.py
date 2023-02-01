from abc import ABC, abstractmethod
from typing_extensions import override

import random

from .dao import *
from .entiry import *
from .msg import Msg, setting 

msg = Msg(**setting) 

class EventInterf(ABC):

    @abstractmethod
    def execute(self, *args, **kwargs) -> str:
        pass

class PKEvent(EventInterf):
    
    def __init__(self) -> None:
        super().__init__()
        self.niuzi_dao = NiuziDAO()

    def update(self, niuzi: NiuZi, niuzi_target: NiuZi) -> None:
        self.niuzi_dao.update(niuzi)
        self.niuzi_dao.update(niuzi_target)

    @abstractmethod
    def execute(self, niuzi: NiuZi, 
                    qq_name: str, 
                    niuzi_target: NiuZi, 
                    qq_name_target: str) -> str:
        pass


class PKLost(PKEvent):

    @override
    def execute(self, niuzi: NiuZi, 
                    qq_name: str, 
                    niuzi_target: NiuZi, 
                    qq_name_target: str) -> str:

        random_len = random.random() * random.randint(0, 100)
        niuzi.length -= random_len
        niuzi_target.length += random_len

        self.update(niuzi, niuzi_target)

        return msg.pk.lost.format(
                    you = qq_name,
                    target = qq_name_target,
                    lenght = random_len
                )

class PKWin(PKEvent):

    @override
    def execute(self, niuzi: NiuZi, 
                    qq_name: str, 
                    niuzi_target: NiuZi, 
                    qq_name_target: str) -> str:

        random_len = random.random() * random.randint(0, 100)
        niuzi.length += random_len
        niuzi_target.length -= random_len

        self.update(niuzi, niuzi_target)

        return msg.pk.win.format(
                    you = qq_name,
                    target = qq_name_target,
                    lenght = random_len
                )

        
class PKAllLost(PKEvent):

    @override
    def execute(self, niuzi: NiuZi, 
                    qq_name: str, 
                    niuzi_target: NiuZi, 
                    qq_name_target: str) -> str:

        random_len = random.random() * random.randint(0, 100)
        niuzi.length -= random_len
        niuzi_target.length -= random_len

        self.update(niuzi, niuzi_target)

        return msg.pk.lost.format(
                    you = qq_name,
                    target = qq_name_target,
                    lenght = random_len
                )

pk_event = [
            PKLost,
            PKWin,
            PKAllLost
        ]

def randomPkevent() -> object:
    return random.choice(pk_event)



