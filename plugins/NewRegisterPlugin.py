from gui import NewRegisterWin



class NewRegisterPlugin(object):
	"""docstring for ClassName"""
	def __init__(self, settings = {
									'projectHandler' : {
														'db'   :   None,
														'paths':   None
													   }
								  }

				):
		#load settings
		self.settings = settings
		#load database client
		self.DataManager = self.settings['projectHandler']['db']
		# GUI component
		self.NewRegisterWin	= NewRegisterWin.NewRegisterWin(project_Handler = self.settings['projectHandler']['paths'])
		#set signals
		self.set_signals()


	#launch gui
	def launch_gui(self):
		self.NewRegisterWin.show()	

	#setting signals and methods
	def set_signals(self):
		self.NewRegisterWin.onData.connect(self.save_patient)

	# save patient
	def save_patient(self):
		#retrieve patient from GUI form
		d = self.NewRegisterWin.getPatient()
		#register patient in database
		self.DataManager.register( 
								   name = d['name'],
								   age = d['age'],
								   gender =d['gender'],
								   height = d['height'],
								   crotch=d['crotch'],
								   id_number = d['id']
								 )
    
	#find the patient on th database and update the register status
	def validate_patient(self):
		print('enter validate patient')
		#get the id for comparison
		id_number = self.IdRegisterWin.getId()
		
		self.DataManager.find_patient(id_number)

		if self.DataManager.RegisterStatus[0] == 0:
		    #call register window
		    self.NewRegisterWin.show()
		elif self.DataManager.RegisterStatus[0] == 1:
		    #the patient is already registered and the therapy can start
		    self.start_session()