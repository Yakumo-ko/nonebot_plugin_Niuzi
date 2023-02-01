
from abc import ABC, abstractmethod
from typing_extensions import override

from nonebot import get_driver, get_bot
from nonebot.adapters import Message 

from nonebot.adapters.mirai2.event import GroupMessage
from nonebot.adapters.mirai2.message import MessageSegment, MessageType
from nonebot.adapters.mirai2.permission import GROUP_ADMIN, GROUP_OWNER
from nonebot.typing import T_State
from nonebot.matcher import Matcher

import datetime
import re

from .utils import checkCondition, getNickName, hasAT, member_profile, toChinese, toNode
from .config import Config 
from .msg import Msg, setting 
from .entiry import *
from .dao import * 
from .event import *
from .enum import Sex, CDType

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
        niuzi = self.niuzi_dao.findNiuziByQQ(event.get_user_id())
        await checkCondition(matcher, niuzi==None, msg.info.niuzi_info)

        await matcher.finish(msg.info.niuzi_info.format(
                        qq = niuzi.qq,
                        name = niuzi.name,
                        sex =  toChinese(niuzi.sex),
                        length = niuzi.length,
                        qq_name = event.sender.name 
                    )
                )

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
        await checkCondition(matcher, niuzi==None, msg.change_sex.no_niuzi)

        await checkCondition(matcher, niuzi.sex==Sex.FEMALE, msg.change_sex.already_woman)

        self.__toWoman(niuzi)
        await matcher.finish(
                msg.change_sex.success.format(plugin_config.change2woman)
            )

    def __toWoman(self, niuzi: NiuZi) -> None:
        niuzi.length -= plugin_config.change2woman 
        niuzi.sex = Sex.FEMALE
        self.niuzi_dao.update(niuzi) 


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
        await matcher.finish(msg.get.success.format(subcmd=self.useage()))

class NameCmd(BaseSubCmd):
    @override
    def desrcibe(self) -> str:
        return "改你牛子的名字, 支持空格, 最长10个字"

    @override
    def useage(self) -> str:
        return self.cmd_prefix + " [name]"

    @override
    async def execute(self, 
                matcher: Matcher,
                stats: T_State, 
                event: GroupMessage,
                args: str
            ) -> None:
        niuzi = self.niuzi_dao.findNiuziByQQ(event.get_user_id())
        await checkCondition(matcher, niuzi == None, msg.no_niuzi)

        await checkCondition(matcher, len(args) == 0, msg.no_arg)
        await checkCondition(matcher, len(args) > 10, msg.name.name_too_long)

        niuzi.name = args 
        self.niuzi_dao.update(niuzi)
        await matcher.finish(msg.name.success)

