import gui.ModalityWin as ModalityWin
import db.database as database


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
		#create database resource
		self.database = settings['projectHandler']['db'].DbManager

	def set_signals(self):
		self.ModalityWin.onBws.connect(self.SetBwsMode)
		self.ModalityWin.onLokomat.connect(self.SetLokomatMode)

	def launch_gui(self):
		self.ModalityWin.show()

	def setLokomatMode(self):
		self.database.update_modality_settings('lokomat')
		
	def setBwsMode(self):
		self.database.update_modality_settings('bws')
	







	



