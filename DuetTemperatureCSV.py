#!/usr/bin/env python3
# Python Script to take poll a Duet printer for temperatures and write a CSV file. 
#
# Copyright (C) 2020 Danal Estes all rights reserved.
# Released under The MIT License. Full text available via https://opensource.org/licenses/MIT
#
# Implemented to run on Raspbian on a Raspberry Pi.  May be adaptable to other platforms. 
# 
# The Duet printer must be RepRap firmware V2 or V3 and must be network reachable. 
#

import subprocess
import sys
import argparse
import time
try: 
    import DuetWebAPI as DWA
except ImportError:
    print("Python Library Module 'DuetWebAPI.py' is required. ")
    print("Obtain from https://github.com/DanalEstes/DuetWebAPI ")
    print("Place in same directory as script, or in Python libpath.")
    exit(2)

###########################
# Methods begin here
###########################


def init():
    # parse command line arguments
    parser = argparse.ArgumentParser(description='Program to create time lapse video from camera pointed at Duet3D based printer.', allow_abbrev=False)
    parser.add_argument('fileName',help="Specify name of CSV file to write")
    parser.add_argument('-duet',type=str,nargs=1,default=['localhost'],help='Name or IP address of Duet printer. You can use -duet=localhost if you are on the embedded Pi on a Duet3.')
    args=vars(parser.parse_args())

    global fileName, duet
    fileName = args['fileName']
    duet     = args['duet'][0]

    print('Attempting to connect to printer at '+duet)
    global printer
    printer = DWA.DuetWebAPI('http://'+duet)
    if (not printer.printerType()):
        print('Device at '+duet+' either did not respond or is not a Duet V2 or V3 printer.')
        exit(2)
    printer = DWA.DuetWebAPI('http://'+duet)

    print("Connected to a Duet V"+str(printer.printerType())+" printer at "+printer.baseURL())
    
    if (not fileName[-4:] == '.csv'): fileName += '.csv'

    global FH
    FH = open(fileName, 'w')
    sensors=printer.getTemperatures()
    FH.write('timestamp')
    for sensor in sensors:
        FH.write(','+sensor['name'])
    FH.write('\n')


    # Tell user options in use. 
    print()
    print("#################################################################")
    print("# Options in force for this run:                                #")
    print("#   printer = {0:50s}#".format(duet))
    print("# file name = {0:50s}#".format(fileName))
    print("#################################################################")
    print()
    print('Now writing temperatures, press Ctrl-C to exit. ')

###########################
# Main begins here
###########################
init()
while(1):
    sensors=printer.getTemperatures()
    FH.write(time.strftime('%m-%d-%y %H:%M:%S',time.localtime()))
    for sensor in sensors:
        FH.write(','+'{0:4.2f}'.format((sensor['lastReading'])))
    FH.write('\n')
    time.sleep(2)