# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import*
from PyQt4.QtGui import*
import ctypes

class SummaryWin(QtGui.QMainWindow):

    def __init__(self,project_Handler):
        super(SummaryWin,self).__init__()
        self.init_ui()
        self.project_Handler=project_Handler
    def init_ui(self):
        #-------------main config---------------
        #Window title
        self.setWindowTitle("Summary Window")
        #Window size
        self.user32=ctypes.windll.user32
        self.screensize=self.user32.GetSystemMetrics(0), self.user32.GetSystemMetrics(1),
        #Resizing MainWindoe to a percentage of the total
        self.winsize_h=int(self.screensize[0])
        self.winsize_v=int(self.screensize[1])
        self.resize(self.winsize_h,self.winsize_v)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        #setting backgroung image
        self.label_background=QtGui.QLabel(self)
        self.label_background.setGeometry(QtCore.QRect(0,0,self.winsize_h,self.winsize_v))
        self.label_background.setPixmap(QtGui.QPixmap(self.project_Handler.paths["img"]+"/Window.png"))
        self.label_background.setScaledContents(True)
     
        #setting background close image
        self.stop=QtGui.QLabel(self)
        self.stop.setGeometry(QtCore.QRect(self.winsize_h*0.943,self.winsize_v*0.02,self.winsize_h*0.038 ,self.winsize_h*0.038))
        Icon4=QtGui.QPixmap(self.project_Handler.paths["img"]+"/closebtn.png")
        Icon_resize5= Icon4.scaled(self.winsize_h*0.038 ,self.winsize_h*0.038,QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
        self.stop.setPixmap(Icon_resize5)
        #Weight Label
        self.weight={}
        self.weight['name']= QtGui.QLabel(self)
        self.weight['name'].setText("Peso")
        self.weight['name'].setStyleSheet("font-size:18px; Arial")
        self.weight['name'].setGeometry(QtCore.QRect(self.winsize_h*0.15,self.winsize_v*0.70,self.winsize_h*0.2 ,self.winsize_h*0.2))
        self.weight['read']= QtGui.QLineEdit(self)
        self.weight['read'].setStyleSheet("font-size:20px; Arial")
        self.weight['read'].setGeometry(QtCore.QRect(self.winsize_h*0.20,self.winsize_v*0.85,self.winsize_h*0.3 ,self.winsize_h*0.03))
        #Borg Scale Label and edit text
        self.labelSummary=BorgScaleLabel(self)
        #-----------Buttons config----------
        #setting background user image
        self.start=QtGui.QLabel(self)
        self.start.setGeometry(QtCore.QRect(self.winsize_h*0.75,self.winsize_v*0.65,self.winsize_h*0.15 ,self.winsize_h*0.15))
        Icon3=QtGui.QPixmap(self.project_Handler.paths["img"]+"/registerbutt.png")
        Icon_resize3= Icon3.scaled(self.winsize_h*0.15 ,self.winsize_h*0.15,QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
        self.start.setPixmap(Icon_resize3)
        #Close button
        self.controlButtons={}
        self.controlButtons['close'] = QtGui.QCommandLinkButton(self)
        self.controlButtons['close'].setGeometry(QtCore.QRect(self.winsize_h*0.943,self.winsize_v*0.02,self.winsize_h*0.038 ,self.winsize_h*0.038))
        self.controlButtons['close'].setIconSize(QSize(0,0))
        #register button
        self.controlButtons['register'] =QtGui.QCommandLinkButton(self)
        self.controlButtons['register'].setGeometry(QtCore.QRect(self.winsize_h*0.75,self.winsize_v*0.65,self.winsize_h*0.135 ,self.winsize_h*0.15))
        self.controlButtons['register'].setIconSize(QSize(0,0))

        self.show()

class BorgScaleLabel(object):

    def __init__(self, window):
        
        self.window=window
        self.Requestnumber=5
        #get Borg scale label
        self.create_label()
        
    def create_label(self):
        
        self.BorgScale=[]
        self.BorgRequest=[]
        ep = self.window.winsize_h*0.08
        xp = self.window.winsize_h*0.15
        yp = self.window.winsize_v*0.07
        hp = self.window.winsize_h*0.1
        wp = self.window.winsize_h*0.1
        ht = self.window.winsize_h*0.3
        wt = self.window.winsize_h*0.03
        yt = self.window.winsize_v*0.13
        xt = self.window.winsize_h*0.3
        x = xp
        e = ep
        y = yp
        h = hp
        w = wp
        for i in range(self.Requestnumber):
            self.BorgScale.append(QtGui.QLabel(self.window))
            self.BorgScale[i].setText("Escala de Borg " + str(i+1))
            self.BorgScale[i].setStyleSheet("font-size:18px; Arial")
            self.BorgScale[i].setGeometry(x,y,h,w)
            self.BorgRequest.append(QtGui.QLineEdit(self.window))
            self.BorgRequest[i].setStyleSheet("font-size:18px; Arial")
            self.BorgRequest[i].setGeometry(xt,yt,ht,wt)
            yt=yt+e
            y = y + e
            
def main():
    app=QtGui.QApplication(sys.argv)
    GUI=SummaryWin()
    sys.exit(app.exec_())
A=main()

if __name__ == '__main__':
    app=QtGui.QApplication(sys.argv)
    GUI=MainMenuWin()
    sys.exit(app.exec_())     
        
