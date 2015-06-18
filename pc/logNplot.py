#!/usr/bin/python2.7


import numpy as numpy
import time
import serial
import os, sys
import argparse
from dynamic-plot import live_plots

class serialCOM:
	"""A simple class to fetch temperature and humidity information via a arduino micro connected to a DHT22"""

	def __init__(self, port, baud=9600, timeout=1):
		self.ser = serial.Serial(port,baud,timeout=timeout)
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
	

	def getTemperature(self):
		self.ser.write('t')
		self.ser.flush()
		time.sleep(0.25)
		self.latestTemperature=float(self.ser.read(50))


	def returnLatest(self):
		self.getTemperature()
		self.getHumidity()
		return self.latestTemperature, self.latestHumidity

	def writeFile(self,filename):
		date=time.asctime()
		f = open(filename, 'a')
		f.write(date + '\t' + str(self.latestTemperature + '\t' + str(self.latestHumidity) + '\n')
		f.close()
	
	def ___writeFile(self,filename):
		date=time.time()
		f = open(filename, 'a')
		f.write(str(date) + '\t' + str(self.latestTemperature + '\t' + str(self.latestHumidity) + '\n')
		f.close()


if __name__=="__main__":
	parser = argparse.ArgumentParser(description='This script is meant to read the humidity and temperature from an arduino connected to a DHT22 or alike. It allows to display the results in a dynamic plot or save them to file')
	parser.add_argument('-P', '--plot', dest='SEC', action='store', type=int, help='The last SEC Seconds will be displayed in a dynamic plot. Leave empty for no Plot.')
	parser.add_argument('-F', '--file', dest='FILE', action='store', type=str, help='A name for the output file. No output file if not set.')
	
	args = parser.parse_args()
	if(args.SEC):
		if(args.SEC < 2):
			print "Error! Please choose a value greater 2 sconds."
			return


	sC=serialCOM("/dev/ttyACM0")
	if(args.Sec):
		lp = live_plots(0,args.SEC,two_plots=True)
	while True:
		time.sleep(2)
		t,h=sC.returnLatest()
		if(args.Sec):
			lp.update(2,t,h)
			lp.clean_arrays()
		if(args.FILE):
			sc.writeFile(args.FILE)

