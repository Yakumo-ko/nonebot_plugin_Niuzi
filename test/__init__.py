from re import I
import pytest
from nonebug import App

from typing import TYPE_CHECKING, Set, Type, Dict, Any

from ..msg import Msg, setting 

if TYPE_CHECKING:
    from nonebot.plugin import Plugin

@pytest.fixture
def load_plugins(nonebug_init: None) -> Set['Plugin']:
    import nonebot

    nonebot.init(custom_config="/home/yakumo_ko/yakumo/py/nonebot/yakumo/.env.plugin_niuzi")

    config = nonebot.get_driver().config
    config.nonebot_plugin_niuzi = {
            "defalut_nick_name": "牛子",
            "change2woman": 50,
            "pk_cd": 60,
            "mysql_host":"localhost",
            "mysql_user": "root",
            "mysql_password": "18377556863",
            "mysql_database": "miraiNiuzi",
            "mysql_port": 5252
        }



    return nonebot.load_plugins("yakumo/plugin/nonebot_plugin_niuzi")


async def shouldDo(
        app: App,
        args: str, 
        expected: str, 
        qq: int) -> None:

    from nonebot.adapters.mirai2.message import MessageChain 
    from nonebot.adapters.mirai2.event import GroupMessage 
    from nonebot.adapters.mirai2.event import GroupChatInfo

    from ..command import matcher

    Message: Type[MessageChain] = MessageChain 

    sender_arg = {
            'id': qq, 
            'name': '八云幽', 
            'memberName': '八云幽',
            'permission': 'OWNER', 
            'group': {
                'id': 814926456, 
                'name': 'Minecraft拓歌群', 
                'permission': 'MEMBER'
                }
            }

    sender: GroupChatInfo = GroupChatInfo(**sender_arg)

    async with app.test_matcher(matcher) as ctx:

            bot = ctx.create_bot()
            msg: MessageChain = Message(args)
            event: GroupMessage = GroupMessage(
                    self_id=3582446171, 
                    type='GroupMessage', 
                    messageChain = msg, 
                    sender=sender , 
                    to_me=True
                    )

            ctx.receive_event(bot, event)
            ctx.should_call_send(event, expected, True)
            ctx.should_finished()

async def shouldDoWithAt(
        app: App, 
        args: str, 
        expected: str, 
        qq: int,
        target_qq: int 
        ) -> None:
    from nonebot.internal.adapter.message import Message
    from nonebot.adapters.mirai2.event import GroupMessage 
    from nonebot.adapters.mirai2.message import MessageSegment, MessageType

    from ..command import matcher

    plain = MessageSegment(type=MessageType.PLAIN)
    plain.data = {"text": args}
    at = MessageSegment(type=MessageType.AT)
    at.data = { "target": target_qq }

    tmp = {
    'self_id': 3582446171, 
    'type': 'GroupMessage', 
    'messageChain': [plain, at], 
    'source': {
        'id': 34311, 
        'time': '2023-01-21T07:48:23+00:00'
        }, 
    'sender': {
        'id': qq, 
        'name': '八云幽', 
        'memberName': '八云幽',
        'permission': 'OWNER', 
        'group': {
            'id': 814926456, 
            'name': 'Minecraft拓歌群', 
            'permission': 'MEMBER'
            }
        }, 
    'to_quote': False, 
    'quote': None, 
    'to_me': True
}

    event = GroupMessage.parse_obj(tmp)

    async with app.test_matcher(matcher) as ctx:
            bot = ctx.create_bot()

            ctx.receive_event(bot, event)
            ctx.should_call_send(event, expected, True)
            ctx.should_finished()

