from pydantic import BaseModel


class Lovers(BaseModel):
    qq: int 
    target: int 

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

class CoolDown(BaseModel):
    qq: int
    timestampe: int
 
