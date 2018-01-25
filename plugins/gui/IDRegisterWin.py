# -*- coding: utf-8 -*-import sys
import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import*
from PyQt4.QtGui import*
import ctypes

class IDRegisterWin(QtGui.QMainWindow):
    onRegister = QtCore.pyqtSignal()

    def __init__(self):
        super(IDRegisterWin,self).__init__()
        self.init_ui()
        ##Signals
        self.set_signals()
    def init_ui(self):
        #-------main config-------
        #Window title
        self.setWindowTitle("ID Register Window")
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
        self.label_background.setPixmap(QtGui.QPixmap("gui/img/Window.png"))
        self.label_background.setScaledContents(True)
        #----------------------------------
        #-----------Labels config----------
        #ID Label:
        self.NameDisplay = {}
        
        self.NameDisplay['name'] = QtGui.QLabel(self)
        self.NameDisplay['name'].setText("ID:")
        self.NameDisplay['name'].setStyleSheet("font-size:24px; Arial")
        self.NameDisplay['name'].setGeometry(QtCore.QRect(self.winsize_h*0.35,self.winsize_v*0.33,self.winsize_h*0.35 ,self.winsize_h*0.1))
        self.NameDisplay['read'] = QtGui.QLineEdit(self)
        self.NameDisplay['read'].setStyleSheet("font-size:20px; Arial")
        self.NameDisplay['read'].setGeometry(QtCore.QRect(self.winsize_h*0.40,self.winsize_v*0.38,self.winsize_h*0.3 ,self.winsize_h*0.05))

        
        #-----------Buttons config----------
        #setting background user image
        self.start=QtGui.QLabel(self)
        self.start.setGeometry(QtCore.QRect(self.winsize_h*0.75,self.winsize_v*0.65,self.winsize_h*0.15 ,self.winsize_h*0.15))
        Icon3=QtGui.QPixmap("gui/img/terapiastart.png")
        Icon_resize3= Icon3.scaled(self.winsize_h*0.15 ,self.winsize_h*0.15,QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
        self.start.setPixmap(Icon_resize3)
        #setting background close image
        self.stop=QtGui.QLabel(self)
        self.stop.setGeometry(QtCore.QRect(self.winsize_h*0.943,self.winsize_v*0.02,self.winsize_h*0.038 ,self.winsize_h*0.038))
        Icon4=QtGui.QPixmap("gui/img/closebtn.png")
        Icon_resize5= Icon4.scaled(self.winsize_h*0.038 ,self.winsize_h*0.038,QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
        self.stop.setPixmap(Icon_resize5)

        
        
        self.controlButtons = {}
        #register button
        self.controlButtons['register'] =QtGui.QCommandLinkButton(self)
        self.controlButtons['register'].setGeometry(QtCore.QRect(self.winsize_h*0.75,self.winsize_v*0.65,self.winsize_h*0.135 ,self.winsize_h*0.15))
        self.controlButtons['register'].setIconSize(QSize(0,0))

  
        #Close button
        self.controlButtons['close'] = QtGui.QCommandLinkButton(self)
        self.controlButtons['close'].setGeometry(QtCore.QRect(self.winsize_h*0.943,self.winsize_v*0.02,self.winsize_h*0.038 ,self.winsize_h*0.038))
        self.controlButtons['close'].setIconSize(QSize(0,0))
        

    def set_signals(self):
        self.controlButtons['close'].clicked.connect(self.hide)
        self.controlButtons['register'].clicked.connect(self.get_id_data)

    def get_id_data(self):
        self.id = self.NameDisplay['read'].text()
        self.onRegister.emit()
        self.hide()

    def getId(self):
        return self.id

#def main():
    #app=QtGui.QApplication(sys.argv)
    #GUI=IDRegisterWin()
    #sys.exit(app.exec_())
#A=main()


if __name__ == '__main__':
    app=QtGui.QApplication(sys.argv)
    GUI=IDRegisterWin()
    sys.exit(app.exec_())

	
