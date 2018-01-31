import gui.ModalityWin as ModalityWin


class ModalityPlugin(object):
	def __init__(selfsettings = {
									'projectHandler' : {
														'db'   :   None,
														'paths':   None
													   }
								  }
				):
		#load settings
		self.setting = settings
		#create GUI resource
		self.ModalityWin = ModalityWin.ModalityWin(project_Handler = self.settings['projectHandler']['paths'])


	def launch_gui(self):
		self.ModalityWin.show()

	



