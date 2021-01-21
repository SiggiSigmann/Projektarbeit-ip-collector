#!/usr/bin/python3

import pymysql
import socket
from datetime import datetime
import threading
import sys
import json
import sys

# Database connector
class DBconnector:
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

    #connect to db
    def _connect(self):
        if self.db is None:
            self.db = pymysql.connect(self._address, self._user, self._pwd, db=self._database)

    #dissconect db
    def _dissconect(self):
        if self.db is not None:
            self.db.close()
            self.db = None

    #insert measurement and one trace (needed to get TraceID)
    def insert(self, user, ip, info):
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
            trace_id = str(cur.fetchone()[0])

            #insert new Measurement
            cur.execute('Insert into Measurement (PersonName, IpAddress, TraceID , IpTimestamp, Country, Region, City) \
                            values ( "'+ user+'", "'+ ip +'", '+ trace_id +', "'+dt_string+'", "'+info[0]+'", "'+info[1]+'", "'+info[2]+'");')

        self.db.commit()
        self._dissconect()
        self.lock.release()

        return trace_id

    #insert Trace in Tracert
    def insert_trace(self, trace_id, trace):
        self.lock.acquire()
        self._connect()

        with self.db.cursor() as cur:

            #iterate over given trace
            for tr in range(len(trace)):
                #get info out of tracestep
                hop = str(trace[tr][0])
                ip_address = trace[tr][1]
                name = trace[tr][2]

                #insert
                cur.execute('Insert into Tracert (TraceID, IpAddress, AddressName, Hop) values \
                                                ( "'+ str(trace_id) +'", "'+ ip_address +'", "'+ name +'",'+ hop+');')

        self.db.commit()
        self._dissconect()
        self.lock.release()

    #read data out of DT
    def read(self, name = ""):
        self.lock.acquire()
        self._connect()

        #create json string
        info = '{ "measurements":['
        
        with self.db.cursor() as cur:
            
            #check if filtering needed
            if name == "":
                #read in all Measurement
                cur.execute('SELECT * FROM Measurement order by IpTimestamp desc')
            else:
                cur.execute('SELECT * FROM Measurement WHERE PersonName = "' + name +'" order by IpTimestamp desc')

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

                    info += '"measurement": "' + str((mea[0], mea[1], mea[2], mea[3], str(mea[4]), mea[5], mea[6], mea[7])) + '",'
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
    def get_persons(self):
        self.lock.acquire()
        self._connect()

        #create json string
        info = '{ "persons":['

        with self.db.cursor() as cur:
            #get total amount
            cur.execute('SELECT COUNT(*) From Measurement')
            total =  cur.fetchall()

            info += '{"name":"Total", "number": "'+ str(total[0][0]) +'"},'

            #get all usernames and count entries for it    
            cur.execute('SELECT PersonName, COUNT(*) From Measurement Group by PersonName order by Count(*) DESC')
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

    #get timestamps from measurements per given user
    def get_person_timestamps(self, username = "Total"):
        self.lock.acquire()
        self._connect()

        with self.db.cursor() as cur:
            #get total amount
            if username == "Total":
                #get timestaps orderd by value
                cur.execute('SELECT PersonName, IpTimestamp from Measurement order by IpTimestamp DESC;')
                total =  cur.fetchall()
            else:
                #get timestamps filterd by username / only for one user
                cur.execute('SELECT PersonName, IpTimestamp from Measurement where PersonName = "'+ username +'" order by IpTimestamp DESC;')
                total =  cur.fetchall()

        self._dissconect()
        self.lock.release()

        return total

    #get all ip addresses which user ones owned
    def get_ip_address_distribution(self, username):
        self.lock.acquire()
        self._connect()

        with self.db.cursor() as cur:
            #get total amount
            if username == "Total":
                cur.execute('SELECT IpAddress, count(IpAddress) from Measurement group by IpAddress order by count(IpAddress) DESC;')
                total =  cur.fetchall()
            else:
                cur.execute('SELECT IpAddress, count(IpAddress)  from Measurement where PersonName = "'+ username +'"group by IpAddress order by count(IpAddress) DESC;')
                total =  cur.fetchall()

        self._dissconect()
        self.lock.release()

        return total

    #get all ip addresses which occures in trace for given user
    def get_ip_address_in_trace_distribution(self, username):
        self.lock.acquire()
        self._connect()

        with self.db.cursor() as cur:
            #get total amount
            if username == "Total":
                cur.execute('SELECT Tracert.IpAddress, count(Tracert.IpAddress)  FROM   Tracert   JOIN Measurement ON Measurement.TraceID = Tracert.TraceID group by Tracert.IpAddress order by count(Tracert.IpAddress) DESC;')
                total =  cur.fetchall()
            else:
                cur.execute('SELECT Tracert.IpAddress, count(Tracert.IpAddress)  FROM   Tracert   JOIN Measurement ON Measurement.TraceID = Tracert.TraceID where Measurement.PersonName  = "'+username+'" group by Tracert.IpAddress order by count(Tracert.IpAddress) DESC;')
                total =  cur.fetchall()

        self._dissconect()
        self.lock.release()

        return total

        #get all ip addresses which occures in trace for given user
    
    #get ip with timestamps
    def get_ip_and_time(self, username):
        self.lock.acquire()
        self._connect()

        with self.db.cursor() as cur:
            #get total amount
            if username == "Total":
                cur.execute('SELECT IpAddress, IpTimestamp FROM Measurement;')
                total =  cur.fetchall()
            else:
                cur.execute('SELECT IpAddress, IpTimestamp FROM Measurement where PersonName  = "'+username+'";')
                total =  cur.fetchall()

        self._dissconect()
        self.lock.release()

        return total

    #get ip with timestamps from trace
    def get_ip_and_time_trace(self, username):
        self.lock.acquire()
        self._connect()

        with self.db.cursor() as cur:
            #get total amount
            if username == "Total":
                cur.execute('SELECT Tracert.IpAddress, Measurement.IpTimestamp FROM Tracert JOIN Measurement ON Measurement.TraceID = Tracert.TraceID;')
                total =  cur.fetchall()
            else:
                cur.execute('SELECT Tracert.IpAddress, Measurement.IpTimestamp FROM Tracert JOIN Measurement ON Measurement.TraceID = Tracert.TraceID where Measurement.PersonName  = "'+username+'";')
                total =  cur.fetchall()

        self._dissconect()
        self.lock.release()

        return total

    #get ip sorted by time
    def get_ip_sorted_by_time(self, username):
        self.lock.acquire()
        self._connect()

        with self.db.cursor() as cur:
            #get total amount
            if username == "Total":
                cur.execute('select IpAddress from Measurement order by IpTimestamp;')
                total =  cur.fetchall()
            else:
                cur.execute('select IpAddress from Measurement where PersonName = "'+ username +'" order by IpTimestamp;')
                total =  cur.fetchall()

        self._dissconect()
        self.lock.release()

        return total

    #get ip sorted by time
    def get_ip_and_time_sorted(self, username):
        self.lock.acquire()
        self._connect()

        with self.db.cursor() as cur:
            #get total amount
            if username == "Total":
                cur.execute('select IpAddress, IpTimestamp from Measurement order by IpTimestamp;')
                total =  cur.fetchall()
            else:
                cur.execute('select IpAddress, IpTimestamp from Measurement where PersonName = "'+ username +'" order by IpTimestamp;')
                total =  cur.fetchall()

        self._dissconect()
        self.lock.release()

        return total

    #get user for ip
    def get_user_distribution_for_ip(self, ip):
        self.lock.acquire()
        self._connect()

        with self.db.cursor() as cur:
            #get total amount
            cur.execute('Select PersonName, count(PersonName) From Measurement where IpAddress = "'+ip+'" group by PersonName order by count(*) DESC;')
            total =  cur.fetchall()

        self._dissconect()
        self.lock.release()

        return total

    #get distribution of citys
    def get_city_distribution(self, username):
        self.lock.acquire()
        self._connect()

        with self.db.cursor() as cur:
            #get total amount
            if username == "Total":
                cur.execute('SELECT City, count(City) from Measurement group by City order by count(City) DESC;')
                total =  cur.fetchall()
            else:
                cur.execute('SELECT City, count(City)  from Measurement where PersonName = "'+ username +'"group by City order by count(City) DESC;')
                total =  cur.fetchall()

        self._dissconect()
        self.lock.release()

        return total

    #get city sorted by time
    def get_city_sorted(self, username):
        self.lock.acquire()
        self._connect()

        with self.db.cursor() as cur:
            #get total amount
            if username == "Total":
                cur.execute('SELECT City from Measurement order by IpTimestamp;')
                total =  cur.fetchall()
            else:
                cur.execute('SELECT City from Measurement where PersonName = "'+ username +'" order by IpTimestamp;')
                total =  cur.fetchall()

        self._dissconect()
        self.lock.release()

        return total

    #get ip address and city wher it was located
    def get_ip_and_city(self, username):
        self.lock.acquire()
        self._connect()

        with self.db.cursor() as cur:
            #get total amount
            if username == "Total":
                cur.execute('SELECT IpAddress, City FROM Measurement;')
                total =  cur.fetchall()
            else:
                cur.execute('SELECT IpAddress, City FROM Measurement where PersonName  = "'+username+'";')
                total =  cur.fetchall()

        self._dissconect()
        self.lock.release()

        return total

    #get city and when user was there
    def get_city_time(self, username):
        self.lock.acquire()
        self._connect()

        with self.db.cursor() as cur:
            #get total amount
            if username == "Total":
                cur.execute('SELECT City, IpTimestamp FROM Measurement order by IpTimestamp DESC;')
                total =  cur.fetchall()
            else:
                cur.execute('SELECT City, IpTimestamp FROM Measurement where PersonName  = "'+username+'" order by IpTimestamp DESC;')
                total =  cur.fetchall()

        self._dissconect()
        self.lock.release()

        return total

    def get_measurements_per_day_last_20(self):
        self.lock.acquire()
        self._connect()

        with self.db.cursor() as cur:
            #get total amount
            
            cur.execute('select PersonName, datediff(now(), date(IpTimestamp)) as dist, count(IpAddress) from Measurement where IpTimestamp > DATE_SUB(now(), INTERVAL 19 DAY) group by dist, PersonName order by PersonName, dist;')
            total =  cur.fetchall()
            

        self._dissconect()
        self.lock.release()

        return total