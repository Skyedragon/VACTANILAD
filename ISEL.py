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
    
if __name__ == "__main__":
    ISEL = ISEL(19200, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, 1)
    a = ISEL.send(sys.argv[1])
    print(a)
