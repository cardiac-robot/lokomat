from gui import MainTherapyWin
import robotController.controller as controller
import lib.SensorManager as Manager     
from PyQt4 import QtCore, QtGui
import time
class MainTherapyPlugin(object):
	"""docstringMainTherapyPluginsName"""
	def __init__(self, settings = {
									'robot'          : None,
									'sensor'         : None,
									'projectHandler' : {
														'db'   :   None,
														'paths':   None
													   }
									'modality': None
								  }
			    ):
		
		# load settings
		self.settings = settings
		#load settings from database
		self.load_settings()
		# GUI component
		self.MainTherapyWin  = MainTherapyWin.MainTherapyWin(project_Handler = self.settings['projectHandler']['paths'], modalities=self.settings['modalities'])
		#update display thread
		self.SensorUpdateThread = SensorUpdateThread(f = self.sensor_update, sample = 1)
		#create sensor manager
		self.Manager = Manager.ManagerRx(settings = self.settings['sensor'])
		#robot
		if self.settings['robot']['use']:
			self.launch_robot()
		#sensor
		if self.settings['sensor']['use']:
			self.launch_sensors()

		self.set_signals()	
		
		#database

#####################Methods#######################:
	# set signals and connections
	def set_signals(self):
		self.MainTherapyWin.connectStartButton(f = self.on_start_clicked)
		self.MainTherapyWin.connectStopButton(f = self.shutdown)
		self.MainTherapyWin.connectStopButton(f = self.finish_session)
		self.MainTherapyWin.onSensorUpdate.connect(self.update_database)

	# show GUI 
	def launch_gui(self):
		self.MainTherapyWin.show()

	#Launch robot object
	def launch_robot(self):
		#create robot controller object
		self.robotController = controller.RobotController(self.settings['robot'])
		#set robot sentences
		self.robotController.set_sentences()
		#set robot limits
		self.robotController.set_limits()
		#connect to signals from the GUI 
		self.MainTherapyWin.onStart.connect(self.robotController.start_session)
		self.MainTherapyWin.onStart.connect(self.robotController.set_routines)
		self.MainTherapyWin.onStop.connect(self.robotController.stop_routines)
		self.MainTherapyWin.onStop.connect(self.robotController.shutdown)
		self.MainTherapyWin.onBorg.connect(self.send_borg_to_robot)

	#launch sensor manager
	def launch_sensors(self):
		
		# set sensors
		self.Manager.set_sensors(ecg = False, imu = True)
		#sensor update processes
		self.ImuCaptureThread   = ImuCaptureThread(interface = self)
		self.JoyCaptureThread   = JoyCaptureThread(interface = self)
		self.EcgCaptureThread   = EcgCaptureThread(interface = self)

	#load settings from database
	def load_settings(self):
		db = self.settings['projectHandler']['db']
		if db:
			s = db.get_settings()
			self.settings['robot'] = s['robot']
			self.settings['sensor'] = s['sensor']
			print self.settings
	
		else:
			
			self.settings['robot'] = { 
										'name' : 'palin',
									    'ip'             : '192.168.1.1',
									    'port'           :  9559,
									    'UseSpanish'     :  True,
		                                'MotivationTime' :  300000000,
		                                'use'            :  False,
									   }

			self.settings['sensor'] =  {
										'joy_port'  : 'COM5',
										'imu_port'  : 'COM4',
										'ecg_port'  : 'COM6',
										'joy_sample':  0.1,
										'imu_sample':  1,
										'joy_baud'  :  9600,
										'imu_baud'  :  9600,
										'ecg_sample':  1,
										'use'		: False
									   }

	#callback function when start button is pressed									   
	def on_start_clicked(self):
		#launch sensor display update thread
		self.SensorUpdateThread.start()
		#create patient's session
		self.settings['projectHandler']['db'].create_session()
		self.settings['projectHandler']['db'].create_data_folder()
		#validate settings
		if self.settings['sensor']['use']:
			print('sensors')
			self.ImuCaptureThread.start()
			self.JoyCaptureThread.start()
			self.EcgCaptureThread.start()
		
		if self.settings['robot']['use']:
			self.RobotCaptureThread.start()


	#display update process
	def sensor_update(self):
		if self.settings['sensor']['use'] :
			self.data = self.Manager.get_data()
			print(self.data)
			self.MainTherapyWin.update_display_data(d = {
															'hr': self.data['ecg']['hr'],
															'yaw_t': self.data['imu1']['yaw'],
															'pitch_t': self.data['imu1']['pitch'],
															'roll_t':self.data['imu1']['roll'],
															'yaw_c' : self.data['imu2']['yaw'],
                                                        	'pitch_c' : self.data['imu2']['pitch'],
                                                        	'roll_c' : self.data['imu2']['roll'] 
														})
			self.MainTherapyWin.onSensorUpdate.emit()


		else:
			print('no sensors')
			self.Manager.simulate_data()
			self.data = self.Manager.get_data()
			self.MainTherapyWin.update_display_data(d = {
			                                            'hr' : self.data['ecg']['hr'],
			                                            'yaw_t' : self.data['imu1']['yaw'],
			                                            'pitch_t' : self.data['imu1']['pitch'],
			                                            'roll_t' : self.data['imu1']['roll'],
			                                            'yaw_c' : self.data['imu2']['yaw'],
			                                            'pitch_c' : self.data['imu2']['pitch'],
			                                            'roll_c' : self.data['imu2']['roll']
			                                          })
			self.MainTherapyWin.onSensorUpdate.emit()
	
	# updata db handler with last data measured
	def update_database(self):
		self.settings['projectHandler']['db'].get_sensor_reading(
																 speed          ="no data" ,
																 heart_rate     = self.data['ecg']['hr'],
																 steplength     = "no data", 
																 cadence        = "no data", 
																 blood_pressure = "no data",
																 imu_head       = self.data['imu1'],
																 imu_torso      = self.data['imu2']
																)
	def finish_session(self):
		self.settings['projectHandler']['db'].save_session()


	# shutdown all threads and processes
	def shutdown(self):
		self.SensorUpdateThread.shutdown()
		if self.settings['sensor']['use']:
			#sensor update processes
			self.ImuCaptureThread.shutdown()
			self.JoyCaptureThread.shutdown()
			self.EcgCaptureThread.shutdown()

