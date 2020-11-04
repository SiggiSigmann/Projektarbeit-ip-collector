#!/usr/bin/python3

import pymysql
import socket
from datetime import datetime
import threading
import sys
import json

# Database connector
class dbconnector:
    
    def __init__(self, address, database, user, pwd):
        self._address = address
        self._database = database
        self._user = user
        self._pwd = pwd
        self.db = None
        self.lock = threading.Lock()

        #check connection
        #will restart docker when fail
        self._connect()
        self._dissconect()

    def _connect(self):
        if self.db is None:
            self.db = pymysql.connect(self._address, self._user, self._pwd, db=self._database)

    def _dissconect(self):
        if self.db is not None:
            self.db.close()
            self.db = None

    #insert measurement and one trace (needed to get TraceID)
    def insert(self, user, ip):
        self.lock.acquire()
        self._connect()

        with self.db.cursor() as cur:

            #get Date and time  (2020-11-04 10:40:00)
            now = datetime.now()
            dt_string = now.strftime("%Y-%m-%d %H:%M:%S")

            #insert new entry in Tracert
            cur.execute('Insert into Tracert ( IpAddress, AddressName, Hop) values \
                                            (  "'+ ip +'", "start", 0);')
            
            #get new TraceID
            cur.execute('select MAX(TraceID) from Tracert')
            TraceID = str(cur.fetchone()[0])
            
            #insert new Measurement
            cur.execute('Insert into Measurement (PersonName, IpAddress, TraceID , IpTimestamp) \
                            values ( "'+ user+'", "'+ ip +'", '+ TraceID +', "'+dt_string+'");')

        self.db.commit()
        self._dissconect()
        self.lock.release()

        return TraceID

    #insert Trace in Tracert
    def insertTrace(self, traceID, trace):
        self.lock.acquire()
        self._connect()

        with self.db.cursor() as cur:

            #iterate over given trace
            for tr in range(len(trace)):
                #get info out of tracestep
                hop = str(trace[tr][0])
                ipAddress = trace[tr][1]
                name = trace[tr][2]

                #insert
                cur.execute('Insert into Tracert (TraceID, IpAddress, AddressName, Hop) values \
                                                ( "'+ str(traceID) +'", "'+ ipAddress +'", "'+ name +'",'+ hop+');')

        self.db.commit()
        self._dissconect()
        self.lock.release()

    #read data out of DT
    def read(self):
        self.lock.acquire()
        self._connect()

        #create json string
        info = '{ "measurements":['
        
        with self.db.cursor() as cur:
            #read in all Measurement
            cur.execute('SELECT * FROM Measurement')
            measurement =  cur.fetchall()

            #check if emty
            if measurement is []:
                info = '{ "measurements":[]}'

            elif measurement == ():
                info = '{ "measurements":[]}'

            else:
                #itterate over Measurements
                for mea in measurement:
                    info += '{'

                    #get TraceID
                    TraceID =  mea[3]

                    #read all Tracertes with TraceID
                    cur.execute('SELECT * FROM Tracert where TraceID = ' + str(TraceID))
                    trace =  cur.fetchall()

                    info += '"measurement": "' + str((mea[0], mea[1], mea[2], mea[3], str(mea[4]))) + '",'
                    info += '"traces": ['
                    
                    #insert all Tracesteps in json
                    for tr in trace:
                        info += '"' + str(tr) + '",'
                    info = info[:-1]
                    info += ']},'

                #close json   
                info = info[:-1]
                info += ']}'
             
            #create json out of string
            info = json.loads(info)

                
        self._dissconect()
        self.lock.release()
        return info

    #get amount of entries per user
    def getpersondata(self):
        self.lock.acquire()
        self._connect()

        #create json string
        info = '{ "persons":['

        with self.db.cursor() as cur:
            #get all usernames and count entries for it    
            cur.execute('SELECT PersonName, COUNT(*) From Measurement Group by PersonName')
            measurement =  cur.fetchall()

            #check if emty
            if measurement is []:
                info = '{ "persons":[]}'
            elif measurement == ():
                info = '{ "persons":[]}'

            else:
                for mea in measurement:
                    info += '{'

                    #get infos from select statement
                    Personname =  mea[0]
                    number =  mea[1]

                    #add to json string
                    info += '"name": "' + str(Personname) + '",'
                    info += '"number": "' + str(number) + '"'
                    info += '},'

                info = info[:-1]
                info += ']}'
             
            #creat json out of string
            info = json.loads(info)
  
        self._dissconect()
        self.lock.release()

        return info
