import os
import subprocess
import time
import threading
import signal
from subprocess import PIPE, STDOUT

class Ble:

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

	def BleStart():
		while 1:
			BleConfig()
			BleScan()

			print "Result..."
			with open("result.txt","r") as f:
				for line in f:
					print line

			BleAdvertise()

			print "done"
		

