from typing import Dict, Any
from nonebot import get_bot
from nonebot.adapters.mirai2.event import GroupMessage
from nonebot.adapters import Message 
from nonebot.adapters.mirai2.message import MessageSegment, MessageType
from nonebot.matcher import Matcher
from nonebot.params import CommandArg, Received
from nonebot.permission import Permission
from nonebot.plugin import on_command
from nonebot.typing import T_State

from .utils import toNode
from .subcommand import ( ChangeSexCmd, GetCmd, NameCmd, 
            InfoCmd, PKCmd, LeaveCmd, LoveRequestCmd, 
            DoiCmd, LoverInfoCmd, Admin, BaseSubCmd, TopCmd
        ) 


subcmds: Dict[str, Any] = {
        "变女性": ChangeSexCmd,
        "牛子榜": TopCmd,
        "领养牛子": GetCmd,
        "我的牛子": InfoCmd,
        "改牛子名": NameCmd,
        "比划比划": PKCmd,
        "我要分手": LeaveCmd,
        "搞对象": LoveRequestCmd,
        "贴贴": DoiCmd,
        "我的对象": LoverInfoCmd,
        "admin": Admin
        }


matcher = on_command("niuzi")

@matcher.handle()
async def info (
        matcher: Matcher, 
        event: GroupMessage, 
        stats: T_State,
        message: Message = CommandArg()
        ) -> None:
    text = message.extract_plain_text()

    args = text.split(' ')

    for item in subcmds.items():
        if args[0] == item[0] :
            args = text.replace(args[0], '').strip()
            cmd: BaseSubCmd = item[1](item[0])
            try:
                await cmd.execute(matcher, stats, event, args)
            except Exception as e:
                print(e.with_traceback(None))
                await matcher.finish("未知错误, 该命令不可用")

    await listSubCmd(matcher, event.sender.group.id)

# TODO: set a vaild datetime for session
@matcher.permission_updater
async def checkPerm(matcher: Matcher, stats: T_State) -> Permission:
    assert stats.get('subcmd') != None
    async def _(event: GroupMessage):
        return await stats.get('subcmd').checkPerm(matcher, stats, event)
    
    return Permission(_)
            
@matcher.receive()
async def request(matcher: Matcher, stats: T_State, event: GroupMessage = Received()) :
    await stats.get('subcmd').request(matcher, stats, event)

async def listSubCmd(matcher: Matcher, group: int) -> None:
    usage = "用法: /niuzi [subcmd]\n下边是列出的subcmd"
    
    # [] 用来代替<>  带有<>两字符的消息发不出去, 我也不知道为啥
    tmp = [usage, "注: []是必选项"]
    for item in subcmds.items():
        cmd: BaseSubCmd = item[1](item[0])
        tmp.append(f"{cmd.useage()}: {cmd.desrcibe()}")

    # bot_pro_file不可用 
    id = int(get_bot().self_id)
    name= await get_bot().member_profile(member_id=id, target=group)
    await matcher.finish(MessageSegment(
                type=MessageType.FORWARD,
                nodeList=[toNode(i, id, name['nickname']) for i in tmp ]
            )
        )
    


    

