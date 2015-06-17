#!/usr/bin/python2.7


import numpy as numpy
import time
import serial
import os, sys
import argparse
from continuus_plot import live_plots

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
	parser = argparse.ArgumentParser(description='This script is meant for the analysis of WLS capture efficiency.')
	parser.add_argument('-c', '--calibration', dest='CALIB', action='store', type=str, help='Calibration measurement (fiber directly to signal PD)')
	parser.add_argument('-f', '--files', dest='FILES', action='store', type=str, nargs='+', help='Files containing the diodes output. These should be formatted as wavelength TAB signal/refference TAB error(signal/refference)')
	parser.add_argument('-s', '--spectrum', dest='SPECTRUM', type=str, action='store', help="Spectrum of the WLS measured.")
	parser.add_argument('-t', '--target-folder', dest='TARGET', action='store', type=str, default='./results/', help='Folder to save results (default=\'./results\')')
	parser.add_argument('-p', '--pre-factor', dest='PREFACTOR', action='store', type=float, help='Prefactor for geometry correction. (optional)' ,default=10000) #constants.pi*(10**2 - (10-2)**2) *2/(2*6),)#Default asumes 2cm PMMA pipe with 2mm frame
	parser.add_argument('-z', '--Zeuthen', dest='ZEUTHEN', action='store_true', default=False, help='Use the file for the Zeuthen PD')
	
	args = parser.parse_args()


	sC=serialCOM("/dev/ttyACM0")
	lp = live_plots(0,120,two_plots=True)
	while True:
		time.sleep(1)
		t,h=sC.returnLatest()
		lp.update(1,t,h)
		lp.clean_arrays()
		sc.writeFile(output.txt)


#creat args for plot and or file