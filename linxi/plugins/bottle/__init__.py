import asyncio
import random
from nonebot.plugin import PluginMetadata
from nonebot import on_command
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GroupMessageEvent, GROUP, Message
from .data_source import bottle,text_audit,ba
from .config import Config

__plugin_meta__ = PluginMetadata(
    name="漂流瓶",
    description="群与群互通的漂流瓶插件",
    usage=f"""
指令：
    扔漂流瓶 <文本 | 图片>
    捡漂流瓶
    评论漂流瓶 <漂流瓶编号> <文本>
    举报漂流瓶 <漂流瓶编号>
    查看漂流瓶 <漂流瓶编号>
    删除漂流瓶 <漂流瓶编号>
SUPERUSER指令：
    清空漂流瓶
    恢复漂流瓶 <漂流瓶编号>
    删除漂流瓶评论 <漂流瓶编号> <QQ号>
    漂流瓶白名单 <QQ | 群聊> [QQ号 | 群号]
    漂流瓶黑名单 <QQ | 群聊 | 举报> [QQ号 | 群号]
    漂流瓶详情 <漂流瓶编号>

详情请见文档。
""".strip(),
    extra={
        "unique_name": "bottle"
    }
)

throw = on_command("扔漂流瓶 ", aliases=set(["bottle throw ","丢漂流瓶 "]),permission=GROUP, priority=100, block=True)
get = on_command("捡漂流瓶", aliases=set(["bottle pick"]), priority=100, block=True)
report = on_command("举报漂流瓶 ", priority=100, block=True)
comment = on_command("评论漂流瓶 ", aliases=set(["bottle comment"]), priority=100, block=True)
check_bottle = on_command("查看漂流瓶 ", priority=100, block=True)
remove = on_command("删除漂流瓶 ", priority=100, block=True)

resume = on_command("恢复漂流瓶 ", permission=SUPERUSER, priority=100, block=True)
clear = on_command("清空漂流瓶", permission=SUPERUSER, priority=100, block=True)
comrem = on_command("删除漂流瓶评论",permission=SUPERUSER, priority=100, block=True)
listqq = on_command("漂流瓶详情",permission=SUPERUSER, priority=100, block=True)
ban = on_command("漂流瓶黑名单",aliases=set(["bottle ban"]),permission=SUPERUSER, priority=100, block=True)
white = on_command("漂流瓶白名单",aliases=set(["bottle unban"]),permission=SUPERUSER, priority=100, block=True)

@throw.handle()
async def thr(bot: Bot, event: GroupMessageEvent):
    if not ba.verify(event.user_id,event.group_id):
        await throw.finish(ba.bannedMessage)

    try:
        message = str(event.message).split(maxsplit=1)[1]
    except:
        await throw.finish("想说些什么话呢？在指令后边写上吧！")
    
    try:
        message_text = event.message.extract_plain_text().split(maxsplit=1)[1]
    except:
        message_text = ""

    audit = await text_audit(text=message_text)
    if not audit == 'pass':
        if audit == 'Error': 
            await throw.finish("文字审核未通过！" )
        elif audit['conclusion'] == '不合规':
            await throw.finish("文字审核未通过！原因：" + audit['data'][0]['msg'])

    group_name = await bot.get_group_info(group_id=event.group_id)
    group_name = group_name['group_name']
    user_name = await bot.get_group_member_info(group_id=event.group_id,user_id=event.user_id)
    user_name = user_name['nickname']

    add_index = bottle.add(bot=bot,user=event.user_id, group=event.group_id, text=message, user_name=user_name, group_name=group_name)
    if add_index:
        # 添加个人冷却
        ba.add('cooldown',event.user_id)
        await asyncio.sleep(2)
        await throw.finish(f'你将编号No.{add_index}的漂流瓶以时速{random.randint(0,2**16)}km/h的速度扔出去，谁会捡到这个瓶子呢...')
    else:
        await asyncio.sleep(2)
        await throw.finish("你的瓶子以奇怪的方式消失掉了！")

