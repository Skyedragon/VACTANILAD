import serial
import sys
import time

class ISEL:
    def __init__(self, baudrate, bytesize, parity, stopbits, timeout):
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.timeout = timeout 
        
    def send(self, command):
        self.ser = serial.Serial('/dev/ttyUSB0', self.baudrate, self.bytesize, self.parity, self.stopbits, self.timeout)
        print('Port: ' ,self.ser.name)         # check which port was really used
        self.ser.write( (command + '\r').encode('utf-8') )     # write a string
        print( 'Command: ', (command + '\r').encode('utf-8') )
        while (True):
            answer = self.ser.readline()
            if answer != b'':
                break
        print('Answer:', answer)
        self.ser.close()             # close port
        return answer.decode('utf-8')

    def calibrate(self):
        #parameters of ISEL are given in manual. They are constant 
        IS = self.__class__(19200, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, 1)
        IS.send('@03')
        IS.send('@0R3')
        #IS.send('@0N3') #set current point as '0 point'
        return IS.send('@0P')
    
    def go_horiz_pos(self, along, side, speed):
        IS = self.__class__(19200, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, 1)
        steps_per_mm = 320
        along = int(along) * int(steps_per_mm)
        side = int(side) * int(steps_per_mm)
        IS.send('@0M ' + str(along) + ',' + str(speed) + ',' + str(side) + ',' + str(speed) ) #320 steps per 1 mm           
        curr_pos = IS.send('@0P')#[1:7] # returns 19 symbols. first 0 is default answer, then next 6 digits are carriage positio\   
        return curr_pos#show position converted from HEX to DEC and in mm                                                     
if __name__ == "__main__":
    ISEL = ISEL(19200, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, 1)
    ISEL.calibrate()
    a = ISEL.go_horiz_pos(sys.argv[1],sys.argv[2],1000) #in mm
    print(a)
