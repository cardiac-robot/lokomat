from gui import IDRegisterWin 


class IdRegisterPlugin(object):
	def __init__(self, settings = {
									'projectHandler' : {
														'db'   :   None,
														'paths':   None
													   }
								  }
		        ):
		#load settings
		self.settings = settings
		#create GUI 
		self.IdRegisterWin = IDRegisterWin.IDRegisterWin(project_Handler = self.settings['projectHandler']['paths'])

		self.set_signals()


	def launch_gui(self):
		self.IdRegisterWin.show()

	def set_signals(self):
		self.IdRegisterWin.onRegister.connect(self.validate_patient)
	
	def connectToOnFound(self, f):
		self.IdRegisterWin.onFound.connect(f)


	def connectToNotFound(self, f):
		self.IdRegisterWin.onNotFound.connect(f)

	def validate_patient(self):
		#jdjdjdjd
		I = self.IdRegisterWin.getId()
		r = self.settings['projectHandler']['db'].find_patient(I)
		
		if self.settings['projectHandler']['db'].RegisterStatus[0]:
			self.IdRegisterWin.onFound.emit()
		else:
			self.IdRegisterWin.onNotFound.emit()
