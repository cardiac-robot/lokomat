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
		# GUI component
		self.NewRegisterWin	= NewRegisterWin.NewRegisterWin()


	#launch gui
	def launch_gui(self):
		self.NewRegisterWin.show()	

	# save patient
	def save_patient(self):
		d = self.NewRegisterWin.getPatient()
		self.DataManager.register( name = d['name'], age = d['age'], gender =d['gender'] , height = d['height'], crotch=d['crotch'], id_number = d['id'])
    
