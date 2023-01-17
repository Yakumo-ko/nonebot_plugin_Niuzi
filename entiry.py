from pydantic import BaseModel


class Lovers(BaseModel):
    qq: str
    target: str

"""
class NiuZi(BaseModel):
    owner: str
    name: str
    length: float
    sex: int
"""

class NiuZi(BaseModel):
    qq: int
    name: str
    length: float 
    sex: int
    level: int
    points: int
 
