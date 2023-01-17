from pydantic import BaseModel


class Lovers(BaseModel):
    qq: str
    target: str

class NiuZi(BaseModel):
    owner: str
    name: str
    length: float
    sex: int
 
