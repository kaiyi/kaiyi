#import requests
import uuid 
import blescan
import sys
import random 
import bluetooth._bluetooth as bluez
#import Adafruit_BMP.BMP085 as BMP085
#import smbus
import time
import math
import os
#from Positioning import Positioning
#from ParticleFilter import ParticleFilter
#from Trilateration import Trilateration
#from Line import Line
#from Point import Point, Particle
#from IndoorMap import IndoorMap
#from Beacon import Beacon
# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

#bus = smbus.SMBus(1)
#addrMPU = 0x68
#addrHMC = 0x1e

#serverAddr = "http://140.113.208.146:8090/" 
minorlist = [11,13,14]
#sensor = BMP085.BMP085()
#positioning = Positioning();
clientidParam = "clientid=" + str(random.randint(0,100000));
devid = 0
refbaro = 993.76

def init_ble():
	try:
		sock = bluez.hci_open_dev(devid)
		print "ble thread started"
	except:
		print "error accessing bluetooth device..."
		sys.exit(1)

	blescan.hci_le_set_scan_parameters(sock)
	blescan.hci_enable_le_scan(sock)

	return sock

def ble_scan(sock, num):
	rssiDict = dict()
	returnedList = blescan.parse_encounter_event(sock, num)
	for beacon in returnedList:
		tmptuple = beacon.split(',')
		print tmptuple
		#uuid = tmptuple[1].lower()
		#print tmptuple[1][:4]
		minor = tmptuple[3]
		idnum = int(tmptuple[2])*100 + int(tmptuple[3])
		if (uuid == "1534516467ab3e49f9d6e29000000008"): 
			#(uuid == 1534516467ab3e49f9d6e29000000008") and (int(minor) in minorlist):
			rssi = tmptuple[5]
			print idnum
			rssiDict[str(idnum)] = rssi
	return rssiDict	

"""def read_byte(address, adr):
	return bus.read_byte_data(address, adr)

def read_word(address, adr):
	high = bus.read_byte_data(address, adr)
	low = bus.read_byte_data(address, adr + 1)
	val = (high << 8) + low
	return val

def read_word_2c(address, adr):
	val = read_word(address, adr)
	if (val >= 0x8000):
		return -((65535 - val) + 1)
	else:
	return val
"""
def main():

	sock = init_ble()
	rssiDict = ble_scan(sock, 20)

	beaconidList = list()
	rssiList = list()
	#mybaro = '{0:0.2f}'.format(sensor.read_pressure()) 
	#print mybaro 
	for beaconid in rssiDict:
		beaconidList.append( beaconid )
		rssiList.append( rssiDict[beaconid] )

	 #pos, stdX, stdY, floor=  positioning.initPosition(beaconidList, rssiList);
	 #url = serverAddr + "nctu.hscc.cplin.jersey/rest/hello?" + clientidParam +"&pos="+pos+"&StdX="+str(stdX)+"&StdY="+str(stdY)+"&floor=" + str(floor)
	 #print url
	 #r = requests.get(url)
	 #print(r.text)
	 #refbaro = float(r.text)
	 #floor =  positioning.initPressure(mybaro, refbaro);
	 #print("floor="+str(floor))
	 
	 #init_imu()
	 #check_step(sock)


if __name__ == "__main__":
	main()
