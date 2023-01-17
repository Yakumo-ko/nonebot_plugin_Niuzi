from nonebot import get_driver
from nonebot.adapters.mirai2.event import GroupMessage
from nonebot.adapters import Message
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.plugin import on_command
from nonebot.rule import to_me
from .subcommand import ChangeSex, InfoCmd


matcher = on_command("niuzi", rule=to_me())

@matcher.handle()
async def info (matchar: Matcher, event: GroupMessage, message: Message = CommandArg()) -> None:
    args = message.extract_plain_text()

    if len(args) == 0:
        await matchar.finish("参数捏")

    cmd_list = args.split(' ') 
    if len(cmd_list) == 0:
        cmd_list.append(args)

    if cmd_list[0] == "变女性": 
        await matchar.finish(ChangeSex().change2Woman(event.get_user_id()))

