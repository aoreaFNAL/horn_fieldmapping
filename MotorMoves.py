import pyvisa as visa
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC
import time
import numpy as np
from os import system
from datetime import datetime

def move(dir_pin, step_pin, direction, nstp):
    npulses = nstp #2000 steps per inch, ~79 steps per mm
    pulse = 1
    if direction == 1:
        GPIO.output(dir_pin, GPIO.HIGH)
    elif direction == 0:
        GPIO.output(dir_pin, GPIO.LOW)

    while pulse != (npulses+1):
        GPIO.output(step_pin, GPIO.HIGH)
        time.sleep(0.0005)
        GPIO.output(step_pin, GPIO.LOW)
        pulse = pulse+1
        time.sleep(0.0005)

    GPIO.output(dir_pin, GPIO.LOW)

def read_position(X_pos, Y_pos, Z_pos):
    ref = 1.8 # ADC reference voltage

    X = ref*float(ADC.read(X_pos))
    Y = ref*float(ADC.read(Y_pos))
    Z = ref*float(ADC.read(Z_pos))
    print("X: %.2f\tY: %.2f\tZ: %.2f"%(X,Y,Z))  
    return X, Y, Z

##def initialize_scope(IP_address):
##    ''' Initalize and connect to oscilliscope.'''
##
##    print("Connecting to scope @ {}".format(IP_address))
##    rm = visa.ResourceManager('@py')
##    try:
##        # Initialize connection to scope
##        scope = rm.open_resource('TCPIP0::%s::inst0::INSTR'%(IP_address))
##        print(scope.query('*IDN?'))
##        if scope:
##            print("Connection successful. Configuring scope.")
##
##        # Clear the status data structures, the device-defined error queue, and the Request-for-OPC flag
##        scope.write('*CLS')
##
##        # Set up scope parameters
##        scope.write(":ACQuire:TYPE NORMal")
##        scope.write(":TIMebase:MODE MAIN")
##
##        # External triggering
##        #scope.write(":TRIGger:MODE EDGE")
##        #scope.write(":TRIGger:SOURce EXTernal")
##        #scope.write(":TRIGger:LEVel 0.5")
##        print("Configuration complete.")
##    except Exception as e:
##        print(e)
##        print("Error connecting to scope.")
##        #exit(1)
##    return scope

##def get_waveform(scope, ch_num):
##    '''Acquire data from a given scope's channel, returning a time and voltage array for that trigger.'''
##
##    print("Getting data from Channel "+str(ch_num))
##    scope.write(":WAVeform:SOURce CHANnel{}".format(ch_num))
##    preamble = scope.query(':WAVeform:PREamble?').split(',')
##    print(preamble)
##    values = scope.query_binary_values(':WAVeform:DATA?', datatype='h', container=np.array)
##
##    num_samples = int(preamble[2])
##
##    x_increment, x_origin, x_reference = float(preamble[4]), float(preamble[5]), float(preamble[6])
##    time = np.array([(np.arange(num_samples)-x_reference)*x_increment + x_origin]) # compute x-values
##    time = time.T # make x values vertical
##
##    y_increment, y_origin, y_reference = float(preamble[7]), float(preamble[8]), float(preamble[9])
##    voltage = (values-y_reference)*y_increment + y_origin
##
##
##    return time, voltage

def get_data(filename, stripline_scope, field_scope, X_pos, Y_pos, Z_pos):

##    # Wait for a horn trigger
##    print('Waiting for horn trigger.')
##    GPIO.wait_for_edge(trigger, GPIO.RISING)
##
##    stripline_scope.write(":SINGle")
##    # Make sure WORD and BYTE data is transeferred as signed ints and lease significant bit first
##    stripline_scope.write(':WAVeform:UNSigned OFF')
##    stripline_scope.write(':WAVeform:BYTeorder LSBFirst') # MSBF is default, must be overridden for WORD to work
##    stripline_scope.write(":WAVeform:FORMat WORD")
##    stripline_scope.write(":WAVeform:POINts 100")
##
##    field_scope.write(":SINGle")
##    # Make sure WORD and BYTE data is transeferred as signed ints and lease significant bit first
##    field_scope.write(':WAVeform:UNSigned OFF')
##    field_scope.write(':WAVeform:BYTeorder LSBFirst') # MSBF is default, must be overridden for WORD to work
##    field_scope.write(":WAVeform:FORMat WORD")
##    field_scope.write(":WAVeform:POINts 100")
##    
##    # Wait for a horn trigger
##    print('Waiting for horn trigger.')
##    GPIO.wait_for_edge(trigger, GPIO.RISING)
##
##    # Acquire stripline and field probe waveforms
##    stripline_time1, stripline_voltage1 = get_waveform(stripline_scope, 1)
##    stripline_time2, stripline_voltage2 = get_waveform(stripline_scope, 2)
##    stripline_time3, stripline_voltage3 = get_waveform(stripline_scope, 3)
##    stripline_time4, stripline_voltage4 = get_waveform(stripline_scope, 4)
##    Xfield_time, Xfield_voltage = get_waveform(field_scope, 1)
##    Yfield_time, Yfield_voltage = get_waveform(field_scope, 2)
##    Zfield_time, Zfield_voltage = get_waveform(field_scope, 3) 
##    
##    # Need to add a conversion to mm and Tesla here
    
    # Get the position of the stage
    print('Acquiring stage position.')
    X, Y, Z = read_position(X_pos, Y_pos, Z_pos)

