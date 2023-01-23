from datetime import timedelta
from typing import Type, Dict, Any
from async_asgi_testclient.testing import receive
from nonebot import get_driver
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
        }


matcher = on_command("niuzi", rule=to_me(), expire_time=timedelta(seconds=360))

@matcher.permission_updater
async def checkPerm(matcher: Matcher, stats: T_State, event: GroupMessage) -> Permission:
    async def _():
        if stats.get("target_qq") == event.get_user_id():
            return True
        return False

    return Permission(_)

@matcher.handle()
async def info (matchar: Matcher, event: GroupMessage, message: Message = CommandArg()) -> None:
    args = message.extract_plain_text()

    if len(args) == 0:
        await matchar.finish("参数捏")

    for item in subcmds.items():
        if args.startswith(item[0]) :
            args = args.replace(item[0], "")
            cmd_list = args.split(' ') 
            cmd_list.remove('')

            cmd: BaseSubCmd = item[1](item[0])
            res: str = await cmd.execute(cmd_list, event)
            await matchar.finish(res)
            
@matcher.receive()
async def request(matcher: Matcher, event = Received(), message: Message = CommandArg()):
    args = message.extract_plain_text()
    

