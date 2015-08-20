import os
import Queue

import Blecontrl

#user param

class Ble:

	def __init__(self):
		self.l_device = []
		self.l_beacon = []
		self.sock = Blecontrl.init_ble()

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
	
	def BleAdvertise(self):
		print "Advertising..."
		Blecontrl.ble_adv()
		print "Advertise Finish"

	def getDevicePktList(self):
		return self.l_device

	def getBeaconPktList(self):	
		return self.l_beacon

	def resetPktList(self):
		del self.l_device[:]
		del self.l_beacon[:]
		
	#def getDeviceRssiByName(self,name)
		#for 


