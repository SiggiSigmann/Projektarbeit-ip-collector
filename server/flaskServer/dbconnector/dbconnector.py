#!/usr/bin/python3

import pymysql
import socket
from datetime import datetime

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
            self.db = None

    def insert(self, user, ip):
        
        self._connect()

        with self.db.cursor() as cur:

            #2020-03-04 01:01:01
            now = datetime.now()
            dt_string = now.strftime("%Y-%m-%d %H:%M:%S")

            cur.execute('Insert into Tracert ( IpAddress, AddressName, Hop) values \
                                            (  "'+ ip +'", "fake", 1);')
            
            cur.execute('select MAX(TraceID) from Tracert')
            TraceID = str(cur.fetchone()[0])
            

            cur.execute('Insert into Measurement (PersonName, IpAddress, TraceID , IpTimestamp) \
                            values ( "'+ user+'", "'+ ip +'", '+ TraceID +', "'+dt_string+'");')

        self.db.commit()
        self._dissconect()

    def select(self):
        self._connect()

        info = []

        with self.db.cursor() as cur:
            
            cur.execute('SELECT * FROM Tracert')
            s1 = cur.fetchall()
            cur.execute('SELECT * FROM Measurement')
            s2 =  cur.fetchall()
            #cur.execute('select * from Measurement join Tracert')
            #join = cur.fetchone()

            if(s1 is not [] and s2 is not []):# and join is not None):

                for i in range(len(s1)):
                    entry = []
                    entry.append(s1[i])
                    entry.append(s2[i])
                    info.append(entry)
                
        self._dissconect()
        print(info)
        return info



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