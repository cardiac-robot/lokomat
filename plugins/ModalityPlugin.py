import gui.ModalityWin as ModalityWin
import db.database as database


class ModalityPlugin(object):
	def __init__(self, settings = {
									'projectHandler' : {
														'db'   :   None,
														'paths':   None
													   }
								  }
				):
		#load settings
		self.settings = settings
		#create GUI resource
		self.ModalityWin = ModalityWin.ModalityWin(project_Handler = self.settings['projectHandler']['paths'])
		#create database resource
		self.database = settings['projectHandler']['db'].DbManager
		#print(self.database)
		self.set_signals()

	def set_signals(self):
		self.ModalityWin.onBws.connect(self.setBwsMode)
		self.ModalityWin.onLokomat.connect(self.setLokomatMode)

	def launch_gui(self):
		self.ModalityWin.show()

	def setLokomatMode(self):
		self.database.update_modality_settings('lokomat')
		
	def setBwsMode(self):
		self.database.update_modality_settings('bws')
	


	







	



