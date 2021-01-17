import io
import random
import sys
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import dbconnector.dbconnector as dbcon
import json
import matplotlib 
import matplotlib.pyplot as plt
from matplotlib import rcParams
from subnetze import Subnetze
import networkx as nx

###
# create plots for website
###
class Plotter():
    def __init__(self, datadb, subnet):
        self.datadb = datadb
        self.sub = subnet
        rcParams.update({'figure.autolayout': True})
        size = 8
        matplotlib.rc('xtick', labelsize=size) 
        matplotlib.rc('ytick', labelsize=size) 

    #create diagram corresponding to filename
    def create_image(self, image_name, dark = 1):
        if dark:
            plt.style.use('dark_background')
            rcParams.update({'figure.autolayout': True})
        else:
            plt.style.use('default')
            rcParams.update({'figure.autolayout': True})
        #0: name (total => all, name => only for this person)
        #1: diagramtype
        #2: diagramsubtype
        #e.g. Total_2_2.png

        #split filename
        parts = image_name.split('_')
        end = parts[-1].split(".")
        fig_number = int(parts[1])
        fig_subplot =int(end[0])

        #creat plot
        fig = Figure()
        if(fig_number == 0):
            if(fig_subplot == 0):
                fig = self.hour_based_figure(parts[0])
            elif(fig_subplot == 1):
                fig = self.measurement_per_day(parts[0])
            elif(fig_subplot == 2):
                fig = self.measurement_per_hour(parts[0])
            else:
                fig = self._create_random_figure()

        elif(fig_number == 1):
            if(fig_subplot == 0):
                fig = self.ip_distribution(parts[0])
            elif(fig_subplot == 1):
                fig = self.ip_distribution_trace(parts[0])
            elif(fig_subplot == 2):
                fig = self.ip_distribution_ip_ownder(parts[0])
            elif(fig_subplot == 3):
                fig = self.ip_distribution_trace_ownder(parts[0])
            else:
                fig = self._create_random_figure()

        elif(fig_number == 2):
            if(fig_subplot== 0):
                fig = self.ip_time_comparison(parts[0])
            elif(fig_subplot == 1):
                fig = self.ip_time_comparison_trace(parts[0])
            elif(fig_subplot== 2):
                fig = self.subnet_time_comparison(parts[0])
            else:
                fig = self._create_random_figure()

        elif(fig_number == 3):
            if(fig_subplot == 0):
                fig = self.ip_change(parts[0])
            elif(fig_subplot== 1):
                fig = self.ip_change_time(parts[0])
            elif(fig_subplot== 2):
                fig = self.ip_change_time_color(parts[0])
            elif(fig_subplot== 3):
                fig = self.subnet_change(parts[0])
            elif(fig_subplot == 4):
                fig = self.subnet_change_graph(parts[0], dark)
            elif(fig_subplot == 5):
                fig = self.subnet_change_time(parts[0])
            else:
                fig = self._create_random_figure()

        elif(fig_number == 4):
            if(fig_subplot == 0):
                fig = self.city_vs_time(parts[0])
            elif(fig_subplot== 1):
                fig = self.city_vs_ip(parts[0])
            elif(fig_subplot== 2):
                fig = self.city_graph(parts[0], dark)
            elif(fig_subplot== 3):
                fig = self.city_isp(parts[0])
            else:
                fig = self._create_random_figure()

        else:
            fig = self._create_random_figure()

        plt.close('all')

        return fig

    #create rondom plot
    def _create_random_figure(self, person="total", dark=1):
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
        for i in range(0,len(timestamps)-1):
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
            for i in range(len(total_count)):
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
        for i in range(0,len(timestamps)):
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
            for i in range(len(total_count)):
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

    #create a plot which sohows measurement per hour
    def measurement_per_hour(self, person):
        #get timestamps from db
        timestamps = self.datadb.get_timestamps(person)

        #init count array
        total_count=[0 for i in range(24)] 
        

        #calculate difference between two timestamps and count 
        for i in range(0,len(timestamps)):
            t1 = int(timestamps[i][1].strftime("%H"))

            idx = t1
            total_count[idx] = total_count[idx]+1


        #calc percentage per entry
        values=[0.0 for i in range(24)] 
        sum_total = sum(total_count)
        
        #avoide devicion with 0
        if sum_total == 0:
            values = total_count
        else:
            #calc percentage
            for i in range(len(total_count)):
                values[i] = total_count[i] / sum_total

        #create label
        labels=[i for i in range(24)]

        #create figure
        fig, axis = plt.subplots()
        axis.bar(labels, values)

        #description
        #axis.set_title('Time between measurements (hour based)')
        axis.set_xlabel('Time')
        axis.set_ylabel('Percent')

        #set how many lables where needed and text for it
        axis.set_xticks(labels)
        axis.set_xticklabels(labels)

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
            for i in range(len(total)):
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
            if i[0] == '-' : continue
            ips.append(i[0])

        label = []
        total = []

        for i in trace_ip:
            if i[0] in ips: continue
            if i[0] == '-': continue
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
            for i in range(len(total)):
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
            if i[0] == '-': continue
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
            for i in range(len(size)):
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
            if i[0] == '-' : continue
            ips.append(i[0])

        labels_old = []
        size_old = []

        for i in timestamps:
            if i[0] in ips: continue
            if i[0] == '-': continue
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
            for i in range(len(size)):
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

    #create ip vs time graph
    def ip_time_comparison(self, person):
        timestamps = self.datadb.get_ip_and_time(person)

        label = []
        x = [0 for i in range(len(timestamps))]
        y = [0 for i in range(len(timestamps))]

        #calculate x,y coordinates for dots
        idx = 0
        for i in timestamps:
            if i[0] not in label:
                label.append(i[0])

            time = int(i[1].strftime("%H"))

            x[idx] = time
            y[idx] = label.index(i[0])

            idx += 1

        #create figure
        fig, axis = plt.subplots()
        axis.scatter(x,y)

        #description
        #axis.set_title('ISP\'s of IP-Addresses in Trace')
        axis.set_xlabel('Hour')

        #set how many lables where needed and text for it
        axis.set_yticks(range(len(label)))
        axis.set_yticklabels(label)

        axis.set_xticks(range(24))
        axis.set_xticklabels(range(24))

        return fig

    #create ip in trace vs time
    def ip_time_comparison_trace(self, person):
        timestamps = self.datadb.get_ip_and_time_trace(person)
        own_ip = self.datadb.get_ip_address(person)
        ips = []
        for i in own_ip:
            if i[0] == '-' : continue
            ips.append(i[0])

        label = []
        x = [0 for i in range(len(timestamps))]
        y = [0 for i in range(len(timestamps))]

        #calculate x,y coordinates for dots
        idx = 0
        for i in timestamps:
            if i[0] in ips: continue
            if i[0] not in label:
                label.append(i[0])

            time = int(i[1].strftime("%H"))

            x[idx] = time
            y[idx] = label.index(i[0])

            idx += 1

        #create figure
        fig, axis = plt.subplots()
        axis.scatter(x,y)

        #description
        #axis.set_title('ISP\'s of IP-Addresses in Trace')
        axis.set_xlabel('Hour')

        #set how many lables where needed and text for it
        axis.set_yticks(range(len(label)))
        axis.set_yticklabels(label)

        axis.set_xticks(range(24))
        axis.set_xticklabels(range(24))

        return fig

    #create subnet vs time graph
    def subnet_time_comparison(self, person):
        timestamps = self.datadb.get_ip_and_time(person)

        label = []
        x = [0 for i in range(len(timestamps))]
        y = [0 for i in range(len(timestamps))]

        #calculate x,y coordinates for dots
        idx = 0
        for i in timestamps:
            subnet = self.sub.find_Ownder(i[0])
            if subnet not in label:
                label.append(subnet)

            time = int(i[1].strftime("%H"))

            x[idx] = time
            y[idx] = label.index(subnet)

            idx += 1

        #create figure
        fig, axis = plt.subplots()
        axis.scatter(x,y)

        #description
        #axis.set_title('ISP\'s of IP-Addresses in Trace')
        axis.set_xlabel('Hour')

        #set how many lables where needed and text for it
        axis.set_yticks(range(len(label)))
        axis.set_yticklabels(label)

        axis.set_xticks(range(24))
        axis.set_xticklabels(range(24))

        return fig

    #creates graph which shows amount of direct change in ip adresses
    def ip_change(self, person):
        ips = self.datadb.get_ip_sorted_by_time(person)

        labels = []
        values = []

        #count changes 
        for i in range(len(ips)-1):
            #create label
            label = ""
            if ips[i][0] == ips[i+1][0]: continue
            if ips[i][0] < ips[i+1][0]:
                label = ips[i][0] + "<->"+ ips[i+1][0]
            else:
                label = ips[i+1][0] + "<->"+ ips[i][0]

            #check if label exists
            if label not in labels:
                labels.append(label)
                values.append(0)

            idx = labels.index(label)
            values[idx] += 1

        #create figure
        fig, axis = plt.subplots()
        axis.barh(range(len(labels)), values)

        #description
        #axis.set_title('IP-Addresses in trace')
        axis.set_xlabel('Total')
        #axis.set_ylabel('Addresses')

        #set how many lables where needed and text for it
        axis.set_yticks(range(len(labels)))
        axis.set_yticklabels(labels)
        return fig

    #graph shows when a change accured
    def ip_change_time(self, person):
        ips = self.datadb.get_ip_and_time(person)

        labels = []
        x = [0 for i in range(len(ips))]
        y = [0 for i in range(len(ips))]

        #create edge [["from", "to"], ...]
        idx = 0
        for i in range(len(ips)-1):
            #create label
            label = ""
            ip1   = ips[i][0]
            ip2   = ips[i+1][0]
            if ip1 ==ip2: continue
            if ip1 < ip2:
                label = ip1 + "<->"+ ip2
            else:
                label = ip2 + "<->"+ ip1

            time = int(ips[i][1].strftime("%H"))

            #add label
            if label not in labels:
                labels.append(label)

            x[idx] = time
            y[idx] = labels.index(label)

            idx += 1

        #create figure
        fig, axis = plt.subplots()
        axis.scatter(x,y)

        #description
        #axis.set_title('ISP\'s of IP-Addresses in Trace')
        axis.set_xlabel('Hour')

        #set how many lables where needed and text for it
        axis.set_yticks(range(len(labels)))
        axis.set_yticklabels(labels)

        axis.set_xticks(range(24))
        axis.set_xticklabels(range(24))

        return fig#
    
    #graph shows when and how often a change accured
    def ip_change_time_color(self, person):
        ips = self.datadb.get_ip_and_time(person)

        labels = []
        unique = []
        x = []
        y = []
        count = []

        for i in range(len(ips)-1):
            #create label
            label = ""
            ip1   = ips[i][0]
            ip2   = ips[i+1][0]
            if ip1 == ip2: continue
            if ip1 < ip2:
                label = ip1 + "<->"+ ip2
            else:
                label = ip2 + "<->"+ ip1

            time = int(ips[i][1].strftime("%H"))

            label1 = label+str(time)

            #add label
            if label not in labels:
                labels.append(label)

            if label1 not in unique:
                unique.append(label1)
                x.append(time)
                y.append(labels.index(label))
                count.append(0)

            count[unique.index(label1)] += 1

        color_label =[]
        for i in count:
            if i not in color_label:
                color_label.append(i)


        #create figure
        fig, axis = plt.subplots()
        scatter = axis.scatter(x,y, c = count)

        #description
        #axis.set_title('ISP\'s of IP-Addresses in Trace')
        axis.set_xlabel('Hour')

        #set how many lables where needed and text for it
        axis.set_yticks(range(len(labels)))
        axis.set_yticklabels(labels)

        axis.set_xticks(range(24))
        axis.set_xticklabels(range(24))

        axis.legend(*scatter.legend_elements(), loc="lower left", title="Classes")

        return fig

    #creates graph which shows amount of direct change in isp 
    def subnet_change(self, person):
        ips = self.datadb.get_ip_sorted_by_time(person)

        labels = []
        values = []

        #count changes 
        for i in range(len(ips)-1):
            #create label
            label = ""
            ip1   = self.sub.find_Ownder(ips[i][0])
            ip2   = self.sub.find_Ownder(ips[i+1][0])
            if ip1 ==ip2: continue
            if ip1 < ip2:
                label = ip1 + "<->"+ ip2
            else:
                label = ip2 + "<->"+ ip1

            #check if label exists
            if label not in labels:
                labels.append(label)
                values.append(0)

            idx = labels.index(label)
            values[idx] += 1

        #create figure
        fig, axis = plt.subplots()
        axis.barh(range(len(labels)), values)

        #description
        #axis.set_title('IP-Addresses in trace')
        axis.set_xlabel('Total')
        #axis.set_ylabel('Addresses')

        #set how many lables where needed and text for it
        axis.set_yticks(range(len(labels)))
        axis.set_yticklabels(labels)
        return fig

    #create graph which shows chnage in ISP visualy
    def subnet_change_graph(self, person, dark=1):
        ips = self.datadb.get_ip_sorted_by_time(person)

        labels = []
        values = []

        #create edge [["from", "to"], ...]
        for i in range(len(ips)-1):
            #create label
            label = ""
            ip1   = self.sub.find_Ownder(ips[i][0])
            ip2   = self.sub.find_Ownder(ips[i+1][0])
            if ip1 ==ip2: continue
            if ip1 < ip2:
                label = ip1 + "<->"+ ip2
            else:
                label = ip2 + "<->"+ ip1

            #add edge
            if label not in labels:
                labels.append(label)
                values.append([ip1, ip2])
                values.append([ip2, ip1])

        #create graph
        G = nx.DiGraph()
        G.add_edges_from(values)

        #create figure
        fig, axis = plt.subplots()
        pos = nx.spring_layout(G)
        if dark == 1:
            rcParams.update({'figure.autolayout': True})
            nx.draw_networkx_nodes(G, pos, node_color=["cyan" for i in range(len(pos))], ax=axis)
            nx.draw(G,pos, edge_color=["yellow" for i in range(len(pos))] ,  ax=axis)
            nx.draw_networkx_labels(G, pos, font_color="white", ax=axis)
            axis.set_facecolor('black')
            fig.set_facecolor('black')
        else:
            rcParams.update({'figure.autolayout': True})
            nx.draw_networkx_nodes(G, pos, ax=axis)
            nx.draw(G,pos, ax=axis)
            nx.draw_networkx_labels(G, pos, ax=axis)
            
        return fig

    def subnet_change_time(self, person):
        ips = self.datadb.get_ip_sorted_with_time(person)

        labels = []
        x = [0 for i in range(len(ips))]
        y = [0 for i in range(len(ips))]

        #create edge [["from", "to"], ...]
        idx = 0
        for i in range(len(ips)-1):
            #create label
            label = ""
            ip1   = self.sub.find_Ownder(ips[i][0])
            ip2   = self.sub.find_Ownder(ips[i+1][0])
            if ip1 ==ip2: continue
            if ip1 < ip2:
                label = ip1 + "<->"+ ip2
            else:
                label = ip2 + "<->"+ ip1

            time = int(ips[i][1].strftime("%H"))

            #add label
            if label not in labels:
                labels.append(label)

            x[idx] = time
            y[idx] = labels.index(label)

            idx += 1

        #create figure
        fig, axis = plt.subplots()
        axis.scatter(x,y)

        #description
        #axis.set_title('ISP\'s of IP-Addresses in Trace')
        axis.set_xlabel('Hour')

        #set how many lables where needed and text for it
        axis.set_yticks(range(len(labels)))
        axis.set_yticklabels(labels)

        axis.set_xticks(range(24))
        axis.set_xticklabels(range(24))

        return fig

    def city_vs_time(self, person):
        timestamps = self.datadb.get_city(person)
        label = []
        total = []

        #fill array
        for i in timestamps:
            if i[0] == '-' : continue
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
            for i in range(len(total)):
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

    def city_vs_ip(self, person):
        timestamps = self.datadb.get_ip_and_city(person)

        label_ip = []
        label_city = []
        x = [0 for i in range(len(timestamps))]
        y = [0 for i in range(len(timestamps))]

        #calculate x,y coordinates for dots
        idx = 0
        for i in timestamps:
            if i[0] == '-' : continue
            if i[0] not in label_ip:
                label_ip.append(i[0])

            if i[i] not in label_city:
                label_city.append(i[i])


            x[idx] = label_city.index(i[1])
            y[idx] = label_ip.index(i[0])

            idx += 1

        #create figure
        fig, axis = plt.subplots()
        axis.scatter(x,y)

        #description
        #axis.set_title('ISP\'s of IP-Addresses in Trace')
        axis.set_xlabel('City')

        #set how many lables where needed and text for it
        axis.set_yticks(range(len(label_ip)))
        axis.set_yticklabels(label_ip)

        axis.set_xticks(range(range(label_city)))
        axis.set_xticklabels(label_city)

        return fig

    def city_graph(self, person, dark=1):
        ips = self.datadb.get_city_time(person)

        labels = []
        values = []

        #create edge [["from", "to"], ...]
        for i in range(len(ips)-1):
            #create label
            label = ""
            ip1   = ips[i][0]
            ip2   = ips[i+1][0]
            if ip1 ==ip2: continue
            if ip1 < ip2:
                label = ip1 + "<->"+ ip2
            else:
                label = ip2 + "<->"+ ip1

            #add edge
            if label not in labels:
                labels.append(label)
                values.append([ip1, ip2])
                values.append([ip2, ip1])

        #create graph
        G = nx.DiGraph()
        G.add_edges_from(values)

        #create figure
        fig, axis = plt.subplots()
        pos = nx.spring_layout(G)
        if dark == 1:
            rcParams.update({'figure.autolayout': True})
            nx.draw_networkx_nodes(G, pos, node_color=["cyan" for i in range(len(pos))], ax=axis)
            nx.draw(G,pos, edge_color=["yellow" for i in range(len(pos))] ,  ax=axis)
            nx.draw_networkx_labels(G, pos, font_color="white", ax=axis)
            axis.set_facecolor('black')
            fig.set_facecolor('black')
        else:
            rcParams.update({'figure.autolayout': True})
            nx.draw_networkx_nodes(G, pos, ax=axis)
            nx.draw(G,pos, ax=axis)
            nx.draw_networkx_labels(G, pos, ax=axis)
            
        return fig

    def city_isp(self, person):
        timestamps = self.datadb.get_ip_and_city(person)

        label_ip = []
        label_city = []
        x = [0 for i in range(len(timestamps))]
        y = [0 for i in range(len(timestamps))]

        #calculate x,y coordinates for dots
        idx = 0
        for i in timestamps:
            if i[0] == '-' : continue

            isp = self.sub.find_Ownder(i[0])

            if isp not in label_ip:
                label_ip.append(isp)

            if i[i] not in label_city:
                label_city.append(i[1])


            x[idx] = label_city.index(i[1])
            y[idx] = label_ip.index(isp)

            idx += 1

        #create figure
        fig, axis = plt.subplots()
        axis.scatter(x,y)

        #description
        #axis.set_title('ISP\'s of IP-Addresses in Trace')
        axis.set_xlabel('City')

        #set how many lables where needed and text for it
        axis.set_yticks(range(len(label_ip)))
        axis.set_yticklabels(label_ip)

        axis.set_xticks(range(range(label_city)))
        axis.set_xticklabels(label_city)

        return fig

    #get json which descripes possible images and description for the iages
    def get_Json(self, user):
        json_str = \
            '{"content":['+\
                '{"name": "Measurement", "images": ['+\
                    '{"url": "/image/'+user+'_0_0.png", "alt":"Hour", "description":"Shows how frequently measurements were taken. e.g. 1 and 0.6 means, 60% of the measurements were taken one hour apart."} '+\
                    ',{"url": "/image/'+user+'_0_1.png", "alt":"Day", "description":"Shows how many measurements were done per week day."} '+\
                    ',{"url": "/image/'+user+'_0_2.png", "alt":"Time", "description":"Shows at which time the reqest was send."} '+\
                ']}'+\
                ',{"name": "Address", "images": ['+\
                    '{"url": "/image/'+user+'_1_0.png", "alt":"IpAddresses", "description":"Shows distribution of IP-End-Addresses of the user\'s device."}'+\
                    ',{"url": "/image/'+user+'_1_1.png", "alt":"IpAddresses in Trace", "description":"Shows different IP-Addresses of the route to the user captured by trace."}'+\
                    ',{"url": "/image/'+user+'_1_2.png", "alt":"Subnet IP-Addresses", "description":"Shows ISP of the IP-End-Addresses of the user\'s device."}'+\
                    ',{"url": "/image/'+user+'_1_3.png", "alt":"Subnet IP-Addresses trace", "description":"Shows ISP of the IP-Addresses of the route to the user captured by trace."}'+\
                ']}'+\
                ',{"name": "Address vs Time", "images": ['+\
                    '{"url": "/image/'+user+'_2_0.png", "alt":"IP / Time Overview", "description":"Shows which IP-Address was used at which time"}'+\
                    ',{"url": "/image/'+user+'_2_1.png", "alt":"IP / Time Overview Trace", "description":"Shows which IP-Address in Trace was used at which time"}'+\
                    ',{"url": "/image/'+user+'_2_2.png", "alt":"IP / Time Overview Subnet", "description":"Shows which Subnet was used at which time"}'+\
                ']}'+\
                ',{"name": "Changes in IP", "images": ['+\
                    '{"url": "/image/'+user+'_3_0.png", "alt":"IP Address changes", "description":"shows how often change within IP Adresses accured"}'+\
                    ',{"url": "/image/'+user+'_3_1.png", "alt":"IP Address changes", "description":"shows how often change within IP Subnet accured and time"}'+\
                    ',{"url": "/image/'+user+'_3_2.png", "alt":"IP Address changes frequency", "description":"shows frequency of changes"}'+\
                    ',{"url": "/image/'+user+'_3_3.png", "alt":"IP Subnet changes", "description":"shows how often change within IP Subnet accured"}'+\
                    ',{"url": "/image/'+user+'_3_4.png", "alt":"IP Subnet changes", "description":"shows how often change within IP Subnet accured graph"}'+\
                    ',{"url": "/image/'+user+'_3_5.png", "alt":"IP Subnet changes vs time", "description":"shows how often change within IP Subnet accured and when"}'+\
                ']}'+\
                ',{"name": "Geographical", "images": ['+\
                    '{"url": "/image/'+user+'_4_0.png", "alt":"Todo", "description":"Todo"} '+\
                    ',{"url": "/image/'+user+'_4_1.png", "alt":"Todo", "description":"Todo"} '+\
                    ',{"url": "/image/'+user+'_4_2.png", "alt":"Todo", "description":"Todo"} '+\
                    ',{"url": "/image/'+user+'_4_3.png", "alt":"Todo", "description":"Todo"} '+\
                ']}'+\
            ']}'
        #print(json_str, file = sys.stderr)
        return json.loads(json_str)

    #create compare json from the get_Json method 
    def get_compare_json(self, user1, user2):
        j = self.get_Json(user1)

        new_j = {}
        new_cat = []

        #ad url1 to each image entry in the json
        for i in j['content']:
            new_j = {}
            new_image = []
            new_j["name"] = i["name"]
            for k in i['images']:
                val = k['url'].split("_")
                k['url1'] = "/image/" + user2 + "_" + val[1] +"_" +val[2]
                new_image.append(k)
            new_j['images'] = new_image
            new_cat.append(new_j)

        new_j["content"] = new_cat

        return new_j
