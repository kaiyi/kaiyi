from Ble import Ble
	
def main():

	mBle = Ble()
	
	for i in range(0,9):
		n = mBle.BleScan()
		
		if n == 0:
			print "No data!"
		else:	
			dev = mBle.getDevicePktList();
			bea = mBle.getBeaconPktList();
			print 'Devices',
			print '\n\t'.join([repr(x) for x in dev])
			print 'Beacons',
			print '\n\t'.join([repr(x) for x in bea])
			
		for device in dev:
			print mBle.getDeviceRssiByName(device[0])
			
		mBle.resetPktList()
		
		#print len(l_device)
		#print len(l_beacon)
			
		
		#mBle.BleAdvertise()

		print "done"
		
if __name__ == "__main__":
	main()