#QtThread classes 

#thred for ECG capture
class EcgCaptureThread(QtCore.QThread):
    def __init__(self, parent = None, sample = 1, interface = None):
        super(EcgCaptureThread,self).__init__()
        self.on = False 
        self.interface = interface

    def run(self):
        self.interface.Manager.ecg_thread()

    def shutdown(self):
        self.on = False 
        self.interface.Manager.ecg_shutdown()

#thread for IMU capture
class ImuCaptureThread(QtCore.QThread):
    def __init__(self, parent = None, sample = 1, interface = None):
        super(ImuCaptureThread,self).__init__()
        self.on = False 
        self.interface = interface

    def run(self):
        self.interface.Manager.imu_thread()

    def shutdown(self):
        self.on = False 
        self.interface.Manager.imu_shutdown()

#thread for Robot data transmission
class RobotCaptureThread(QtCore.QThread):
    def __init__(self, parent = None, sample = 10, interface = None):
        super(RobotCaptureThread,self).__init__()
        self.Ts = sample
        self.ON = True
        self.interface = interface   
        
    def run(self):
        #self.interface.robotController.posture.goToPosture("StandZero", 1.0)
        while self.ON:
            d = self.interface.Manager.get_data()
            self.interface.robotController.set_data(d)
            time.sleep(self.Ts)
            
                
    def shutdown(self):
        self.ON = False

#Thread for sensor update
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