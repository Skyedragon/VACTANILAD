#Program awaits (dimensions x 3) numbers. First is left-right displacement, second is top-bottom, third is forward-backward                                                                                                                                  
# 0 90 5 means from 0 to 90 mm with step of 5 mm from left to the right                                                                                                                                                                       
# 0 90 5 120 155 10 - in addition do left-right movements for every height from 120 mm to 155 mm with step of 10 mm in height                                                                                                                 
# 0 90 5 120 155 10 0 200 20 - XYZ movement. For each Y do all Z with all X for each Z

#For lime measurements in 2D:
#--xstart 0 --xstop 90 --xstep 5 --ystart 160 --ystop 200 --ystep 5 --meastime 1 --center 500e6 --samprate 1e6 --bw 4e6 --channel 1 2

from MCP3204 import *
from SwissBOY import *
from ISEL import *
#from NetwAnalyser import *
from Lime import *
from datetime import datetime
import sys
import time

ISEL = ISEL(19200, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, 1)
S = SwissBOY(15)

#this function moves the cavity in 2D (left-right-top-bottom) and records data for every cavity position
#VNA and LimeSDR measurements are possible, one has to uncomment needed lines
def measureXY(xstart, xstop, xstep, ystart, ystop, ystep, center, meas_time, bw, samprate, channel):
    ISEL.go_horiz_pos(xstart, 0, 2000)
    #next two lines are needed to initialize and connect to VNA
    #myvna=NetworkAnalyser('VACTANILAD.cal','192.168.1.3', measurement='S11')
    #myvna.connect()
    S.go_to_vert_pos(ystart)
    for y in range(ystart, ystop, ystep):
        for x in range (xstart, xstop + xstep, xstep):
            ISEL.go_horiz_pos(x,0,2000)
            print ('Meas at: ', x, y)
            time.sleep(1)#for measurements make 10
            Lime = LimeSDR(center, meas_time, bw, samprate, channel)

            #next line is needed for measurements using VNA
            #print("Filename " + myvna.save_to_file(myvna.get_nice_filename(), myvna.get_data(), touchstone = False)  + " was created")

            #next line is needed for measurement with different filenames
            #Lime.make_iq( (str (datetime.now().time() )+'ch1.bin', str(datetime.now().time() )+'ch2.bin'), int(meas_time) )

            #next line is needed for test measurements for 36 hours. Data was saved in the same file
            Lime.make_iq( ('ch1.bin', 'ch2.bin'), int(meas_time) ) 
            x += xstep
        S.go_to_vert_pos(y+ystep)

    for x in range (xstart, xstop + xstep, xstep):
        print ('Meas at: ', x, y)
        time.sleep(1)#for measurements make 10
        #print("Filename " + myvna.save_to_file(myvna.get_nice_filename(), myvna.get_data(),touchstone = False)  + " was created")
        Lime = LimeSDR(center, meas_time, bw, samprate, channel)
        Lime.make_iq( ('ch1.bin', 'ch2.bin'), int(meas_time) )
        #Lime.make_iq( ( str( datetime.now().time() )+'ch1.bin', str( datetime.now().time() )+'ch2.bin'), int(meas_time) )  
        ISEL.go_horiz_pos(x+xstep,0,2000)

#This function was made for bead measurements and it allows to move cavity in 3D.
#Measurements using VNA are possible
def measureXYZ(xstart, xstop, xstep, ystart, ystop, ystep, zstart, zstop, zstep):
    ISEL.go_horiz_pos(xstart, zstart, 2000)
    S.go_to_vert_pos(ystart)
    #myvna=NetworkAnalyser('VACTANILAD.cal','192.168.1.3', measurement='S11')
    #myvna.connect()

    for y in range(ystart, ystop + ystep, ystep):
        for z in range (zstart, zstop + zstep, zstep):
            for x in range (xstart, xstop + xstep, xstep):
                print ('Meas at: ', x, y, z)
                time.sleep(10)
                #print("Filename " + myvna.save_to_file(myvna.get_nice_filename(), myvna.get_data(), touchstone = False)  + " was created")
                ISEL.go_horiz_pos(x + xstep, z, 2000 )
            ISEL.go_horiz_pos(0,  z + zstep, 2000)
        S.go_to_vert_pos(y)

    for z in range (zstart, zstop + zstep, zstep):
        for x in range (xstart, xstop + xstep, xstep):
            print ('Meas at: ', x, y, z)
            time.sleep(10)
            #print("Filename " + myvna.save_to_file(myvna.get_nice_filename(), myvna.get_data(), touchstone = False)  + " was created")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--xstart", type=int, nargs='?', help="Initial position for horizontal movement")
    parser.add_argument("--xstop", type=int, nargs='?', help="Final position for horizontal movement")
    parser.add_argument("--xstep", type=int, nargs='?', help="Step size for horizontal movement")
    parser.add_argument("--ystart", type=int, nargs='?', help="Initial position for vertical movement")
    parser.add_argument("--ystop", type=int, nargs='?', help="Final position for vertical movement")
    parser.add_argument("--ystep", type=int, nargs='?', help="step size for vertical movement")
    parser.add_argument("--center", type=float, nargs='?', help="Set local oscillator frequency")
    parser.add_argument("--meastime", type=int, nargs='?', help="Set measurement time")
    parser.add_argument("--samprate", type=float, nargs='?', help="Set sampling rate")
    parser.add_argument("--bw", type=float, nargs='?', help="Set bandwidth")
    parser.add_argument("--channel", type=int, nargs='+', help="Set channels to read data from")
    parser.add_argument("--filename", type=str, action='append', nargs='+', help="Path to saved file")
    args = parser.parse_args()

    if args.meastime and args.samprate and args.bw and args.channel:
        print ("Central frequency set to ", args.center, " Hz.")
        print ("Measurement time set to ", args.time, " sec.")
        print ("Sampling rate set to ", args.samprate, " Samples/sec.")
        print ("Bandwidth set to ", args.bw, " Hz.")

        if ( len(args.channel) == len(args.filename[0]) and len(args.channel) == 1 ):
            print ("Reading from channels ", args.channel[0])
    
        elif ( len(args.channel) == len(args.filename[0]) and len(args.channel) == 2 ):
            print ("Reading from channels ", args.channel[0],args.channel[1])
        
        else:
            print ("channels amount not equal to amount of files")
    else:
        print ("Wrong set of parameters was given")
    while (1):
        ISEL.calibrate()
        Vertpos = S.get_vert_pos()
        Horpos = ISEL.get_horiz_pos()
        print("Horiz: ", Horpos, "Vert: ", Vertpos)
        measureXY(args.xstart, args.xstop, args.xstep, args.ystart, args.ystop, args.ystep, args.center, args.meastime, args.bw, args.samprate, args.channel )
        #measureXYZ( int(sys.argv[1]), int(sys.argv[2]),int(sys.argv[3]), int(sys.argv[4]),int( sys.argv[5]), int(sys.argv[6]), int(sys.argv[7]), int(sys.argv[8]), int(sys.argv[9]) )
