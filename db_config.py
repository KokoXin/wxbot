# -*- coding: utf-8 -*-

import pymysql

config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'root_password',
    'database': 'weibit_spider',
    'charset': 'utf8'
}

conn = pymysql.connect(autocommit=True, **config)
