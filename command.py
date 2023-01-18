from typing import Type, Dict, Any
from nonebot import get_driver
from nonebot.adapters.mirai2.event import GroupMessage
from nonebot.adapters import Message
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.plugin import on_command
from nonebot.rule import to_me
from .subcommand import * 


subcmds: Dict[str, Any] = {
        "变女性": ChangeSexCmd,
        "领养牛子": GetCmd,
        "我的牛子": InfoCmd,
        }


matcher = on_command("niuzi", rule=to_me())

@matcher.handle()
async def info (matchar: Matcher, event: GroupMessage, message: Message = CommandArg()) -> None:
    args = message.extract_plain_text()

    if len(args) == 0:
        await matchar.finish("参数捏")

    for item in subcmds.items():
        if args.startswith(item[0]) :
            cmd_list = args.split(' ') 

            if len(cmd_list) == 0:
                cmd_list.append(args)

            cmd: BaseSubCmd = item[1](item[0])
            res: str = cmd.execute(cmd_list, event)
            await matchar.finish(res)
            
