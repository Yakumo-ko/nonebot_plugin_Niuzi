from nonebug import App
import pytest

from typing import TYPE_CHECKING, Set, Type, Union

from . import load_plugins, shouldDo 

from ..utils.Sex import Sex
from ..entiry import NiuZi

from ..msg import Msg, setting 

msg = Msg(**setting) 

class TestInfo:

    @pytest.mark.asyncio
    async def test_no_niuzi(self, app: App, load_plugins) -> None:
        qq = 250139082
        await shouldDo(
                app,
                "/niuzi 我的牛子", 
                msg.info.no_niuzi,
                qq
                )

    @pytest.mark.asyncio
    async def test_has_niuzi(self, app: App, load_plugins) -> None:
        from ..dao import NiuziDAO
        from ..entiry import NiuZi

        niuzi_dao = NiuziDAO()


        niuzi: Union[NiuZi, None] = niuzi_dao.findNiuziByQQ("2501390802")
        expected = msg.info.niuzi_info.format(
                    qq = niuzi.qq,
                    name = niuzi.name,
                    sex =  '女' if niuzi.sex == Sex.FEMALE else '男',
                    length = niuzi.length,
                    qq_name = "八云幽" 
                    )
        await shouldDo(app, "/niuzi 我的牛子", expected, 2501390802)
                            
