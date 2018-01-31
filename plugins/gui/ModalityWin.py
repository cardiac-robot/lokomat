# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import*
from PyQt4.QtGui import*
import ctypes

class ModalitiesWin(QtGui.QMainWindow):
    onLokomat = QtCore.pyqtSignal()
    onBws     = QtCore.pyqtSignal()

    def __init__(self,project_Handler):
        super(ModalitiesWin,self).__init__()
        self.init_ui()
        self.project_Handler=project_Handler
        #Signals
        
    def init_ui(self):
        #-------------main config---------------
        #Window title
        self.setWindowTitle("Modalities Window")
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
        #----------------------------------
        #----------- Buttons config----------
        #setting background lokomat image
        self.start=QtGui.QLabel(self)
        self.start.setGeometry(QtCore.QRect(self.winsize_h*0.20,self.winsize_v*0.30,self.winsize_h*0.21 ,self.winsize_h*0.21))
        Icon3=QtGui.QPixmap(self.project_Handler.paths["img"]+"/lokomat.png")
        Icon_resize3= Icon3.scaled(self.winsize_h*0.21 ,self.winsize_h*0.21,QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
        self.start.setPixmap(Icon_resize3)
        #setting background Boddy Weight support image
        self.start=QtGui.QLabel(self)
        self.start.setGeometry(QtCore.QRect(self.winsize_h*0.58,self.winsize_v*0.30,self.winsize_h*0.21 ,self.winsize_h*0.21))
        Icon3=QtGui.QPixmap(self.project_Handler.paths["img"]+"/bws.png")
        Icon_resize3= Icon3.scaled(self.winsize_h*0.21 ,self.winsize_h*0.21,QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
        self.start.setPixmap(Icon_resize3)
        #setting background close image
        self.stop=QtGui.QLabel(self)
        self.stop.setGeometry(QtCore.QRect(self.winsize_h*0.943,self.winsize_v*0.02,self.winsize_h*0.038 ,self.winsize_h*0.038))
        Icon4=QtGui.QPixmap(self.project_Handler.paths["img"]+"/closebtn.png")
        Icon_resize5= Icon4.scaled(self.winsize_h*0.038 ,self.winsize_h*0.038,QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
        self.stop.setPixmap(Icon_resize5)
        self.controlButtons = {}
        #register button
        self.controlButtons['lokomat'] =QtGui.QCommandLinkButton(self)
        self.controlButtons['lokomat'].setGeometry(QtCore.QRect(self.winsize_h*0.20,self.winsize_v*0.30,self.winsize_h*0.20 ,self.winsize_h*0.21))
        self.controlButtons['lokomat'].setIconSize(QSize(0,0))
        #new register button
        self.controlButtons['bws'] =QtGui.QCommandLinkButton(self)
        self.controlButtons['bws'].setGeometry(QtCore.QRect(self.winsize_h*0.58,self.winsize_v*0.30,self.winsize_h*0.20 ,self.winsize_h*0.21))
        self.controlButtons['bws'].setIconSize(QSize(0,0))
        #Close button
        self.controlButtons['close'] = QtGui.QCommandLinkButton(self)
        self.controlButtons['close'].setGeometry(QtCore.QRect(self.winsize_h*0.943,self.winsize_v*0.02,self.winsize_h*0.038 ,self.winsize_h*0.038))
        self.controlButtons['close'].setIconSize(QSize(0,0))
        #Lokomat
        self.lokomat= QtGui.QLabel(self)
        self.lokomat.setText("Lokomat")
        self.lokomat.setStyleSheet("font-size:18px; Arial")
        self.lokomat.setGeometry(QtCore.QRect(self.winsize_h*0.27,self.winsize_v*0.55,self.winsize_h*0.2 ,self.winsize_h*0.2))
        #BWS
        self.Bws= QtGui.QLabel(self)
        self.Bws.setText("Soporte de peso Corporal")
        self.Bws.setStyleSheet("font-size:18px; Arial")
        self.Bws.setGeometry(QtCore.QRect(self.winsize_h*0.61,self.winsize_v*0.55,self.winsize_h*0.2 ,self.winsize_h*0.2))
        

#def main():
    #app=QtGui.QApplication(sys.argv)
    #GUI=ModalitiesWin()
    #sys.exit(app.exec_())
#A=main()

if __name__ == '__main__':
    app=QtGui.QApplication(sys.argv)
    GUI=MainMenuWin()
    sys.exit(app.exec_())     
        
