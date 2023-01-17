
from abc import ABC, abstractmethod
from typing_extensions import override

from nonebot import get_driver

from .config import Config
from .service import InfoService, ChangeSexService 

plugin_config = Config.parse_obj(get_driver().config.nonebot_plugin_niuzi)


class BaseSubCmd(ABC):

    def desrcibe(self) -> str:
        return "null"
    
    @abstractmethod
    def useage(self) -> str:
        pass

class InfoCmd(BaseSubCmd):

    @override
    def useage(self) -> str:
        return "女性"

    def getInfo(self, qq: str) -> str:
        return InfoService().getNiuziInfo(qq)


class ChangeSex(BaseSubCmd):

    @override
    def useage(self) -> str:
        return "变女性"

    def change2Woman(self, qq: str) -> str:
        return ChangeSexService().change2Woman(qq, plugin_config.change2woman)

