import spidev
import time
import os
import threading

class Analog_Joystick(object):

    def __init__(self):
        # Open SPI bus
        self.spi = spidev.SpiDev()
        self.spi.open(0,0)

    def ReadChannel(self,channel):
        self.spi.max_speed_hz = 1350000
        adc = self.spi.xfer2([1,(8+channel)<<4,0])
        data = ((adc[1]&3) << 8) + adc[2]
        return data

    def Channel_data(self):

        switch= 0
        Vr_X= 1
        Vr_Y= 2
        # MCP3008 channels
        X= ""
        Y= ""
        choice= ""

        # Delay between readings
        self.delay = 0.5
        self.Position = {}
        # Read the joystick position data
        vrx_pos = self.ReadChannel(Vr_X)
        # 10 bits resolution
        vrx_pos =vrx_pos/1023.
        if 0.8 <=  vrx_pos <=1:
            pos= 4
        elif 0<=  vrx_pos <= 0.2 :
            pos=2
        else:
            pos=0
        #self.Position= self.Position +str(pos)
        self.Position['x'] = pos
        vry_pos = self.ReadChannel(Vr_Y)
        vry_pos =vry_pos/1023.
        if 0.8 <=  vry_pos <=  1.2:
            pos= 1
        elif 0<= vry_pos <= 0.2 :
            pos=3
        else:
            pos=0
        #self.Position= self.Position +','+str(pos)
        self.Position['y'] = pos
        # Read switch state
        swt_val = self.ReadChannel(switch)
        swt_val =swt_val/1013.

        if swt_val == 0 :
            pos= 5
        else:
            pos = 0
        #self.Position= self.Position +','+str(pos)
        self.Position['z'] = pos
        return self.Position

class JoyHandler(Analog_Joystick):
    def __init__(self, sample = 1, man = None):
        super(JoyHandler, self).__init__()
        self.Ts  = sample
        self.ON  = True
        self.data = {}
        self.man = man



    def process(self):
        while self.ON:
            self.data = self.Channel_data()  
            self.man.data['joy'] = self.data           
            '''
            if self.therapy_win:
                self.therapy_win.Borg.j = self.data['x']
                self.therapy_win.onJoy.emit()
            '''
            time.sleep(self.Ts)

    def launch_thread(self):
        self.JoyThread = threading.Thread(target = self.process)
        self.JoyThread.start()

    def shutdown(self):
        self.ON = False



def main():
     joy= Analog_Joystick()
     while True:
         pos=joy.Channel_data()
         time.sleep(joy.delay)
         print(pos)
def main2():
    joy = JoyHandler(sample = 1)
    joy.launch_thread()
    for i in range(10):
        print(joy.data)
        time.sleep(1)
    joy.shutdown()

if __name__ == '__main__':
    main2()
