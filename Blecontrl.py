#BLE iBeaconScanner based on https://github.com/adamf/BLE/blob/master/ble-scanner.py
# JCS 06/07/14

DEBUG = False
# BLE scanner based on https://github.com/adamf/BLE/blob/master/ble-scanner.py
# BLE scanner, based on https://code.google.com/p/pybluez/source/browse/trunk/examples/advanced/inquiry-with-rssi.py

# https://github.com/pauloborges/bluez/blob/master/tools/hcitool.c for lescan
# https://kernel.googlesource.com/pub/scm/bluetooth/bluez/+/5.6/lib/hci.h for opcodes
# https://github.com/pauloborges/bluez/blob/master/lib/hci.c#L2782 for functions used by lescan

# performs a simple device inquiry, and returns a list of ble advertizements 
# discovered device

# NOTE: Python's struct.pack() will add padding bytes unless you make the endianness explicit. Little endian
# should be used for BLE. Always start a struct.pack() format string with "<"


import os
import sys
import struct
import bluetooth._bluetooth as bluez

LE_META_EVENT = 0x3e
LE_PUBLIC_ADDRESS=0x00
LE_RANDOM_ADDRESS=0x01
LE_SET_SCAN_PARAMETERS_CP_SIZE=7
OGF_LE_CTL=0x08
OCF_LE_SET_SCAN_PARAMETERS=0x000B
OCF_LE_SET_SCAN_ENABLE=0x000C
OCF_LE_CREATE_CONN=0x000D

LE_ROLE_MASTER = 0x00
LE_ROLE_SLAVE = 0x01

# these are actually subevents of LE_META_EVENT
EVT_LE_CONN_COMPLETE=0x01
EVT_LE_ADVERTISING_REPORT=0x02
EVT_LE_CONN_UPDATE_COMPLETE=0x03
EVT_LE_READ_REMOTE_USED_FEATURES_COMPLETE=0x04

# Advertisment event types
ADV_IND=0x00
ADV_DIRECT_IND=0x01
ADV_SCAN_IND=0x02
ADV_NONCONN_IND=0x03
ADV_SCAN_RSP=0x04

DEV_ID = 0
ADV_TIME = 0.1
SCAN_TIME = 0.9
SYS_TIME = 0

def returnnumberpacket(pkt):
	myInteger = 0
	multiple = 256
	for c in pkt:
		myInteger +=  struct.unpack("B",c)[0] * multiple
		multiple = 1
	return myInteger 

def returnstringpacket(pkt):
	myString = "";
	for c in pkt:
		myString +=  "%02x" %struct.unpack("B",c)[0]
	return myString 

def printpacket(pkt):
	for c in pkt:
		sys.stdout.write("%02x " % struct.unpack("B",c)[0])

def get_packed_bdaddr(bdaddr_string):
	packable_addr = []
	addr = bdaddr_string.split(':')
	addr.reverse()
	for b in addr: 
		packable_addr.append(int(b, 16))
	return struct.pack("<BBBBBB", *packable_addr)

def packed_bdaddr_to_string(bdaddr_packed):
	return ':'.join('%02x'%i for i in struct.unpack("<BBBBBB", bdaddr_packed[::-1]))

def hci_enable_le_scan(sock):
	hci_toggle_le_scan(sock, 0x01)

def hci_disable_le_scan(sock):
	hci_toggle_le_scan(sock, 0x00)

def hci_toggle_le_scan(sock, enable):
# hci_le_set_scan_enable(dd, 0x01, filter_dup, 1000);
# memset(&scan_cp, 0, sizeof(scan_cp));
 #uint8_t         enable;
 #       uint8_t         filter_dup;
#        scan_cp.enable = enable;
#        scan_cp.filter_dup = filter_dup;
#
#        memset(&rq, 0, sizeof(rq));
#        rq.ogf = OGF_LE_CTL;
#        rq.ocf = OCF_LE_SET_SCAN_ENABLE;
#        rq.cparam = &scan_cp;
#        rq.clen = LE_SET_SCAN_ENABLE_CP_SIZE;
#        rq.rparam = &status;
#        rq.rlen = 1;

#        if (hci_send_req(dd, &rq, to) < 0)
#                return -1;
	cmd_pkt = struct.pack("<BB", enable, 0x00)
	bluez.hci_send_cmd(sock, OGF_LE_CTL, OCF_LE_SET_SCAN_ENABLE, cmd_pkt)