##    print('Writing data to file.')
##    # Initialize the file with the current date and time
##    with open(filename, 'a') as f:
##        f.write('X = %.4f \t Y = %.4f \t Z = %.4f \n'%(X, Y, Z))
##        data_format = '%.4f %18.4f %18.4f %18.4f %18.4f %18.4f %18.4f %18.4f %18.4f %18.4f %18.4f %18.4f %18.4f %18.4f \n'
##        for i in range(len(stripline_time1)):
##            f.write(data_format % (stripline_time1[i], stripline_voltage1[i], stripline_time2[i], stripline_voltage2[i], stripline_time3[i], stripline_voltage3[i], stripline_time4[i], stripline_voltage4[i], Xfield_time[i], Xfield_voltage[i], Yfield_time[i], Yfield_voltage[i], Zfield_time[i], Zfield_voltage[i]))
##    
##    print('Data acquisition complete.')

### Setup GPIO ###
MotorX_dir = 'P8_10'
MotorX_step = 'P8_8'
MotorY_dir = 'P8_14'
MotorY_step = 'P8_12'
MotorZ_dir = 'P8_18'
MotorZ_step = 'P8_16'

X_pos = 'P9_40'
Y_pos = 'P9_38'
Z_pos = 'P9_36'

trigger = 'P8_7'
###

### Setup motor pulse pins ###
GPIO.setup(MotorX_dir, GPIO.OUT)
GPIO.setup(MotorX_step, GPIO.OUT)
GPIO.setup(MotorY_dir, GPIO.OUT)
GPIO.setup(MotorY_step, GPIO.OUT)
GPIO.setup(MotorZ_dir, GPIO.OUT)
GPIO.setup(MotorZ_step, GPIO.OUT)
###

### Setup trigger input pin ###
GPIO.setup(trigger, GPIO.IN)
###


### Setup ADC ###
ADC.setup()
###

### Setup oscilloscopes ###
##stripline_scope_IP = '192.168.1.10'
##
##field_scope_IP = '192.168.1.11'

# Setup BBB ethernet connection
##print('Setting up BeagleBone ethernet connection.')
##system('sudo ifconfig eth0 192.168.1.1 netmask 255.255.248.0')

# Setup stripline scope
##print('Initializing stripline scope.')
##stripline_scope = initialize_scope(stripline_scope_IP)

# Setup field scope
##print('Initializing magnetic field scope.')
##field_scope = initialize_scope(field_scope_IP)

# Generate filename from datetime
##now = datetime.now()
##filename = str(now).replace(" ", "_")+'.txt'
##print('Data filename is: %s'%(filename))

##header_format = '%s %10s %10s %10s %10s %10s %10s %10s %10s %10s %10s %10s %10s %10s \n'
##with open(filename, 'w') as f:
##    f.write(str(now)+'\n\n')
##    f.write(header_format % ('stripline_time1', 'stripline_voltage1', 'stripline_time2', 'stripline_voltage2', 'stripline_time3', 'stripline_voltage3', 'stripline_time4', 'stripline_voltage4', 'Xfield_time', 'Xfield_voltage', 'Yfield_time', 'Yfield_voltage', 'Zfield_time', 'Zfield_voltage'+'\n'))

instructions = 'Press: [L]eft, [R]ight, [U]p, [D]own, [F]orward, or [B]ack then <Enter>. Press CTRL+C to exit.'
##instructions = 'Press: [L]eft, [R]ight, [U]p, [D]own, [F]orward, [B]ack, or [A]cquire data, then <Enter>. Press CTRL+C to exit.'

print('Starting positions:')
X, Y, Z = read_position(X_pos, Y_pos, Z_pos)
print('\nX: %.4f \nY: %.4f \nZ: %.4f \n'%(X,Y,Z))
while 1:
    print(instructions)
    print('Y is double the travel')
    variable = str(input())
    #variable = str(raw_input())
    if variable == 'f':
        print("Moving forward\n")
        stp = int(input("How many steps?\t"))
        move(MotorZ_dir, MotorZ_step, 0, stp)
        X, Y, Z = read_position(X_pos, Y_pos, Z_pos)
    elif variable == 'b':
        print("Moving backward\n")
        stp = int(input("How many steps?\t"))
        move(MotorZ_dir, MotorZ_step, 1, stp)
        X, Y, Z = read_position(X_pos, Y_pos, Z_pos)
    elif variable == 'r':
        print("Moving right\n")
        stp = int(input("How many steps?\t"))
        move(MotorX_dir, MotorX_step, 1, stp)
        X, Y, Z = read_position(X_pos, Y_pos, Z_pos)
    elif variable == 'l':
        print("Moving left\n")
        stp = int(input("How many steps?\t"))
        move(MotorX_dir, MotorX_step, 0, stp)
        X, Y, Z = read_position(X_pos, Y_pos, Z_pos)
    elif variable == 'u':
        print("Moving up\n")
        stp = int(input("How many steps?\t"))
        move(MotorY_dir, MotorY_step, 1, stp)
        X, Y, Z = read_position(X_pos, Y_pos, Z_pos)
    elif variable == 'd':
        print("Moving down\n")
        stp = int(input("How many steps?\t"))
        move(MotorY_dir, MotorY_step, 0, stp)
        X, Y, Z = read_position(X_pos, Y_pos, Z_pos)
##    elif variable == 'a':
##        for p in range(0,10,1):
##            get_data(filename, stripline_scope, field_scope, X_pos, Y_pos, Z_pos)
    else:
        print('Invalid command.')
        X, Y, Z = read_position(X_pos, Y_pos, Z_pos)
        print('\nX: %.4f \nY: %.4f \nZ: %.4f \n'%(X,Y,Z))
