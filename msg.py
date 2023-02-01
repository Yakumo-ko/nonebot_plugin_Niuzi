from pydantic import BaseModel

setting = {
    "admin": {
        "change": {
            "no_args": "不给要改的人和长度我怎么改",
            "no_length": "不给长度我怎么改"
            },
        "view": {
            "no_args": "我要查谁？你啥都不给让我查空气?"  
            }
        },

    "cum": {
        "already": "你已经爽过了, 注意身体",
        "success": "爽死你了吧骚货, 本次射出{0}厘米"
        },

    "get": {
        "has_niuzi": "你有了你还领, 有病",   
        "success": "领养了，可输入相关命令查看你的牛子信息"
        },

    "name": {
        "success": "行了行了行了",
        "name_too_long": "你牛子名字太长了，最多只支持10个字",
        "no_args": "你牛子要改的名字给忘了, 我怎么改?" 
        },

    "pk": {
        "no_args": "不艾特人家我怎么知道你想跟谁比划?",
        "same": "你跟自己比划什么？",
        "target_no_niuzi": "真可惜！你选的比划对象人家没有牛子",
        "source_in_cd": "你牛子红肿了，等 {0} 秒。",
        "target_in_cd": "对方牛子红肿了，等 {0} 秒。",
        "lost": "{you} 和 {target} 开始比划牛子，输了 {lenght} 厘米。",
        "win": "{you} 和 {target} 开始比划牛子，赢到了 {lenght} 厘米。",
        "both_lost": "{me} 和 {target} 开始比划牛子，不小心缠住了，两人都断了 {lenght} 厘米。"
        },

    "info": {
        "no_niuzi": "没有牛子你查什么查滚",
        "niuzi_info": "主人：{qq_name}({qq})\n名称：{name}\n性别：{sex}\n长度：{length}厘米"
        },

    "change_sex": {
        "already_woman": "你已经是女的了，怎么？",
        "success": "行了行了，你短了{0}厘米",
        "no_niuzi": "你都没有牛子"
        },

    "lover": {
        "get": {
            "self": "你跟自己你搞什么对象？",
            "has_lover": "你有对象了你还找对象？",
            "target_no_niuzi": "真可惜！Ta没有牛子",
            "fail": "真可惜！人家有对象了"
           },

        "request": {
          "send": "{target} 你好，{sender}想跟你搞对象\n输入命令「{subcmd}」",
          "agree": "{0} 恭喜！！！！对方同意了你的请求",
          "disagree": "{0} 真遗憾……对方没有同意你的请求",
          "exists": "已存在请求，可能是别人发的"
            } 
        },

    "leave": {
        "no_lover": "你没对象你分哪门子手？",
        "request": {
            "send": "{target} 你好，{sender} 想跟你分手\n输入命令「{subcmd}」",
            "agree": "{0} 对方同意了你的分手请求……",
            "disagree": "{0} 对方没有同意你的请求"
        }
    },

      "status": "你的对象：{qq_name}({qq})\nTa的牛子：{name}\n牛子性别：{sex}\n牛子长度：{length}厘米",
      "no_lover": "你没有对象你在这叭叭什么？",

      "doi":{
        "no_lover": "贴你ma 你都没人跟你贴",
        "success": "行行行 贴贴贴 一会儿粘上了😅 加了 {length} 厘米，{msg} {second} 秒后才可以再次贴贴",
        "fail": "你俩能不能消停会儿 都粘掉皮了😅 等 {0} 秒再贴"
        },

    "no_arg": "参数捏",
    "no_at_args": "你不艾特人家我怎么知道是谁？",
    "no_at": "你发的什么东西我看不懂，你重新@一下",
    "member_not_found": "群里都没这人你瞎搞什么？",
    "number_error": "你看看你发的什么东西，是数字吗？",
    "not_perm": "你没有权限执行该命令。",
    "no_niuzi": "你没有牛子你在这你想干什么啊",
    "no_request": "没有待处理的请求",
    "command_header": "牛子养成系统(未开发完成)",
    "command_helper": "命令：{0} {1}  {2}"
}

class Admin(BaseModel):
    class Change(BaseModel):
        no_args: str
        no_length: str

    class View(BaseModel):
        no_args: str

    change: Change
    view: View

class Cum(BaseModel):
    already: str
    success: str

class Get(BaseModel):
    has_niuzi: str
    success: str

class Name(BaseModel):
    no_args: str
    name_too_long: str
    success: str

class PK(BaseModel):
    no_args: str
    same: str
    target_no_niuzi: str
    source_in_cd: str
    target_in_cd: str
    lost: str
    win: str
    both_lost: str

class Info(BaseModel):
    no_niuzi: str
    niuzi_info: str

class ChangeSex(BaseModel):
    already_woman: str
    success: str
    no_niuzi: str

class Lover(BaseModel):
    class Get(BaseModel):
        self: str
        has_lover: str
        target_no_niuzi: str
        fail: str

    class Request(BaseModel):
        send: str
        agree: str 
        disagree: str
        exists: str

       
    get: Get
    request: Request

class Leave(BaseModel):
    class Request(BaseModel):
        send: str
        agree: str
        disagree: str

    no_lover: str
    request: Request


class DOI(BaseModel):
    no_lover: str
    success: str
    fail: str
    
class Msg(BaseModel):
    admin: Admin
    cum: Cum
    get: Get
    name: Name
    pk: PK
    info: Info
    change_sex: ChangeSex
    lover: Lover
    leave: Leave
    status: str
    no_lover: str
    doi: DOI
    no_arg: str 
    no_at_args: str
    no_at: str
    member_not_found: str
    number_error: str
    not_perm: str
    no_niuzi: str
    no_request: str
    command_header: str
    command_helper: str

