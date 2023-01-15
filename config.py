from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    
    defalut_nick_name: str = '牛子'
    pk_cd: int = 60
    host: str = ""
    user: str = ""
    password: str = ""
    database: str = ""
    port: int = 3308

