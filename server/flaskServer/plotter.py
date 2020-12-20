import io
import random
import sys
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import dbconnector.dbconnector as dbcon

class Plotter():
    def __init__(self, datadb):
        self.datadb = datadb

    def create_random_figure(self):
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
        print(timestamps , file=sys.stderr)
        ys=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        for i in range(0,len(timestamps)-2):
            t1 = int(timestamps[i][1].strftime("%H"))
            t2 = int(timestamps[i+1][1].strftime("%H"))

            idx = abs(t2-t1)
            ys[idx] = ys[idx]+1

        
        fig = Figure()
        axis = fig.add_subplot(1, 1, 1)
        xs=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,17,18,19,20,21,22,23]
        print(ys , file=sys.stderr)
        print(xs , file=sys.stderr)
        axis.set_title('Time between measurement (hour based)')
        axis.set_xlabel('Distance')
        axis.set_ylabel('Amount')
        axis.bar(xs, ys, 1)
        axis.set_xticks(xs, range(max(ys)))

        return fig

    def dmeasurement_per_day(self, person, start=0, stop=0):
        timestamps = self.datadb.getTimestamps(person)
        print(timestamps , file=sys.stderr)
        ys=[0,0,0,0,0,0,0]
        for i in range(0,len(timestamps)-1):
            twday = int(timestamps[i][1].strftime("%w"))
            ys[twday] = ys[twday]+1

        
        fig = Figure()
        axis = fig.add_subplot(1, 1, 1)
        xs=[0,1,2,3,4,5,6]
        print(ys , file=sys.stderr)
        print(xs , file=sys.stderr)
        axis.set_title('Measurement Day')
        axis.set_xlabel('Day')
        axis.set_ylabel('Amount')
        axis.bar(xs, ys, 1)
        axis.set_xticks(xs, range(max(ys)))

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
            fig = self.create_random_figure()
        else:
            fig = self.create_random_figure()

        return fig


        


