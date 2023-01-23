
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
        self.hasRequest = False
        self.cmd_prefix = cmd_prefix

    def desrcibe(self) -> str:
        return "null"
    
    @abstractmethod
    def useage(self) -> str:
        pass

    @abstractmethod
    async def execute(self, args: list, event: GroupMessage) -> str:
        pass

class InfoCmd(BaseSubCmd):

    @override
    def desrcibe(self) -> str:
        return "查看你牛子"

    @override
    def useage(self) -> str:
        return "女性"

    @override
    async def execute(self, args: list, event: GroupMessage) -> str:
        return InfoService().getNiuziInfo(
                    event.get_user_id(),
                    qq_name = event.sender.name
                )

class ChangeSexCmd(BaseSubCmd):

    @override
    def useage(self) -> str:
        return self.cmd_prefix

    @override
    async def execute(self, args: list, event: GroupMessage) -> str:
        return ChangeSexService().change2Woman(event.get_user_id())

class GetCmd(BaseSubCmd):
    
    @override
    def useage(self) -> str:
        return self.cmd_prefix

    @override
    async def execute(self, args: list, event: GroupMessage) -> str:
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
    async def execute(self, args: list, event: GroupMessage) -> str:
        name = " ".join(args)
        return NameService().changeName(event.get_user_id(), name) 

class PKCmd(BaseSubCmd):

    @override
    def desrcibe(self) -> str:
        return "比划一下, 赢加长度输减长度, 断掉双方都减长度"

    @override
    def useage(self) -> str:
        return self.cmd_prefix + " <@target>"

    @override
    async def execute(self, args: list, event: GroupMessage) -> str:
        jor seg in event.get_message().export():
            if seg['type'] == MessageType.AT:

                # pytest likely can't get bot here
                """
                bot: Bot = get_bot()
                member= await bot.member_profile(
                            target = event.sender.group.id, 
                            member_id = seg['target'] 
                        )

                return PKService().pk(
                    event.get_user_id(),
                    event.sender.name,
                    seg['target'],
                    member["nickname"],
                    plugin_config.pk_cd
                        )
                """
                return PKService().pk(
                    event.get_user_id(),
                    event.sender.name,
                    str(seg['target']),
                    "none",
                    plugin_config.pk_cd
                        )

        return PKService().pk(
                    event.get_user_id(), 
                    event.sender.name, 
                    None, 
                    None, 
                    plugin_config.pk_cd
                )

class TopCmd(BaseSubCmd):
    @override
    def desrcibe(self) -> str:
        return "查看牛子排行榜"

    @override
    def useage(self) -> str:
        return "none"

    @override
    async def execute(self, args: list, event: GroupMessage) -> MessageChain:
        res: Union[List[str], None] = InfoService().getAll() 

        bot_info = await get_bot().bot_pro_file()

        if res == None:
            return MessageChain(
                    [MessageSegment.plain("太可惜了，本群还没有人领养过牛子")]
                    )

        node_list = MessageChain(
                [MessageSegment.plain(msg) for msg in res] 
            )
           

        return MessageChain([MessageSegment.forward(
                        "",
                        int(get_bot().self_id),
                        int(datetime.datetime.now().timestamp()),
                        bot_info['nickname'],
                        node_list,
                        233
                    )
                ])

class LeaveCmd(BaseSubCmd):
    @override
    def desrcibe(self) -> str:
        return "和你的对象分手"

    @override
    def useage(self) -> str:
        return "none"

    @override
    async def execute(self, args: list, event: GroupMessage) -> MessageChain:
        pass

         
