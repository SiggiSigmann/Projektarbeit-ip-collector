import io
import random
import sys
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import dbconnector.dbconnector as dbcon
import json

class Plotter():
    def __init__(self, datadb):
        self.datadb = datadb

    def get_Json(self, user):
        return json.loads('{"images":[{"url": "/image/'+user+'_0.png", "alt":"Hour", "height":400, "width":400, "description":"Shows distance between measurements"}, '+\
                                     '{"url": "/image/'+user+'_1.png", "alt":"Day", "height":400, "width":400, "description":"Shows how many measurements where done per ay"}, '+\
                                     '{"url": "/image/'+user+'_2.png", "alt":"IpAdresses", "height":400, "width":400, "description":"Shows distribution of IP-Adresses of the Users device"},'+\
                                     '{"url": "/image/'+user+'_3.png", "alt":"IpAdresses in Trace", "height":400, "width":400, "description":"Shows distribution of IP-Adresses in Trace"}'+\
                                     ']}')

    def _create_random_figure(self):
        fig = Figure()
        axis = fig.add_subplot(1, 1, 1)
        xs = range(100)
        ys = [random.randint(1, 50) for x in xs]
        axis.set_title('Smarts')
        axis.set_xlabel('Probability')
        axis.set_ylabel('Histogram of IQ')
        axis.plot(xs, ys)
        return fig

    def hour_based_figure(self, person, start=0, stop=0):
        timestamps = self.datadb.getTimestamps(person)
        ys_total=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        ys=[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
        xs=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
        for i in range(0,len(timestamps)-2):
            t1 = int(timestamps[i][1].strftime("%H"))
            t2 = int(timestamps[i+1][1].strftime("%H"))

            idx = abs(t2-t1)
            ys_total[idx] = ys_total[idx]+1

        sum_total = sum(ys_total)
        for i in range(len(ys_total)-1):
            ys[i] = ys_total[i] / sum_total

        fig = Figure()
        axis = fig.add_subplot(1, 1, 1)
        axis.set_title('Time between measurement (hour based)')
        axis.set_xlabel('Distance')
        axis.set_ylabel('Amount')
        axis.bar(xs, ys, 1)
        axis.set_xticks(xs)
        axis.set_xticklabels(xs)
        return fig

    def dmeasurement_per_day(self, person, start=0, stop=0):
        timestamps = self.datadb.getTimestamps(person)
        ys=[0,0,0,0,0,0,0]
        xs=[0,1,2,3,4,5,6]

        for i in range(0,len(timestamps)-1):
            twday = int(timestamps[i][1].strftime("%w"))
            ys[twday] = ys[twday]+1

        fig = Figure()
        axis = fig.add_subplot(1, 1, 1)
        axis.set_title('Measurement Day')
        axis.set_xlabel('Day')
        axis.set_ylabel('Amount')
        axis.bar(xs, ys)
        axis.set_xticks(xs)
        axis.set_xticklabels(["Sunday","Mondayc","Tuesday","Wednesday","Thursday","Friday","Saturday",])
        return fig

    def ip_distribution(self, person):
        timestamps = self.datadb.getIPAdress(person)
        labels = []
        size = []

        for i in timestamps:
            labels.append(i[0])
            size.append(i[1])
        
        # Pie chart, where the slices will be ordered and plotted counter-clockwise:
        fig = Figure()
        axis = fig.add_subplot(1, 1, 1)
        axis.pie(size, labels=labels, autopct='%1.2f%%',  startangle=90)
        axis.axis('equal')
        return fig

    def ip_distribution_trace(self, person):
        timestamps = self.datadb.getIPAdressInTrace(person)
        labels = []
        size = []

        for i in timestamps:
            labels.append(i[0])
            size.append(i[1])

        # Pie chart, where the slices will be ordered and plotted counter-clockwise:
        fig = Figure()
        axis = fig.add_subplot(1, 1, 1)
        axis.pie(size, labels=labels, autopct='%1.2f%%',  startangle=90)
        axis.axis('equal')
        return fig


    def create_image(self, image_name):
        #0: name (total => all, name => only for this person)
        #1: diagramtype
        #2: start timestamp (optinal)
        #3: stop timestamp (optinal)
        parts = image_name.split('_')
        end = parts[-1].split(".")
        parts[-1] = end[0]
        
        last = parts[-1]
        for i in range(4-len(parts)):
            parts.append("0")

        print(parts, file=sys.stderr)
        fig = Figure()
        if(parts[1] == "0"):
            fig = self.hour_based_figure(parts[0])
        elif(parts[1] == "1"):
            fig = self.dmeasurement_per_day(parts[0])
        elif(parts[1] == "2"):
            fig = self.ip_distribution(parts[0])
        elif(parts[1] == "3"):
            fig = self.ip_distribution_trace(parts[0])
        else:
            fig = self._create_random_figure()

        return fig



        


