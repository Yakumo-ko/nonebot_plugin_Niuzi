
from typing import NoReturn, Tuple, List, Union, Dict, Any
from nonebot import get_bot
from nonebot.adapters.mirai2.event import GroupMessage
from nonebot.adapters.mirai2.message import MessageType
from nonebot.internal.adapter.bot import Bot
from nonebot.matcher import Matcher

import pymysql
import pymysql.cursors
from pymysql.cursors import Cursor, DictCursor
from pymysql import Connection

from .enum import Sex


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

async def member_profile(group: int, member: int) -> Union[dict, None]:
    """
    获取指定群的某个群成员信息, 若此成员不在该群返回None
    """
    bot: Bot  = get_bot()
    members = await bot.member_list(target = group)
    if not member in members:   
        return None
    return await bot.member_profile(target=group, member_id=member)

def toChinese(sex: int) -> str:
    return '女' if sex == Sex.FEMALE else '男'

def hasAT(event: GroupMessage) -> Union[str, None]:
        for seg in event.get_message().export():
            if seg['type'] == MessageType.AT:
                return str(seg['target'])
        return None

async def checkCondition(matcher: Matcher, condition: bool, msg: str) -> Union[NoReturn, None]:
    """
    条件检查器，用来解决一堆动不动就要判断条件来决定是否结束或继续执行的繁琐情况
    条件不符合直接结束该事件处理, 并发送消息 
    """
    if condition:
        await matcher.finish(msg)


