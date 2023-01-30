from nonebug import App
import pytest

from typing import TYPE_CHECKING, Set, Type, Union

import datetime

from . import load_plugins, shouldDo, shouldDoWithAt 

from ..enum import Sex
from ..entiry import * 

from ..msg import Lover, Msg, setting 

msg = Msg(**setting) 

event = {
    'self_id': 3582446171, 
    'type': 'GroupMessage', 
    'messageChain': [
            {'type': 'Plain', 
            'data': {
                'text': '比划比划 '
                }
            }, 
            {'type': 'At', 
             'data': {
                 'target': 727416332, 
                 'display': ''
                 }
             }
        ], 
    'source': {
        'id': 34311, 
        'time': '2023-01-21T07:48:23+00:00'
        }, 
    'sender': {
        'id': 2501390802, 
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
    'to_me': False
}

class TestLeave:
    @pytest.mark.asyncio
    async def test_no_args(self, app: App, load_plugins) -> None:
        from ..dao import LoversDAO
        qq = 123
       
        lovers_dao = LoversDAO()
        assert lovers_dao.findloversByQQ(str(qq)) == None
        
        await shouldDo(app, "/niuzi 搞对象", msg.no_lover, qq)


    @pytest.mark.asyncio
    async def test_success(self, app: App, load_plugins) -> None:
        from ..dao import LoversDAO
        from nonebot.adapters.mirai2.message import MessageChain 
        from nonebot.adapters.mirai2.event import GroupMessage 
        from nonebot.adapters.mirai2.event import GroupChatInfo

        from ..command import matcher

        Message: Type[MessageChain] = MessageChain 
        
        qq = 2501390802
        target_qq = 2501390800
        lovers_dao = LoversDAO()
        if lovers_dao.findloversByQQ(str(qq)) == None:
            lovers_dao.insert(Lovers.parse_obj({
                "qq": qq,
                "target": target_qq 
                }))

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

        sender_arg2 = {
                'id': target_qq, 
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
        sender2: GroupChatInfo = GroupChatInfo(**sender_arg2)

        async with app.test_matcher(matcher) as ctx:

                bot = ctx.create_bot()
                m: MessageChain = Message("/niuzi 我要分手")
                event: GroupMessage = GroupMessage(
                        self_id=3582446171, 
                        type='GroupMessage', 
                        messageChain = m, 
                        sender = sender, 
                        to_me = True
                        )
                msg2: MessageChain = Message("同意")
                event2: GroupMessage = GroupMessage(
                        self_id = 3582446171, 
                        type = 'GroupMessage', 
                        messageChain = msg2.append(MessageSegment.at(2501390802)), 
                        sender = sender, 
                        to_me = True
                        )

                res = Message([MessageSegment.at(2501390800)])
                res.append(MessageSegment.plain(msg.leave.request.send.format(
                        target = 2501390800,
                        sender = 2501390802
                    )))
                
                ctx.receive_event(bot, event)
                ctx.should_call_send(event, res, True)

                event2.sender.id = 2501390800
                ctx.receive_event(bot, event2)
                
                res = Message(msg.leave.request.agree)
                ctx.should_call_send(event2, res, True)
                ctx.should_finished()

        assert lovers_dao.findloversByQQ(str(qq)) == None
