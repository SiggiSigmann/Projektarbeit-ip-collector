import io
import random
import sys
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import dbconnector.dbconnector as dbcon
import json
import matplotlib.pyplot as plt
from matplotlib import rcParams
from subnetze import Subnetze

class Plotter():
    def __init__(self, datadb):
        self.datadb = datadb
        self.sub = Subnetze("/files/de.csv")
        plt.style.use('dark_background')
        rcParams.update({'figure.autolayout': True})

    #create diagram corresponding to filename
    def create_image(self, image_name):
        #0: name (total => all, name => only for this person)
        #1: diagramtype
        #e.g. Total_2.png

        #split filename
        parts = image_name.split('_')
        end = parts[-1].split(".")
        fig_number = int(end[0])

        #creat plot
        fig = Figure()
        if(fig_number == 0):
            fig = self.hour_based_figure(parts[0])
        elif(fig_number == 1):
            fig = self.measurement_per_day(parts[0])
        elif(fig_number == 2):
            fig = self.ip_distribution(parts[0])
        elif(fig_number == 3):
            fig = self.ip_distribution_trace(parts[0])
        elif(fig_number == 4):
            fig = self.ip_distribution_ip_ownder(parts[0])
        elif(fig_number == 5):
            fig = self.ip_distribution_trace_ownder(parts[0])
        elif(fig_number== 6):
            fig = self.ip_distribution_ip_ownder_alt(parts[0])
        elif(fig_number == 7):
            fig = self.ip_distribution_trace_ownder_alt(parts[0])
        else:
            fig = self._create_random_figure()

        plt.close('all')

        return fig

    #create rondom plot
    def _create_random_figure(self):
        fig, axis = plt.subplots()
        xs = range(100)
        ys = [random.randint(1, 50) for x in xs]
        #axis.set_title('Smarts')
        axis.set_xlabel('Probability')
        axis.set_ylabel('Histogram of IQ')
        axis.plot(xs, ys)
        return fig

    #create plot that shows time between measurements
    def hour_based_figure(self, person):
        #get timestamps from db
        timestamps = self.datadb.get_timestamps(person)

        #init count array
        total_count=[0 for i in range(24)] 
        

        #calculate difference between two timestamps and count 
        for i in range(0,len(timestamps)-2):
            t1 = int(timestamps[i][1].strftime("%H"))
            t2 = int(timestamps[i+1][1].strftime("%H"))

            idx = abs(t2-t1)
            total_count[idx] = total_count[idx]+1


        #calc percentage per entry
        values=[0.0 for i in range(24)] 
        sum_total = sum(total_count)
        
        #avoide devicion with 0
        if sum_total == 0:
            values = total_count
        else:
            #calc percentage
            for i in range(len(total_count)-1):
                values[i] = total_count[i] / sum_total

        #create label
        labels=[i for i in range(24)]

        #create figure
        fig, axis = plt.subplots()
        axis.bar(labels, values)

        #description
        #axis.set_title('Time between measurements (hour based)')
        axis.set_xlabel('Distance')
        axis.set_ylabel('Percent')

        #set how many lables where needed and text for it
        axis.set_xticks(labels)
        axis.set_xticklabels(labels)

        return fig

    #create plot to display how many measurements where made per day of the week
    def measurement_per_day(self, person, start=0, stop=0):
        timestamps = self.datadb.get_timestamps(person)
        total_count=[0 for i in range(7)] 

        #count weekdays
        for i in range(0,len(timestamps)-1):
            twday = int(timestamps[i][1].strftime("%w"))
            total_count[twday] = total_count[twday]+1

        #calc percentage per entry
        values=[0.0 for i in range(7)] 
        sum_total = sum(total_count)
        
        #avoide devicion with 0
        if sum_total == 0:
            values = total_count
        else:
            #calc percentage
            for i in range(len(total_count)-1):
                values[i] = total_count[i] / sum_total

        #create label
        labels=[i for i in range(7)]

        #create figure
        fig, axis = plt.subplots()
        axis.bar(labels, values)

        #description
        #axis.set_title('Measurement Day')
        #axis.set_xlabel('Week Day')
        axis.set_ylabel('Percent')

        #set how many lables where needed and text for it
        axis.set_xticks(labels)
        axis.set_xticklabels(["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday",])

        return fig

    #create diagram which shows ip adresses of the user and how often it was used
    def ip_distribution(self, person):
        timestamps = self.datadb.get_ip_address(person)
        label = []
        total = []

        #fill array
        for i in timestamps:
            label.append(i[0])
            total.append(i[1])
        
        #calc percentage per entry
        values=[0.0 for i in range(len(total))] 
        sum_total = sum(total)
        
        #avoide devicion with 0
        if sum_total == 0:
            values = total
        else:

            #calc percentage
            for i in range(len(total)-1):
                values[i] = total[i] / sum_total

        #check if to big
        if(len(values) > 20):
            label=label[:20]
            values=values[:20]

        #create figure
        fig, axis = plt.subplots()
        axis.barh(range(len(label)), values)

        #description
        #axis.set_title('IP Addresses form user')
        axis.set_xlabel('Percent')
        #axis.set_ylabel('Addresses')

        #set how many lables where needed and text for it
        axis.set_yticks(range(len(label)))
        axis.set_yticklabels(label)

        return fig

    #create plot which shows ip adresses in trace and amount
    def ip_distribution_trace(self, person):
        trace_ip = self.datadb.get_ip_address_in_trace(person)
        own_ip = self.datadb.get_ip_address(person)

        ips = []
        for i in own_ip:
            ips.append(i[0])

        label = []
        total = []

        for i in trace_ip:
            if i[0] in ips: continue
            if i[0] == "-": continue
            label.append(i[0])
            total.append(i[1])

        #calc percentage per entry
        values=[0.0 for i in range(len(total))] 
        sum_total = sum(total)
        
        #avoide devicion with 0
        if sum_total == 0:
            values = total
        else:
            #calc percentage
            for i in range(len(total)-1):
                values[i] = total[i] / sum_total

        #check if to big
        if(len(values) > 20):
            label=label[:20]
            values=values[:20]

        #create figure
        fig, axis = plt.subplots()
        axis.barh(range(len(label)), values)

        #description
        #axis.set_title('IP-Addresses in trace')
        axis.set_xlabel('Percent')
        #axis.set_ylabel('Addresses')

        #set how many lables where needed and text for it
        axis.set_yticks(range(len(label)))
        axis.set_yticklabels(label)

        return fig

    #create diagram which shows distribution of ISP of the end addresses
    def ip_distribution_ip_ownder(self, person):
        timestamps = self.datadb.get_ip_address(person)
        labels_old = []
        size_old = []

        for i in timestamps:
            if i[0] == "-": continue
            labels_old.append(i[0])
            size_old.append(i[1])

        label = []
        size = []
        for i in range(len(labels_old)):
            owner = self.sub.find_Ownder(labels_old[i])
            if owner not in label:
                label.append(owner)
                size.append(size_old[i])
            else:
                idx = label.index(owner)
                size[idx] += size_old[i]

        #calc percentage per entry
        values=[0.0 for i in range(len(size))] 
        sum_total = sum(size)
        
        #avoide devicion with 0
        if sum_total == 0:
            values = size
        else:
            #calc percentage
            for i in range(len(size)-1):
                values[i] = size[i] / sum_total

        #check if to big
        if(len(values) > 20):
            label=label[:20]
            values=values[:20]

        #create figure
        fig, axis = plt.subplots()
        axis.barh(range(len(label)), values)

        #description
        #axis.set_title('ISP\'s of IP-Addresses')
        axis.set_xlabel('Percent')

        #set how many lables where needed and text for it
        axis.set_yticks(range(len(label)))
        axis.set_yticklabels(label)

        return fig

    #create diagram which shows distribution of ISP of the trace addresses
    def ip_distribution_trace_ownder(self, person):
        timestamps = self.datadb.get_ip_address_in_trace(person)
        own_ip = self.datadb.get_ip_address(person)

        ips = []
        for i in own_ip:
            ips.append(i[0])

        labels_old = []
        size_old = []

        for i in timestamps:
            if i[0] in ips: continue
            if i[0] == "-": continue
            labels_old.append(i[0])
            size_old.append(i[1])

        label = []
        size = []
        for i in range(len(labels_old)):
            owner = self.sub.find_Ownder(labels_old[i])
            if owner not in label:
                label.append(owner)
                size.append(size_old[i])
            else:
                idx = label.index(owner)
                size[idx] += size_old[i]

        #calc percentage per entry
        values=[0.0 for i in range(len(size))] 
        sum_total = sum(size)
        
        #avoide devicion with 0
        if sum_total == 0:
            values = size
        else:
            #calc percentage
            for i in range(len(size)-1):
                values[i] = size[i] / sum_total

        #check if to big
        if(len(values) > 20):
            label=label[:20]
            values=values[:20]

        #create figure
        fig, axis = plt.subplots()
        axis.barh(range(len(label)), values)

        #description
        #axis.set_title('ISP\'s of IP-Addresses in Trace')
        axis.set_xlabel('Percent')

        #set how many lables where needed and text for it
        axis.set_yticks(range(len(label)))
        axis.set_yticklabels(label)

        return fig

    """def ip_distribution_ip_ownder_alt(self, person):
        timestamps = self.datadb.get_ip_address(person)
        labels_old = []
        size_old = []

        for i in timestamps:
            if i[0] == "-": continue
            labels_old.append(i[0])
            size_old.append(i[1])

        label = []
        size = []
        for i in range(len(labels_old)):
            owner = self.sub.find_Ownder_alt(labels_old[i])
            if owner not in label:
                label.append(owner)
                size.append(size_old[i])
            else:
                idx = label.index(owner)
                size[idx] += size_old[i]

        #print(label , file=sys.stderr)


        # Pie chart, where the slices will be ordered and plotted counter-clockwise:
        fig, axis = plt.subplots()

        #axis.pie(size, labels=label, autopct='%1.2f%%',  startangle=90, rotatelabels = True)
        axis.barh(range(len(label)), size, tick_label=label)
        #axis.axis('equal')
        return fig
    def ip_distribution_trace_ownder_alt(self, person):
        timestamps = self.datadb.get_ip_address_in_trace(person)
        labels_old = []
        size_old = []

        for i in timestamps:
            if i[0] == "-": continue
            labels_old.append(i[0])
            size_old.append(i[1])

        label = []
        size = []
        for i in range(len(labels_old)):
            owner = self.sub.find_Ownder_alt(labels_old[i])
            if owner not in label:
                label.append(owner)
                size.append(size_old[i])
            else:
                idx = label.index(owner)
                size[idx] += size_old[i]

        #print(label , file=sys.stderr)


        # Pie chart, where the slices will be ordered and plotted counter-clockwise:
        fig, axis = plt.subplots()
        #axis.pie(size, labels=label, autopct='%1.2f%%',  startangle=90, rotatelabels = True)
        axis.barh(range(len(label)), size, tick_label=label)
        #axis.axis('equal')
        return fig"""

    #get json which descripes possible images and description for the iages
    def get_Json(self, user):
        return json.loads(\
            '{"images":['+\
                '{"url": "/image/'+user+'_0.png", "alt":"Hour", "description":"Shows how frequently measurements were taken. e.g. 1 and 0.6 means, 60% of the measurements were taken one hour apart."} '+\
                ',{"url": "/image/'+user+'_1.png", "alt":"Day", "description":"Shows how many measurements were done per week day."} '+\
                ',{"url": "/image/'+user+'_2.png", "alt":"IpAddresses", "description":"Shows distribution of IP-End-Addresses of the user\'s device."}'+\
                ',{"url": "/image/'+user+'_3.png", "alt":"IpAddresses in Trace", "description":"Shows different IP-Addresses of the route to the user captured by trace."}'+\
                ',{"url": "/image/'+user+'_4.png", "alt":"Subnet IP-Addresses", "description":"Shows ISP of the IP-End-Addresses of the user\'s device."}'+\
                ',{"url": "/image/'+user+'_5.png", "alt":"Subnet IP-Addresses trace", "description":"Shows ISP of the IP-Addresses of the route to the user captured by trace."}'+\
                #',{"url": "/image/'+user+'_6.png", "alt":"Subnet IP-Addresses", "description":"Show IP ownder duration"}'+\
                #',{"url": "/image/'+user+'_7.png", "alt":"Subnet IP-Addresses trace", "description":"Show IP ownder duration of trace"}'+\
                ']}'\
        )

    #create compare json from the get_Json method 
    def get_compare_json(self, user1, user2):
        j = self.get_Json(user1)
        new_j = []

        #ad url1 to each image entry in the json
        for i in j['images']:
            val = i['url']
            i['url1'] = "/image/" + user2 + val[-6:]
            new_j.append(i)
        j['images'] = new_j

        return j
