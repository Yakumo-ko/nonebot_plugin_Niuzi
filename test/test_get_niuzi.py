from nonebug import App
import pytest

from typing import TYPE_CHECKING, Set, Type, Union

from . import load_plugins, shouldDo 

from ..enum import Sex
from ..entiry import NiuZi

from ..msg import Msg, setting 

msg = Msg(**setting) 

class TestGetNiuzi:

    @pytest.mark.asyncio
    async def test_has_niuzi(self, app: App, load_plugins) -> None:
        qq = 2501390802
        
        await shouldDo(
                    app, 
                    "/niuzi 领养牛子", 
                    msg.get.has_niuzi,
                    qq
                ) 


    @pytest.mark.asyncio
    async def test_success(self, app: App, load_plugins) -> None:
        from ..dao import NiuziDAO
        from ..entiry import NiuZi

        niuzi_dao = NiuziDAO()

        await shouldDo(app, "/niuzi 领养牛子", msg.get.success, 250139082)
        niuzi: Union[NiuZi, None] = niuzi_dao.findNiuziByQQ("250139082")
        assert niuzi!= None

        await shouldDo(app, "/niuzi 领养牛子", msg.get.has_niuzi, 250139082)
        niuzi_dao.delete(niuzi)
        niuzi: Union[NiuZi, None] = niuzi_dao.findNiuziByQQ("250139082")
        assert niuzi == None




