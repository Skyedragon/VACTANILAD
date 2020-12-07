from MCP3204 import *
from SwissBOY import *
from ISEL import *

MCP = MCP3204()
pot0 = 400 - MCP.getAnalogData(sleep = 1,channel = 0)/4096*400-0.09765625
pot1 = 400 - MCP.getAnalogData(sleep = 1,channel = 1)/4096*400

ISEL = ISEL(19200, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, 1)

SW = SwissBOY(1)
SW.flush()
SW.go_up()
print(pot0, pot1)
SW.go_down()
print(pot0, pot1)
ISEL.send('@01')
ISEL.send('@0R1')
#ISEL.send('@0M 32000,1000')