class PKCmd(BaseSubCmd):
    @override
    def desrcibe(self) -> str:
        return "比划一下, 赢加长度输减长度, 断掉双方都减长度"

    @override
    def useage(self) -> str:
        return self.cmd_prefix + " [@target]"

    @override
    async def execute(self, 
                matcher: Matcher,
                stats: T_State, 
                event: GroupMessage,
                args: str
            ) -> None:
        sender = event.get_user_id()
        niuzi = self.niuzi_dao.findNiuziByQQ(sender)
        target = hasAT(event) 
        await checkCondition(matcher, niuzi==None, msg.no_niuzi)
        await checkCondition(matcher, target==None, msg.pk.no_args)
        await checkCondition(matcher, sender==target, msg.pk.same)

        time: datetime.timedelta = self.cd_dao.getCd(sender, CDType.pk)
        await checkCondition(matcher, time.seconds < plugin_config.pk_cd, 
                    msg.pk.source_in_cd.format(
                        plugin_config.pk_cd - time.seconds
                        )
                    )

        target_niuzi = self.niuzi_dao.findNiuziByQQ(target)
        await checkCondition(matcher,target_niuzi==None,msg.pk.target_no_niuzi)

        time: datetime.timedelta = self.cd_dao.getCd(target, CDType.pk)
        await checkCondition(matcher, 
                time.seconds < plugin_config.pk_cd, 
                msg.pk.target_in_cd.format(
                        plugin_config.pk_cd - time.seconds
                    )
                )

        self.cd_dao.updateCd(sender, target, CDType.pk)

        pk_event = randomPkevent()
        group = event.sender.group.id
        await matcher.finish(
                pk_event().execute(
                        niuzi, 
                        event.sender.name,
                        target_niuzi, 
                        await getNickName(group, target_niuzi.qq),
                    )         
            )

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
        group = event.sender.group.id
        res: Union[List[str], None] = await self.getAll(group) 
        await checkCondition(matcher, res == None, "太可惜了, 本群还没有人领养过牛子")

        id = int(get_bot().self_id)
        nickname = await getNickName(group, id)
        await matcher.finish(MessageSegment(
                    type=MessageType.FORWARD,
                    nodeList=[toNode(msg, id, nickname) for msg in res]
                )
            )

    async def getAll(self, group: int) -> Union[List[str], None]:
        niuzi_list = self.niuzi_dao.getAll()
        if niuzi_list == None:
            return None

        niuzi_list.sort(key=lambda a: a.length, reverse=True)
        
        res = []
        for i in range(0, len(niuzi_list)):
            niuzi = niuzi_list[i]
            nickname= await getNickName(group, niuzi.qq)
            if nickname == "none":
                continue
            tmp = msg.info.niuzi_info.format(
                    qq = niuzi.qq,
                    name = niuzi.name,
                    sex =  toChinese(niuzi.sex),
                    length = niuzi.length,
                    qq_name = nickname 
                )
              
            res.append(f"{i}: "+ tmp)

        return res

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
        sender = int(event.get_user_id())
        niuzi = self.niuzi_dao.findNiuziByQQ(sender)
        await checkCondition(matcher, niuzi==None, msg.info.niuzi_info)

        lover = self.lovers_dao.findloversByQQ(sender)
        await checkCondition(matcher, lover==None, msg.no_lover)

        group = event.sender.group.id
        target = lover.getOther(sender)
        target_nickname= await getNickName(group, target)
        await checkCondition(matcher, target_nickname=="none", "你的对象不在这个群")

        await matcher.send(Message.template("{at}{msg}").format(
            at = MessageSegment.at(target),
            msg = MessageSegment.plain(msg.leave.request.send.format(
                        sender = event.sender.name,
                        target = target_nickname,
                        subcmd = "同意/不同意 [@target]"
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
        nickname = event.sender.name
        if event.get_plaintext().strip() == "同意":
            self.lovers_dao.deleteByQQ(event.sender.id)
            await matcher.finish(msg.leave.request.agree.format(nickname))
        await matcher.finish(msg.leave.request.disagree.format(nickname))

    @override
    async def checkPerm(self, matcher: Matcher, stats: T_State, event: GroupMessage
            ) -> bool:
        at_qq = hasAT(event) 
        if at_qq == None:
            return False 

        sender = event.get_user_id()
        target = stats.get('target')
        return target == sender and at_qq == stats.get("sender")

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
        sender = int(event.get_user_id())
        niuzi = self.niuzi_dao.findNiuziByQQ(sender)
        await checkCondition(matcher, niuzi==None, msg.info.niuzi_info)
        lover = self.lovers_dao.findloversByQQ(sender)
        if lover == None:
            await matcher.finish(msg.no_lover)

        target = lover.getOther(sender)
        niuzi = self.niuzi_dao.findNiuziByQQ(target)
        target_nickname= await getNickName(event.sender.group.id, target)
        await checkCondition(matcher, target_nickname=="none", "你的对象不在这个群")
        await matcher.finish(msg.status.format(
                    qq = niuzi.qq,
                    qq_name = target_nickname,
                    name = niuzi.name,
                    sex = toChinese(niuzi.sex),
                    length = niuzi.length
            ))
        
class LoveRequestCmd(BaseSubCmd):
    @override
    def desrcibe(self) -> str:
        return "和别人搞对象"

    @override
    def useage(self) -> str:
        return self.cmd_prefix + " [@target]"

    async def execute(self, 
                matcher: Matcher, 
                stats: T_State, 
                event: GroupMessage, 
                args: str
            ) -> None:
        sender = event.get_user_id()
        niuzi = self.niuzi_dao.findNiuziByQQ(sender)
        await checkCondition(matcher, niuzi==None, msg.info.niuzi_info)
        if self.lovers_dao.findloversByQQ(sender) != None:
            await matcher.finish(msg.lover.get.has_lover)

        target = hasAT(event)
        await checkCondition(matcher, target==None, msg.lover.get.has_lover)
        # await checkCondition(matcher, target==sender, msg.lover.get.self)

        if self.lovers_dao.findloversByQQ(target) != None:
            await matcher.finish(msg.lover.get.fail)

        if self.niuzi_dao.findNiuziByQQ(target) == None:
            await matcher.finish(msg.lover.get.target_no_niuzi)
        
        await matcher.send(Message.template("{at}{msg}").format(
            at = MessageSegment.at(int(target)),
            msg = MessageSegment.plain(msg.lover.request.send.format(
                        target = target,
                        sender = sender,
                        subcmd = "同意/不同意 [@target]"
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
        nickname = event.sender.name
        if event.get_plaintext().strip() == "同意":
            assert stats.get('sender') != None
            self.lovers_dao.insert(
                    Lovers(
                        qq=int(stats.get('sender')),
                        target=int(stats.get('target')),
                        )
                )
            await matcher.finish(msg.lover.request.agree.format(nickname))
        await matcher.finish(msg.lover.request.disagree.format(nickname))

    @override
    async def checkPerm(self, matcher: Matcher, stats: T_State, event: GroupMessage
            ) -> bool:
        at_qq = hasAT(event) 
        if at_qq == None:
            return False

        target = stats.get("target")
        sender = event.get_user_id()
        return target == sender and at_qq == stats.get('sender')

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
        niuzi = self.niuzi_dao.findNiuziByQQ(event.get_user_id())
        await checkCondition(matcher, niuzi==None, msg.info.niuzi_info)
        lover = self.lovers_dao.findloversByQQ(event.get_user_id())
        await checkCondition(matcher, lover==None, msg.doi.no_lover)

        qq = lover.getOther(int(event.get_user_id()))
        group = event.sender.group.id
        await checkCondition(matcher, (await member_profile(group, qq))==None, "你的对象不在这个群")

        cd = plugin_config.doi_cd
        sender = self.cd_dao.getCd(lover.qq, CDType.doi) 
        target = self.cd_dao.getCd(lover.target, CDType.doi) 
        if sender.seconds <= cd and target.seconds <= cd:
            await matcher.finish(msg.doi.fail.format(cd - sender.seconds))

        length = random.randrange(1, 121) * random.random()
        self.__updateLenght(lover.qq, lover.target, length)
        self.cd_dao.updateCd(lover.qq, lover.target, CDType.doi)
        await matcher.finish(msg.doi.success.format(
                length = length,
                msg = "", # TODO
                second = plugin_config.doi_cd
            ))

    def __updateLenght(self, 
                sender: Union[str, int], 
                target: Union[str, int],
                length: float
            ) -> None:
        niuzi = self.niuzi_dao.findNiuziByQQ(sender)
        niuzi.length += length
        self.niuzi_dao.update(niuzi)
        niuzi = self.niuzi_dao.findNiuziByQQ(target)
        niuzi.length += length
        self.niuzi_dao.update(niuzi)

# //TODO
class ReuqestCmd(BaseSubCmd):
    pass

class Admin(BaseSubCmd):
    @override
    def desrcibe(self) -> str:
        return "管理员命令, 仅允许群主和管理员"

    @override
    def useage(self) -> str:
        return self.cmd_prefix + " [subcmd]\n subcmd:\n  get [@target]\n  chlen [len] [@target]"

    @override
    async def execute(self, 
            matcher: Matcher, 
            stats: T_State, 
            event: GroupMessage, 
            args: str
        ) -> None:
        if not (await GROUP_OWNER(get_bot(), event) or await GROUP_ADMIN(get_bot(), event)):
            await matcher.finish("你没有权限执行该命令")

        if args.startswith("get"):
            await self.__getNiuziByAT(
                        matcher, 
                        stats, 
                        event, 
                        args.replace("get", "").strip()
                )
        elif args.startswith("chlen"):
            await self.__changeLengthByAT(
                        matcher, 
                        stats, 
                        event, 
                        args.replace("chlen", "").strip()
                )
        else:
            await matcher.finish(self.useage())

        
    async def __getNiuziByAT(self, 
            matcher: Matcher, 
            stats: T_State, 
            event: GroupMessage, 
            args: str
        ) -> None:
        at = hasAT(event)
        if at == None:
            await matcher.finish("[@target]?")
        await InfoCmd("").execute(matcher, stats, event, args)
        
    async def __changeLengthByAT(self, 
            matcher: Matcher, 
            stats: T_State, 
            event: GroupMessage, 
            args: str
        ) -> None:
        at = hasAT(event)
        await checkCondition(matcher, at==None, "[@target]?")
        niuzi = self.niuzi_dao.findNiuziByQQ(
                    event.get_user_id()
                )

        await checkCondition(matcher, niuzi==None, msg.info.no_niuzi)
        await checkCondition(matcher, not self.__is_num(args), "len must be digit")
        niuzi.length = float(args)
        self.niuzi_dao.update(niuzi)
        await matcher.finish("success")
    
    def __is_num(self, num: str) -> bool:
        return re.match("-|[\d]+\.[\d]{1,}", num) != None
