#!/usr/bin/python
import smbus
import time
bus = smbus.SMBus(1)
address = 0x04

def writeNumber(value):
   bus.write_byte(address, value)
   return -1

def readNumber():
   number = bus.read_byte(address)
   return number

def callForDrug(numA, numB):
   encodedNum = numA * 16 + numB
   writeNumber(encodedNum)
   print ("RPI: Hi Arduino, I ask you for ")
   print ("# of drug A: ", int(encodedNum / 16))
   print ("# of drug B: ", encodedNum % 16)
   time.sleep(1)
   
   number = readNumber()
   print ("Arduino: Hey RPI, I have received a request for ")
   print ("# of drug A: ", int(number / 16))
   print ("# of drug B: ", number % 16)
   print ()

#while True:
#   drugNumA = input("Enter 1 - 255 for the number of drug A:")
#   if not drugNumA:
#      continue
#   drugNumB = input("Enter 1 - 255 for the number of drug B:")
#   if not drugNumB:
#      continue
#   callForDrug(int(drugNumA), int(drugNumB))
