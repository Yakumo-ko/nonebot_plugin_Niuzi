from nonebot import get_driver, logger

# Export something for other plugin
# export = nonebot.export()
# export.foo = "bar"

# @export.xxx
# def some_function():
#     pass

from .config import Config
global_config = get_driver().config

status = True 
for field, value in Config.__fields__.items():
    if global_config.__dict__.get(field) == None and value.required:
        logger.error(f"你需要设置 {field} 的值才能正常使用本插件")
        status = False

if status:
    logger.info("达达没牛子")
    from . import command

logger.info("关于本插件的相关配置请阅读README或访问https://github.com/Yakumo-ko/nonebot-plugin-Niuzi")

