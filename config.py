from pydantic import BaseModel, Extra


class Config(BaseModel, extra = Extra.ignore):
    # Your Config Here
    
    defalut_nick_name: str
    change2woman: int 
    pk_cd: int
    doi_cd: int
    host: str 
    user: str
    password: str
    database: str
    port: int


