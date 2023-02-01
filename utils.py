
from typing import NoReturn, Tuple, List, Union, Dict, Any
from nonebot import get_bot
from nonebot.adapters.mirai2.event import GroupMessage
from nonebot.adapters.mirai2.message import MessageSegment, MessageType
from nonebot.internal.adapter.bot import Bot
from nonebot.matcher import Matcher

import pymysql
import pymysql.cursors
from pymysql.cursors import Cursor, DictCursor
from pymysql import Connection
from datetime import datetime, timedelta

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
    if member == int(bot.self_id):
        return await bot.member_profile(target=group, member_id=member)

    members = await bot.member_list(target = group)
    for mem in members['data']:
        if member == mem['id']:
            return await bot.member_profile(target=group, member_id=member)
    return None

async def getNickName(group: int, member: int) -> str:
    """
    获取指定群的某个群成员的昵称, 若此成员不在该群返回"none"
    """
    member_info = await member_profile(group, member)
    return member_info['nickname'] if member_info != None else "none"

def toChinese(sex: int) -> str:
    return '女' if sex == Sex.FEMALE else '男'

def hasAT(event: GroupMessage) -> Union[str, None]:
    for seg in event.get_message().export():
        if seg['type'] == MessageType.AT:
            return str(seg['target'])
    if event.to_me:
        return get_bot().self_id
    return None

async def checkCondition(matcher: Matcher, condition: bool, msg: str) -> Union[NoReturn, None]:
    """
    条件检查器，用来解决一堆动不动就要判断条件来决定是否结束或继续执行的繁琐情况
    条件不符合直接结束该事件处理, 并发送消息 
    """
    if condition:
        await matcher.finish(msg)
    return None

def toNode(msg: str, id: int, nickname: str) -> dict:
    """
    构造一个转发节点
    """
    return {
            "senderId": id,
            "time": int(datetime.now().timestamp()),
            "senderName": nickname, 
            "messageChain": [MessageSegment.plain(msg)]
        }

