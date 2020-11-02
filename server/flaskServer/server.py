#!/usr/bin/python3

import pymysql
import socket


db = pymysql.connect(socket.gethostbyname('db'),"test", "1234567")

try:

    

    print("sucess")

    with db.cursor() as cur:

        cur.execute('SELECT VERSION()')

        version = cur.fetchone()

        print(f'Database version: {version[0]}')

    db.close()

finally:
    try:
        db.close()
    finally:
        print("-------")