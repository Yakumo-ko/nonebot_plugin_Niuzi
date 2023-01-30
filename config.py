from pydantic import BaseModel, Extra


class Config(BaseModel, extra = Extra.ignore):
    # Your Config Here
    
    defalut_nick_name: str = "牛子"
    change2woman: int  = 50
    pk_cd: int = 60
    doi_cd: int = 10
    mysql_host: str 
    mysql_user: str
    mysql_password: str
    mysql_database: str
    mysql_port: int





