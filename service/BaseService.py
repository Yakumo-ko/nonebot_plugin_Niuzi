from typing import Union

from ..dao.LoversDAO import LoversDAO
from ..dao.NiuziDAO import NiuziDAO

class BaseService:

    def __init__(self) -> None:
        self.niuzi_dao = NiuziDAO()
        self.lovers_dao = LoversDAO()

    def describe(self) -> Union[str, None]:
        return None

    def usage(self) -> Union[str, None]:
        return None
    
    def needPerm(self) -> bool:
        return False


