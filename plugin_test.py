import pytest
from nonebug import App

from typing import TYPE_CHECKING, Set, Type, Union

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
            "host":"localhost",
            "user": "root",
            "password": "18377556863",
            "database": "miraiNiuzi",
            "port": 5252
        }



    return nonebot.load_plugins("yakumo/plugin/nonebot_plugin_niuzi")


@pytest.mark.asyncio
async def test_niuzi(app: App, load_plugins) -> None:
    from .msg import Msg, setting 

    msg = Msg(**setting) 

    from nonebot.adapters.mirai2.message import MessageChain 
    from nonebot.adapters.mirai2.event import GroupMessage 
    from nonebot.adapters.mirai2.event import GroupChatInfo

    from .command import matcher
    from .entiry import NiuZi
    from .utils.Sex import Sex
    from .dao import NiuziDAO

    Message: Type[MessageChain] = MessageChain 


    async def testCase(args: str, expected: str, qq: int) -> None:
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
            event: GroupMessage = GroupMessage(self_id=3582446171, type='GroupMessage', messageChain = msg, sender=sender , to_me=True)

            ctx.receive_event(bot, event)
            ctx.should_call_send(event, expected, True)
            ctx.should_finished()

    niuzi_dao =  NiuziDAO()

    # for not args
    await testCase("/niuzi", "参数捏", 2501390802)

    # for change sex
    await testCase("/niuzi 变女性", msg.change_sex.no_niuzi, 201390802)
    niuzi = niuzi_dao.findNiuziByQQ(2501390802)
    assert niuzi != None

    await testCase("/niuzi 变女性", msg.change_sex.already_woman, 2501390802)

    # for get new niuzi
    await testCase("/niuzi 领养牛子", msg.get.has_niuzi, 2501390802)
    await testCase("/niuzi 领养牛子", msg.get.success, 250139082)
    niuzi: Union[NiuZi, None] = niuzi_dao.findNiuziByQQ("250139082")
    assert niuzi!= None

    await testCase("/niuzi 领养牛子", msg.get.has_niuzi, 250139082)
    niuzi_dao.delete(niuzi)
    niuzi: Union[NiuZi, None] = niuzi_dao.findNiuziByQQ("250139082")
    assert niuzi == None

    # for get niuzi info
    await testCase("/niuzi 我的牛子", msg.info.no_niuzi, 250139082)

    niuzi: Union[NiuZi, None] = niuzi_dao.findNiuziByQQ("2501390802")
    expected = msg.info.niuzi_info.format(
                qq = niuzi.qq,
                name = niuzi.name,
                sex =  '女' if niuzi.sex == Sex.FEMALE else '男',
                length = niuzi.length,
                qq_name = "八云幽" 

            )
    await testCase("/niuzi 我的牛子", expected, 2501390802)
    await testCase("/niuzi 我的牛子", msg.info.no_niuzi, 222)

    " for change name for niuzi"
    await testCase("/niuzi 改牛子名", msg.no_arg, 222)
    await testCase("/niuzi 改牛子名 niuzidsgfdgdfgdfg", 
                   msg.name.name_too_long, 2501390802)
    await testCase("/niuzi 改牛子名 niuzi n", msg.name.success, 2501390802)
    niuzi: Union[NiuZi, None] = niuzi_dao.findNiuziByQQ("2501390802")
    assert niuzi.name == "niuzi n"
    await testCase("/niuzi 改牛子名 牛子", msg.name.success, 2501390802)
    


        
    



