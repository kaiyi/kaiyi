import os
import Queue

import Blecontrl

#user param
PKT_QUEUE = Queue.Queue()
l_device = []
l_beacon = []



def BleConfig():
	print "Configuring..."
	os.popen("hciconfig hci0 down")
	os.popen("hciconfig hci0 up")
	
	sock = Blecontrl.init_ble()
	print "Config Finish"
	return sock

def BleScan(sock):

	print "Scanning..."
	
	PKT_QUEUE = Blecontrl.ble_scan(sock)
	
	
	while not PKT_QUEUE.empty():
		Str = Blecontrl.parse_events(PKT_QUEUE)
		#print len(Str)
		if len(Str) == 7 :
			l_device.append(Str)
		elif len(Str) == 6:
			l_beacon.append(Str)
			
	print "Scan Finish."
	#print "Result: "
	#print 'Devices',
	#print '\n\t'.join([repr(x) for x in l_device])
	#print 'Beacons',
	#print '\n\t'.join([repr(x) for x in l_beacon])
	return len(l_beacon)+len(l_device)
	
def BleAdvertise():
	print "Advertising..."
	ble_adv()
	print "Advertise Finish"

def getDevicePktList():
	return l_device

def getBeaconPktList():	
	return l_beacon

def resetPktList():
	del l_device[:]
	del l_beacon[:]
	
def main():

	sock = BleConfig()
	
	while 1:
		n = BleScan(sock)
		
		if n == 0:
			print "No data!"
		else:	
			dev = getDevicePktList();
			bea = getBeaconPktList();
			print 'Devices',
			print '\n\t'.join([repr(x) for x in dev])
			print 'Beacons',
			print '\n\t'.join([repr(x) for x in bea])
			
		resetPktList()
		
		#print len(l_device)
		#print len(l_beacon)
			
		
		BleAdvertise()

		print "done"



if __name__ == "__main__":
	main()
		

