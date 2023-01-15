
from typing import Tuple, List, Union, Dict, Any

import pymysql
from pymysql.cursors import Cursor
from pymysql import Connection


class Sql:
    def __init__(self, host: str, port: int, usr: str, passwd: str, database: str) -> None:
        self.host = host
        self.port = port 
        self.usr = usr
        self.passwd = passwd
        self.database = database

        self.db: Connection[Cursor]

    def __connect(self)-> Cursor:
        self.db = pymysql.connect(
                host=self.host, 
                user=self.usr, 
                passwd=self.passwd, 
                database=self.database, 
                port=self.port
            )

        return self.db.cursor()

    def __close(self) -> None:
        self.db.close()
    
    def executeQuerySql(self, sql: str) -> Union[Tuple[Dict[str, Any]], None]: 

        cursor: Cursor = self.__connect()
        size: int = cursor.execute(sql)
        if size==0:
            return None

        res: List[Dict[str, Any]] = []
        for row in cursor.fetchall():
            res.append({item[0]:item[1] for item in row})
        
        cursor.close()
        return tuple(res)

    def executeNotQuerySql(self, sql: str) -> bool: 
        """
        : execute a sql except for query 
        """

        cursor: Cursor = self.__connect()
        res: int  = cursor.execute(sql) 
        self.__close()

        return True if res!=0 else False

    
