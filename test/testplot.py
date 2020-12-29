import io
import random
import sys
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import json
import matplotlib.pyplot as plt
from matplotlib import rcParams


label = ['93.199.152.26', '84.141.184.4', '46.114.149.213', '185.52.247.41', '93.199.153.203', '46.114.149.79', '46.114.151.235', '46.114.145.44', '46.114.150.105', '46.114.148.85', '46.114.151.91', '46.114.149.184', '46.114.151.136', '46.114.148.68', '46.114.150.246', '46.114.145.103', '46.114.147.154', '46.114.144.141', '82.113.106.8', '46.114.147.183', '46.114.151.203', '46.114.151.192', '46.114.151.161']
size = [231, 13, 12, 8, 4, 3, 3, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]


plt.style.use('dark_background')
rcParams.update({'figure.autolayout': True})

fig, axis = plt.subplots()
axis.set_title('Time between measurement (hour based)')
axis.set_xlabel('Distance')
axis.set_ylabel('Amount')
axis.barh(range(len(label)), size, tick_label=label)
axis.axis('equal')

plt.savefig('foo.png')