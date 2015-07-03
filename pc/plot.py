#!/usr/bin/python

import numpy as np
import time
import os, sys
import argparse
import matplotlib.pyplot as plt
from datetime import datetime
from dateutil import parser


parser_ = argparse.ArgumentParser(description='Script to plot temperature logs from the lab')
parser_.add_argument('-F', '--file', dest='FILE', action='store', type=str, help='Log file name')

args = parser_.parse_args()

time_=[]
temp=[]
humid=[]

f=open(args.FILE,"r")
for line in f.readlines():
	data=line.split('\t')
	time_.append(parser.parse(data[0]))
	temp.append([data[1],data[3]])
	humid.append([data[2],data[4]])
f.close()
temp=np.swapaxes(temp,0,1)
humid=np.swapaxes(humid,0,1)


color=['#aa9900','#ff0000','#0000ff','#0099aa','#ff0000','#ff8800','#00ffff','#88ffff','#ff00ff','#00ff00','#880088','#8888ff','#00ff88','#88ff00','#88ff88','#ff0088','#ff8888','#ffff00' ,'#ff88ff']*3
#fig1 = plt.figure()
fig, ax1 = plt.subplots()
ax1.plot_date(time_, temp[0], 'b-', color=color[0], label="Temp LAB")
ax1.plot_date(time_, temp[1], 'b-', color=color[1], label="Temp BOX")
ax1.set_xlabel("Time", size='x-large')
ax1.set_ylabel('Temperature [C]', color='r')

ax2 = ax1.twinx()
ax2.plot_date(time_, humid[0], 'b-', color=color[2], label="Humidity LAB")
ax2.plot_date(time_, humid[1], 'b-', color=color[3], label="Humidity BOX")
ax2.set_ylabel('Humidity [%]', color='b')

ax1.legend(loc='upper left')
ax2.legend(loc='upper right')
plt.savefig('climate_log.png', bbox_inches=0)
plt.show()





