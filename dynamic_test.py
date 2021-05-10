#give nine or six numbers. First is left-right displacement, second is top-bottom, third is forward-backward
# 0 90 5 means from 0 to 90 mm with step of 5 mm from left to the right
# 0 90 5 120 155 10 - in addition do left-right movements for every height from 120 mm to 155 mm with step of 10 mm in height
# 0 90 5 120 155 10 0 200 20 - XYZ movement. For each Y do all Z with all X for each Z
from MCP3204 import *
from SwissBOY import *
from ISEL import *
from NetwAnalyser import *
import sys
import time

ISEL = ISEL(19200, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, 1)
S = SwissBOY(15)

def measureXY(xstart, xstop, xstep, ystart, ystop, ystep):
    ISEL.go_horiz_pos(xstart, 0, 2000)
    myvna=NetworkAnalyser('VACTANILAD.cal','192.168.1.3', measurement='S11')
    myvna.connect()
    S.go_to_vert_pos(ystart)
    for y in range(ystart, ystop, ystep):
        for x in range (xstart, xstop + xstep, xstep):
            print ('Meas at: ', x, y)
            time.sleep(10)
            print("Filename " + myvna.save_to_file(myvna.get_nice_filename(), myvna.get_data(), touchstone = False)  + " was created")
            ISEL.go_horiz_pos(x + xstep,0,2000)
        S.go_to_vert_pos(y+ystep)
        
    for x in range (xstart, xstop + xstep, xstep):
        print ('Meas at: ', x, y)
        time.sleep(10)
        print("Filename " + myvna.save_to_file(myvna.get_nice_filename(), myvna.get_data(),touchstone = False)  + " was created")
        ISEL.go_horiz_pos(x+xstep,0,2000)

def measureXYZ(xstart, xstop, xstep, ystart, ystop, ystep, zstart, zstop, zstep):
    ISEL.go_horiz_pos(xstart, zstart, 2000)
    S.go_to_vert_pos(ystart)
    myvna=NetworkAnalyser('VACTANILAD.cal','192.168.1.3', measurement='S11')
    myvna.connect()

    for y in range(ystart, ystop + ystep, ystep):
        for z in range (zstart, zstop + zstep, zstep):
            for x in range (xstart, xstop + xstep, xstep):
                print ('Meas at: ', x, y, z)
                time.sleep(10)
                print("Filename " + myvna.save_to_file(myvna.get_nice_filename(), myvna.get_data(), touchstone = False)  + " was created")
                ISEL.go_horiz_pos(x + xstep, z, 2000 )
            ISEL.go_horiz_pos(0,  z + zstep, 2000)
        S.go_to_vert_pos(y)

    for z in range (zstart, zstop + zstep, zstep):
        for x in range (xstart, xstop + xstep, xstep):
            print ('Meas at: ', x, y, z)
            time.sleep(10)
            print("Filename " + myvna.save_to_file(myvna.get_nice_filename(), myvna.get_data(), touchstone = False)  + " was created")
            ISEL.go_horiz_pos(x + xstep, z, 2000 )
        ISEL.go_horiz_pos(0,  z + zstep, 2000)

    
if __name__ == "__main__":
    ISEL.calibrate()
    Vertpos = S.get_vert_pos()
    Horpos = ISEL.get_horiz_pos()
    print("Horiz: ", Horpos, "Vert: ", Vertpos)
    measureXY( int(sys.argv[1]), int(sys.argv[2]),int(sys.argv[3]), int(sys.argv[4]),int( sys.argv[5]), int(sys.argv[6]) )
    #measureXYZ( int(sys.argv[1]), int(sys.argv[2]),int(sys.argv[3]), int(sys.argv[4]),int( sys.argv[5]), int(sys.argv[6]), int(sys.argv[7]), int(sys.argv[8]), int(sys.argv[9]) )
