from nonebug import App
import pytest

from typing import TYPE_CHECKING, Set, Type, Union

import datetime

from . import load_plugins, shouldDo, shouldDoWithAt 

from ..utils.Sex import Sex
from ..entiry import CoolDown, NiuZi

from ..msg import Msg, setting 

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

class TestPk:
    
    @pytest.mark.asyncio
    async def test_no_args(self, app: App, load_plugins) -> None:
        await shouldDo(app, "/niuzi 比划比划", msg.pk.no_args, 2501390802)
        #await shouldDoWithAt(app, msg.pk.no_args, event)

    @pytest.mark.asyncio
    async def test_same(self, app: App, load_plugins) -> None:
        from ..dao import CoolDownDAO
        
        cd_dao = CoolDownDAO()
        cd = cd_dao.findCoolDownByQQ("2501390802")
        if cd != None:
            cd_dao.deleteByQQ("2501390802")

        await shouldDoWithAt(
                app, 
                "/niuzi 比划比划", 
                msg.pk.same, 
                2501390802,
                2501390802
                )

    @pytest.mark.asyncio
    async def test_no_niuzi(self, app: App, load_plugins) -> None:
        from ..dao import CoolDownDAO
        
        cd_dao = CoolDownDAO()
        cd = cd_dao.findCoolDownByQQ("2501390802")
        if cd != None:
            cd_dao.deleteByQQ("2501390802")
            cd = cd_dao.findCoolDownByQQ("2501390802")
            assert cd == None

        await shouldDoWithAt(
                app, 
                "/niuzi 比划比划", 
                msg.pk.target_no_niuzi, 
                2501390802,
                1111
                )

    @pytest.mark.asyncio
    async def test_source_in_cd(self, app: App, load_plugins) -> None:
        from ..dao import CoolDownDAO
        
        cd_dao = CoolDownDAO()
        cd = cd_dao.findCoolDownByQQ("727416332")
        if cd != None:
            cd_dao.deleteByQQ("727416332")
        
        cd_dao = CoolDownDAO()
        cd = cd_dao.findCoolDownByQQ("2501390802")
        if cd == None:
            cd_dao.insert(CoolDown.parse_obj({
                    "qq": 2501390802,
                    "timestampe": datetime.datetime.now().timestamp(),
                }))
        


        await shouldDoWithAt(
                app, 
                "/niuzi 比划比划", 
                msg.pk.source_in_cd, 
                2501390802,
                727416332
                )

        cd_dao.deleteByQQ("2501390802")

    @pytest.mark.asyncio
    async def test_target_in_cd(self, app: App, load_plugins) -> None:
        from ..dao import CoolDownDAO
        
        cd_dao = CoolDownDAO()
        cd = cd_dao.findCoolDownByQQ("2501390802")
        if cd != None:
            cd_dao.deleteByQQ("2501390802")
        
        cd_dao = CoolDownDAO()
        cd = cd_dao.findCoolDownByQQ("727416332")
        if cd == None:
            cd_dao.insert(CoolDown.parse_obj({
                    "qq": 727416332,
                    "timestampe": datetime.datetime.now().timestamp(),
                }))
        


        await shouldDoWithAt(
                app, 
                "/niuzi 比划比划", 
                msg.pk.target_in_cd, 
                2501390802,
                727416332
                )

        cd_dao.deleteByQQ("727416332")


    @pytest.mark.asyncio
    async def test_success(self, app: App, load_plugins) -> None:
        from ..dao import CoolDownDAO

        cd_dao = CoolDownDAO()
        cd_dao.deleteByQQ("2501390802")
        cd_dao.deleteByQQ("727416332")

        await shouldDoWithAt(
                app, 
                "/niuzi 比划比划", 
                "",
                2501390802,
                727416332
                )