def hci_le_set_scan_parameters(sock):
	old_filter = sock.getsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, 14)
	
	SCAN_RANDOM = 0x01
	OWN_TYPE = SCAN_RANDOM
	SCAN_TYPE = 0x01

def init_ble():

	try:
		sock = bluez.hci_open_dev(DEV_ID)
		print "ble thread started"
	except:
		print "error accessing bluetooth device..."
		sys.exit(1)

	hci_le_set_scan_parameters(sock)
	hci_enable_le_scan(sock)

	return sock
	
def extract_beacon_data(pkt):
	report_pkt_offset = 0
	
	if (DEBUG == True):
		print "-------------"
		print "\tfullpacket: ", printpacket(pkt)
		print "\tUDID: ", printpacket(pkt[report_pkt_offset -22: report_pkt_offset - 6])
		print "\tMAJOR: ", printpacket(pkt[report_pkt_offset -6: report_pkt_offset - 4])
		print "\tMINOR: ", printpacket(pkt[report_pkt_offset -4: report_pkt_offset - 2])
		print "\tMAC address: ", packed_bdaddr_to_string(pkt[report_pkt_offset + 3:report_pkt_offset + 9])
		# commented out - don't know what this byte is.  It's NOT TXPower
		txpower, = struct.unpack("b", pkt[report_pkt_offset - 2])
		print "\tTXpower(Unknown):", txpower
		
		rssi, = struct.unpack("b", pkt[report_pkt_offset -1])
		print "\tRSSI:%i"%rssi
	# build the return string
	Adstring = packed_bdaddr_to_string(pkt[report_pkt_offset + 3:report_pkt_offset + 9])#MAC
	Adstring += ","
	Adstring += returnstringpacket(pkt[report_pkt_offset -22: report_pkt_offset - 6])#UUID 
	Adstring += ","
	Adstring += "%i" % returnnumberpacket(pkt[report_pkt_offset -6: report_pkt_offset - 4])#MAJOR 
	Adstring += ","
	Adstring += "%i" % returnnumberpacket(pkt[report_pkt_offset -4: report_pkt_offset - 2])#MINOR 
	Adstring += ","
	Adstring += "%i" % struct.unpack("b", pkt[report_pkt_offset -2])#TXPOWER
	Adstring += ","
	Adstring += "%i" % struct.unpack("b", pkt[report_pkt_offset -1])#RSSI
	
	return Adstring

def extract_device_data(pkt):
	report_pkt_offset = 0
	
	if (DEBUG == True):
		print "-------------"
		print "\tfullpacket: ", printpacket(pkt)
		
		name = returnstringpacket( pkt[report_pkt_offset +12: report_pkt_offset -21])
		print "\tDevice Name: ", printpacket(pkt[report_pkt_offset +12: report_pkt_offset -21]), " ", name.decode('hex')
		cenX = returnstringpacket( pkt[report_pkt_offset -14: report_pkt_offset -18:-1])
		print "\tcenX: ", printpacket(pkt[report_pkt_offset -14: report_pkt_offset -18:-1]), " ", struct.unpack('!f', cenX.decode('hex'))[0]#cenX#returnstringpacket( pkt[report_pkt_offset -22: report_pkt_offset - 18])
		cenY = returnstringpacket( pkt[report_pkt_offset -10: report_pkt_offset -14:-1])		
		print "\tcenY: ", printpacket(pkt[report_pkt_offset -10: report_pkt_offset -14:-1]), " ", struct.unpack('!f', cenY.decode('hex'))[0]
		stdNorm = returnstringpacket( pkt[report_pkt_offset -6: report_pkt_offset -10:-1])		
		print "\tstdNorm: ", printpacket(pkt[report_pkt_offset -6: report_pkt_offset -10:-1]), " ", struct.unpack('!f', stdNorm.decode('hex'))[0]
		floor = returnstringpacket( pkt[report_pkt_offset -4: report_pkt_offset -6:-1])
		print "\tFloor: ", printpacket(pkt[report_pkt_offset -4: report_pkt_offset -6:-1]), " ", int(floor,16)
		trustValue = returnstringpacket( pkt[report_pkt_offset -2: report_pkt_offset -4:-1])
		print "\trustValue: ", printpacket(pkt[report_pkt_offset -2: report_pkt_offset -4:-1]), " ", int(trustValue,16)
		rssi, = struct.unpack("b", pkt[report_pkt_offset -1])
		print "\tRSSI:%i"%rssi
		
	# build the return string
	name = returnstringpacket( pkt[report_pkt_offset +12: report_pkt_offset -21])
	cenX = returnstringpacket( pkt[report_pkt_offset -14: report_pkt_offset -18:-1])
	cenY = returnstringpacket( pkt[report_pkt_offset -10: report_pkt_offset -14:-1])		
	stdNorm = returnstringpacket( pkt[report_pkt_offset -6: report_pkt_offset -10:-1])		
	floor = returnstringpacket( pkt[report_pkt_offset -4: report_pkt_offset -6:-1])
	trustValue = returnstringpacket( pkt[report_pkt_offset -2: report_pkt_offset -4:-1])
	
	Adstring = name.decode('hex')#Device Name
	Adstring += ","
	Adstring += "%i" % struct.unpack('!f', cenX.decode('hex'))[0]#Center X
	Adstring += ","
	Adstring += "%i" % struct.unpack('!f', cenY.decode('hex'))[0]#Center Y
	Adstring += ","
	Adstring += "%i" % struct.unpack('!f', stdNorm.decode('hex'))[0]#std Norm 
	Adstring += ","
	Adstring += "%i" % int(floor,16)#Floor
	Adstring += ","
	Adstring += "%i" % int(trustValue,16)#Trust Value
	Adstring += ","
	Adstring += "%i" % struct.unpack("b", pkt[report_pkt_offset -1])#RSSI
	
	return Adstring

