#!/usr/bin/python

import serial
import time
import os
import sys
path="/path/to/sb/file/"#enter the path to your sb file
filename="sb_file" #WARNING: do not add the .sb extension

def waitForSeq(seq):
	out=""
	it=0
	while out.find(seq)==-1 and it<1000:
		out += ser.read(1)
		it=it+1
	

input=1
while 1 :
	# get keyboard input
	input = raw_input(">> ")
	# Python 3 users
	# input = input(">> ")
	if input == 'exit':
		ser.close()
		exit()
	else:
		out = ''

	ret=os.system( "/usr/bin/wine XComp_RM186_PE_EU_FDF5_E990.exe "+path+filename+".sb") #change with your compiler 
	print("Compile returned "+str(ret))
	if ret!=0:
		break
	ser = serial.Serial(
		port='/dev/ttyUSB0', #here is the path to your serial interface
		baudrate=115200
	)
	ser.isOpen()

	ser.sendBreak(duration=1)
	time.sleep(2)

	ser.write("atz" + '\x0d')
	it=0
	while out.find("00")==-1 and it<1000:
		out += ser.read(1)
		print(out)
		it=it+1
	print("module performed reset")
	ser.write("at&f 1" + '\r\n')
	# let's wait one second before reading output (let's give device time to answer)
	time.sleep(1)
	it=0
	print(out)
	print(out.find("00"))
	while out.find("00")==-1 and it<1000:
		out += ser.read(1)
		it=it+1
	uwcfile=open(path+filename+".uwc").read()
	ser.write("AT+DEL \""+filename+"\" +\x0d")
	waitForSeq("\x0a\x30\x30\x0d")
	ser.write("AT+FOW \""+filename+"\"\x0d")
	waitForSeq("\x0a\x30\x30\x0d")

	#Write the file
	write=True
	if write:
		while len(uwcfile)>=50:
			chunk=''
			for i in range(0,50):
				chunk=chunk+uwcfile[i].encode('hex').upper()
			print(len(uwcfile))
			uwcfile=uwcfile[50:]
			chunk="AT+FWRH \""+chunk+"\"\x0d"
			ser.write(chunk)
			waitForSeq("\x0a\x30\x30\x0d")

		chunk=''
		for i in range(0,len(uwcfile)):
			chunk=chunk+uwcfile[i].encode('hex').upper()
		chunk="AT+FWRH \""+chunk+"\"\x0d"
		ser.write(chunk)
		waitForSeq("\x0a\x30\x30\x0d")

		ser.write("AT+FCL\x0d")
		waitForSeq("\x0a\x30\x30\x0d")


		ser.write("at+run \""+filename+ '\"\r\n')
	ser.close()
