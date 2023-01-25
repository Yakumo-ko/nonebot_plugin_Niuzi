
from abc import ABC, abstractmethod
from typing_extensions import override

from nonebot import get_driver, get_bot

from nonebot.adapters.mirai2.event import GroupMessage
from nonebot.adapters import Message
from nonebot.adapters.mirai2.message import MessageSegment, MessageType, MessageChain
from nonebot.permission import Permission
from nonebot.typing import T_State
from nonebot.matcher import Matcher

import datetime

from .config import Config
from .msg import Msg, setting 
from .entiry import *
from .dao import * 
from .event import *
from .utils.Sex import Sex

plugin_config = Config.parse_obj(get_driver().config.nonebot_plugin_niuzi)

msg = Msg(**setting) 

class BaseSubCmd(ABC):
    
    def __init__(self, cmd_prefix: str) -> None:
        self.cmd_prefix = cmd_prefix

        self.niuzi_dao = NiuziDAO()
        self.lovers_dao = LoversDAO()
        self.cd_dao = CoolDownDAO()

    def desrcibe(self) -> str:
        return "null"
    
    def useage(self) -> str:
        return "null"
        

    @abstractmethod
    async def execute(self, 
                matcher: Matcher,
                stats: T_State, 
                event: GroupMessage,
                args: str
            ) -> None:
        pass

    async def request(self,
                matcher: Matcher,
                stats: T_State, 
                event: GroupMessage,
              ) -> None:
        pass

    async def checkPerm(self,
                matcher: Matcher,
                stats: T_State, 
                event: GroupMessage,
            ) -> bool:
        return True

class InfoCmd(BaseSubCmd):
    @override
    def desrcibe(self) -> str:
        return "查看你牛子"

    @override
    async def execute(self, 
                matcher: Matcher,
                stats: T_State,
                event: GroupMessage,
                args: str 
            ) -> None:
        niuzi: Union[NiuZi, None]= self.niuzi_dao.findNiuziByQQ(
                event.get_user_id())
        if niuzi == None:
            await matcher.finish(msg.info.no_niuzi)

        await matcher.finish(msg.info.niuzi_info.format(
                        qq = niuzi.qq,
                        name = niuzi.name,
                        sex =  self.__toChinese(niuzi.sex),
                        length = niuzi.length,
                        qq_name = event.sender.name 
                    )
                )

    def __toChinese(self, sex: int) -> str:
        return '女' if sex == Sex.FEMALE else '男'

    def getAll(self) -> Union[List[str], None]:
        niuzi_list = self.niuzi_dao.getAll()
        if niuzi_list == None:
            return None

        niuzi_list.sort(key=lambda a: a.length, reverse=True)
        
        res = []
        i = 0
        for niuzi in niuzi_list:
            tmp = msg.info.niuzi_info.format(
                    qq = niuzi.qq,
                    name = niuzi.name,
                    sex =  self.__toChinese(niuzi.sex),
                    length = niuzi.length,
                    qq_name = "none" 
                )
              
            res.append(f"{i}: "+ tmp)
            i+=1

class ChangeSexCmd(BaseSubCmd):

    @override
    def desrcibe(self) -> str:
        return "变为女孩子"

    @override
    async def execute(self, 
                matcher: Matcher,
                stats: T_State, 
                event: GroupMessage,
                args: str
            ) -> None:
        niuzi: Union[NiuZi, None] = self.niuzi_dao.findNiuziByQQ(
                event.get_user_id()
                )
        if niuzi == None:
            await matcher.finish(msg.change_sex.no_niuzi)

        if niuzi.sex == Sex.FEMALE:
            await matcher.finish(msg.change_sex.already_woman)
        else:
            niuzi.length -= plugin_config.change2woman 
            niuzi.sex = Sex.FEMALE
            self.niuzi_dao.update(niuzi) 

            await matcher.finish(
                    msg.change_sex.success.format(plugin_config.change2woman)
                    )

class GetCmd(BaseSubCmd):
    
    @override
    def desrcibe(self) -> str:
        return "获取新牛子" 

    @override
    async def execute(self, 
                matcher: Matcher,
                stats: T_State, 
                event: GroupMessage,
                args: str
            ) -> None:
        qq = event.get_user_id()
        if self.niuzi_dao.findNiuziByQQ(qq) != None:
            await matcher.finish(msg.get.has_niuzi)

        self.niuzi_dao.insert(
                NiuZi.parse_obj({
                    "qq": qq,
                    "name": plugin_config.defalut_nick_name,
                    "length": random.randint(0, 10),
                    "sex": random.randint(Sex.getMin(), Sex.getMax()),
                    "level": 0,
                    "points": 0
                })
            )
        await matcher.finish(msg.get.success)

class NameCmd(BaseSubCmd):

    @override
    def desrcibe(self) -> str:
        return "改你牛子的名字, 支持空格, 最长10个字"

    @override
    def useage(self) -> str:
        return self.cmd_prefix + " <name>"

    @override
    async def execute(self, 
                matcher: Matcher,
                stats: T_State, 
                event: GroupMessage,
                args: str
            ) -> None:
        if len(args) == 0:
            await matcher.finish(msg.no_arg)
        
        if len(args) > 10:
            await matcher.finish(msg.name.name_too_long)

        niuzi: Union[NiuZi, None] = self.niuzi_dao.findNiuziByQQ(
                event.get_user_id()
                )
        if niuzi == None:
            await matcher.finish(msg.no_niuzi)

        niuzi.name = args 
        self.niuzi_dao.update(niuzi)

        await matcher.finish(msg.name.success)

