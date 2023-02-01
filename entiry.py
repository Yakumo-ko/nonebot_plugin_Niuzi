from pydantic import BaseModel

class Lovers(BaseModel):
    qq: int 
    target: int 

    def getOther(self, id: int) -> int:
        """
        获取这个id的另一方的id
        """
        return self.qq if id!=self.qq else self.target



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
    type: int
 
