# nonebot-plugin-NiuZi

> ~~施工中....~~

## 介绍

这是一个能让群友们愉♂快, 促进群友感情的小插件, 移植于[原项目](https://github.com/Micalhl/NiuZi)的牛子系统. ~~现阶段处于施工状态中, 不可用~~, 大致功能已移植完毕.

插件移植完成时间不长, 个人测试未必能覆盖未料想的情况, 还请各位帮忙抓虫(ᗜˬᗜ) 

## 食用方式
> **注意: 由于我的bot采用的是nonebot+mirai组合, 该插件仅对使用适配器为mirai-adpater2的bot有效** 

### 依赖项

该插件依赖于[nonebot2](https://github.com/nonebot/nonebot2), [nonebot2-adapter-mirai2](https://github.com/ieew/nonebot_adapter_mirai2)和[pymsql](pyp://github.com/PyMySQL/PyMySQL), 请确定你的py环境是否包含以上依赖, python环境大于等于3.8皆可

### 安装方式&配置
因为是自娱自乐的小插件, 并没有打算把插件发布到PyPI, 故采用原始的安装方式

clone该项目到你的plugins文件夹, 在你的.env(.env.\*)文件中写入以下配置并**按实际情况填入正确的值**

```
# 必填
mysql_host=localhost
mysql_user=root
mysql_password=123456
mysql_database=233
mysql_port=3306

# 可选配置
defalut_nick_name: str = "牛子"
change2woman: int  = 50
pk_cd: int = 60
doi_cd: int = 120
```

### 使用
在你的群聊中键入`/niuzi`, 你的bot默认会返回一个包含这个插件使用方式和说明的转发消息.

## Todo: 移植

- 移植以下命令/功能
	- [x] 变女性
	- [x] 领养牛子
	- [x] 我的牛子
	- [x] 改牛子名
	- [x] 比划比划
	- [x] 管理命令
	- [x] 我的对象
	- [x] 搞对象
	- [x] 贴贴
	- ~~[ ] 处理请求~~
	- [x] 我要分手
	- ~~[x] 群牛子排行~~
	- [x] 牛子榜

> 由于对以下命令(搞对象, 我要分手)实现方式与原项目不同, 原项目处理请求命令合并到上述两者命令, 不再重复
>
> 群牛子排行和牛子榜属于重复命令, 已合并 

## 下一步的计划

- [ ] 优化代码结构, 将预设的消息模板分开, 支持自定义消息模板
- [ ] 支持命令/子命令别名(可自定义命令前缀)
- [ ] 在原有的基础上整添新功能(~~魔改~~)
