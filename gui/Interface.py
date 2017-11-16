# -*- coding: utf-8 -*-import sys
import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import*
from PyQt4.QtGui import*
import ctypes

class MainTherapyWin(QtGui.QMainWindow):
    onData=QtCore.pyqtSignal()
    onJoy=QtCore.pyqtSignal()
    def __init__(self):
        super(MainTherapyWin,self).__init__()
        self.init_ui()
        self.dataToDisplay={'hr':0,
                            'yaw_t':0,
                            'pitch_t':0,
                            'roll_t':0,
                            'yaw_v':0,
                            'pitch_v':0,
                            'roll_v':0
                            }
        #set signals
        self.set_signals()
    def init_ui(self):
        #-------main config-------
        #Window title
        self.setWindowTitle("Lokomat therapy")
        #Window size
        self.user32=ctypes.windll.user32
        self.screensize=self.user32.GetSystemMetrics(0), self.user32.GetSystemMetrics(1),
        #Resizing MainWindoe to a percentage of the total
        self.winsize_h=int(self.screensize[0])
        self.winsize_v=int(self.screensize[1])
        #self.winsize_h=int(self.screensize[0])*0.9
        #self.winsize_v=int(self.screensize[1])*0.9
        #self.setGeometry(10,10,self.winsize_h,self.winsize_v)#Tamaño de la ventana
        self.resize(self.winsize_h,self.winsize_v)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        #self.setGeometry(100,100,1000,580)#Tamaño de la ventana
        
        #setting backgroung image
        self.label_background=QtGui.QLabel(self)
        self.label_background.setGeometry(QtCore.QRect(0,0,self.winsize_h,self.winsize_v))
        self.label_background.setPixmap(QtGui.QPixmap("img/Interfaz.png"))
        self.label_background.setScaledContents(True)
        #Image=QImage("img/Interfaz.png")
        #sImage=Image.scaled(self.winsize_h,self.winsize_v,QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
        #palette=QtGui.QPalette()
        #palette.setBrush(10, QBrush(sImage))
        #self.setPalette(palette)
        #----------------------------------
        #-----------Labels config----------
        #Heart rate:
        self.hrDisplay = {}
        #heart rate lcd
        self.hrDisplay['lcd'] = QtGui.QLCDNumber(self)
        #self.hrDisplay['lcd'].setGeometry(QtCore.QRect(120,95, 120,30))
        self.hrDisplay['lcd'].setGeometry(QtCore.QRect(self.winsize_h*0.165,self.winsize_v*0.19,self.winsize_h*0.12 ,self.winsize_h*0.04))
        #Yaw angle:
        self.yawDisplay = {}
        #yaw angle label
        self.yawDisplay['name'] = QtGui.QLabel(self)
        self.yawDisplay['name'].setText("Yaw")
        self.yawDisplay['name'].setStyleSheet("font-size:18px; Arial")
        #self.yawDisplay['name'].setGeometry(120,125, 100,50)
        self.yawDisplay['name'].setGeometry(QtCore.QRect(self.winsize_h*0.18,self.winsize_v*0.2,self.winsize_h*0.12 ,self.winsize_h*0.1))
        #yaw lcd
        self.yawDisplay['lcd'] = QtGui.QLCDNumber(self)
        #self.yawDisplay['lcd'].setGeometry(100,165, 50,30)
        self.yawDisplay['lcd'].setGeometry(QtCore.QRect(self.winsize_h*0.16,self.winsize_v*0.31,self.winsize_h*0.055 ,self.winsize_h*0.04))
        #pitch angle:
        self.pitchDisplay = {}
        #pitch angle label
        self.pitchDisplay['name'] = QtGui.QLabel(self)
        self.pitchDisplay['name'].setText("Pitch")
        self.pitchDisplay['name'].setStyleSheet("font-size:18px; Arial")
        self.pitchDisplay['name'].setGeometry(QtCore.QRect(self.winsize_h*0.24,self.winsize_v*0.2,self.winsize_h*0.12 ,self.winsize_h*0.1))
        #pitch lcd
        self.pitchDisplay['lcd'] = QtGui.QLCDNumber(self)
        self.pitchDisplay['lcd'].setGeometry(QtCore.QRect(self.winsize_h*0.22,self.winsize_v*0.31,self.winsize_h*0.055 ,self.winsize_h*0.04))
        #roll angle:
        self.rollDisplay = {}
        #roll angle label
        self.rollDisplay['name'] = QtGui.QLabel(self)
        self.rollDisplay['name'].setText("Roll")
        self.rollDisplay['name'].setStyleSheet("font-size:18px; Arial")
        self.rollDisplay['name'].setGeometry(QtCore.QRect(self.winsize_h*0.30,self.winsize_v*0.2,self.winsize_h*0.12 ,self.winsize_h*0.1))
        #roll lcd
        self.rollDisplay['lcd'] = QtGui.QLCDNumber(self)
        self.rollDisplay['lcd'].setGeometry(QtCore.QRect(self.winsize_h*0.28,self.winsize_v*0.31,self.winsize_h*0.055 ,self.winsize_h*0.04))
        #Therapy time lcd
        self.TtimeDisplay = {}
        self.TtimeDisplay['lcd'] = QtGui.QLCDNumber(self)
        self.TtimeDisplay['lcd'].setGeometry(QtCore.QRect(self.winsize_h*0.86,self.winsize_v*0.14,self.winsize_h*0.12 ,self.winsize_h*0.04))
     
        #a =300
        #Yaw angle:
        self.yawDisplay1 = {}

        #yaw lcd
        self.yawDisplay1['lcd'] = QtGui.QLCDNumber(self)
        self.yawDisplay1['lcd'].setGeometry(QtCore.QRect(self.winsize_h*0.16,self.winsize_v*0.42,self.winsize_h*0.055 ,self.winsize_h*0.04))
        #pitch angle:
        self.pitchDisplay1 = {}
        #pitch lcd
        self.pitchDisplay1['lcd'] = QtGui.QLCDNumber(self)
        self.pitchDisplay1['lcd'].setGeometry(QtCore.QRect(self.winsize_h*0.22,self.winsize_v*0.42,self.winsize_h*0.055 ,self.winsize_h*0.04))
        #roll angle:
        self.rollDisplay1 = {}

        #roll lcd
        self.rollDisplay1['lcd'] = QtGui.QLCDNumber(self)
        self.rollDisplay1['lcd'].setGeometry(QtCore.QRect(self.winsize_h*0.28,self.winsize_v*0.42,self.winsize_h*0.055 ,self.winsize_h*0.04))



        #----------------------------------

        #----------buttons config----------
        #setting background start image
        
        self.start=QtGui.QLabel(self)
        self.start.setGeometry(QtCore.QRect(self.winsize_h*0.87,self.winsize_v*0.35,self.winsize_h*0.055 ,self.winsize_h*0.055))
        Icon3=QtGui.QPixmap("gui/img/play3.png")
        Icon_resize3= Icon3.scaled(self.winsize_h*0.055 ,self.winsize_h*0.055,QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
        self.start.setPixmap(Icon_resize3)
        
        #setting background stop image
        
        self.stop=QtGui.QLabel(self)
        self.stop.setGeometry(QtCore.QRect(self.winsize_h*0.87,self.winsize_v*0.48,self.winsize_h*0.055 ,self.winsize_h*0.055))
        Icon4=QtGui.QPixmap("gui/img/stop1.png")
        Icon_resize5= Icon4.scaled(self.winsize_h*0.055 ,self.winsize_h*0.055,QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
        self.stop.setPixmap(Icon_resize5)
        

        
        self.controlButtons = {}
        #start button
        self.controlButtons['start'] = QtGui.QCommandLinkButton(self)
        self.controlButtons['start'].setIconSize(QSize(0,0))
        self.controlButtons['start'].setGeometry(QtCore.QRect(self.winsize_h*0.87,self.winsize_v*0.35,self.winsize_h*0.055 ,self.winsize_h*0.055))
        
        
        self.controlButtons['stop'] = QtGui.QCommandLinkButton(self)
        self.controlButtons['stop'].setGeometry(QtCore.QRect(self.winsize_h*0.87,self.winsize_v*0.48,self.winsize_h*0.055 ,self.winsize_h*0.055))
        self.controlButtons['stop'].setIconSize(QSize(0,0))
        #self.controlButtons['stop'].setEnabled(False)

        self.controlButtons['close'] = QtGui.QCommandLinkButton(self)
        self.controlButtons['close'].setGeometry(QtCore.QRect(self.winsize_h*0.943,self.winsize_v*0.02,self.winsize_h*0.038 ,self.winsize_h*0.038))
        self.controlButtons['close'].setIconSize(QSize(0,0))

        # Borg Scale Status LCD
        
        self.BorgDisplay= QtGui.QLCDNumber(self)
        self.BorgDisplay.setGeometry(QtCore.QRect(self.winsize_h*0.18,self.winsize_v*0.52,self.winsize_h*0.055 ,self.winsize_h*0.04))


        
        #----------------------------------
        #
        #self.LabelPosture=QtWidgets.QLabel(self)
        #self.LabelPosture.setGeometry(760,60,220,440)
        #self.LabelPosture.setPixmap(QtGui.QPixmap('gui/img/cervical'))
        #
    
        #self.Stop.setIconSize(QSize(800,500))
        #self.LabelPosture1=QtWidgets.QLabel(self)
        #self.LabelPosture1.setGeometry(340,100,400,300)
        #self.LabelPosture1.setPixmap(QtGui.QPixmap('gui/img/cervical'))

        #create borgscale button
        self.Borg = BorgButton(self)

        self.show()


    def set_signals(self):
        self.controlButtons['start'].clicked.connect(self.onStartClicked)
        self.controlButtons['stop'].clicked.connect(self.onStopClicked)
        self.onData.connect(self.display_data)
        self.onJoy.connect(self.Borg.move)

    #----------------------------- SIGNAL METHODS ------------------------------
    def connectStartButton(self, f):
        print('connectStartButton')
        self.controlButtons['start'].clicked.connect(f)

    def connectStopButton(self, f):
        self.controlButtons['stop'].clicked.connect(f)
    #---------------------------------------------------------------------------

    def onStartClicked(self):
        #function to modify the interface state and visuals
        print('start clicked')
        #lock start button
        self.controlButtons['start'].setEnabled(False)
        self.controlButtons['stop'].setEnabled(True)
        self.update_display_data(d = {
                                        'hr' : 1,
                                        'yaw_t' : 2,
                                        'pitch_t' : 3,
                                        'roll_t' : 4,
                                        'yaw_c' : 5,
                                        'pitch_c' : 6,
                                        'roll_c' : 7
                                        }
                                )
        self.Borg.j = 4
        self.Borg.move()

    def display_data(self):

        self.hrDisplay['lcd'].display(self.dataToDisplay['hr'])
        self.yawDisplay['lcd'].display(self.dataToDisplay['yaw_t'])
        self.pitchDisplay['lcd'].display(self.dataToDisplay['pitch_t'])
        self.rollDisplay['lcd'].display(self.dataToDisplay['roll_t'])
        self.yawDisplay1['lcd'].display(self.dataToDisplay['yaw_c'])
        self.pitchDisplay1['lcd'].display(self.dataToDisplay['pitch_c'])
        self.rollDisplay1['lcd'].display(self.dataToDisplay['roll_c'])

    def update_display_data(self,
                            d = {
                                'hr' : 0,
                                'yaw_t' : 0,
                                'pitch_t' : 0,
                                'roll_t' : 0,
                                'yaw_c' : 0,
                                'pitch_c:' : 0,
                                'roll_c' : 0
                                }
                            ):
        self.dataToDisplay =  d
        self.onData.emit()

    def onStopClicked(self):
        #function to modify the interface state and visuals
        self.controlButtons['start'].setEnabled(True)
        self.controlButtons['stop'].setEnabled(False)
        print('stop clicked')
        self.update_display_data(d = {
                                        'hr' : 0,
                                        'yaw_t' : 0,
                                        'pitch_t' : 0,
                                        'roll_t' : 0,
                                        'yaw_c' : 0,
                                        'pitch_c' : 0,
                                        'roll_c' : 0
                                        }
                                        )
        self.Borg.j = 2
        self.Borg.move()

#Borg Button object
class BorgButton(object):
    def __init__(self, window):
        self.window = window
        self.cursorStatus = 0
        self.j = None
        #setting background Label Borgº
        self.Labelborg=QtGui.QLabel(self.window)
        self.Labelborg.setGeometry(QtCore.QRect(self.window.winsize_h*0.05,self.window.winsize_v*0.81,self.window.winsize_h*0.7 ,self.window.winsize_h*0.05))
        Icon2=QtGui.QPixmap("gui/img/borgh")
        Icon_resize= Icon2.scaled(self.window.winsize_h*0.7 ,self.window.winsize_h*0.045,QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
        self.Labelborg.setPixmap(Icon_resize)
        self.Labelborg.setScaledContents(True)

        #get borg scale buttons
        self.create_borg_button()

    def create_borg_button(self):
        self.Borg = []
        offset = 1
        ep = self.window.winsize_h*0.046
        xp = self.window.winsize_h*0.054
        yp = self.window.winsize_v*0.82
        hp = self.window.winsize_h*0.042
        wp = self.window.winsize_h*0.042
        x = xp
        e = ep
        y = yp
        h = hp
        w = wp
        for i in range(15):
            self.Borg.append(QtGui.QLabel(self.window))
            Icon2=QtGui.QPixmap("gui/img/l" + str(i))
            Icon_resize= Icon2.scaled(h,w,QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
            self.Borg[-1].setPixmap(Icon_resize)
            self.Borg[-1].setGeometry(x,y,h,w)
            x = x + e
            

        self.set_cursor(0)

    def set_cursor(self, p):
        self.Borg[self.cursorStatus].setStyleSheet("border-style: outset")
        self.Borg[p].setStyleSheet("border:2.5px solid rgb(50,50,50); border-radius:10px;")
        self.cursorStatus = p

    def move(self):
        print('MOVE FUNCTION ON')
        if self.j == '4':
            if self.cursorStatus < 14:
                self.set_cursor(self.cursorStatus + 1)
        elif self.j =='2':
            if self.cursorStatus > 0:
                self.set_cursor(self.cursorStatus -1)

    #def

    #TODO: to implement these functions
    def lock_buttons(self):
        print('lock borg buttons')

    def unlock_buttons(self):
        print('unlock borg buttons')

#def main():
    #app=QtGui.QApplication(sys.argv)
    #GUI=MainTherapyWin()
    #sys.exit(app.exec_())
#A=main()

if __name__ == '__main__':
    app=QtGui.QApplication(sys.argv)
    GUI=MainTherapyWin()
    sys.exit(app.exec_())

