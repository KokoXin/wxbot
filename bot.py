# coding: utf8
from wxpy import *
import re
from utils import search_coin_info
from cotrol import *

# new_welcome = True
#
# coin_search = True
#
# friends_accept = False
#
# bot_auto = False

bot = Bot(cache_path=True,console_qr=False)
#图灵机器人接口
tuling = Tuling()

# 统计微信好友信息,并发送[文件传输助手]
tongji = bot.friends().stats_text()
# 并将结果发送到微信[文件传输助手]
bot.file_helper.send(tongji)



# group2 = bot.groups().search(name=u'tests')[0]
groups = bot.groups()

# 新人入群的欢迎语 文本
welcome_text = u'''
    🎉 欢迎 @{} 的加入群聊！
                '''
# 新人入群通知的匹配正则
rp_new_member_name = (
    re.compile(r'^"(.+)"通过'),
    re.compile(r'邀请"(.+)"加入'),
)


# 获取新人的微信昵称
def get_new_member_name(self,msg):
    # itchat 1.2.32 版本未格式化群中的 Note 消息
    from itchat.utils import msg_formatter
    msg_formatter(msg.raw, 'Text')
    for rp in self.rp_new_member_name:
        match = rp.search(msg.text)
        if match:
            return match.group(1)

# 新人欢迎消息
if new_welcome :
    @bot.register(groups, NOTE)
    def welcome(msg):
        name = get_new_member_name(msg)
        if name:
            return welcome_text.format(name)

#查询币信息
if coin_search:
    @bot.register(groups, TEXT)
    def group_text_reply(msg):
        if re.match('\w{2,5}', msg.text):
            rep_msg = search_coin_info(msg.text)
            if rep_msg:
                return rep_msg

#自动添加好友，推送群名片
if friends_accept:
    @bot.register(msg_types=FRIENDS)
    def auto_accept_friends(msg):
        #接受好友
        new_friends = bot.accept_friend(msg.card)
        #向新的好友发送信息
        new_friends.send('''你好,我是微信机器人''')
        # #更新群成员信息
        # group2.update_group(True)
        # if new_friends.user_name in group2:
        #     new_friends.send('您已经在机器人攻坚小队群里了')
        # else:
        #     if len(group2) < int(500):
        #         new_friends.send('即将发送群聊邀请')
        #         group2.add_members(new_friends.user_name,use_invitation=True)


#关键词自动回复--智能机器人客服
if bot_auto:
    @bot.register(Friend,[PICTURE,TEXT])
    def send_card(msg):
        print(msg.type)
        if u'你好' in msg.text:
            msg.chat.send(u'我很好')
        # elif u'群' in msg.text:
        #     #发送群聊邀请
        #     if len(group2) < int(500):
        #         print(u'即将发送群聊邀请')
        #         group2.add_members(msg.chat.user_name,use_invitation=True)
        #     else:
        #         msg.chat.send(u'1群已满，将邀请进入2群')
        elif u'图片' in msg.text:
            msg.chat.send_image(u'' + u'180122-154201.png')
        elif u'图灵' in msg.text:
            msg.chat.send(u'您已经进入图灵模式')
            @bot.register(msg.chat)
            def replay_myfriend(self,msg):
                if u'退出' in msg.text:
                    msg.chat.send(u'您已经退出图灵模式')
                    self.bot.registered.disable(replay_myfriend)
                else:
                    self.tuling.do_reply(msg)


bot.join()

