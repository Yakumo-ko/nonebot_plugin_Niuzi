import pytest
from nonebug import App

from . import load_plugins, shouldDo

from ..msg import Msg, setting 
from ..enum import Sex

msg = Msg(**setting) 

class TestChangeSex:

    @pytest.mark.asyncio
    async def test_not_args(self, app: App, load_plugins) -> None:
        await shouldDo(app, "/niuzi", "参数捏", 2501390802)

    @pytest.mark.asyncio
    async def test_not_niuzi(self, app: App, load_plugins) -> None:
        await shouldDo(
                    app, 
                   "/niuzi 变女性", 
                   msg.change_sex.no_niuzi, 
                   201390802
               )
        
    @pytest.mark.asyncio
    async def test_always_woman(self, app: App, load_plugins) -> None:
        from ..dao import NiuziDAO

        niuzi_dao: NiuziDAO = NiuziDAO()  

        qq = "2501390802"
        niuzi = niuzi_dao.findNiuziByQQ(qq)
        assert niuzi != None, \
                    f"table not has {qq}'s niuzi in database"

        await shouldDo(
                    app, 
                    "/niuzi 变女性", 
                    msg.change_sex.already_woman, 
                    2501390802
                )

    @pytest.mark.asyncio
    async def test_success(self, app: App, load_plugins) -> None:
        from ..dao import NiuziDAO

        niuzi_dao: NiuziDAO = NiuziDAO()  

        qq = "2501390802"
        niuzi = niuzi_dao.findNiuziByQQ(qq)

        assert niuzi != None, \
                    f"table not has {qq}'s niuzi in database"

        niuzi.sex = Sex.MALE

        niuzi_dao.update(niuzi)
          
        await shouldDo(
                    app, 
                    "/niuzi 变女性",
                    msg.change_sex.success.format(50),
                    2501390802,
                )

