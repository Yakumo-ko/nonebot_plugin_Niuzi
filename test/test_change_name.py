from nonebug import App
import pytest

from typing import TYPE_CHECKING, Set, Type, Union

from . import load_plugins, shouldDo 

from ..enum import Sex
from ..entiry import NiuZi

from ..msg import Msg, setting 

msg = Msg(**setting) 

class TestChangeName:

    @pytest.mark.asyncio
    async def test_name_to_long(self, app: App, load_plugins) -> None:
        await shouldDo(app, "/niuzi 改牛子名 niuzidsgfdgdfgdfg", 
                   msg.name.name_too_long, 2501390802)


    @pytest.mark.asyncio
    async def test_success(self, app: App, load_plugins) -> None:
        from ..dao import NiuziDAO
        from ..entiry import NiuZi

        niuzi_dao = NiuziDAO()

        await shouldDo(app, "/niuzi 改牛子名 niuzi n", msg.name.success, 2501390802)
        niuzi: Union[NiuZi, None] = niuzi_dao.findNiuziByQQ("2501390802")
        assert niuzi.name == "niuzi n", "The name should be changed"

        await shouldDo(app, "/niuzi 改牛子名 牛子", msg.name.success, 2501390802)