@get.handle()
async def g(bot: Bot, event: GroupMessageEvent):
    if not ba.verify(event.user_id,event.group_id):
        await throw.finish(ba.bannedMessage)

    if not bottle.select():
        await get.finish("好像一个瓶子也没有呢..要不要扔一个？")
    else:
        bott = bottle.select()
        data = bott[1]
        try:
            user = await bot.get_group_member_info(group_id=data['group'], user_id=data['user'])
            user = user["nickname"]
        except:
            user = data['user_name']
        try:    
            group = await bot.get_group_info(group_id=data['group'])
            group = group["group_name"]
        except:
            group = data['group_name']

        comment_list = bottle.check_comment(bott[0])
        comment:str = ""
        for i in comment_list[-3:]:
            comment += i+"\n"
        ba.add('cooldown',event.user_id)
        await get.finish(f'【漂流瓶No.{bott[0]}|被捡到{data["picked"]}次】来自【{group}】的 {user} ！\n'+Message(data['text']) + (f"\n★评论共 {len(comment_list)} 条★\n{comment.strip()}" if comment else ""))

@report.handle()
async def rep(bot: Bot, event: GroupMessageEvent):
    if (not ba.verify(event.user_id,event.group_id)) or (not ba.verifyReport(event.user_id)):
        await throw.finish(ba.bannedMessage)

    index = int(str(event.message).split(maxsplit=1)[1])
    result = bottle.report(index,event.user_id)
    if result == 0:
        await report.finish("举报失败！")
    if result == 1:
        ba.add('cooldown',event.user_id)
        await report.finish(f"举报成功！关于此漂流瓶已经有 {bottle.check_report(index)} 次举报")
    if result == 2:
        # 获取漂流瓶详情
        data = bottle.check_bottle(int(index))
        mes = f"有一漂流瓶遭到封禁！\n编号：{index}\n用户QQ：{data['user']}\n来源群组：{data['group']}\n"
        mes += Message(data['text'])
        commentList = ""
        for i in data['comment']:
            commentList += f"【{i[0]}】{i[1]}\n"

        # 私聊发送被删除的漂流瓶详情
        for i in list(bot.config.superusers):
            await bot.send_private_msg(user_id = i,message=mes)
            await bot.send_private_msg(user_id = i,message=commentList)
            await asyncio.sleep(0.5)
        await report.finish("举报成功！已经进行删除该漂流瓶处理！")
    if result == 3:
        await report.finish("该漂流瓶已经被删除！")

@comment.handle()
async def com(bot: Bot, event: GroupMessageEvent):
    if not ba.verify(event.user_id,event.group_id):
        await throw.finish(ba.bannedMessage)
        
    mes = str(event.message.extract_plain_text()).split(maxsplit=2)
    index = int(mes[1])
    data = bottle.check_bottle(index)
    if not data or data['del']:
        await check_bottle.finish("该漂流瓶不存在或已被删除！")
    user = await bot.get_group_member_info(group_id=event.group_id, user_id=event.user_id)
    try:
        commen = f"{user['nickname']}：{mes[2]}"
    except:
        await comment.finish("想评论什么呀，在后边写上吧！")
    
    # 进行文字审核
    audit = await text_audit(text=commen)
    if not audit == 'pass':
        if audit == 'Error': 
            await comment.finish("文字审核未通过！原因：调用审核API失败，请检查违禁词词表格式是否正确，或token是否正确设置！" )
        elif audit['conclusion'] == '不合规':
            await comment.finish("文字审核未通过！原因：" + audit['data'][0]['msg'])

    # 审核通过
    bottle.comment(index,event.user_id, commen)
    try:
        await bot.send_msg(group_id=bottle.check_bottle(index)['group'], message=Message(f"[CQ:at,qq={bottle.check_bottle(index)['user']}] 你的{index}号漂流瓶被评论啦！\n{commen}"))
        await asyncio.sleep(2)
    finally:
        ba.add('cooldown',event.user_id)
        await comment.finish("回复成功！")

@check_bottle.handle()
async def che(bot: Bot, event: MessageEvent):
    index = int(str(event.message).split(maxsplit=1)[1])
    comment_list = bottle.check_comment(index)
    data = bottle.check_bottle(index)

    if data['del'] == 1:
        await check_bottle.finish("该漂流瓶不存在或已被删除！")
    try:
        user = await bot.get_group_member_info(group_id=data['group'], user_id=data['user'])
        user = user["nickname"]
    except:
        user = data['user_name']
    try:    
        group = await bot.get_group_info(group_id=data['group'])
        group = group["group_name"]
    except:
        group = data['group_name']
    if not comment_list:
        await check_bottle.finish(f"这个编号的漂流瓶还没有评论,不能给你看里面的东西！\n【该#{index} 漂流瓶来自【{group}】的 {user}，被捡到{data['picked']}次，于{data['time']}扔出】")
    comment = ""
    for i in comment_list:
        comment += i+"\n"
    ba.add('cooldown',event.user_id)
    await check_bottle.finish(f"来自【{group}】的 {user} 的第{index}号漂流瓶：\n" + Message(data['text']) + f"\n★评论共 {len(comment_list)} 条★\n{comment}【被捡到{data['picked']}次，于{data['time']}扔出】")

