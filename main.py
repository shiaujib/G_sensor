#!/usr/bin/env python
#

import os
import struct
import sys,getopt
import time
import datetime
import random 
import MPU6050Read
import subprocess
import RPi.GPIO as GPIO
import threading
import numpy as np

sensitive4g = 0x1c

#=========================================================================
# button control
GPIO.setmode(GPIO.BCM)
GPIO.setup(4,GPIO.IN,pull_up_down=GPIO.PUD_UP)

timeArray=[None]*100000000
#/*=========================================================================*/

        
    
    
# Main Program
def main(argv):
    try:
        opts,args=getopt.getopt(argv,"h:n:s:",["help=","deviceNumber"])
    except getopt.GetoptError:
        print 'usage:muti_accelerometer.py -n <deviceNumber> -s <subjectName>'
        sys.exit(2)
    if findElement(argv,'-n')==0:
        print 'usage:muti_accelerometer.py -n <deviceNumber> -s <subjectName>'
        sys.exit(2)
    if findElement(argv,'-s')==0:
        print 'usage:muti_accelerometer.py -n <deviceNumber> -s <subjectName>'
        sys.exit(2)
    for opt,arg in opts:
        if opts=='-h':
            print 'usage:muti_accelerometer.py -i <deviceNumber>'
        elif opt in ("-n","--deviceNumber"):
            deviceNum=arg
	elif opt in ("-s","--subjectName"):
            subName=arg

    accel=[[] for i in range(int(deviceNum))]  #create dynamic list
    gyro=[[] for i in range(int(deviceNum))]
    fileName=[subName+'_accel_sensor1.txt',subname+'_gyro_sensor1.txt',subname+'_gyro_sensor2.txt',subname+'_gyro_sensor2.txt',]
    
    print ""
    print "Program Started at:"+ time.strftime("%Y-%m-%d %H:%M:%S")
    print ""

    starttime = datetime.datetime.utcnow()



    file0=open(fileName[0],'w')
    file1=open(fileName[1],'w')
    if int(deviceNum)==1:
        file2=open(fileName[2],'w')
        file3=open(fileName[3],'w')
    timeFile=open("dataTime.txt",'w')
    fileList=[file0,file1,file2,file3]
        

    accel_tmp=[0]*int(deviceNum)
    while True:
        fileIndex=0
        input_state=GPIO.input(4)   #get switch state
	print "getting data please press button to stop........"
        mpu6050 = MPU6050Read.MPU6050Read(0x68,1)
        tca9548.write_control_register(BusChannel[fileIndex])
        #get gyro and accelerometer value
        gyro_xout = mpu6050.read_word_2c(0x43)
        gyro_yout = mpu6050.read_word_2c(0x45)
        gyro_zout = mpu6050.read_word_2c(0x47)
        accel_xout = mpu6050.read_word_2c(0x3b)
        accel_yout = mpu6050.read_word_2c(0x3d)
        accel_zout = mpu6050.read_word_2c(0x3f)
        accel_xout=accel_xout/16384
        accel_yout=accel_yout/16384
        accel_zout=accel_zout/16384
        gyro_xout=gyro_xout/131
        gyro_yout=gyro_yout/131
        gyro_zout=gyro_zout/131
        fileList[fileIndex].write("%f\t%f\t%f\n" %(accel_xout,accel_yout,accel_zout))
        fileList[fileIndex+1].write("%f\t%f\t%f\n" %(gyro_xout,gyro_yout,gyro_zout))
        if int(deviceNum)==1:
            #read slave sensor
            mpu6050_sla=MPU6050Read.MPU6050Read(0x69,1)
            gyro_xout = mpu6050_sla.read_word_2c(0x43)
            gyro_yout = mpu6050_sla.read_word_2c(0x45)
            gyro_zout = mpu6050_sla.read_word_2c(0x47)
            accel_xout = mpu6050_sla.read_word_2c(0x3b)
            accel_yout = mpu6050_sla.read_word_2c(0x3d)
            accel_zout = mpu6050_sla.read_word_2c(0x3f)
            accel_xout=accel_xout/16384
            accel_yout=accel_yout/16384
            accel_zout=accel_zout/16384
            fileList[fileIndex+2].write("%f\t%f\t%f\n" %(accel_xout,accel_yout,accel_zout))
            fileList[fileIndex+3].write("%f\t%f\t%f\n" %(gyro_xout,gyro_yout,gyro_zout))
                
                    
        count+=1
        if input_state==False:
            print "Button Pressed experimental stop"
            print "count Num = %d" %count
            sys.exit()
            break 
        



if __name__=="__main__":
    sub_name=None
    main(sys.argv[1:])
        


