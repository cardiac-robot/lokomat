# -*- coding: utf-8 -*-import sys
import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import*
from PyQt4.QtGui import*
import ctypes

class NewRegisterWin(QtGui.QMainWindow):

    def __init__(self):
        super(NewRegisterWin,self).__init__()
        self.init_ui()
        ##Signals
    def init_ui(self):
        #-------main config-------
        #Window title
        self.setWindowTitle("New Register Window")
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
        self.label_background.setPixmap(QtGui.QPixmap("Window.png"))
        self.label_background.setScaledContents(True)
        #----------------------------------
        #-----------Labels config----------
        #Name Label:
        self.NameDisplay = {}
        
        self.NameDisplay['name'] = QtGui.QLabel(self)
        self.NameDisplay['name'].setText("Nombre:")
        self.NameDisplay['name'].setStyleSheet("font-size:24px; Arial")
        self.NameDisplay['name'].setGeometry(QtCore.QRect(self.winsize_h*0.12,self.winsize_v*0.03,self.winsize_h*0.1 ,self.winsize_h*0.1))
        self.NameDisplay['read'] = QtGui.QLineEdit(self)
        self.NameDisplay['read'].setStyleSheet("font-size:20px; Arial")
        self.NameDisplay['read'].setGeometry(QtCore.QRect(self.winsize_h*0.20,self.winsize_v*0.1,self.winsize_h*0.3 ,self.winsize_h*0.03))

        #ID Label:
        self.IDDisplay = {}
        
        self.IDDisplay['name'] = QtGui.QLabel(self)
        self.IDDisplay['name'].setText("ID:")
        self.IDDisplay['name'].setStyleSheet("font-size:24px; Arial")
        self.IDDisplay['name'].setGeometry(QtCore.QRect(self.winsize_h*0.55,self.winsize_v*0.03,self.winsize_h*0.1 ,self.winsize_h*0.1))
        self.IDDisplay['read'] = QtGui.QLineEdit(self)
        self.IDDisplay['read'].setStyleSheet("font-size:20px; Arial")
        self.IDDisplay['read'].setGeometry(QtCore.QRect(self.winsize_h*0.60,self.winsize_v*0.1,self.winsize_h*0.3 ,self.winsize_h*0.03))


        #Year Label:
        self.YearDisplay = {}
    
        self.YearDisplay['name'] = QtGui.QLabel(self)
        self.YearDisplay['name'].setText("Edad:")
        self.YearDisplay['name'].setStyleSheet("font-size:24px; Arial")
        self.YearDisplay['name'].setGeometry(QtCore.QRect(self.winsize_h*0.12,self.winsize_v*0.20,self.winsize_h*0.1 ,self.winsize_h*0.1))
        self.YearDisplay['read'] = QtGui.QLineEdit(self)
        self.YearDisplay['read'].setStyleSheet("font-size:20px; Arial")
        self.YearDisplay['read'].setGeometry(QtCore.QRect(self.winsize_h*0.20,self.winsize_v*0.27,self.winsize_h*0.3 ,self.winsize_h*0.03))

        #Gender Label:
        self.GenderDisplay = {}
    
        self.GenderDisplay['name'] = QtGui.QLabel(self)
        self.GenderDisplay['name'].setText("Genero:")
        self.GenderDisplay['name'].setStyleSheet("font-size:24px; Arial")
        self.GenderDisplay['name'].setGeometry(QtCore.QRect(self.winsize_h*0.12,self.winsize_v*0.37,self.winsize_h*0.1 ,self.winsize_h*0.1))
        self.GenderDisplay['read'] = QtGui.QComboBox(self)
        self.GenderDisplay['read'].setStyleSheet("font-size:20px; Arial")
        self.GenderDisplay['read'].setGeometry(QtCore.QRect(self.winsize_h*0.20,self.winsize_v*0.44,self.winsize_h*0.3 ,self.winsize_h*0.03))
        self.GenderDisplay['read'].addItem("")
        self.GenderDisplay['read'].addItem("Femenino")
        self.GenderDisplay['read'].addItem("Maculino")
        

        #Altura Label:
        self.AlturaDisplay = {}
        
        self.AlturaDisplay['name'] = QtGui.QLabel(self)
        self.AlturaDisplay['name'].setText("Altura:")
        self.AlturaDisplay['name'].setStyleSheet("font-size:24px; Arial")
        self.AlturaDisplay['name'].setGeometry(QtCore.QRect(self.winsize_h*0.12,self.winsize_v*0.54,self.winsize_h*0.1 ,self.winsize_h*0.1))
        self.AlturaDisplay['read'] = QtGui.QLineEdit(self)
        self.AlturaDisplay['read'].setStyleSheet("font-size:20px; Arial")
        self.AlturaDisplay['read'].setGeometry(QtCore.QRect(self.winsize_h*0.20,self.winsize_v*0.61,self.winsize_h*0.3 ,self.winsize_h*0.03))

         #Altura entrepierna Label:
        self.AlturaEDisplay = {}
        
        self.AlturaEDisplay['name'] = QtGui.QLabel(self)
        self.AlturaEDisplay['name'].setText("Altura entrepierna:")
        self.AlturaEDisplay['name'].setStyleSheet("font-size:24px; Arial")
        self.AlturaEDisplay['name'].setGeometry(QtCore.QRect(self.winsize_h*0.12,self.winsize_v*0.71,self.winsize_h*0.4 ,self.winsize_h*0.1))
        self.AlturaEDisplay['read'] = QtGui.QLineEdit(self)
        self.AlturaEDisplay['read'].setStyleSheet("font-size:20px; Arial")
        self.AlturaEDisplay['read'].setGeometry(QtCore.QRect(self.winsize_h*0.30,self.winsize_v*0.78,self.winsize_h*0.1 ,self.winsize_h*0.03))
        
        
        #-----------Buttons config----------
        #setting background user image
        self.start=QtGui.QLabel(self)
        self.start.setGeometry(QtCore.QRect(self.winsize_h*0.75,self.winsize_v*0.65,self.winsize_h*0.15 ,self.winsize_h*0.15))
        Icon3=QtGui.QPixmap("gui/img/registerbutt.png")
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
        
        self.show()

#def main():
    #app=QtGui.QApplication(sys.argv)
    #GUI=NewRegisterWin()
    #sys.exit(app.exec_())
#A=main()

if __name__ == '__main__':
    app=QtGui.QApplication(sys.argv)
    GUI=NewRegisterWin()
    sys.exit(app.exec_())
