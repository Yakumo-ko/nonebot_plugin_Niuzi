
from typing import Tuple, List, Union, Dict, Any

import pymysql
import pymysql.cursors
from pymysql.cursors import Cursor, DictCursor
from pymysql import Connection


class Sql:
    def __init__(self, host: str, port: int, usr: str, passwd: str, database: str) -> None:
        self.host = host
        self.port = port 
        self.usr = usr
        self.passwd = passwd
        self.database = database

        self.db: Connection[Cursor]

    def __connect(self)-> DictCursor:
        self.db = pymysql.connect(
                host=self.host, 
                user=self.usr, 
                passwd=self.passwd, 
                database=self.database, 
                port=self.port,
                cursorclass=pymysql.cursors.DictCursor
            )

        return self.db.cursor(DictCursor)

    def __close(self) -> None:
        self.db.close()
    
    def executeQuerySql(self, sql: str) -> Union[Tuple[Dict[str, Any]], None]: 
        cursor: DictCursor = self.__connect()
        size: int = cursor.execute(sql)
        if size==0:
            return None

        res: Tuple[Dict[str, Any], ...] = cursor.fetchall()
        
        cursor.close()
        return res

    def executeNotQuerySql(self, sql: str) -> bool: 
        """
        : execute a sql except for query 
        """

        cursor: DictCursor = self.__connect()
        res: int  = cursor.execute(sql) 
        self.db.commit()
        self.__close()

        return True if res!=0 else False

