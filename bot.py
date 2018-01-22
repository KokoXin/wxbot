# -*- coding: utf-8 -*-

import re
import itchat
from itchat.content import (
    TEXT, MAP, CARD, NOTE, SHARING, PICTURE, RECORDING, ATTACHMENT, VIDEO
)
from utils import search_coin_info


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    msg.user.send('%s: %s' % (msg.type, msg.text))


@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    msg.download(msg.fileName)
    typeSymbol = {
        PICTURE: 'img',
        VIDEO: 'vid', }.get(msg.type, 'fil')
    return '@%s@%s' % (typeSymbol, msg.fileName)


@itchat.msg_register(TEXT, isGroupChat=True)
def group_text_reply(msg):
    if re.match('\w{2,5}', msg.text):
        msg.user.send(
            search_coin_info(msg.text)
        )


itchat.auto_login(True)
itchat.run(True)
