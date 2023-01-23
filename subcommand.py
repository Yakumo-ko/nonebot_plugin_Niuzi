
from abc import ABC, abstractmethod
from typing_extensions import override

from nonebot import get_driver, get_bot

from nonebot.adapters.mirai2.event import GroupMessage
from nonebot.adapters import Message
from nonebot.adapters.mirai2.message import MessageSegment, MessageType, MessageChain
from nonebot.typing import T_State

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
        self.hasRequest = False
        self.cmd_prefix = cmd_prefix

        self.niuzi_dao = NiuziDAO()
        self.lovers_dao = LoversDAO()
        self.cd_dao = CoolDownDAO()

    def desrcibe(self) -> str:
        return "null"
    
    @abstractmethod
    def useage(self) -> str:
        pass

    @abstractmethod
    async def execute(
                self, 
                stats: T_State, 
                args: list, 
                event: GroupMessage
            ) -> Any:
        pass

class InfoCmd(BaseSubCmd):

    @override
    def desrcibe(self) -> str:
        return "查看你牛子"

    @override
    def useage(self) -> str:
        return "女性"

    @override
    async def execute(self, 
                stats: T_State,
                args: list, 
                event: GroupMessage
            ) -> str:
        return self.getNiuziInfo(
                    event.get_user_id(),
                    qq_name = event.sender.name
                )

    def __toChinese(self, sex: int) -> str:
        return '女' if sex == Sex.FEMALE else '男'

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
                sex =  self.__toChinese(niuzi.sex),
                length = niuzi.length,
                qq_name = qq_name
                )

        return  res

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
    def useage(self) -> str:
        return self.cmd_prefix

    def __change2Woman(self, qq: str, length: int = 50) -> str:
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

    def __change2Man(self, qq: str) -> str:
        assert False


    @override
    async def execute(self, 
                stats: T_State,
                args: list, 
                event: GroupMessage
            ) -> str:
        return self.__change2Woman(event.get_user_id())

class GetCmd(BaseSubCmd):
    
    @override
    def useage(self) -> str:
        return self.cmd_prefix

    @override
    async def execute(self, 
                stats: T_State,
                args: list, 
                event: GroupMessage
            ) -> str:
        return self.getNewNiuzi(
                    event.get_user_id(), 
                    plugin_config.defalut_nick_name
                )
        
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

class NameCmd(BaseSubCmd):

    @override
    def desrcibe(self) -> str:
        return "改你牛子的名字, 支持空格, 最长10个字"

    @override
    def useage(self) -> str:
        return self.cmd_prefix + " <name>"

    @override
    async def execute(self, 
                stats: T_State,
                args: list, 
                event: GroupMessage
            ) -> str:
        name = " ".join(args)
        return self.changeName(event.get_user_id(), name) 

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

class PKCmd(BaseSubCmd):

    def __init__(self, cmd_prefix: str) -> None:
        super().__init__(cmd_prefix)
        self.events = [
                    PKLost,
                    PKWin,
                    PKAllLost
                ]

    @override
    def desrcibe(self) -> str:
        return "比划一下, 赢加长度输减长度, 断掉双方都减长度"

    @override
    def useage(self) -> str:
        return self.cmd_prefix + " <@target>"

    @override
    async def execute(self, 
                stats: T_State,
                args: list, 
                event: GroupMessage
            ) -> str:
        for seg in event.get_message().export():
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
                return self.pk(
                    event.get_user_id(),
                    event.sender.name,
                    str(seg['target']),
                    "none",
                    plugin_config.pk_cd
                        )

        return self.pk(
                    event.get_user_id(), 
                    event.sender.name, 
                    None, 
                    None, 
                    plugin_config.pk_cd
                )

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


class TopCmd(BaseSubCmd):
    @override
    def desrcibe(self) -> str:
        return "查看牛子排行榜"

    @override
    def useage(self) -> str:
        return "none"

    @override
    async def execute(self, 
                stats: T_State,
                args: list, 
                event: GroupMessage
            ) -> MessageChain:
        res: Union[List[str], None] = self.getAll() 

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
        self.hasRequest = True

    @override
    def desrcibe(self) -> str:
        return "和你的对象分手"

    @override
    def useage(self) -> str:
        return "none"

    @override
    async def execute(self, stats: T_State, args: list, event: GroupMessage) -> str:
       target_qq = self.getLover(event.get_user_id())
       if target_qq == None:
           return msg.no_lover

       stats.update({
           "qq": event.get_user_id(),
           "target_qq": target_qq,
           "request": LeaveCmd
           })

       return self.leaveRequest(event.get_user_id())

    async def request(self, stats: T_State, event : GroupMessage) -> str:
       if event.get_plaintext() == "同意":
           self.leaveAgree(stats.get("qq"))
           return msg.leave.request.agree
       return msg.leave.request.disagree
        

    def getLover(self, qq: str) -> Union[str, None]:
        lover: Union[Lovers, None] = self.lovers_dao.findloversByQQ(qq)
        return lover.target if lover != None else None

    def leaveRequest(self, qq: str) -> str:
        lover: Lovers = self.lovers_dao.findloversByQQ(qq)

        assert lover != None

        return msg.leave.request.send.format(
                target = lover.target,
                sender = lover.qq
                )

    def leaveAgree(self, qq: str) -> None:
        self.lovers_dao.deleteByQQ(qq)

     
    def getInfo(self, qq: str) -> str:
        niuzi = self.niuzi_dao.findNiuziByQQ(qq)

        return msg.status.format(
                    qq = qq,
                    qq_name = "",
                    name = niuzi.name,
                    sex = niuzi.sex,
                    length = niuzi.length
                )

    
