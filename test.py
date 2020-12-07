from MCP3204 import *
from SwissBOY import *
from ISEL import *

#this function will move the lifter top plate until it will reach given position
def go_vert_pos(pos, speed): 

    SW = SwissBOY(float(1/speed))# speed is steps/second, and SwissBOY initialized with time delay between steps
    bits = 12 #MCP3204 is 12-bit ADC
    rc35len = 400 #RC35 can stretch up to 400 mm
    mcp_vert_zero = 0.09765625 # MCP output at physical zero vertical point
    aver = 100 #for averaging of the MCP output
    MCP = MCP3204()
    pos = float (pos) #convert string from sys.argv into number
    step = 0
    curr_pos = rc35len-MCP.getAnalogData(sleep = 0.0,channel = 0)/2**bits*rc35len-mcp_vert_zero
    print("Current position: ", curr_pos)

    if (curr_pos < pos): #if entered value is bigger than current position     
        while (curr_pos < pos):
            SW.go_up() #make one step up
            for i in range (aver): #average MCP output. It is a bit unstable around real position
                #position goes from 0 until 400 mm. But MCP counts 0 point at the 4095
                #that`s why position in mm = MAX_pos - ADC_output / MAX_ADC_output * total_length
                curr_pos +=  rc35len-MCP.getAnalogData(sleep = 0.0,channel = 0)/2**bits*rc35len-mcp_vert_zero
            curr_pos = round(curr_pos/(aver+1), 2)    
            step += 1
            print(curr_pos, step)
        SW.flush() #it is necessary to swith off the relays after each turn. In case you will stop your program in the middle
        return curr_pos

    if (curr_pos > pos):      
        while (curr_pos > pos):
            SW.go_down()
            for i in range (aver):
                curr_pos +=  rc35len-MCP.getAnalogData(sleep = 0.0,channel = 0)/2**bits*rc35len-mcp_vert_zero
            curr_pos = round(curr_pos/(aver+1), 2)    
            step += 1
            print(curr_pos, step)
        SW.flush()
        return curr_pos
            
def start_isel():
    #parameters of ISEL are given in manual. They are constant
    IS = ISEL(19200, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, 1)
    IS.send('@01') #initialize 1 axis
    IS.send('@0R1')# return to '0 point' 
    return 0    

def go_horiz_pos(pos, speed):
    IS = ISEL(19200, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, 1)
    steps_per_mm = 320
    pos = int(pos) * int(steps_per_mm)
    IS.send('@0M '+ str(pos) +',' + str(speed)) #320 steps per 1 mm
    curr_pos = IS.send('@0P')[1:7] # returns 19 symbols. first 0 is default answer, then next 6 digits are carriage position
    return (int (curr_pos, 16) / steps_per_mm)#show position converted from HEX to DEC and in mm

if __name__ == "__main__":
    start_isel()
    pos = (sys.argv[1], sys.argv[2])
    Y = go_vert_pos(pos[0], 10)
    X = go_horiz_pos(pos[1],1000)
    print(X, Y)
    #go_vert_pos(40,10)
