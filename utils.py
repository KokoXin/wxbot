# -*- coding: utf-8 -*-

from db_config import conn


def search_coin_info(coin):
    query = '''select * from jinse_coin where short_name="%s" order by id desc limit 5''' % coin
    print query
    with conn.cursor() as cursor:
        cursor.execute(query)
        records = cursor.fetchall()
        if not records:
            return u'没有: %s' % coin
        record = records[0]
        msg = u'''coin: %s
当前价格: %s
24小时成交量: %s
24小时涨幅: %s
''' % (record[1], record[4], record[5], record[6])
        return msg
