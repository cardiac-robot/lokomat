#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 17:23:31 2017

@author: pi
"""

import threading
import plugins.gui.MainTherapyWin as MainTherapyWin
import plugins.gui.IDRegisterWin as IdRegisterWin
import plugins.gui.MainMenuWin as MainMenuWin
import plugins.gui.NewRegisterWin as NewRegisterWin
import plugins.gui.ModalityWin as ModalityWin
import db.database as database
#import lib.Analog_Joystick_rpi as Joy
#import lib.manager as man
import plugins.MainTherapyPlugin as MainTherapyPlugin
import plugins.NewRegisterPlugin as NewRegisterPlugin 
import plugins.IdRegisterPlugin as IdRegisterPlugin  
import plugins.ModalityPlugin as ModalityPlugin    
import plugins.lib.SensorManager as Manager       
import plugins.robotController.controller as controller
from PyQt4 import QtCore, QtGui



import time
import sys

class Index(object):
    def __init__(self):

        self.MainMenuPlugin = self.MainMenuPlugin()





class MainMenuPlugin(object):
    def __init__(self):
        #create database client
        self.DataManager = database.DataManager()
        #launch project handler and paths controller
        self.ProjectHandler = database.ProjectHandler()
        #create GUI for main menu
        self.MainMenuWin = MainMenuWin.MainMenuWin(project_Handler = self.ProjectHandler)
        #self.ModalityWin = ModalityWin.ModalityWin(project_Handler = self.ProjectHandler)
        #Plugins creation
        print self.DataManager
        print self.DataManager
        print self.ProjectHandler
        print self.MainMenuWin
        #create MainTherapyPlugin
        self.MainTherapyPlugin = MainTherapyPlugin.MainTherapyPlugin(settings = {
                                                                                    'projectHandler' : {
                                                                                                        'db'   :   self.DataManager,
                                                                                                        'paths':   self.ProjectHandler
                                                                                                        } 
                                                                                }
                                                                    )

        #create NewRegisterPlugin
        self.NewRegisterPlugin = NewRegisterPlugin.NewRegisterPlugin( settings = {
                                                                                    'projectHandler' : {
                                                                                                        'db'   :   self.DataManager,
                                                                                                        'paths':   self.ProjectHandler
                                                                                                        } 
                                                                                }
                                                                    )    

        
        self.IdRegisterPlugin = IdRegisterPlugin.IdRegisterPlugin(  settings = {
                                                                                    'projectHandler' : {
                                                                                                        'db'   :   self.DataManager,
                                                                                                        'paths':   self.ProjectHandler
                                                                                                        } 
                                                                                }
                                                                  )
        self.ModalityPlugin = ModalityPlugin.ModalityPlugin(   settings = {         'projectHandler': {
                                                                                                        'db' :      self.DataManager,
                                                                                                        'paths':    self.ProjectHandler
                                                                                                        }
                                                                            }                        
                                                                 )
       
        #set signals and connections
        self.set_signals()
        #show GUI
        self.MainMenuWin.show()


    def set_signals(self):
        #connect start therapy button with start threapy plugin
        
        self.MainMenuWin.connectStartButton(self.IdRegisterPlugin.launch_gui)
        #connect new Register button with the new register plugin
        
        self.MainMenuWin.connectNewRegisterButton(self.NewRegisterPlugin.launch_gui)
        #connect to id registerwin logic
       
        self.IdRegisterPlugin.connectToOnFound(self.ModalityPlugin.launch_gui)
       
        self.IdRegisterPlugin.connectToNotFound(self.NewRegisterPlugin.launch_gui)
        
        #connect to ModalityWin Logic.
    
        self.ModalityPlugin.ModalityWin.onLokomat.connect(self.MainTherapyPlugin.launch_gui)
 
        self.ModalityPlugin.ModalityWin.onBws.connect(self.MainTherapyPlugin.launch_gui)
        







class LokomatInterface(object):
    
    def __init__(self, settings = {
                                    'UseSensors': True,
                                    'UseRobot'  : True,
                                    'RobotIp'   : "192.168.0.101",
                                    'RobotPort' : 9559
                                  }
                                    ):
        #load settings
        self.settings = settings
        #Interface Objects
        #self.therapy_win = interface.MainTherapyWin()
        #self.IdRegisterWin = IdRegisterWin.IDRegisterWin()
        self.MainMenuWin = MainMenuWin. MainMenuWin()
        
        #self.NewRegisterWin = NewRegisterWin.NewRegisterWin()
        #create database manager
        #self.DataManager = database.DataManager()

        

        #therapy win interface object
        if self.settings['UseRobot']:
            self.RobotCaptureThread = RobotCaptureThread(interface = self)

            self.robotController = controller.RobotController({
                                                                 'name'       : "Palin",
                                                                 'ip'         : self.settings['RobotIp'],
                                                                 'port'       : self.settings['RobotPort'],
                                                                 'UseSpanish' : True,
                                                                 'MotivationTime': 300000000
                                                              }
                                                             
                                                              )

            self.robotController.set_sentences()
            self.robotController.set_limits()


            self.therapy_win.onStart.connect(self.robotController.start_session)
            self.therapy_win.onStart.connect(self.robotController.set_routines)
            self.therapy_win.onStop.connect(self.robotController.stop_routines)     
            self.therapy_win.onStop.connect(self.robotController.shutdown)
            self.therapy_win.onBorg.connect(self.send_borg_to_robot)

        #creating Joy object
        #self.Joy = Joy.JoyHandler(sample = 0.3, gui = self.therapy_win)
        #create robot controller
        '''self.RobotController = controller.RobotController(ip = self.settings['UseRobot'], useSpanish = True)
        self.RobotController.set_sentences()
        self.RobotController.set_limits()
        self.NaoThread = RobotCaptureThread(self)
        '''

        # display data update data 
        self.SensorUpdateThread = SensorUpdateThread(f = self.sensor_update, sample = 1)
        
        #create sensor Manager
        self.ManagerRx  = ManagerTx.ManagerRx(settings = {
                            'joy_port'  : 'COM9',
                            'imu_port'  : 'COM4',
                            'ecg_port'  : 'COM3',
                            'joy_sample': 0.2,
                            'imu_sample': 1,
                            'joy_baud'  : 9600,
                            'imu_baud'  : 9600,
                            'ecg_sample': 1
                          })

        if self.settings['UseSensors']:
            
            # set sensors
            self.ManagerRx.set_sensors(ecg = True, imu = True)
            # threads
            
            #sensor update processes
            self.ImuCaptureThread   = ImuCaptureThread(interface = self)
            self.JoyCaptureThread   = JoyCaptureThread(interface = self)
            self.EcgCaptureThread   = EcgCaptureThread(interface = self)
            #binding functions
            self.ManagerRx.joy_gui_bind(self.joy_handler)
            self.ManagerRx.imu_gui_bind(self.imu_handler)  
            #


        #BOOL
        self.ON = True
        #sample time

       
        #conntecting to interface
        self.therapy_win.connectStartButton(self.on_start_clicked)
        self.therapy_win.connectStopButton(self.on_stop_clicked)
        self.therapy_win.connectStopButton(self.DataManager.pipe_sensor_data)
        self.therapy_win.connectCloseButton(self.DataManager.clearRegisterStatus)
        # Interface Signals connections
        self.MainMenuWin.connectNewRegisterButton(f = self.NewRegisterWin.show)
        self.MainMenuWin.connectStartButton(f = self.start_therapy)
        self.NewRegisterWin.onData.connect(self.save_patient)
        self.therapy_win.onSensorUpdate.connect(self.save_sensor_data)
        self.IdRegisterWin.onRegister.connect(self.validate_patient)

        #
        self.MainMenuWin.show()


    # save patient
    def save_patient(self):
        d = self.NewRegisterWin.getPatient()
        self.DataManager.register( name = d['name'], age = d['age'], gender =d['gender'] , height = d['height'], crotch=d['crotch'], id_number = d['id'])
    
    # save sensor data in database     
    def save_sensor_data(self):
        self.DataManager.get_sensor_reading(speed = "nd",
                                            heart_rate = self.data['ecg']['hr'],
                                            steplength = "nd", 
                                            cadence = "nd", 
                                            blood_pressure = "nd",
                                            imu_head =  self.data['imu1'],
                                            imu_torso = self.data['imu2']
                                            )

    #start therapy logic implementation
    def start_therapy(self):
        if self.DataManager.RegisterStatus[0]:
        
            self.therapy_win.show()
        
        else:
            self.IdRegisterWin.show()

    #find the patient on th database and update the register status
    def validate_patient(self):
        print('enter validate patient')
        id_number = self.IdRegisterWin.getId()
        self.DataManager.find_patient(id_number)
        
        if self.DataManager.RegisterStatus[0] == 0:
            #call register window
            self.NewRegisterWin.show()
        elif self.DataManager.RegisterStatus[0] == 1:
            #the patient is already registered and the therapy can start
            self.start_session()

    

    def start_session(self):

        self.therapy_win.show()
        self.DataManager.create_session()
        self.DataManager.create_data_folder()


#################################################################################################

    def on_start_clicked(self):
        print('started from index')
        #self.therapy_win.onStart.emit()        
        #self.Joy.launch_thread()
        self.SensorUpdateThread.start()
        if self.settings['UseSensors']:
            print('sensors')
            self.ImuCaptureThread.start()
            self.JoyCaptureThread.start()
            self.EcgCaptureThread.start()

        if self.settings['UseRobot']:
            self.RobotCaptureThread.start()

            
            #self.manager.launch_sensors()
            #self.manager.play_sensors()
            #self.SensorUpdateThread.start()
            #self.NaoThread.start()

    def on_stop_clicked(self):
        self.shutdown()
        print('stopped from index')
        if self.settings['UseSensors']:
            print('sensors')
            self.ManagerRx.shutdown()

        if self.settings['UseRobot']:
            self.RobotCaptureThread.shutdown()
        
            #self.manager.shutdown()
            #self.SensorUpdateThread.shutdown()
            #self.NaoThread.stop()



    def send_borg_to_robot(self):
        print("SEND BORG")
        d = self.therapy_win.Borg.cursorStatus + 6  
        self.robotController.get_borg(d)


    #bind functions to the sensor data manager

    def imu_handler(self, data):
        print('Getting IMU data ')



    def joy_handler(self, data):
        print('MOVING CURSOR')
        self.therapy_win.Borg.j  = data['joy']
        print(self.therapy_win.Borg.j)
        self.therapy_win.onJoy.emit()

    def sensor_update(self):

        if self.settings['UseSensors']:
            #self.ManagerRx  .update_data()
            self.data = self.ManagerRx.get_data()
            print(self.data)
            self.therapy_win.update_display_data(d = {
                                                        'hr' : self.data['ecg']['hr'],
                                                        'yaw_t' : self.data['imu1']['yaw'],
                                                        'pitch_t' : self.data['imu1']['pitch'],
                                                        'roll_t' : self.data['imu1']['roll'],
                                                        'yaw_c' : self.data['imu2']['yaw'],
                                                        'pitch_c' : self.data['imu2']['pitch'],
                                                        'roll_c' : self.data['imu2']['roll']
                                                      }
                                    )
            self.therapy_win.onSensorUpdate.emit()

        else:
            print('no sensors')
            self.ManagerRx.simulate_data()
            self.data = self.ManagerRx.get_data()
            self.therapy_win.update_display_data(d = {
                                                        'hr' : self.data['ecg']['hr'],
                                                        'yaw_t' : self.data['imu1']['yaw'],
                                                        'pitch_t' : self.data['imu1']['pitch'],
                                                        'roll_t' : self.data['imu1']['roll'],
                                                        'yaw_c' : self.data['imu2']['yaw'],
                                                        'pitch_c' : self.data['imu2']['pitch'],
                                                        'roll_c' : self.data['imu2']['roll']
                                                      })
            self.therapy_win.onSensorUpdate.emit()


    def shutdown(self):
        self.SensorUpdateThread.shutdown()
        if self.settings['UseSensors']:
            
            #sensor update processes
            self.ImuCaptureThread.shutdown()
            self.JoyCaptureThread.shutdown()
            self.EcgCaptureThread.shutdown()






class EcgCaptureThread(QtCore.QThread):
    def __init__(self, parent = None, sample = 1, interface = None):
        super(EcgCaptureThread,self).__init__()
        self.on = False 
        self.interface = interface

    def run(self):
        self.interface.ManagerRx.ecg_thread()

    def shutdown(self):
        self.on = False 
        self.interface.ManagerRx.ecg_shutdown()


class ImuCaptureThread(QtCore.QThread):
    def __init__(self, parent = None, sample = 1, interface = None):
        super(ImuCaptureThread,self).__init__()
        self.on = False 
        self.interface = interface

    def run(self):
        self.interface.ManagerRx.imu_thread()

    def shutdown(self):
        self.on = False 
        self.interface.ManagerRx.imu_shutdown()      

class JoyCaptureThread(QtCore.QThread):
    def __init__(self, parent = None, sample = 1, interface = None):
        super(JoyCaptureThread,self).__init__()
        self.on  = True
        self.interface   = interface    
    def run(self):
        self.interface.ManagerRx.joy_thread()
            
    def shutdown(self):
        self.on = False 
        self.interface.ManagerRx.joy_shutdown()    



class RobotCaptureThread(QtCore.QThread):
    def __init__(self, parent = None, sample = 10, interface = None):
        super(RobotCaptureThread,self).__init__()
        self.Ts = sample
        self.ON = True
        self.interface = interface
        
        
        
    def run(self):
        #self.interface.robotController.posture.goToPosture("StandZero", 1.0)
        while self.ON:
            d = self.interface.ManagerRx.get_data()
            self.interface.robotController.set_data(d)
            time.sleep(self.Ts)
            
                
    def shutdown(self):
        self.ON = False

class SensorUpdateThread(QtCore.QThread):

     def __init__(self, parent = None, f = None, sample = 1):
        super(SensorUpdateThread,self).__init__()
        self.f = f
        self.Ts = sample
        self.ON = True
        
     def run(self):

        if self.f:
            while self.ON:
                self.f()
                time.sleep(self.Ts)

     def shutdown(self):
        self.ON = False


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    a =MainMenuPlugin()
    sys.exit(app.exec_())
