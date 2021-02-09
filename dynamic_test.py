from MCP3204 import *
from SwissBOY import *
from ISEL import *
import sys

ISEL = ISEL(19200, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, 1)
S = SwissBOY(15)

if __name__ == "__main__":
    ISEL.calibrate()
    ISEL.go_horiz_pos(sys.argv[1],sys.argv[2],1000)
    S.go_to_vert_pos(sys.argv[3])
