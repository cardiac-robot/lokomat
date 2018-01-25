from gui import MainTherapyWin
import robotController.controller as controller
import lib.SensorManager as Manager     

class MainTherapyPlugin(object):
	"""docstringMainTherapyPluginsName"""
	def __init__(self, settings = {
									'robot'          : None,
									'sensor'         : None,
									'projectHandler' : {
														'db'   :   None,
														'paths':   None
													   }
								  }
			    ):
		
		# load settings
		self.settings = settings
		#load settings from database
		self.load_settings()
		# GUI component
		self.MainTherapyWin  = MainTherapyWin.MainTherapyWin()
		#robot
		if self.settings['robot']['use']:
			self.robotController = controller.RobotController(self.settings['robot'])
			self.robotController.set_sentences()
			self.robotController.set_limits()
			self.MainTherapyWin.onStart.connect(self.robotController.start_session)
			self.MainTherapyWin.onStart.connect(self.robotController.set_routines)
			self.MainTherapyWin.onStop.connect(self.robotController.stop_routines)
			self.MainTherapyWin.onStop.connect(self.robotController.shutdown)
			self.MainTherapyWin.onBorg.connect(self.send_borg_to_robot)

		self.Manager  = Manager.ManagerRx(settings = self.settings['sensor'])
		
		#database

	def launch_gui(self):
		self.MainTherapyWin.show()

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



