from MCP3204 import *
from SwissBOY import *
from ISEL import *

MCP = MCP3204()
#ISEL = ISEL(19200, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, 1)
SW = SwissBOY(0.1)

def go_vert_pos(pos):
    pos = float (pos)
    curr_pos = 400-MCP.getAnalogData(sleep = 0.0,channel = 1)/4096*400-0.09765625
    print("Current position: ", curr_pos)
    aver = 10
    step = 0
    
    if (curr_pos < pos):      
        while (curr_pos < pos):
            SW.go_up()
            for i in range (aver):
                curr_pos +=  400-MCP.getAnalogData(sleep = 0.0,channel = 1)/4096*400-0.09765625
            curr_pos = round(curr_pos/(aver+1), 2)    
            step += 1
            print(curr_pos, step)
        SW.flush()
        return curr_pos

    if (curr_pos > pos):      
        while (curr_pos > pos):
            SW.go_down()
            for i in range (aver):
                curr_pos +=  400-MCP.getAnalogData(sleep = 0.0,channel = 1)/4096*400-0.09765625
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
