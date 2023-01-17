from nonebot import on_command
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters.mirai2 import GroupMessage 
from nonebot.params import Arg, CommandArg, ArgPlainText

from service.ChangeSexService import ChangeSexService

change_woman = on_command("变女性", rule=to_me())

@change_woman.handle()
async def handle_first_receive \
        (matcher: Matcher, event: GroupMessage):
    await matcher.finish(ChangeSexService().change2Woman(event.get_user_id()))

