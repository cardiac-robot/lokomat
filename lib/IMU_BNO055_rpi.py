import sys,getopt
import smbus
import numpy as np
import time
import os
import threading


UNIT_SEL=0X3B # Units register
OPR_MODE=0x3D #Operation mode register
CALIB_STAT=0X35 # Calibration register
#Euler angles register
EUL_Pitch_MSB = 0x1F
EUL_Pitch_LSB = 0x1E
EUL_Roll_MSB = 0x1D
EUL_Roll_LSB = 0x1C
EUL_Heading_MSB = 0x1B
EUL_Heading_LSB = 0x1A

class IMU_BNO055(object):
    def __init__(self, device_address,bus):
        self.device_address = device_address
        self.bus=smbus.SMBus(bus) #1
        self.bus.write_byte_data(self.device_address,UNIT_SEL,0b00000010)
        self.bus.write_byte_data(self.device_address, OPR_MODE, 0b00001100) #NDOF mode: all sensors and absolute orientation
        self.acquired_data=0


    def read_Euler(self):
        self.acquired_data=self.read_i2c()
        print("Pitch, Roll, Yaw:")
        print(self.acquired_data)

    def read_i2c(self):
        Euler = {}
        msb = self.bus.read_byte_data(self.device_address,EUL_Pitch_MSB)
        lsb = self.bus.read_byte_data(self.device_address,EUL_Pitch_LSB)
        data = (msb << 8) + lsb
        if (data & 0x8000)== 0x8000:
            data= data ^ 0xFFFF
            data= data * -1
            if data < -2880:
                data= data*-1
                data= data ^ 0xFFFF
                data= data & 0x7FFF
        data=data/16.
        #Euler= Euler +str(data)
        Euler['pitch'] = data


        msb = self.bus.read_byte_data(self.device_address,EUL_Roll_MSB)
        lsb = self.bus.read_byte_data(self.device_address,EUL_Roll_LSB)
        data = (msb << 8) + lsb
        if (data & 0x8000)== 0x8000:
            data= data ^ 0xFFFF
            data= data * -1
            if data < -2880:
                data= data*-1
                data= data ^ 0xFFFF
                data= data & 0x7FFF

        data=data/16.
        #Euler= Euler+" , "+str(data)
        Euler['roll'] = data


        msb = self.bus.read_byte_data(self.device_address,EUL_Heading_MSB)
        lsb = self.bus.read_byte_data(self.device_address,EUL_Heading_LSB)
        data = (msb << 8) + lsb
        if (data & 0x8000)== 0x8000:
            data= data ^ 0xFFFF
            data= data * -1
            if data < -2880:
                data= data*-1
                data= data ^ 0xFFFF
                data= data & 0x7FFF
        data=data/16.
        #Euler= Euler+", "+str(data)
        Euler['yaw'] = data
        return(Euler)



class ImuHandler(IMU_BNO055):
    def __init__(self, sample = 1, dev1 = 0x28, b  = 1):
        super(ImuHandler,self).__init__(device_address = dev1, bus = b)
        self.ON = True
        self.data = {}
        self.Ts  = sample
        self.pause  = True

    def process(self):
        print('start imu acquire process')
        while self.ON:
            if not self.pause:
                self.data = self.read_i2c()
                time.sleep(self.Ts)
        print('finishing imu acquiring process')

    def get_data(self):
        return self.data

    def shutdown(self):
        self.ON = False

    def play(self):
        self.pause = False

    def pause(self):
        self.pause = True

    def launch_thread(self):
        self.ImuThread = threading.Thread(target = self.process)
        self.ImuThread.start()





def main():
    bus=1
    device_address=0x28
    imu = IMU_BNO055(device_address, bus)
    for i in range (50):
        imu.read_Euler()

def main2():
    imu = ImuHandler(sample = 1, dev1 = 0x28, b = 1)
    imu.launch_thread()
    for i in range(10):
        print (imu.data)
        time.sleep(1)
    imu.shutdown()


if __name__ == '__main__':
    main2()
