#!/usr/bin/python2.7


import numpy as numpy
import time
import serial
import os, sys
import argparse
from dynamic_plot import live_plots

class serialCOM:
	"""A simple class to fetch temperature and humidity information via a arduino micro connected to a DHT22"""

	def __init__(self, port, two, baud=9600, timeout=1):
		self.ser = serial.Serial(port,baud,timeout=timeout)
		self.two=two
		time.sleep(1)
		self.ser.read(100)
		if(self.ser.isOpen()):
			return
		else:
			print "error opening serial connection!"
			return

	
	def close(self):
		self.ser.close()


	def getHumidity(self):
		self.ser.write('h')
		self.ser.flush()
		time.sleep(0.25)
		self.latestHumidity=float(self.ser.read(50))
		if(self.two):
			self.ser.write('j')
			self.ser.flush()
			time.sleep(0.25)
			self.latestHumidity2=float(self.ser.read(50))
	

	def getTemperature(self):
		self.ser.write('t')
		self.ser.flush()
		time.sleep(0.25)
		self.latestTemperature=float(self.ser.read(50))
		if(self.two):
			self.ser.write('z')
			self.ser.flush()
			time.sleep(0.25)
			self.latestTemperature2=float(self.ser.read(50))


	def returnLatest(self):
		self.getTemperature()
		self.getHumidity()
		return self.latestTemperature, self.latestHumidity

	def returnLatest2(self):
		self.getTemperature()
		self.getHumidity()
		return self.latestTemperature2, self.latestHumidity2

	def writeFile(self,filename):
		date=time.asctime()
		if filename == "STDOUT":
			if(self.two):
				sys.stdout.write(date + '\t' + str(self.latestTemperature) + '\t' + str(self.latestHumidity) + '\t' + str(self.latestTemperature2) + '\t' + str(self.latestHumidity2) +'\n')
			else:
				sys.stdout.write(date + '\t' + str(self.latestTemperature) + '\t' + str(self.latestHumidity) + '\n')
			return
		f = open(filename, 'a')
		if(self.two):
			f.write(date + '\t' + str(self.latestTemperature) + '\t' + str(self.latestHumidity) + '\t' + str(self.latestTemperature2) + '\t' + str(self.latestHumidity2) +'\n')
		else:
			f.write(date + '\t' + str(self.latestTemperature) + '\t' + str(self.latestHumidity) + '\n')
		f.close()
	
	def ___writeFile(self,filename):
		date=time.time()
		if filename == "STDOUT":
			if(self.two):
				sys.stdout.write(date + '\t' + str(self.latestTemperature) + '\t' + str(self.latestHumidity) + '\t' + str(self.latestTemperature2) + '\t' + str(self.latestHumidity2) +'\n')
			else:
				sys.stdout.write(date + '\t' + str(self.latestTemperature) + '\t' + str(self.latestHumidity) + '\n')
			return
		f = open(filename, 'a')
		if(self.two):
			f.write(date + '\t' + str(self.latestTemperature) + '\t' + str(self.latestHumidity) + '\t' + str(self.latestTemperature2) + '\t' + str(self.latestHumidity2) +'\n')
		else:
			f.write(date + '\t' + str(self.latestTemperature) + '\t' + str(self.latestHumidity) + '\n')
		f.close()


if __name__=="__main__":
	parser = argparse.ArgumentParser(description='This script is meant to read the humidity and temperature from an arduino connected to a DHT22 or alike. It allows to display the results in a dynamic plot or save them to file')
	parser.add_argument('-P', '--plot', dest='SEC', action='store', type=int, help='The last SEC Seconds will be displayed in a dynamic plot. Leave empty for no Plot.')
	parser.add_argument('-F', '--file', dest='FILE', action='store', type=str, help='A name for the output file. No output file if not set.')
	parser.add_argument('-t', '--two', dest='TWO', action='store_true', default=False, help='Defines whether to read one or two Sensors.')
	parser.add_argument('-T', '--time', dest='TIME', action='store', type=int, default=2, help='Defines the time interval between measurements. Measures only one value for -1.')
	parser.add_argument('-p', '--port', dest='PORT', action='store', type=str, default="COM3", help='Defines the Port to connect to the arduino.')
	
	args = parser.parse_args()
	if(args.SEC):
		if((args.SEC < 2 or args.SEC > args.TIME )):
			print "Error! Please choose a value greater than 2 seconds and the time interval."
			exit

	sC=serialCOM(args.PORT ,args.TWO)
	if(args.SEC):
		lp = live_plots(0,args.SEC,two_plots=True)
		if(args.TWO):
			lp2 = live_plots(0,args.SEC,two_plots=True)
	if args.TIME != -1:
		while True:
			time.sleep(args.TIME)
			t,h=sC.returnLatest()
			if(args.TWO):
				t2,h2=sC.returnLatest2()
			if(args.SEC):
				lp.update_time(args.TIME,t,h)
				lp.clean_arrays()
				if(args.TWO):
					lp2.update_time(args.TIME,t2,h2)
					lp2.clean_arrays()
			if(args.FILE):
				sC.writeFile(args.FILE)
	else:
		time.sleep(2)
		t,h=sC.returnLatest()
		if(args.TWO):
			t2,h2=sC.returnLatest2()
		if(args.FILE):
			sC.writeFile(args.FILE)
		else:
			sC.writeFile("STDOUT")