@remove.handle()
async def rem(bot:Bot, event: GroupMessageEvent):
    index = int(str(event.message).split()[1])
    if str(event.user_id) in list(bot.config.superusers) or bottle.check_bottle(index)['user'] == event.user_id:
        if bottle.remove(index):
            await remove.finish(f"成功删除 {index} 号漂流瓶！")
        else:
            await remove.finish('删除失败！请检查编号')
    else:
        await remove.finish('删除失败！你没有相关的权限！')

###### SUPERUSER命令 ######

@resume.handle()
async def res(bot: Bot, event: MessageEvent):
    index = int(str(event.message).split()[1])
    if bottle.resume(index):
        await resume.finish(f"成功恢复 {index} 号漂流瓶！")
    else:
        await resume.finish('恢复失败！请检查编号')

@clear.handle()
async def cle(bot: Bot, event: MessageEvent):
    bottle.clear()
    await clear.finish("所有漂流瓶清空成功！")

@listqq.handle()
async def lis(bot: Bot, event: MessageEvent):
    command = str(event.message).split(" ")[1]
    data = bottle.check_bottle(int(command))
    if data:
        mes = f"漂流瓶编号：{command}\n用户QQ：{data['user']}\n来源群组：{data['group']}\n发送时间：{data['time']}\n"
        mes += Message(data['text'])
        await listqq.send(mes)
        
        commentList = ""
        for i in data['comment']:
            commentList += f"【{i[0]}】{i[1]}\n"
        if commentList :
            await listqq.finish(commentList)
        else:
            await listqq.finish("漂流瓶暂无回复")


@ban.handle()
async def li(bot:Bot, event: MessageEvent):
    command = str(event.message).split(" ")[1:]
    if command[0] in ['group','群聊','群号']:
        if ba.add('group',command[1]):
            await ban.finish(f"成功封禁{command[0]}：{command[1]}")
        else:
            ba.remove('group',command[1])
            await ban.finish(f"成功解封{command[0]}：{command[1]}")

    if command[0] in ['qq','QQ','user','用户','qq号','QQ号']:
        if ba.add('user',command[1]):
            await ban.finish(f"成功封禁{command[0]}：{command[1]}")
        else:
            ba.remove('user',command[1])
            await ban.finish(f"成功解封{command[0]}：{command[1]}")
    
    if command[0] in ['report','举报']:
        result = ba.banreport(command[1])
        if result == 1:
            await ban.finish(f"成功取消{command[0]}权限：{command[1]}")
        elif result == 0:
            await ban.finish(f"成功赋予{command[0]}权限：{command[1]}")
        else:
            await ban.finish(result)

@white.handle()
async def wh(bot:Bot, event: MessageEvent):
    command = str(event.message).split(" ")[1:]
    if command[0] in ['group','群聊','群号']:
        if ba.add('whiteGroup',command[1]):
            await ban.finish(f"成功设置白名单{command[0]}：{command[1]}")
        else:
            ba.remove('whiteGroup',command[1])
            await ban.finish(f"成功移除白名单{command[0]}：{command[1]}")

    if command[0] in ['qq','QQ','user','用户','qq号','QQ号']:
        if ba.add('whiteUser',command[1]):
            await ban.finish(f"成功设置白名单{command[0]}：{command[1]}")
        else:
            ba.remove('whiteUser',command[1])
            await ban.finish(f"成功移除白名单{command[0]}：{command[1]}")


@comrem.handle()
async def cr(bot:Bot,event: MessageEvent):
    command = str(event.message).split(" ")[1:]
    if bottle.remove_comment(int(command[0]),int(command[1])):
        await comrem.finish("删除成功！")
    else:
        await comrem.finish("删除失败，请检查编号！")