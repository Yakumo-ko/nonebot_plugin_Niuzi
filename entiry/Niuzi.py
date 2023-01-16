from pydantic import BaseModel

class NiuZi(BaseModel):
    owner: str
    name: str
    length: float
    sex: int
   
