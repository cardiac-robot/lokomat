# -*- coding: utf-8 -*-
"""
Created on Tue Aug 08 11:33:41 2017

@author: Nathalia
"""

import serial
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

##Comunicación Serial
IMU= serial.Serial('COM4',9600)
while True:
    ##lECTURA DE LOS ÁNGULOS 
    ##Orden X,Y,Z
    Info=IMU.readline()
    Info_Split=Info.split(',')
    x=Info_Split[0]
    y=Info_Split[1]
    z=Info_Split[2]
    
    print(Info)
    


