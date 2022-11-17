#Code written by Justin deMattos (MIIP Optics Track '20)
#Designed for use with Jobin Yvon-Spex HR460 Spectrometer
#Advanced Project Lab University of Oregon
#Function: Creates functions to allow user and GUI to communicate with spectrometer

import struct
import serial
from serial import Serial
import sys
import math
import numpy as np 
import csv


class Spectrometer:
    #Set up serial port connection.
    #Parameters: USB port name in a string format.
    #Returns: NA
    def __init__(self,usb):
        self.usb = usb
        usbdir = '/dev/' + self.usb
        self.s = serial.Serial(usbdir,19200,timeout=1)

    #Determine what menu the device is in. Prints where the device is.
    #Parameters: NA
    #Returns: NA. Prints where user is.
    def whereAmI(self):
        self.s.write(b' ')
        output=self.s.readline()
        output=output.decode('utf-8')
        print("You are here: " + output)

    #Reset the spectrometer. Print restart message
    #Parameters: NA
    #Returns: NA. Prints restarting though.
    def reset(self):
        self.s.write(struct.pack('!B',222))
        print("Restarting device")
    
    #Turn on the device. Includes switching to intelligent mode and F main menu.
    #Parameters: NA
    #Returns: NA. Prints that it is done though.
    def on(self):
        self.s.write(b' ')
        output=self.s.readline()
        output=output.decode('utf-8')
        timer = 0

        if output=='F':
            return

        if output=='B':
            self.s.write(b'O2000'+struct.pack('!B',0))
            output = self.s.readline()
            output = output.decode('utf-8')
            timer = 100

            #If the device doesn't return that the command was accepted, exit
            while output!= '*' and timer>0:
                print("Bad response for F mode " + output + ". Restarting...")
                self.s.write(b'O2000'+struct.pack('!B',0))
                output = self.s.readline()
                output = output.decode('utf-8')
                timer=timer-1

            print("Switched to F mode!")
            return

        else:

            #Make sure device turns on and is ready for commands
            timer=0
            try:
                while output[0]!='*' and timer<20:
                    self.s.write(b' ')
                    output=self.s.readline()
                    output=output.decode('utf-8')
                    print('Wating for startup...' + output)
                    timer+=1
                if timer>=20:
                    sys.exit("Exited due to timeout starting spectrometer!")

            except IndexError:
                print('Not ready, trying again...')
                self.on()

            #Switch device to intelligent mode
            self.s.write(struct.pack('!B',247))
            output = self.s.readline()
            output = output.decode('utf-8')
            timer = 100

            while output != '=' and timer>0:
                print("Bad response for intelligent mode: " + output + ". Restarting...")
                self.s.write(struct.pack('!B',247))
                output = self.s.readline()
                output = output.decode('utf-8')
                timer=timer-1


            print("Switched to intelligent mode.")
        
            #Switch device into main mode (F mode)
            self.s.write(b'O2000'+struct.pack('!B',0))
            output = self.s.readline()
            output = output.decode('utf-8')
            timer = 100

            #If the device doesn't return that the command was accepted, exit
            while output!= '*' and timer>0:
                print("Bad response for F mode " + output + ". Restarting...")
                self.s.write(b'O2000'+struct.pack('!B',0))
                output = self.s.readline()
                output = output.decode('utf-8')
                timer=timer-1

            print("Switched to F mode!")

            #Check that the device is in 'F' mode
            #Parameters: NA
            #Returns: NA
            self.s.write(b' ')
            output = self.s.readline()
            output = output.decode('utf-8')
            print("Checking for main mode. Response; " + output)

            #If the device did not switch to F mode, exit
            if output != 'F':
                sys.exit('Exited because not in F mode!')

            print("Ready!")
            return
    
    #Set the motor speed for the device. This needs to be done just before or just after initialization
    #Parameters: mono = monochramtor input number  min = minimum frequency (steps/s)  max = maximum frequency (steps/s)  ramp = ramp time (ms)
    #Returns: NA. Prints when completed though.
    def setMotorSpeed(self,mono='0',min='2560',max='5500',ramp='2000'):
        mono = str.encode(mono)
        min = str.encode(min)
        max = str.encode(max)
        ramp = str.encode(ramp)
        
        #Set motor speed
        self.s.write(b'B' + mono + b',' + min + b',' + max + b',' + ramp + b'\r')
        output = self.s.readline()
        output = output.decode('utf-8')

        #If motor speed was not set correctly, exit
        if output != 'o':
            sys.exit('Exited being unable to set motor speed!' + output)

        print("Set motor speed.")

    #Print values of the set motor speed
    #Parameters: mono = monochramtor input number
    #Returns: NA. Prints minimum and maximum frequency and ramp time.
    def getMotorSpeed(self,mono='0'):
        mono = str.encode(mono)

        self.s.write(b'C' + mono + b'\r')
        output = self.s.readline()
        output = output.decode('utf-8')

        try:
            if output[0]!='o':
                sys.exit("Bad confirmation for getting motor speed. Response: " + output)
        except IndexError:
            sys.exit("Bad confirmation for getting motor speed. Response: " + output)
        
        output = output[1:]
        output = output.split(",")

        print("Minimum frequency (steps/s): " + output[0] + "\n" + "Maximum frequency (steps/s): " + output[1] + "\n" + "Ramp time (ms): " + output[2])

    #Check the status of the motor to determine if it is still running
    #Parameters: NA
    #Returns: True if motor is still running  False if motor is not running
    def checkMotor(self):
        self.s.write(b'E')
        output = self.s.readline()
        output = output.decode('utf-8')

        if output!='oz' and output!='oq':
            sys.exit("Bad confirmation for checking motor. Response: " + output)
        
        if output=='oz':
            return False
        else:
            return True

    #Move the motor a certain number of steps
    #Parameters: steps=a string representation of the number of steps to move  mono=monochromator input number
    #Returns: NA. Prints when complete    
    def moveMotor(self,steps,mono='0'):

        if int(steps)+int(self.getMotorPos())>208701 or int(steps)+int(self.getMotorPos())<0:
            print("Cannot move motor beyond range of 0-208701!")
            return 0

        mono = str.encode(mono)
        steps = str.encode(steps)

        self.s.write(b'F' + mono + b',' + steps + b'\r')
        output = self.s.readline()
        output = output.decode('utf-8')

        if output!='o':
            sys.exit("Bad confirmation for moving motor. Response: " + output)
        
        print("Moving motor " + steps.decode('utf-8') + " steps...")

        moving = self.checkMotor()

        while moving==True:
            moving = self.checkMotor()
        
        print("Move complete")

        return 1

    #Move the motor a certain number of steps
    #Parameters: steps=a string representation of the number of steps to move  mono=monochromator input number
    #Returns: NA. Prints when complete    
    def moveMotorScan(self,steps,mono='0'):

        if int(steps)+int(self.getMotorPos())>208701 or int(steps)+int(self.getMotorPos())<0:
            print("Cannot move motor beyond range of 0-208701!")
            return 0

        mono = str.encode(mono)
        steps = str.encode(steps)

        self.s.write(b'F' + mono + b',' + steps + b'\r')
        output = self.s.readline()
        output = output.decode('utf-8')

        if output!='o':
            sys.exit("Bad confirmation for moving motor. Response: " + output)
        
        print("Moving motor " + steps.decode('utf-8') + " steps...")

        return 1
    
    #Set current step position of motor. Used for calibration
    #Parameters: pos=step number to move grating to  mono=monochromator input number
    #Return: 0 if cannot execute  1 if executed. Prints what position the motor was set to.
    def setMotorPos(self,pos,mono='0'):

        if int(pos)>208701 or int(pos)<0:
            print("Invalid position! Must be between 0-208701.")
            return 0

        pos = str.encode(pos)
        mono = str.encode(mono)

        self.s.write(b'G' + mono + b',' + pos + b'\r')
        output = self.s.readline()
        output = output.decode('utf-8')

        if output!='o':
            sys.exit("Bad confirmation for setting motor position. Response: " + output)
        
        print("Set motor to position: " + pos.decode('utf-8'))

        return 1

    #Get the position of the motor
    #Parameters: mono=monochromator input number
    #Return: output, the current step position of the motor
    def getMotorPos(self,mono='0'):
        mono = str.encode(mono)

        self.s.write(b'H' + mono + b'\r')
        output = self.s.readline()
        output = output.decode('utf-8')

        try:
            if output[0]!='o':
                sys.exit("Bad confirmation for getting motor position. Response: " + output)
        except IndexError:
            sys.exit("Bad confirmation for getting motor position. Response: " + output)

        output = output[1:]
        output = output[:-1]
        return output

    #Stop the motor
    #Parameters: NA
    #Return: NA. Print that the motor was stopped.
    def stopMotor(self):
        self.s.write(b'L')
        output = self.s.readline()
        output = output.decode('utf-8')

        if output!='o':
            sys.exit("Bad confirmation for stopping motor!")
        
        print("Motor stopped.")

    #Initialize the device
    #Parameters: NA
    #Return: NA. Print through initialization process and print when done.
    def initialize(self):
        #Tell device to initialize
        self.s.write(b'A')
        output = self.s.readline()
        output = output.decode('utf-8')
        print("Began initialization")

        #Check to make sure device is done initializing before continuing. 
        timer=0
        while output != 'o' and timer<10000:
            output = self.s.readline()
            output = output.decode('utf-8')
            print("Initializing...")
            timer += 1

        #If timeout occurs, exit
        if timer>=10000:
            sys.exit("Exited due to timeout initializing!")
        
        print("Initialization complete!")

    #Set speed of slit motor. Needs to be done either just before or just after initialization. 320 recommended for HR460
    #Parameters: slit=string representation of slit number (0-3)  speed:string representation of speed (steps/s) mono=monochromator input number
    def setSlitSpeed(self,slit,speed='320',mono='0'):
        slit=str.encode(slit)
        speed=str.encode(speed)
        mono=str.encode(mono)

        #Set slit speed
        self.s.write(b'g' + mono + b',' + slit + b',' + speed + b'\r')
        output = self.s.readline()
        output = output.decode('utf-8')
        speed = speed.decode('utf-8')

        #Check that command for setting speed was received correctly
        if output != 'o':
            sys.exit('Exited being unable to set slit speed!')

        print("Set slit speed to " + speed + ". Response: " + output)

    #Change slit width (0=front entrance, 1=side entrance, 2=front exit, 3=side exit). Note: Will not allow move past 0 step position
    #Parameters: slit=slit number (0-3)  width=steps to open slit  mono=monochromator input number
    #Return: NA. Print when done. Return with error message if trying to set slit beyond 0.
    def moveSlit(self,slit,width,mono='0'):
        mono = str.encode(mono)
        slit = str.encode(slit)
        width = str.encode(width)
        self.s.write(b'j' + mono + b',' + slit + b'\r')
        output = self.s.readline()
        output = output.decode('utf-8')

        try:
            if output[0]!='o':
                sys.exit('Bad confirmation for checking slit position! Response: ' + output)
        except IndexError:
            sys.exit("Bad confirmation for checking slit position. Response: " + output)
        
        if float(output[1:])+float(width)<0:
            print("Setting beyond 0. Cannot close slits more! Slit opening at: " + output[1:])
            return

        if float(width)<0:
            negative = True
        else:
            negative = False
        #Open the entrance slit
        self.s.write(b'k' + mono + b',' + slit + b',' + width + b'\r')
        output = self.s.readline()
        output = output.decode('utf-8')
        width = width.decode('utf-8')

        #Check that command for opening entrance slit was received correctly
        if output != 'o':
            sys.exit('Exited being unable to open entrance slit!')

        #Check that motor has finished opening the slit
        self.s.write(b'E')
        output = self.s.readline()
        output = output.decode('utf-8')
 
        timer=0
        while output != 'oz' and timer<10000:
            self.s.write(b'E')
            output = self.s.readline()
            output = output.decode('utf-8')
            print("Checking motor for status after entrance slit opened... Response: " + output)
            timer += 1
        if negative == True:
            print("Slit closed " + str(width) + " steps")
        else:
            print("Slit opened " + str(width) + " steps")
        
        self.s.write(b'j' + mono + b',' + slit + b'\r')
        output = self.s.readline()
        output = output.decode('utf-8')

        try:
            if output[0]!='o':
                sys.exit('Bad confirmation for checking slit position! Response: ' + output)
        except IndexError:
            sys.exit("Bad confirmation for checking slit position. Response: " + output)
        
        output = output[1:]
        output = output[:-1]
        print("Slit now at " + output + " steps.")

    #Get the current width of a slit
    #Parameters: slit=0 for front entrance, 1 for side entrance, 2 for front exit, 3 for side exit  mono=monochromator input number
    #Return: The slit width of the selected slit in the form of a string
    def getSlitWidth(self,slit,mono='0'):
        slit = str.encode(slit)
        mono = str.encode(mono)

        self.s.write(b'j' + mono + b',' + slit + b'\r')
        output = self.s.readline()
        output = output.decode('utf-8')

        try:
            if output[0]!='o':
                sys.exit("Bad confirmation for checking slit width! Response: " + output)
        except IndexError:
            sys.exit("Bad confirmation for checking slit width! Response: " + output)
        
        output = output[1:]
        output = output[:-1]

        return output
        

    #Set the exit mirror position (data collection through the side or through the front)
    #Parameters: position=either 's' or 'f' for side and front data collection  mono=monochromator input number
    #Return: NA. Prints when done.
    def setExitMirror(self,position,mono='0'):
        mono = str.encode(mono)
        #Check that right input selected
        if position=='s':
            mode = 'side detector'
            position='e'
        elif position=='f':
            mode = 'front detector'
            position='f'
        else:
            sys.exit("Exited due to improper mirror position input!")

        position = str.encode(position)

        #Set mirror to specific mode
        self.s.write(position + mono + b'\r')
        output = self.s.readline()
        output = output.decode('utf-8')

        #Check that command for moving mirror was received correctly
        if output != 'o':
            sys.exit('Exited being unable to move mirror position!')

        # Check that the mirror is not still moving before continuing
        self.s.write(b'l')
        output = self.s.readline()
        output = output.decode('utf-8')
        print("Mirror motor status: " + output)

        timer = 0
        while output!='oz' and timer<10000:
            self.s.write(b'l')
            output = self.s.readline()
            output = output.decode('utf-8')
            print("Motor moving mirror...")
            timer+=1
    
        #If timeout occurs, exit
        if timer>=10000:
            sys.exit("Exited due to timeout moving mirror!")
        
        print("Set mirror to " + mode + " mode. Response: " + output)

    #Flip the grating side
    #Parameters: grating='ir' for 1.5 micron infrared  'vis' for visible spectrum grating  mono=monochrometer input number
    #Return: NA. Return if bad parameter input. Print when finished.
    def setGrating(self,grating,mono='0'):
        mono = str.encode(mono)
        if grating!='ir' and grating!='vis':
            print("Invalid grating selection! Must be either \'ir\' or \'vis\'!")
            return
        
        if grating=='ir':
            grating = b'a'
        else:
            grating = b'b'
        

        self.s.write(grating + mono + b'\r')
        output = self.s.readline()
        output = output.decode('utf-8')

        if output!='o':
            sys.exit("Bad confirmation on changing grating. Response: " + output)

        # Check that the grating is not still moving before continuing
        self.s.write(b'l')
        output = self.s.readline()
        output = output.decode('utf-8')
        print("Grating change motor status: " + output)

        timer = 0
        while output!='oz' and timer<30:
            self.s.write(b'l')
            output = self.s.readline()
            output = output.decode('utf-8')
            print("Motor moving grating...")
            timer+=1
    
        #If timeout occurs, exit
        if timer>=30:
            sys.exit("Exited due to timeout moving grating!")

        print("Grating changed.")

    #Measure the gain offsets
    #Parameters: mono=monochromator input number
    #Return: NA. Prints the gain offsets.
    def measureOffsets(self,mono='0'):
        mono=str.encode(mono)
        self.s.write(b'w' + mono + b'\r')
        output = self.s.readline()
        output = output.decode('utf-8')

        try:
            if output[0]!='o':
                sys.exit("Bad confirmation for measuring offsets. Response: " + output)
        except IndexError:
            sys.exit("Bad confirmation for measuring offsets. Response: " + output)
        
        output = output[1:]
        output = output.split(',')
        print("Offset Gain 1: " + output[0] + "\n" + "Offset Gain 10: " + output[1] + "\n" + "Offset Gain 100: " + output[2] + "\n" + "Offset Gain 1000: " + output[3] + "\n")
    
    #Set the gain for the measurement
    #Parameters: gain=string representation of gain setting (0-4) (1x,10x,100x,1000x,auto)  mono=monochromator input number
    #Return: NA. Print when gain set. Return nothing if invalid value entered
    def setGain(self,gain,mono='0'):
        if gain!= '0' and gain!='1' and gain!='2' and gain!='3' and gain!='4':
            print("Invalide gain selection! (0=1x, 1=10x, 2=100x, 3=1000x, 4=AUTO")
            return
        
        gain=str.encode(gain)
        mono=str.encode(mono)

        self.s.write(b'R' + mono + b',' + gain + b'\r')
        output=self.s.readline()
        output=output.decode('utf-8')

        if output!='o':
            sys.exit("Bad confirmation for setting gain. Response: " + output)

        print("Gain set to setting " + gain.decode('utf-8'))
        
    #Show the set gain value
    #Parameters: mono=monochromator input number
    #Return: NA. Print the gain setting value.    
    def getGain(self,mono='0'):
        mono=str.encode(mono)
        self.s.write(b'S' + mono + b'\r')
        output=self.s.readline()
        output=output.decode('utf-8')

        try:
            if output[0]!='o':
                sys.exit("Bad confirmation for getting gain. Response: " + output)
        except IndexError:
            sys.exit("Bad confirmation for getting gain. Response: " + output)
        
        output = output[1:]
        print("Gain setting: " + output[0])

    #Set the integration time
    #Parameters: time=string representation of time in ms  mono=monochromator input number
    #Return: NA. Print when set.
    def setIntegrate(self,time,mono='0'):
        time = str.encode(time)
        mono = str.encode(mono)

        self.s.write(b'O' + mono + b',' + time + b'\r')
        output = self.s.readline()
        output = output.decode('utf-8')

        if output!='o':
            sys.exit("Bad confirmation for setting integration time. Response: " + output)
        
        print("Integration time set to " + time.decode('utf-8') + "ms")

    #Show the value of the set integration time
    #Parameters: mono=monochromator input number
    #Return: NA. Print the set integration time
    def getIntegrate(self,mono='0'):
        mono = str.encode(mono)

        self.s.write(b'P' + mono + b'\r')
        output = self.s.readline()
        output = output.decode('utf-8')

        try:
            if output[0]!='o':
                sys.exit("Bad confirmation for getting integration time. Response: " + output)
        except IndexError:
            sys.exit("Bad confirmation for getting integration time. Response: " + output)
        
        output = output[1:]
        print("Integration time set to: " + output + "ms")

    #Start data acquisition
    #Paramters: mono=monochromator number
    #Return: NA. Print that it is starting
    def startAcq(self,mono='0'):
        mono = str.encode(mono)

        self.s.write(b'M' + mono + b'\r')
        output = self.s.readline()
        output = output.decode('utf-8')

        if output!='o':
            sys.exit("Bad confirmation for starting data acquisition. Response: " + output)
        
        print("Starting data acquisition...")

    #Stop data acquisition  
    #Parameters: NA
    #Return: NA. Print that it is stopped.
    def stopAcq(self):
        self.s.write(b'N')
        output = self.s.readline()
        output = output.decode('utf-8')

        if output!='o':
            sys.exit("Bad confirmation for stopping data acquisition. Response: " + output)

        print("Data acquisition stopped!")
    
    #Check if taking data
    #Parameters: NA
    #Return: False if not taking data  True if taking data
    def busyAcq(self):
        self.s.write(b'Q')
        output = self.s.readline()
        output = output.decode('utf-8')

        if output!='oz' and output!='oq':
            sys.exit("Bad confirmation for checking busy data acquisition. Response: " + output)
        
        if output=='oz':
            return False
        else:
            return True
    
    #Get the intensity measurement from the data point
    #Parameters: mono=monochromator input number
    #Return: intensity measurement as a string (can convert to int value)
    def getData(self,mono='0'):
        mono = str.encode(mono)
        
        self.s.write(b'T' + mono + b'\r')
        output = self.s.readline()
        output = output.decode('utf-8')

        try:
            if output[0]!='o':
                sys.exit("Bad confirmation for collecting data. Response: " + output)
        except IndexError:
            sys.exit("Bad confirmation for collecting data. Response: " + output)
        
        output = output[1:]
        output = output.split(",")
        return output[0]

    #Prepare the spectrometer for a scan. CAUTION: input values have not been secured. So a bad input can cause an error! Assumes use of front entrance slit and side exit slit
    #Parameters: NA. All parameters set by user input at command line when prompted
    #Returns: NA. Prints that parameters were set properly.
    def setScan(self):
        type1 = str.encode(input("Enter the type of scan to be completed:\n0 - Monochromator 1 scan.\n1 - Monochromator 2 scan\n3 - Time Base Scan\n"))
        startPos = str.encode(input("Enter the starting position for scan in steps (0-208701): "))
        endPos = str.encode(input("Enter the ending position for scan in steps (0-208701): "))
        steps = str.encode(input("Enter the interval of steps (This parameter ignored if running Time Base Scan): "))
        intTime = str.encode(input("Enter the integration time in milliseconds (2-300,000) as an even number: "))
        cycles = str.encode(input("Enter the number of scan cycles to be completed: "))
        dwell = str.encode(input("Enter the time (in milliseconds) that the system waits after moving the monochromator (0-2147483648): "))
        delay = str.encode(input("Enter the time (in milliseconds) that the system waits after completing each cycle (0-2147483648): "))
        entSlit = input("Enter the entrance slit width in steps: ")
        extSlit = input("Enter the exit slit width in steps: ")
        startPos2 = str.encode(input("Enter the starting position (in steps) for monochromator 2 (Parameter ignored if no monochromator 2): "))
        parkPos1 = str.encode(input("Enter the position (in steps) to park the monochromator when finished (0-208701): "))
        timeStep = str.encode(input("Enter the time (in milliseconds) between integration starts (Ignored if no time scan): "))
        time = str.encode(input("Enter the total time (in milliseconds) of the scan (0-2147483648): "))
        channel = str.encode(input("Enter the channel used for data acquisition:\n0 - channel 1\n1 - channel 2\n2 - use both channels simultaneously\n"))
        gain1 = str.encode(input("Enter the gain setting for channel 1:\n0 - 1x\n1 - 10x\n 2 - 100x\n3 - 1000x\n4 - AUTO\n"))
        gain2 = str.encode(input("Enter gain for channel 2 using paramters above: "))
        shutter = str.encode(input("Enter shutter mode parameter:\n0 - AUTO\n1 - MANUAL\n"))
        trigger = str.encode(input("Enter trigger mode parameter:\n0 - no trigger\n1 - wait for start of experiment\n2 - wait for start of cycle\n3 - wait for start of each data point\n"))
        data = str.encode(input("Enter data mode parameter:\n0 - stack acquired scans separately\n1 - sum acquired scans in memory\n"))

        self.s.write(b'p' + type1 + b',' + startPos + b',' + endPos + b',' + steps + b',' + intTime + b',' + cycles + b',' + dwell + b',' + delay + b',' + struct.pack('!B',0) + b',' + parkPos1 + b',' + struct.pack('!B',0) + b',' + timeStep + b',' + time + b',' + channel + b',' + gain1 + b',' + gain2 + b',' + shutter + b',' + trigger + b',' + data + b'\r') 
        output = self.s.readline()
        output = output.decode('utf-8')

        if output!= 'o0\r':
            print("Error! Returned: " + output)
            return  
        
        currentWidth = float(self.getSlitWidth('0'))
        moveAmount = str(float(entSlit) - currentWidth)
        self.moveSlit('0',moveAmount)

        currentWidth = float(self.getSlitWidth('3'))
        moveAmount = str(float(extSlit) - currentWidth)
        self.moveSlit('3',moveAmount)

        self.setExitMirror('s')
        self.setGrating('vis')
        self.s.readline()

        print("Set scan parameters and prepared spectrometer for scanning!")

    #Start the scan after being set using the setScan() function
    #Parameters:NA
    #Returns: 0 if okay and 1 if error occurs. Returns if unable to start scan. Prints when finished.
    def startScan(self):
        self.s.write(b'q')
        output = self.s.readline()
        output = output.decode('utf-8')

        if output!='o':
            print("Bad confirmation for starting scan! Response: " + output) 
            return 1

        self.s.write(b'r')
        r = self.s.readline()
        r = r.decode('utf-8')

        while r!='o0\r' and r!='o5\r':
            self.s.write(b'r')
            r = self.s.readline()
            r = r.decode('utf-8')  
        
        return 0
        print("Scan complete!")

     #Prepare the spectrometer for a scan. CAUTION: input values have not been secured. So a bad input can cause an error! Assumes use of front entrance slit and side exit slit
    #Parameters: NA. All parameters set by user input at command line when prompted
    #Returns: 0 if all went well, 1 if failure. Prints that parameters were set properly.
    def setScanGUI(self,startPos,endPos,steps,intTime,entSlit,extSlit,gain1,grating,mirror):
        #type1 = str.encode(input("Enter the type of scan to be completed:\n0 - Monochromator 1 scan.\n1 - Monochromator 2 scan\n3 - Time Base Scan\n"))
        #startPos = str.encode(input("Enter the starting position for scan in steps (0-208701): "))
        #endPos = str.encode(input("Enter the ending position for scan in steps (0-208701): "))
        #steps = str.encode(input("Enter the interval of steps (This parameter ignored if running Time Base Scan): "))
        #intTime = str.encode(input("Enter the integration time in milliseconds (2-300,000) as an even number: "))
        #cycles = str.encode(input("Enter the number of scan cycles to be completed: "))
        #dwell = str.encode(input("Enter the time (in milliseconds) that the system waits after moving the monochromator (0-2147483648): "))
        #delay = str.encode(input("Enter the time (in milliseconds) that the system waits after completing each cycle (0-2147483648): "))
        #entSlit = input("Enter the entrance slit width in steps: ")
        #extSlit = input("Enter the exit slit width in steps: ")
        #startPos2 = str.encode(input("Enter the starting position (in steps) for monochromator 2 (Parameter ignored if no monochromator 2): "))
        #parkPos1 = str.encode(input("Enter the position (in steps) to park the monochromator when finished (0-208701): "))
        #timeStep = str.encode(input("Enter the time (in milliseconds) between integration starts (Ignored if no time scan): "))
        #time = str.encode(input("Enter the total time (in milliseconds) of the scan (0-2147483648): "))
        #channel = str.encode(input("Enter the channel used for data acquisition:\n0 - channel 1\n1 - channel 2\n2 - use both channels simultaneously\n"))
        #gain1 = str.encode(input("Enter the gain setting for channel 1:\n0 - 1x\n1 - 10x\n 2 - 100x\n3 - 1000x\n4 - AUTO\n"))
        #gain2 = str.encode(input("Enter gain for channel 2 using paramters above: "))
        #shutter = str.encode(input("Enter shutter mode parameter:\n0 - AUTO\n1 - MANUAL\n"))
        #trigger = str.encode(input("Enter trigger mode parameter:\n0 - no trigger\n1 - wait for start of experiment\n2 - wait for start of cycle\n3 - wait for start of each data point\n"))
        #data = str.encode(input("Enter data mode parameter:\n0 - stack acquired scans separately\n1 - sum acquired scans in memory\n"))
        
        print(grating)
        print(mirror)
        #Encode data to be sent to spectrometer
        startPos = str.encode(startPos)
        endPos = str.encode(endPos)
        steps = str.encode(steps)
        intTime = str.encode(intTime)
        entSlit = str.encode(entSlit)
        extSlit = str.encode(extSlit)
        gain1 = str.encode(gain1)

        #Send to spectrometer
        self.s.write(b'p' + str.encode('0') + b',' + startPos + b',' + endPos + b',' + steps + b',' + intTime + b',' + str.encode('1') + b',' + str.encode('1') + b',' + str.encode('1') + b',' + struct.pack('!B',0) + b',' + str.encode('0') + b',' + struct.pack('!B',0) + b',' + str.encode('0') + b',' + str.encode('0') + b',' + str.encode('0') + b',' + gain1 + b',' + str.encode('0') + b',' + str.encode('0') + b',' + str.encode('0') + b',' + str.encode('0') + b'\r') 

        #Get response
        output = self.s.readline()
        output = output.decode('utf-8')

        if output!= 'o0\r':
            print("Error! Returned: " + output)
            return 1 
        
        #Move slits
        currentWidth = float(self.getSlitWidth('0'))
        moveAmount = str(float(entSlit) - currentWidth)
        self.moveSlit('0',moveAmount)

        currentWidth = float(self.getSlitWidth('3'))
        moveAmount = str(float(extSlit) - currentWidth)
        self.moveSlit('3',moveAmount)

        self.setExitMirror(mirror)
        self.setGrating(grating)
        self.s.readline()

        print("Set scan parameters and prepared spectrometer for scanning!")
        return 0

    #Function to collect data after scan complete
    #Parameters: cycle=the cycle number that you wish to collect data from, in the form of a string
    #Returns: steps=the numpy array of steps  intensities=the numpy array of measured intensities
    def getDataScan(self,cycle='1'):
        cycle = str.encode(cycle)

        self.s.write(b's' + cycle + b'\r')
        output=self.s.readline()
        output=output.decode('utf-8')

        if output!='o':
            print("Bad confirmation for setting cycle to read from! Response: " + output)
            return
        
        self.s.write(b't')
        output = self.s.readline()
        output = output.decode('utf-8')

        try:
            if output[0]!='o':
                print("Bad confirmation for getting data length! Response: " + output)
                return
        except IndexError:
            print("Bad confirmation for getting data length! Response: " + output)
            return

        output = output[1:]

        output = output.split(',')

        length = int(output[0])

        print(length)

        #file1 = open("Spectrum.txt","w")

        #intensities = list()
        #steps = list()

        xs = list()
        ys = list()

        for i in range(1,length):
            print(i)
            i = str(i)
            i = str.encode(i)
            self.s.write(b'u' + i + b'\r')
            output = self.s.read_until(b'\r',15)
            output = output.decode('utf-8')

            try:
                if output[0]!='o':
                    print("Bad confirmation for getting data point " + i.decode('utf-8') + "! Response: " + output)
                    file1.close()
                    return
            except IndexError:
                print("Bad confirmation for getting data point " + i.decode('utf-8') + "! Response: " + output)
                file1.close()
                return
            
            output = output[1:]

            output = output.split(',')

            intensity = output[0]
            ys.append(float(intensity))

            #file1.write(i.decode('utf-8') + ',' + str(intensity) + '\n')

            xs.append(float(i.decode('utf-8')))

    
        xs = np.array(xs)
        ys = np.array(ys)

        #file1.close()
        print("Data acquisition complete!") 
        return xs,ys                                                  

    
    




        

