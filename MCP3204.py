#!/usr/bin/python
#-*- coding:utf-8 -*-
import time
import RPi.GPIO as GPIO

class MCP3204:
        def __init__(self):
                GPIO.setmode(GPIO.BOARD)
                # Konfiguration Eingangskanal und GPIOs
                self.CLK     = 23 # Clock
                self.DIN     = 19 # Digital in MOSI
                self.DOUT    = 21  # Digital out MISO
                self.CS      = 24  # Chip-Select
        
        def getAnalogData(self, sleep, channel):
            
            HIGH = True
            LOW = False     
        #set SPI(0.0) pins as inputs or outputs
            GPIO.setup(self.CLK, GPIO.OUT)
            GPIO.setup(self.DIN, GPIO.OUT)
            GPIO.setup(self.DOUT, GPIO.IN)
            GPIO.setup(self.CS,   GPIO.OUT)
            #flick the chip select pin to awake the MCP 
            GPIO.output(self.CS,   HIGH)
            GPIO.output(self.CS,   LOW)
            GPIO.output(self.CLK,  LOW)

            time.sleep(sleep)
            cmd = channel
            cmd |= 0b00011000 # Kommando zum Abruf der Analogwerte des Datenkanals adCh
            #Bitfolgesenden
            for i in range(5):
                if (cmd & 0x10): # 4. Bit prüfen und mit 0 anfangen
                    GPIO.output(self.DIN, HIGH)
                else:
                    GPIO.output(self.DIN, LOW)
                # Clocksignal negative Flanke erzeugen 
                GPIO.output(self.CLK, HIGH)
                GPIO.output(self.CLK, LOW)
                cmd <<= 1 # Bitfolge eine Position nach links verschieben
            # Datenabruf                                                                                                                                   
            adchvalue = 0 # Wert auf 0 zurücksetzen
            for i in range(13):
                GPIO.output(self.CLK, HIGH)
                GPIO.output(self.CLK, LOW)
                adchvalue <<= 1 # 1 Postition nach links schieben
                if(GPIO.input(self.DOUT)):
                        adchvalue |= 0x01
            return adchvalue

if __name__ == "__main__":
        MCP=MCP3204() #0.390625 is a value of fully closed pot-r
        while True:
                print ("channel 0: ", 389.8-MCP.getAnalogData(sleep = 1, channel = 0)/4096*400)
                print ("channel 1: ", MCP.getAnalogData(sleep = 1, channel = 1))
