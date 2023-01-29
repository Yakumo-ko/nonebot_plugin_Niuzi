
from abc import ABC, abstractmethod
from typing_extensions import override

from nonebot import get_driver, get_bot
from nonebot.adapters import Message, MessageTemplate

from nonebot.adapters.mirai2.event import GroupMessage
from nonebot.adapters.mirai2.message import MessageSegment, MessageType, MessageChain
from nonebot.typing import T_State
from nonebot.matcher import Matcher

import datetime

from .config import Config
from .msg import Msg, setting 
from .entiry import *
from .dao import * 
from .event import *
from .utils.Sex import Sex, CDType

plugin_config = Config.parse_obj(get_driver().config)

msg = Msg(**setting) 

class BaseSubCmd(ABC):
    def __init__(self, cmd_prefix: str) -> None:
        self.cmd_prefix = cmd_prefix

        self.niuzi_dao = NiuziDAO()
        self.lovers_dao = LoversDAO()
        self.cd_dao = CoolDownDAO()

    def desrcibe(self) -> str:
        return "no desrcibe"
    
    def useage(self) -> str:
        return self.cmd_prefix
        

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
        self.cd_dao.deleteByQQ(sender, CDType.pk)
        self.cd_dao.deleteByQQ(target, CDType.pk)
        self.cd_dao.insert(CoolDown.parse_obj({
                "qq": sender,
                "timestampe": datetime.datetime.now().timestamp(),
                "type": CDType.pk
            }))

        self.cd_dao.insert(CoolDown.parse_obj({
                "qq": target,
                "timestampe": datetime.datetime.now().timestamp(),
                "type": CDType.pk
            }))

    def __getCd(self, qq: str) -> datetime.timedelta:
        cool_down = self.cd_dao.findCoolDownByQQ(qq, CDType.pk)
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

        await matcher.send(Message.template("{at}{msg}").format(
            at = MessageSegment.at(lover.target),
            msg = MessageSegment.plain(msg.leave.request.send.format(
                        target = lover.target,
                        sender =lover.qq 
                    ))
            ))

        stats.update({
               "sender": str(lover.qq),
               "target": str(lover.target),
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
        at_qq = self.__hasAT(event) 
        
        if at_qq == None:
            return False 

        target = stats.get("target")
        sender = event.get_user_id()
        if target == sender and at_qq == stats.get("sender"):
            return True
        return False

    def __hasAT(self, 
                event: GroupMessage
        ) -> Union[str, None]:
        for seg in event.get_message().export():
            if seg['type'] == MessageType.AT:
                return str(seg['target'])
        return None

class LoverInfoCmd(BaseSubCmd):
    @override
    def desrcibe(self) -> str:
        return "查看你的对象的牛子信息"

    async def execute(self, 
                matcher: Matcher, 
                stats: T_State, 
                event: GroupMessage, 
                args: str
            ) -> None:
        lover = self.lovers_dao.findloversByQQ(event.get_user_id())
        if lover == None:
            await matcher.finish(msg.no_lover)
        qq = lover.target if lover.target != event.get_user_id() else lover.qq
        niuzi = self.niuzi_dao.findNiuziByQQ(str(qq))
        await matcher.finish(msg.status.format(
                    qq = "",
                    qq_name = niuzi.qq,
                    name = niuzi.name,
                    sex = niuzi.sex,
                    length = niuzi.length
            ))
        
class LoveRequestCmd(BaseSubCmd):
    @override
    def desrcibe(self) -> str:
        return "和别人搞对象"

    @override
    def useage(self) -> str:
        return self.cmd_prefix + " <@target>"

    async def execute(self, 
                matcher: Matcher, 
                stats: T_State, 
                event: GroupMessage, 
                args: str
            ) -> None:
        sender = event.get_user_id()
        if self.lovers_dao.findloversByQQ(sender) != None:
            await matcher.finish(msg.lover.get.has_lover)

        target = self.__hasAT(event)
        if target == None:
            await matcher.finish(msg.lover.get.has_lover)

        if target == sender:
            await matcher.finish(msg.lover.get.self)

        if self.lovers_dao.findloversByQQ(target) != None:
            await matcher.finish(msg.lover.get.fail)

        if self.niuzi_dao.findNiuziByQQ(target) == None:
            await matcher.finish(msg.lover.get.target_no_niuzi)
        
        await matcher.send(Message.template("{at}{msg}").format(
            at = MessageSegment.at(int(target)),
            msg = MessageSegment.plain(msg.lover.request.send.format(
                        target = target,
                        sender = sender
                    ))
            ))

        stats.update({
               "sender": str(sender),
               "target": str(target),
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
        at_qq = self.__hasAT(event) 
        if at_qq == None:
            return False

        target = stats.get("target")
        sender = event.get_user_id()
        if target == sender and at_qq == stats.get('sender'):
            return True
        return False


    def __hasAT(self, 
                event: GroupMessage
        ) -> Union[str, None]:
        for seg in event.get_message().export():
            if seg['type'] == MessageType.AT:
                return str(seg['target'])
        return None

class DoiCmd(BaseSubCmd):
    @override
    def desrcibe(self) -> str:
        return "和对象贴贴!"

    @override
    async def execute(self, 
                matcher: Matcher, 
                stats: T_State, 
                event: GroupMessage, 
                args: str
            ) -> None:
        lover = self.lovers_dao.findloversByQQ(event.get_user_id())
        if lover == None:
            await matcher.finish(msg.doi.no_lover)

        cd = plugin_config.doi_cd
        sender = self.__getCd(str(lover.qq)) 
        target = self.__getCd(str(lover.target)) 
        if sender.seconds <= cd and target.seconds <= cd:
            await matcher.finish(msg.doi.fail.format(cd - sender.seconds))

        length = random.randrange(1, 121) * random.random()
        self.__updateLenght(str(lover.qq), str(lover.target), length)
        self.__updateCd(str(lover.qq), str(lover.target))
        await matcher.finish(msg.doi.success.format(
                length = length,
                msg = "", # TODO
                second = plugin_config.doi_cd
            ))

    def __getCd(self, qq: str) -> datetime.timedelta:
        cool_down = self.cd_dao.findCoolDownByQQ(qq, CDType.doi)
        if cool_down == None:
            return datetime.timedelta(seconds=99999999)
        old = datetime.datetime.fromtimestamp(cool_down.timestampe)
        return datetime.datetime.now() - old

    def __updateLenght(self, sender: str, target: str, length: float) -> None:
        niuzi = self.niuzi_dao.findNiuziByQQ(sender)
        niuzi.length += length
        self.niuzi_dao.update(niuzi)
        niuzi = self.niuzi_dao.findNiuziByQQ(target)
        niuzi.length += length
        self.niuzi_dao.update(niuzi)


    def __updateCd(self, sender: str, target: str) -> None:
        self.cd_dao.deleteByQQ(sender, CDType.doi)
        self.cd_dao.deleteByQQ(target, CDType.doi)
        self.cd_dao.insert(CoolDown.parse_obj({
                "qq": sender,
                "timestampe": datetime.datetime.now().timestamp(),
                "type": CDType.doi
            }))

        self.cd_dao.insert(CoolDown.parse_obj({
                "qq": target,
                "timestampe": datetime.datetime.now().timestamp(),
                "type": CDType.doi
            }))


# //TODO
class ReuqestCmd(BaseSubCmd):
    pass

# //TODO
class Admin(BaseSubCmd):
    @override
    def desrcibe(self) -> str:
        return "管理员命令"

    @override
    async def execute(self, 
            matcher: Matcher, 
            stats: T_State, 
            event: GroupMessage, 
            args: str
        ) -> None:
        pass

    async def __getNiuziByAT(self, 
            matcher: Matcher, 
            stats: T_State, 
            event: GroupMessage, 
            args: str
        ) -> None:
        pass

    async def __changeLengthByAT(self, 
            matcher: Matcher, 
            stats: T_State, 
            event: GroupMessage, 
            args: str
        ) -> None:
        pass
