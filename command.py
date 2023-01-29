from datetime import timedelta
from typing import Dict, Any
from nonebot.adapters.mirai2.event import GroupMessage
from nonebot.adapters import Message
from nonebot.matcher import Matcher
from nonebot.params import CommandArg, Received
from nonebot.permission import Permission
from nonebot.plugin import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from .subcommand import * 


subcmds: Dict[str, Any] = {
        "变女性": ChangeSexCmd,
        "领养牛子": GetCmd,
        "我的牛子": InfoCmd,
        "改牛子名": NameCmd,
        "比划比划": PKCmd,
        "我要分手": LeaveCmd,
        "搞对象": LoveRequestCmd
        }


matcher = on_command("niuzi", rule=to_me(), expire_time=timedelta(seconds=360))

@matcher.handle()
async def info (
        matcher: Matcher, 
        event: GroupMessage, 
        stats: T_State,
        message: Message = CommandArg()
        ) -> None:
    text = message.extract_plain_text()

    if len(text) == 0:
        await matcher.finish("参数捏")
    args = text.split(' ')

    for item in subcmds.items():
        if args[0] == item[0] :
            args = text.replace(args[0], '').strip()
            cmd: BaseSubCmd = item[1](item[0])
            await cmd.execute(matcher, stats, event, args)

@matcher.permission_updater
async def checkPerm(matcher: Matcher, stats: T_State) -> Permission:
    assert stats.get('subcmd') != None
    async def _(event: GroupMessage):
        return await stats.get('subcmd').checkPerm(matcher, stats, event)
    
    return Permission(_)
            
@matcher.receive()
async def request(matcher: Matcher, stats: T_State, event: GroupMessage = Received()) :
    await stats.get('subcmd').request(matcher, stats, event)


    

        


    

