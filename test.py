from MCP3204 import *
from SwissBOY import *
from ISEL import *

MCP = MCP3204()
#ISEL = ISEL(19200, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, 1)
SW = SwissBOY(0.1)
bits = 12 #MCP3204 is 12-bit ADC
rc35len = 400 #RC35 can stretch up to 400 mm
mcp_vert_zero = 0.09765625 # MCP output at physical zero vertical point

#this function will move the lifter top plate until it will reach given position
def go_vert_pos(pos): 
    pos = float (pos) #convert string from sys.argv into number
    curr_pos = rc35len-MCP.getAnalogData(sleep = 0.0,channel = 1)/2**bits*rc35len-mcp_vert_zero
    print("Current position: ", curr_pos)
    aver = 10
    step = 0
    
    if (curr_pos < pos): #if entered value is bigger than current position     
        while (curr_pos < pos):
            SW.go_up() #make one step up
            for i in range (aver): #average MCP output. It is a bit unstable around real position
                #position goes from 0 until 400 mm. But MCP counts 0 point at the 4095
                #that`s why position in mm = MAX_pos - ADC_output / MAX_ADC_output * total_length
                curr_pos +=  rc35len-MCP.getAnalogData(sleep = 0.0,channel = 1)/2**bits*rc35len-mcp_vert_zero
            curr_pos = round(curr_pos/(aver+1), 2)    
            step += 1
            print(curr_pos, step)
        SW.flush() #it is necessary to swith off the relays after each turn. In case you will stop your program in the middle
        return curr_pos

    if (curr_pos > pos):      
        while (curr_pos > pos):
            SW.go_down()
            for i in range (aver):
                curr_pos +=  rc35len-MCP.getAnalogData(sleep = 0.0,channel = 1)/2**bits*rc35len-mcp_vert_zero
            curr_pos = round(curr_pos/(aver+1), 2)    
            step += 1
            print(curr_pos, step)
        SW.flush()
        return curr_pos
            

if __name__ == "__main__":
    pos = sys.argv[1]
    go_vert_pos(pos)
#ISEL.send('@01')
#ISEL.send('@0R1')
#ISEL.send('@0M 32000,1000')