def parse_events():
		
	pkt = PKT_QUEUE.get()
	ptype, event, plen = struct.unpack("BBB", pkt[:3])
	#print "--------------"
	
	Adstring = ""
	
	if event == bluez.EVT_INQUIRY_RESULT_WITH_RSSI:
		i =0
	elif event == bluez.EVT_NUM_COMP_PKTS:
		i =0 
	elif event == bluez.EVT_DISCONN_COMPLETE:
		i =0 
	elif event == LE_META_EVENT:
		subevent, = struct.unpack("B", pkt[3])
		pkt = pkt[4:]
		if subevent == EVT_LE_CONN_COMPLETE:
			le_handle_connection_complete(pkt)
		elif subevent == EVT_LE_ADVERTISING_REPORT:
			#print "advertising report"
			num_reports = struct.unpack("B", pkt[0])[0]
			
			for i in range(0, num_reports):

				#print "fullpacket: ", printpacket(pkt)
				name = returnstringpacket( pkt[12:-22]).decode('hex')
				#print name
				if ( name == "User" ):
					Adstring = extract_device_data(pkt)
				else:
					Adstring = extract_beacon_data(pkt)

	return Adstring.split(",")

def ble_scan(sock):

	old_filter = sock.getsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, 14)
	
	# perform a device inquiry on bluetooth device #0
	# The inquiry should last 8 * 1.28 = 10.24 seconds
	# before the inquiry is performed, bluez should flush its cache of
	# previously discovered devices
	flt = bluez.hci_filter_new()
	bluez.hci_filter_all_events(flt)
	bluez.hci_filter_set_ptype(flt, bluez.HCI_EVENT_PKT)
	sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, flt )
	
	sock.settimeout(SCAN_TIME)
	
	PKT_QUEUE = Queue.Queue()

	SYS_TIME = time.time()
	cur_time = time.time()
		
	while 1:
		#print ( cur_time - SYS_TIME )
		if ( cur_time - SYS_TIME >= SCAN_TIME ):
			break
		try:
			pkt = sock.recv(255)
			#print "\tfullpacket: ", printpacket(pkt)
			PKT_QUEUE.put(pkt)
			#print ble_data
			cur_time = time.time()
		except:
			break
			
	sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, old_filter )
		
	return PKT_QUEUE

def ble_adv():
	subprocess.Popen("hcitool -i hci0 cmd 0x08 0x0008 1e 02 01 1a 1a ff 4c 00 02 15 e2 c5 6d b5 df fb 48 d2 b0 60 d0 f5 a7 10 96 e0 00 00 00 00 c5 00 00 00 00 00 00 00 00 00 00 00 00 00",shell=True)
	proc = subprocess.Popen(["hciconfig", "hci0", "leadv", "0"])
	t = threading.Timer(ADV_TIME, adv_undo, [proc])
	t.start()
	t.join()
	
	
def adv_undo( p ):
	subprocess.Popen(["hciconfig", "hci0", "noleadv"])


	
