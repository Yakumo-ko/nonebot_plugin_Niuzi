from typing import Union, Dict, Tuple, Any

from entiry import NiuZi

from utils import Sql

class NiuziDAO:
    # sql table name
    __NIUZI_INFO: str = "niuzi_info"
    __LOVERS: str = "lovers"

    # sql 
    __CREAT_NIUZI_INFO: str =  f"CREATE TABLE                     \
                IF NOT EXISTS `{NIUZI_INFO}` (                  \
                    `qq` BIGINT UNIQUE NOT NULL,                \
                    `name` TEXT, `length` FLOAT,                \
                    `sex` INTEGER DEFAULT 0,                    \
                    `level` INT DEFAULT 0,                      \
                    `points` INT DEFAULT 0, PRIMARY KEY (`qq`)  \
                )"

    __CREAT_LOVERS: str = "CREATE TABLE                           \
            IF NOT EXISTS `{LOVERS}` (                          \
                `qq` BIGINT UNIQUE NOT NULL,`target` BIGINT     \
            )"

    __FIND_NIUZI_BY_USR: str = "select * from `{0}` where `qq`='{1}'"

    def __init__(self) -> None:
        self.sql: Sql = Sql()

        sql_query_by_user = f"select * from "

    def findNiuziByQQ(self, qq: str) -> Union[Tuple[bool, Union[NiuZi, None]], None]:
        """
        : Note: The return value **None** stands for a Error about SQLError 
        """

        res: Union[Dict[str, Any],None] = self.sql.executeQuerySql(
                self.__FIND_NIUZI_BY_USR.format(self.__NIUZI_INFO, qq)
                )

        if res == None:
            return res

        if len(res) == 0:
            return (False, None)

        return (True, NiuZi(**res))

    def insert(self, niuzi: Niuzi)
        pass


        
