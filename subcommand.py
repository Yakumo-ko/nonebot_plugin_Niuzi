
from abc import ABC, abstractmethod
from typing_extensions import override

from nonebot import get_driver, get_bot
from nonebot.adapters.mirai2.bot import Bot

from nonebot.adapters.mirai2.event import GroupMessage
from nonebot.adapters import Message
from nonebot.adapters.mirai2.message import MessageSegment, MessageType, MessageChain

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

    @override
    def execute(self, args: list, event: GroupMessage) -> str:
        return GetService().getNewNiuzi(
                    event.get_user_id(), 
                    plugin_config.defalut_nick_name
                )
        
class NameCmd(BaseSubCmd):

    @override
    def desrcibe(self) -> str:
        return "改你牛子的名字, 支持空格, 最长10个字"

    @override
    def useage(self) -> str:
        return self.cmd_prefix + " <name>"

    @override
    def execute(self, args: list, event: GroupMessage) -> str:
        name = " ".join(args)
        return NameService().changeName(event.get_user_id(), name) 

class PKCommand(BaseSubCmd):

    @override
    def desrcibe(self) -> str:
        return "比划一下, 赢加长度输减长度, 断掉双方都减长度"

    @override
    def useage(self) -> str:
        return self.cmd_prefix + " <@target>"

    @override
    async def execute(self, args: list, event: GroupMessage) -> str:
        msg_seg: Union[MessageSegment, None] = event.message_chain. \
                            extract_first(MessageType.AT)
        if msg_seg == None:
            PKService().pk(event.get_user_id(), event.sender.name, "", "", plugin_config.pk_cd)

        bot: Bot = get_bot()
        member= await bot.member_profile(
                target = event.sender.group.id, 
                member_id = msg_seg.data.target)

        return PKService().pk(
            event.get_user_id(),
            event.sender.name,
            msg_seg.data.target,
            member["nickname"],
            plugin_config.pk_cd
                )

