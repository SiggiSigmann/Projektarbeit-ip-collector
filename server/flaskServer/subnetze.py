import csv
from ipaddress import IPv4Address
import sys
import requests
import json

#get infromation about subnet form csv file
#source: #https://www.nirsoft.net/countryip/de.html
class Subnetze():
    def __init__(self, path):
        self.path = path
        self.loadFile()

    #cload csv and split entries
    #store data from file in self.data
    def loadFile(self):
        self.data = []
        #print(self.data , file=sys.stderr)
        with open(self.path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            
            
            for row in csv_reader:
                entry = []
                i = 0
                for part in row:
                    if i == 0:
                        entry.append(IPv4Address(part))
                    elif i == 1:
                        entry.append(IPv4Address(part))
                    elif i == 2:
                        entry.append(int(part))
                    else:
                        entry.append(part)

                    i+=1

                self.data.append(entry)

    #get informations about ip addresses based on csv file loaded before
    def find_Ownder(self, ip):
        ipAddress = IPv4Address(ip)
        for i in self.data:
            if (i[0] >= ipAddress) or (ipAddress <= i[1]):
                if(i[4] == ''):
                    return str(i[0]) +" "+ str(i[1])
                return i[4]
        return "not found"

    """def find_Ownder_alt(self, ip):
        r = requests.get(f"http://ip-api.com/json/{ip}")
        return str(r.json().get("isp", "empty"))"""

        

