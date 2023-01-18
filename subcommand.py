
from abc import ABC, abstractmethod
from typing_extensions import override

from nonebot import get_driver
from nonebot.adapters.mirai2.event import GroupMessage
from nonebot.adapters import Message

from .config import Config
from .service import * 

plugin_config = Config.parse_obj(get_driver().config.nonebot_plugin_niuzi)


class BaseSubCmd(ABC):
    
    def __init__(self, cmd_prefix: str) -> None:
        self.cmd_prefix = cmd_prefix

    def desrcibe(self) -> str:
        return "null"
    
    @abstractmethod
    def useage(self) -> str:
        pass

    @abstractmethod
    def execute(self, args: list, event: GroupMessage) -> str:
        pass

class InfoCmd(BaseSubCmd):

    @override
    def desrcibe(self) -> str:
        return "查看你牛子"

    @override
    def useage(self) -> str:
        return "女性"

    @override
    def execute(self, args: list, event: GroupMessage) -> str:
        return InfoService().getNiuziInfo(
                    event.get_user_id(),
                    qq_name = event.sender.name
                )

class ChangeSexCmd(BaseSubCmd):

    @override
    def useage(self) -> str:
        return self.cmd_prefix

    @override
    def execute(self, args: list, event: GroupMessage) -> str:
        return ChangeSexService().change2Woman(event.get_user_id())

class GetCmd(BaseSubCmd):
    
    @override
    def useage(self) -> str:
        return self.cmd_prefix

    def execute(self, args: list, event: GroupMessage) -> str:
        return GetService().getNewNiuzi(
                    event.get_user_id(), 
                    plugin_config.defalut_nick_name
                )
        

