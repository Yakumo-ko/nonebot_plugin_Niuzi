from datetime import timedelta
from typing import Dict, Any
from nonebot.adapters.mirai2.event import GroupMessage
from nonebot.adapters import Message
from nonebot.matcher import Matcher
from nonebot.params import CommandArg, Received
from nonebot.permission import Permission
from nonebot.plugin import on_command
from nonebot.typing import T_State
from .subcommand import * 


subcmds: Dict[str, Any] = {
        "变女性": ChangeSexCmd,
        "领养牛子": GetCmd,
        "我的牛子": InfoCmd,
        "改牛子名": NameCmd,
        "比划比划": PKCmd,
        "我要分手": LeaveCmd,
        "搞对象": LoveRequestCmd,
        "贴贴": DoiCmd,
        "我的对象": LoverInfoCmd
        }


matcher = on_command("niuzi", expire_time=timedelta(seconds=360))

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
            await cmd.execute(matcher, stats, event, args)

    await listSubCmd(matcher)

@matcher.permission_updater
async def checkPerm(matcher: Matcher, stats: T_State) -> Permission:
    assert stats.get('subcmd') != None
    async def _(event: GroupMessage):
        return await stats.get('subcmd').checkPerm(matcher, stats, event)
    
    return Permission(_)
            
@matcher.receive()
async def request(matcher: Matcher, stats: T_State, event: GroupMessage = Received()) :
    await stats.get('subcmd').request(matcher, stats, event)


async def listSubCmd(matcher: Matcher) -> None:
    usage = "用法: /niuzi <subcmd>\n"

    for item in subcmds.items():
        cmd: BaseSubCmd = item[1](item[0])
        usage += f"{cmd.useage()}: {cmd.desrcibe()}\n"
    
    await matcher.finish()



        


    