class PKCmd(BaseSubCmd):

    def __init__(self, cmd_prefix: str) -> None:
        super().__init__(cmd_prefix)

    @override
    def desrcibe(self) -> str:
        return "比划一下, 赢加长度输减长度, 断掉双方都减长度"

    @override
    def useage(self) -> str:
        return self.cmd_prefix + " <@target>"

    @override
    async def execute(self, 
                matcher: Matcher,
                stats: T_State, 
                event: GroupMessage,
                args: str
            ) -> None:
        sender = event.get_user_id()
        niuzi: Union[NiuZi, None] = self.niuzi_dao.findNiuziByQQ(sender)
        if niuzi == None:
            await matcher.finish(msg.no_niuzi)

        target = self.__hasAT(event) 
        if target == None:
            await matcher.finish(msg.pk.no_args)

        if sender == target:
            await matcher.finish(msg.pk.same)

        time: datetime.timedelta = self.__getCd(sender)
        if time.seconds < plugin_config.pk_cd:
            await matcher.finish(
                    msg.pk.source_in_cd.format(
                        plugin_config.pk_cd - time.seconds
                        )
                    )

        target_niuzi: Union[NiuZi, None] = self. \
                        niuzi_dao.findNiuziByQQ(target)
        if target_niuzi == None:
            await matcher.finish(msg.pk.target_no_niuzi)

        time: datetime.timedelta = self.__getCd(target)
        if time.seconds < plugin_config.pk_cd:
            await matcher.finish(
                    msg.pk.target_in_cd.format(
                        plugin_config.pk_cd - time.seconds
                    )
                )

        self.__updateCd(sender, target)

        pk_event = getPkevent()
        await matcher.finish(
                pk_event().execute(niuzi, "none", target_niuzi, "none")         
            )

    def __updateCd(self, sender: str, target: str) -> None:
        self.cd_dao.deleteByQQ(sender)
        self.cd_dao.deleteByQQ(target)
        self.cd_dao.insert(CoolDown.parse_obj({
                "qq": sender,
                "timestampe": datetime.datetime.now().timestamp()
            }))

        self.cd_dao.insert(CoolDown.parse_obj({
                "qq": target,
                "timestampe": datetime.datetime.now().timestamp()
            }))

    def __getCd(self, qq: str) -> datetime.timedelta:
        cool_down: Union[CoolDown, None] = self.cd_dao.findCoolDownByQQ(qq)
        if cool_down == None:
            return datetime.timedelta(seconds=99999999)
        old = datetime.datetime.fromtimestamp(cool_down.timestampe)
        return datetime.datetime.now() - old

    def __hasAT(self, 
                event: GroupMessage
        ) -> Union[str, None]:
        for seg in event.get_message().export():
            if seg['type'] == MessageType.AT:
                return str(seg['target'])
        return None


class TopCmd(BaseSubCmd):
    @override
    def desrcibe(self) -> str:
        return "查看牛子排行榜"

    @override
    async def execute(self, 
                matcher: Matcher,
                stats: T_State, 
                event: GroupMessage,
                args: str
            ) -> None:
        res: Union[List[str], None] = self.getAll() 

        bot_info = await get_bot().bot_pro_file()

        if res == None:
            await matcher.finish("太可惜了，本群还没有人领养过牛子")

        node_list = MessageChain(
                [MessageSegment.plain(msg) for msg in res] 
            )
           

        await matcher.finish(MessageChain([MessageSegment.forward(
                        "",
                        int(get_bot().self_id),
                        int(datetime.datetime.now().timestamp()),
                        bot_info['nickname'],
                        node_list,
                        233
                    )
                ])
            )

    def __toChinese(self, sex: int) -> str:
        return '女' if sex == Sex.FEMALE else '男'

    def getAll(self) -> Union[List[str], None]:
        niuzi_list = self.niuzi_dao.getAll()
        if niuzi_list == None:
            return None

        niuzi_list.sort(key=lambda a: a.length, reverse=True)
        
        res = []
        i = 0
        for niuzi in niuzi_list:
            tmp = msg.info.niuzi_info.format(
                    qq = niuzi.qq,
                    name = niuzi.name,
                    sex =  self.__toChinese(niuzi.sex),
                    length = niuzi.length,
                    qq_name = "none" 
                )
              
            res.append(f"{i}: "+ tmp)
            i+=1



class LeaveCmd(BaseSubCmd):
    
    def __init__(self, cmd_prefix: str) -> None:
        super().__init__(cmd_prefix)

    @override
    def desrcibe(self) -> str:
        return "和你的对象分手"

    @override
    async def execute(self, 
                matcher: Matcher,
                stats: T_State, 
                event: GroupMessage,
                args: str
            ) -> None:
        lover = self.lovers_dao.findloversByQQ(
                event.get_user_id())

        if lover == None:
            await matcher.finish(msg.no_lover)


        await matcher.send(
                msg.leave.request.send.format(
                    target = lover.target,
                    sender = lover.qq
                )
            )

        stats.update({
               "sender": lover.qq,
               "target": lover.target,
               "subcmd": self
           })


    @override
    async def request(self, matcher: Matcher, stats: T_State, event : GroupMessage
            ) -> None:
       if event.get_plaintext() == "同意":
            assert stats.get('sender') != None
            self.lovers_dao.deleteByQQ(stats.get('sender'))
            await matcher.finish(msg.leave.request.agree)
       await matcher.finish(msg.leave.request.disagree)

    @override
    async def checkPerm(self, matcher: Matcher, stats: T_State, event: GroupMessage
            ) -> bool:
        if stats.get("target") == event.get_user_id():
            return True
        return False



    def getInfo(self, qq: str) -> str:
        niuzi = self.niuzi_dao.findNiuziByQQ(qq)

        return msg.status.format(
                    qq = qq,
                    qq_name = "",
                    name = niuzi.name,
                    sex = niuzi.sex,
                    length = niuzi.length
                )

    
