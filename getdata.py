# coding: utf8
import os,re
import sqlite3
import traceback
import requests
import datetime
import logging
from pyquery import PyQuery as pq

base_dir = os.path.dirname(os.path.abspath(__file__))
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(process)d %(filename)s:%(lineno)d [%(levelname)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

insert_info = False

def init_db():
    sql = '''
    CREATE TABLE jinse_coin (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    sort_id INT NOT NULL,
    name  VARCHAR(255) NOT NULL,
    short_name VARCHAR(255) NOT NULL,
    img_name VARCHAR(255) NOT NULL,
    price VARCHAR(255) NOT NULL,
    volume_24h VARCHAR(255) NOT NULL,
    percent_change_24h VARCHAR(255) NOT NULL,
    market_capital VARCHAR(255) NOT NULL,
    available VARCHAR(255) NOT NULL,
    flow_rate VARCHAR(255) NOT NULL,
    total VARCHAR(255) NOT NULL,
    time TEXT NOT NULL
    );
    '''
    # sql_sort = '''
    #     CREATE TABLE jinse_coin_sort (
    #     id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    #     name  VARCHAR(255) NOT NULL,
    #     short_name VARCHAR(255) NOT NULL,
    #     img_name VARCHAR(255) NOT NULL,
    #     price VARCHAR(255) NOT NULL,
    #     volume_24h VARCHAR(255) NOT NULL,
    #     percent_change_24h VARCHAR(255) NOT NULL,
    #     market_capital VARCHAR(255) NOT NULL,
    #     available VARCHAR(255) NOT NULL,
    #     flow_rate VARCHAR(255) NOT NULL,
    #     total VARCHAR(255) NOT NULL,
    #     time TEXT NOT NULL
    #     );
    #     '''

    if not os.path.exists('./jinse.db'):
        conn = sqlite3.connect('./jinse.db')
        c = conn.cursor()
        c.execute('PRAGMA encoding="UTF-8";')
        c.execute(sql)
        # c.execute(sql_sort)
        conn.commit()
        conn.close()
    return True

def data_sort_insert(data):
    try:
        cursor = conn.cursor()
        sql = '''
    INSERT INTO jinse_coin_sort (
    name, short_name, img_name, price, volume_24h, percent_change_24h, market_capital, available, flow_rate, total, time
    ) VALUES (
    "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s"
    );''' % data
        logger.info(sql)
        cursor.execute(sql)
        cursor.close()
        conn.commit()
        insert_info = True
    except Exception as e:
        traceback.print_exc()
        logger.critical("Error %s", str(e))
        raise


def data_sort_update(data):
    try:
        cursor = conn.cursor()
        sql = '''
    UPDATE jinse_coin_sort SET name="%s", short_name="%s", img_name="%s", price="%s", volume_24h="%s", 
    percent_change_24h="%s", market_capital="%s", available="%s", flow_rate="%s", total="%s", time="%s";''' % data
        logger.info(sql)
        cursor.execute(sql)
        cursor.close()
        conn.commit()
    except Exception as e:
        traceback.print_exc()
        logger.critical("Error %s", str(e))
        raise


def data_sort_deal(data):
    if '万' in data:
        data = data * 1000
    elif '亿' in data:
        data = data * 100000000
    parttern = re.compile(r'(\d+)')
    data = parttern.search(data)
    return data

def data_insert(data):
    try:
        cursor = conn.cursor()
        sql = '''
INSERT INTO jinse_coin (
sort_id, name, short_name, img_name, price, volume_24h, percent_change_24h, market_capital, available, flow_rate, total, time
) VALUES (
"%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s"
);''' % data
        logger.info(sql)
        cursor.execute(sql)
        cursor.close()
        conn.commit()
    except Exception as e:
        traceback.print_exc()
        logger.critical("Error %s", str(e))
        raise


def main():
    global conn
    conn = sqlite3.connect('./jinse.db')
    try:
        url = 'http://www.jinse.com/coin?page={}'
        for i in range(1, 14):
            html = requests.get(url.format(i), timeout=5).content
            _lists = pq(html)('.link')('.font18')
            for j in _lists:
                sort_id = pq(j)('.left.col56.gray8').text()
                _img_url = pq(j)('img').attr('src')
                logger.info(_img_url)
                img_name = _img_url.split('/')[-1].strip()
                short_name = img_name.split('.')[0]
                short_name = short_name.upper()
                with open('tmp/images', 'a') as f:
                    f.write(_img_url + '\n')
                name = pq(j)('a').text()
                price = pq(j)('.left.col160').text()
                percent_change_24h = pq(j)('.left.col120').text()
                volume_24h = pq(j)('.left.col130').eq(0).text()
                market_value = pq(j)('.left.col150').text()
                circulate_value = pq(j)('.left.col140').text()
                flow_rate = pq(j)('.left.col110').text()
                total = pq(j)('.left.col130').eq(1).text()
                now = datetime.datetime.strftime(
                    datetime.datetime.now(),
                    "%Y-%m-%d %H:%M:%S"
                )
                data = (
                    sort_id,name, short_name, img_name, price, percent_change_24h, volume_24h,
                    market_value, circulate_value, flow_rate, total, now
                )
                data_insert(data)
                conn.commit()
            # #=======================================
            # for i in _lists:
            #     _img_url = pq(i)('img').attr('src')
            #     logger.info(_img_url)
            #     img_name = _img_url.split('/')[-1].strip()
            #     short_name = img_name.split('.')[0]
            #     short_name = short_name.upper()
            #     with open('tmp/images', 'a') as f:
            #         f.write(_img_url + '\n')
            #     name = pq(i)('a').text()
            #     price = pq(i)('.left.col160').text()
            #     price = data_sort_deal(price)
            #     percent_change_24h = pq(i)('.left.col120').text()
            #     percent_change_24h = data_sort_deal(percent_change_24h)
            #     volume_24h = pq(i)('.left.col130').eq(0).text()
            #     volume_24h = data_sort_deal(volume_24h)
            #     market_value = pq(i)('.left.col150').text()
            #     market_value = data_sort_deal(market_value)
            #     circulate_value = pq(i)('.left.col140').text()
            #     circulate_value = data_sort_deal(circulate_value)
            #     flow_rate = pq(i)('.left.col110').text()
            #     flow_rate = data_sort_deal(flow_rate)
            #     total = pq(i)('.left.col130').eq(1).text()
            #     total = data_sort_deal(total)
            #     now = datetime.datetime.strftime(
            #         datetime.datetime.now(),
            #         "%Y-%m-%d %H:%M:%S"
            #     )
            #     data_sort = (
            #         name, short_name, img_name, price, percent_change_24h, volume_24h,
            #         market_value, circulate_value, flow_rate, total, now
            #     )
            #     if insert_info == False:
            #         data_sort_insert(data_sort)
            #     else:
            #         data_sort_update(data_sort)
            #     conn.commit()
            #     #================================================================
    except:
        conn.rollback()
        traceback.print_exc()
        return
    finally:
        conn.close()


if __name__ == '__main__':
    init_db()
    while True:
        main()
        import time
        time.sleep(90)


