# -*- coding: utf-8 -*-

import os
import traceback
import pymysql
import requests
import logging
from pyquery import PyQuery as pq

host = '127.0.0.1'
port = '3306'
user = 'root'
password = 'root_password'
database = 'weibit_spider'

base_dir = os.path.dirname(os.path.abspath(__file__))
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(process)d %(filename)s:%(lineno)d [%(levelname)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


def data_insert(data):
    try:
        with conn.cursor() as cursor:
            sql = '''INSERT INTO `jinse_coin` (
                name, short_name, img_name, price, percent_change_24h, volume_24h,
                market_capital, available, flow_rate, total)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) '''
            logger.info(sql + "VALUES" + str(data))
            cursor.execute(sql, data)
            conn.commit()
    except pymysql.err.IntegrityError:
        logger.warn('唯一键重复')
    except Exception as e:
        traceback.print_exc()
        logger.critical("Error %s", str(e))
        raise


def main():
    global conn
    conn = pymysql.connect(
        host=host,
        user=user,
        password=password,
        db=database,
        cursorclass=pymysql.cursors.DictCursor, charset="utf8"
    )
    try:
        url = 'http://www.jinse.com/coin?page={}'
        for i in range(1, 14):
            html = requests.get(url.format(i), timeout=5).content
            _lists = pq(html)('.link')('.font18')
            for j in _lists:
                _img_url = pq(j)('img').attr('src')
                logger.info(_img_url)
                img_name = _img_url.split('/')[-1].strip()
                short_name = img_name.split('.')[0]
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

                # content  = {
                #     'name': name, 'img_name': img_name, 'price': price, 'percent_change_24h': percent_change_24h,
                #     'volume_24h': volume_24h, 'market_capital': market_value, 'available': circulate_value,
                #     'flow_rate': flow_rate, 'total': total
                # }

                data = (
                    name, short_name, img_name, price, percent_change_24h, volume_24h,
                    market_value, circulate_value, flow_rate, total
                )
                data_insert(data)
                conn.commit()
    except:
        conn.rollback()
        traceback.print_exc()
        return
    finally:
        conn.close()


if __name__ == '__main__':
    while True:
        main()
        import time
        time.sleep(90)
"""
表结构
CREATE TABLE `jinse_coin` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `name`  VARCHAR(255) NOT NULL COMMENT '名称',
    `short_name` VARCHAR(255) NOT NULL COMMENT '简称',
    `img_name` VARCHAR(255) NOT NULL COMMENT '图片名称',
    `price` VARCHAR(255) NOT NULL COMMENT '价格',
    `volume_24h` VARCHAR(255) NOT NULL COMMENT '24小时成交额',
    `percent_change_24h` VARCHAR(255) NOT NULL COMMENT '24小时涨幅',
    `market_capital` VARCHAR(255) NOT NULL COMMENT '流通市值(亿)',
    `available` VARCHAR(255) NOT NULL COMMENT '流通数量',
    `flow_rate` VARCHAR(255) NOT NULL COMMENT '流通率',
    `total` VARCHAR(255) NOT NULL COMMENT '发行总量',
    PRIMARY KEY (`id`),
    UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""
