from typing import Union, Dict, Tuple, List, Any

from nonebot import get_driver

from ..config import Config
from ..entiry.Lovers import Lovers
from ..utils.Mysql import Sql



class LoversDAO:
    # sql table name
    __LOVERS: str = "lovers"

    __CREAT_LOVERS: str = """\
            CREATE TABLE IF NOT EXISTS `{table_name}` (                          
                `qq` BIGINT UNIQUE NOT NULL,`target` BIGINT     
            )
            """.format(table_name = __LOVERS)


    def __init__(self) -> None:
        conf = Config.parse_obj(get_driver().config)
        self.sql: Sql = Sql(
                conf.host, 
                conf.port, 
                conf.user, 
                conf.password, 
                conf.database
            )


        self.sql.executeNotQuerySql(self.__CREAT_LOVERS)

    def findloversByQQ(self, qq: str) -> Union[Lovers, None]:
        sql: str = "select * from `{tb_name}` where `qq`='{qq}'".format(
                    tb_name = self.__LOVERS,
                    qq = qq
                )

        res: Union[Tuple[Dict[str, Any]], None]= self.sql.executeQuerySql(sql)

        return Lovers(**res[0]) if res!=None else None

    def getAll(self) -> Union[List[Lovers], None]:
        sql : str = f"select * from `{self.__LOVERS}`"

        rows: Union[Tuple[Dict[str, Any]], None]= self.sql.executeQuerySql(sql)

        if rows == None:
            return rows

        res: List[Lovers] = [Lovers(**row) for row in rows]
        
        return res

    def insert(self, lovers: Lovers) -> bool:
        sql: str =  "INSERT INTO `{table_name}` \
        (qq, target) VALUE\
        ({qq}, {target})".format(
                    qq = lovers.qq,
                    sex = lovers.target,
                    table_name =  self.__LOVERS
                )

        return self.sql.executeNotQuerySql(sql)

    def update(self, lovers: Lovers) -> bool:
        sql: str = """ \
            UPDATE `{table_name}` SET  
                        `qq` = {qq}, 
                        `target` = {target}, 
                    WHERE `qq` = {qq}
            """.format(
                    qq = lovers.qq,
                    target = lovers.target,
                    table_name =  self.__LOVERS
                )

        return self.sql.executeNotQuerySql(sql)

    def delete(self, lovers: Lovers) -> bool:
        sql: str = "DELETE  FROM `{table_name}` WHERE `qq`= {qq}".format(
                    qq=lovers.qq,
                    table_name =  self.__LOVERS
                )

        return self.sql.executeNotQuerySql(sql)
