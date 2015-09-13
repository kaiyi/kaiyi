import os
import Queue

import Blecontrl

#user param

class Ble:

	def __init__(self):
		self.l_device = []
		self.l_beacon = []
		self.sock = Blecontrl.init_ble()
		self.name = "User9"
		self.packet = "0x08 0x0008"

	def BleConfig(self):
		print "Configuring..."
		os.popen("hciconfig hci0 down")
		os.popen("hciconfig hci0 up")
		
		print "Config Finish"

	def BleScan(self):

		print "Scanning..."
		
		PKT_QUEUE = Blecontrl.ble_scan(self.sock)
		
		
		while not PKT_QUEUE.empty():
			Str = Blecontrl.parse_events(PKT_QUEUE)
			#print len(Str)
			if len(Str) == 7 :
				self.l_device.append(Str)
			elif len(Str) == 6:
				self.l_beacon.append(Str)
				
		print "Scan Finish."
		#print "Result: "
		#print 'Devices',
		#print '\n\t'.join([repr(x) for x in l_device])
		#print 'Beacons',
		#print '\n\t'.join([repr(x) for x in l_beacon])
		return len(self.l_beacon)+len(self.l_device)
	
	def BleAdvertise(self,cx,cy,stdev,floor,tvalue):
		print "Advertising..."
		Blecontrl.ble_adv(self.packet,self.name,cx,cy,stdev,floor,tvalue)
		print "Advertise Finish"

	def getDevicePktList(self):
		return self.l_device

	def getBeaconPktList(self):	
		return self.l_beacon

	def resetPktList(self):
		del self.l_device[:]
		del self.l_beacon[:]

#-----------------------------------------------		
	def getDeviceRssiByName(self,name):
		rssi = "1"
		for device in self.l_device:
			#print device[0]
			if name == device[0]:
				rssi = device[6]
				break
		return rssi
	
	def getBeaconRssiByMac(self,mac):
		rssi = "1"
		for device in self.l_device:
			#print device[0]
			if mac == device[0]:
				rssi = device[5]
				break
		return rssi

	def getDevicePosByName(self,name):
		x = "-1"
		y = "-1"
		std = "-1"
		floor = "-1"
		trustVelue = "-1"
		for device in self.l_device:
			#print device[0]
			if name == device[0]:
				x = device[1]
				y = device[2]
				std = device[3]
				floor = device[4]
				trustVelue = device[5]
				break
		return x, y, std, floor, trustVelue
	
	
