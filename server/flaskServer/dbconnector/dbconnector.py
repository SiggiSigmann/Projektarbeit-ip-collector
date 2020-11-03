#!/usr/bin/python3

import pymysql
import socket
from datetime import datetime
import threading
import sys

#socket.gethostbyname('db')
class dbconnector:
    
    def __init__(self, address, database, user, pwd):
        self._address = address
        self._database = database
        self._user = user
        self._pwd = pwd
        self.db = None
        self.lock = threading.Lock()

    def _connect(self):
        if self.db is None:
            self.db = pymysql.connect(self._address, self._user, self._pwd, db=self._database)

    def _dissconect(self):
        if self.db is not None:
            self.db.close()
            self.db = None

    def insert(self, user, ip):
        print('insertt', file=sys.stderr)
        self.lock.acquire()
        self._connect()

        with self.db.cursor() as cur:

            #2020-03-04 01:01:01
            now = datetime.now()
            dt_string = now.strftime("%Y-%m-%d %H:%M:%S")

            cur.execute('Insert into Tracert ( IpAddress, AddressName, Hop) values \
                                            (  "'+ ip +'", "start", 0);')
            
            cur.execute('select MAX(TraceID) from Tracert')
            TraceID = str(cur.fetchone()[0])
            

            cur.execute('Insert into Measurement (PersonName, IpAddress, TraceID , IpTimestamp) \
                            values ( "'+ user+'", "'+ ip +'", '+ TraceID +', "'+dt_string+'");')

        self.db.commit()
        self._dissconect()
        self.lock.release()

        return TraceID

    def insertTrace(self, traceID, trace):
        self.lock.acquire()
        self._connect()
        print(trace, file=sys.stderr)
        with self.db.cursor() as cur:

            for tr in range(len(trace)):
                #if tr == 0:
                #    continue

                hop = str(trace[tr][0])
                ipAddress = trace[tr][1]
                name = trace[tr][2]
                cur.execute('Insert into Tracert (TraceID, IpAddress, AddressName, Hop) values \
                                                ( "'+ str(traceID) +'", "'+ ipAddress +'", "'+ name +'",'+ hop+');')

        self.db.commit()
        self._dissconect()
        self.lock.release()

    def select(self):
        print('select', file=sys.stderr)
        self.lock.acquire()
        self._connect()

        info = []

        with self.db.cursor() as cur:
            
            cur.execute('SELECT * FROM Measurement')
            s1 =  cur.fetchall()

            if s1 is []:
                return []

            for mea in s1:
               TraceID =  mea[3]
               #print("TraceID " + str(TraceID),  file=sys.stderr)

               cur.execute('SELECT * FROM Tracert where TraceID = ' + str(TraceID))
               trace =  cur.fetchall()
               info.append([mea, trace])

            #cur.execute('SELECT * FROM Tracert')
            #s1 = cur.fetchall()
            
            #cur.execute('select * from Measurement join Tracert')
            #join = cur.fetchone()

            #if(s1 is not [] and s2 is not []):# and join is not None):

            #    for i in range(len(s1)):
            #        entry = []
            #        entry.append(s1[i])
            #        entry.append(s2[i])
            #        info.append(entry)
                
        self._dissconect()
        self.lock.release()
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