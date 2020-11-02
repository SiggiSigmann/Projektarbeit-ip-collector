#!/usr/bin/python3

import pymysql
import socket

#socket.gethostbyname('db')
class dbconnector:
    
    def __init__(self, address, database, user, pwd):
        self._address = address
        self._database = database
        self._user = user
        self._pwd = pwd
        self.db = None

    def _connect(self):
        if self.db is None:
            self.db = pymysql.connect(self._address, self._user, self._pwd, db=self._database)

    def _dissconect(self):
        if self.db is not None:
            self.db.close()

    def insert(self):
        print("Insert")
        self._connect()

        with self.db.cursor() as cur:

            cur.execute('Insert into Tracert (TraceID, IpAddress, AddressName, Hop) values (1,  "192.168.178.1", "hippihop", 1);')
            version = cur.fetchone()
            print(version)

            cur.execute('Insert into Measurement (PersonName, IpAddress, TraceID , IpTimestamp) values ( "hallo", "test", 1, "2020-03-04 01:01:01");')
            version = cur.fetchone()
            print(version)

        self._dissconect

    def select(self):
        self._connect()

        with self.db.cursor() as cur:

            cur.execute('SELECT * FROM Measurement')
            version = cur.fetchone()
            print(version)
            cur.execute('SELECT * FROM Tracert')
            version = cur.fetchone()
            print(version)
            cur.execute('select * from Measurement join Tracert')
            version = cur.fetchone()
            print(version)
            
        self._dissconect



"""
db = pymysql.connect(socket.gethostbyname('db'), "test", "1234567", db="networkdata")

try:
    print("sucess")

    with db.cursor() as cur:

        cur.execute('SELECT VERSION()')

        version = cur.fetchone()

        print(f'Database version: {version[0]}')

        cur.execute('SHOW TABLES')

        version = cur.fetchone()

        print(f'Database version: {version[0]}')

finally:
    try:
        db.close()
        print(db)
    finally:
        print("-------")
"""