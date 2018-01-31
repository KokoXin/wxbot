# coding: utf8

import sqlite3

def get_conn():
    conn = sqlite3.connect("./jinse.db")
    return conn

def search_coin_info(coin):
    conn = get_conn()
    query = '''select * from jinse_coin where short_name="%s" order by id desc limit 5''' % coin.upper()
    cursor = conn.cursor()
    cursor.execute(query)
    records = cursor.fetchall()
    if not records:
        return ''
    record = records[0]
    print(record)
    msg = u'''
----  %s 实时行情 ----
\ue10f coin: %s
\ue110 当前价格: %s
\ue110 市值排行： %s
\ue110 24小时涨跌幅: %s
\ue110 24小时成交额: %s
\ue110 流通市值: %s
\ue110 流通数量: %s
\ue110 流通率:%s
-----------------------------
由BCTime机器人提供
''' % (coin.upper(),record[2], record[5],record[1] , record[6], record[7],record[8],record[9],record[10])
    cursor.close()
    conn.close()
    return msg
