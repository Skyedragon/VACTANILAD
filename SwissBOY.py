from MCP3204 import *
import time
import RPi.GPIO as GPIO

class SwissBOY:
    def __init__(self, step):
        self.up = 5
        self.down = 3
        self.step = step
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.up, GPIO.OUT)
        GPIO.setup(self.down, GPIO.OUT)
        GPIO.output(self.up, GPIO.LOW)
        GPIO.output(self.down, GPIO.LOW)

    def go_up(self):
        GPIO.output(self.up, GPIO.HIGH)
        time.sleep(self.step)
        GPIO.output(self.up, GPIO.LOW)
        time.sleep(self.step)
        
    def go_down(self):
        GPIO.output(self.down, GPIO.HIGH)
        time.sleep(self.step)
        GPIO.output(self.down, GPIO.LOW)
        time.sleep(self.step)
                   
    def flush(self):
        GPIO.output(self.up, GPIO.LOW)
        GPIO.output(self.down, GPIO.LOW)
    
if __name__ == "__main__":
    S = SwissBOY(3)
    while True:
        MCP = MCP3204()
        S.flush()
        S.go_up()
        print(MCP.getAnalogData(sleep = 0, channel = 0))
        S.go_down()
        print(MCP.getAnalogData(sleep = 0, channel = 0))
