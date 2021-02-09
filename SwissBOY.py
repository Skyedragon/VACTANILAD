from MCP3204 import *
import time
import RPi.GPIO as GPIO
import sys

class SwissBOY:
    def __init__(self, step):
        self.up = 3
        self.down = 5
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
    
    def go_to_vert_pos(self, pos):
        SW = self.__class__(float(1/self.step))# speed is steps/second, and SwissBOY initialized with time delay between steps           
        bits = 12 #MCP3204 is 12-bit ADC                                                                                       
        rc35len = 400 #RC35 can stretch up to 400 mm                                                                           
        mcp_vert_zero = 0.09765625 # MCP output at physical zero vertical point                                                
        aver = 100 #for averaging of the MCP output                                                                          
        MCP = MCP3204()
        pos = float (pos) #convert string from sys.argv into number                                                            
        step = 0
        copperzero = 10.2
        curr_pos = (rc35len-MCP.getAnalogData(sleep = 0.0,channel = 0)/2**bits*rc35len-mcp_vert_zero)+copperzero
        print("Current position: ", curr_pos)
        if (curr_pos < pos): #if entered value is bigger than current position                                                 
            while (curr_pos < pos):
                SW.go_up() #make one step up                                                                                   
                #time.sleep(1)                                                                                                 
                for i in range (aver): #average MCP output. It is a bit unstable around real position                          
                    #position goes from 0 until 400 mm. But MCP counts 0 point at the 4095                                     
                    #that`s why position in mm = MAX_pos - ADC_output / MAX_ADC_output * total_length                          
                    curr_pos +=  (rc35len-MCP.getAnalogData(sleep = 0.0,channel = 0)/2**bits*rc35len-mcp_vert_zero)+copperzero
                curr_pos = round(curr_pos/(aver+1), 2)
                step += 1
                print(curr_pos, step)
            SW.flush() #it is necessary to swith off the relays after each turn. In case you will stop your program in the mid
            return curr_pos

        if (curr_pos > pos):
            while (curr_pos > pos):
                SW.go_down()
                #time.sleep(1)                                                                                                 
                for i in range (aver):
                    curr_pos +=  (rc35len-MCP.getAnalogData(sleep = 0.0,channel = 0)/2**bits*rc35len-mcp_vert_zero)+copperzero
                curr_pos = round(curr_pos/(aver+1), 2)
                step += 1
                print(curr_pos, step)
            SW.flush() #it is necessary to swith off the relays after each turn. In case you will stop your program in the middle
            return curr_pos

    def get_vert_pos(self):
        return (rc35len-MCP.getAnalogData(sleep = 0.0,channel = 0)/2**bits*rc35len-mcp_vert_zero)+copperzero
    
if __name__ == "__main__":
    S = SwissBOY(15)
    S.go_to_vert_pos(sys.argv[1])
