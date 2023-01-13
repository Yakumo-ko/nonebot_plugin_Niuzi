from typing import Union, Dict, Any, Callable

from nonebot import get_driver

from ..config import Config

import pymysql
from pymysql.cursors import Cursor
from pymysql import MySQLError


class SqlBase:
    def __init__(self) -> None:
        self.config: Config = Config.parse_obj(get_driver().config)

    def executeQuerySql(self, sql: str) -> Union[Dict[str, Any], None]: 
        pass



    def __executeSql(self, function: Callable[[Cursor, str], Any], sql: str) -> Any: 
        """
        : Note:
        :   - return value [str, Any] -> [table_item_name: value]
        :   - The return value **None** stands for a Error about SQLError 
        """
        try:
            db = pymysql.connect(
                        host=self.config.host, 
                        user=self.config.user, 
                        passwd=self.config.password, 
                        database=self.config.database, 
                        port=self.config.port
                    )

            cursor: Cursor = db.cursor() 

            size: int = cursor.execute(sql)
            if size==0:
                return {}

            rows: Dict[str, Any] = {row[0]:row[1] for row in cursor.fetchall()}

            db.close()

        except MySQLError:
            print(MySQLError.args)
            return None

        return rows
