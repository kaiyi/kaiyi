import os
import subprocess
import time
import threading
import signal
import blescan
import bluetooth._bluetooth as bluez
from subprocess import PIPE, STDOUT

#class Ble:

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
	returnedList = blescan.parse_events(sock, num)
	for beacon in returnedList:
		tmptuple = beacon.split(',')
		print tmptuple
		#uuid = tmptuple[1].lower()
		#print tmptuple[1][:4]
		#minor = tmptuple[3]
		#idnum = int(tmptuple[2])*100 + int(tmptuple[3])
		#if (uuid == "1534516467ab3e49f9d6e29000000008"): 
			#(uuid == 1534516467ab3e49f9d6e29000000008") and (int(minor) in minorlist):
			#rssi = tmptuple[5]
			#print idnum
			#rssiDict[str(idnum)] = rssi
	return rssiDict	

def ScanTimeout( p ):
	if p.poll() is None:
		print "Go Terminate pid=%d"%p.pid
		os.kill(p.pid, signal.SIGINT)

def AdvUndo( p ):
	subprocess.Popen(["hciconfig", "hci0", "noleadv"])

def BleConfig():
	print "Configuring..."
	os.popen("hciconfig hci0 down")
	os.popen("hciconfig hci0 up")
	print "Config Finish"

def BleScan():
	print "Scanning..."
	with open("result.txt","w")as f:
		proc = subprocess.Popen(["hcitool", "lescan"], stdout=f)
		t = threading.Timer(0.9, ScanTimeout, [proc])
		t.start()
		t.join()
		proc.wait()
		print "Scan Finish."
		t.cancel()

def BleAdvertise():
	print "Advertising..."
	subprocess.Popen("hcitool -i hci0 cmd 0x08 0x0008 1e 02 01 1a 1a ff 4c 00 02 15 e2 c5 6d b5 df fb 48 d2 b0 60 d0 f5 a7 10 96 e0 00 00 00 00 c5 00 00 00 00 00 00 00 00 00 00 00 00 00",shell=True)
	proc = subprocess.Popen(["hciconfig", "hci0", "leadv", "0"])
	t = threading.Timer(0.1, undoAdv, [proc])
	t.start()
	t.join()
	print "Advertise Finish"
	t.cancle()

def main():
	while 1:
		BleConfig()
		BleScan()

		print "Result..."
		with open("result.txt","r") as f:
			for line in f:
				print line

		BleAdvertise()

		print "done"


if __name__ == "__main__":
	main()
		

