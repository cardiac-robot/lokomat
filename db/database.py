import os

import time

import pymongo

import datetime

import socket

import logging

import pickle

logging.basicConfig(level = logging.DEBUG, format = '[%(levelname)s] (%(threadName)-9s) %(message)s',)

class DataManager(object):
	def __init__(self):

		self.projectManager = ProjectHandler()
		self.DbManager = DbHandler()


		self.date =  datetime.datetime.now()
		#register status codes : 0: no registered, 1: already existing, 2: was just registered  
		self.RegisterStatus = [0, {'name':"no data"}]
	
	def find_patient(self, d):
		r = self.DbManager.check_patient(d)
		if r:
			self.RegisterStatus = [1, r]
		else:
			self.RegisterStatus = [0,{'name':"no data"}]
		print self.RegisterStatus

	def get_settings(self):
		a = self.DbManager.db.settings.find({})	
		for i in a:
			return	i

	#register method, validates the existence of the patient and stores the patient if is new
	def register(self, name = "nd", age = "nd", gender = "nd", height = "nd", crotch= "nd", id_number = 'nd'):
		self.person = {"name": name, "gender": gender, "age": age, "height": height, "crotch": crotch,"id_number":id_number, "times": [self.date]}
		#store personal data on database -- self.RegisterStatus = [is_new_patient, patient_data]
		self.RegisterStatus = self.DbManager.save_person_data(self.person)
		#create folders
		self.create_session()
		self.create_data_folder()



	def create_data_folder(self):
		p = self.projectManager.paths['data']

		folder =  p +'/'+ str(self.RegisterStatus[1]['name'])
		print self.RegisterStatus[1]['name']
		if not os.path.exists(folder):
			os.makedirs(folder)

	def create_session(self):
		p = self.projectManager.paths['backup']
		
		folder = p + "/" + str(self.date.year)+'-'+str(self.date.month)+'-'+str(self.date.day)
		session_file = str(self.RegisterStatus[1]['name']) + str(self.date.hour)
		b_session_file = str(self.RegisterStatus[1]['name']) + str(self.date.hour)+"string"
		if not os.path.exists(folder):
			os.makedirs(folder)

		self.filename = folder +  "/" + session_file + ".txt"
		self.filename1 = folder +  "/" + b_session_file + ".txt"
		self.DataWrapper = SessionDataWrapper(self.RegisterStatus[1]["name"], self.filename, self.filename1)
		self.patient_name = self.RegisterStatus[1]["name"]
		print self.RegisterStatus   		

	def clearRegisterStatus(self):
		self.RegisterStatus = [0,{'name':"no data"}]


	def get_sensor_reading(self, speed ="no data" ,
								 heart_rate = "no data",
								 steplength = "no data", 
								 cadence = "no data", 
								 blood_pressure = "no data",
								 imu_head = "no data",
								 imu_torso = "no data"
						   ):
		
		w = {  
              "speed"      : speed, 
              "heart_rate" : heart_rate, 
              "steplength" : steplength,
              "cadence"    : cadence,
              "blood_pressure" : blood_pressure,
			  "imu_head"  : imu_head,
			  "imu_torso" : imu_torso,	
              "timestamp" : datetime.datetime.utcnow()}
		
		s = str(heart_rate)+","+str(imu_head['yaw'])+","+str(imu_head['pitch'])+","+str(imu_head['roll'])+","+str(imu_torso['yaw'])+","+str(imu_torso['pitch'])+","+str(imu_torso['roll'])+"\n\r"
		self.DataWrapper.loadSensorData(w, s)
	#reads serialized data and loads it into the database
	

	def pipe_sensor_data(self):

		f = open(self.filename, 'r')
		for i in range(self.DataWrapper.sensorSize):
		    sensor_reading = pickle.load(f)
		    #print sensor_reading
		    #print self.patient_name
		    #print self.data_handler.date
		    self.DbManager.update_sensor_reading(name = self.patient_name, date=self.DataWrapper.date, sensor_reading=sensor_reading)

		self.DataWrapper.sensorSize = 0 




class SessionDataWrapper(object):
	def __init__(self, person, backup_file = "backup.csv", file2 = "backup2.csv"):
		
		self.backup_file  = backup_file
		self.backup_file2 = file2
		self.person       = person
		self.date         = datetime.datetime.now()
		self.file         = open(self.backup_file, 'w+')
		self.file2	      =	open(self.backup_file2, 'w+')	
		self.events       = []
		self.wrapped_data = {}
		self.sensorSize   = 0



	def loadSensorData(self, w, s):
		pickle.dump(w, self.file)
		self.file2.write(s)
		self.sensorSize += 1 


	def loadEvent(self, e):
		self.events.append(e)

	def wrapSessionData(self):
		self.wrapped_data = {'patient': self.person, 
                             'date': str(self.date),
                             'sensors': self.sensorBuffer,
                             'events':self.events
                             #'average':self.avrg_data,
                             #'motivation': self.motivation,  
                             #'satisfaction':self.satisfaction   
                             }






class ProjectHandler(object):
	def __init__(self):

		self.paths = {
						'db'  			  : '/db',
						'backup'		  : '/db/backup',
						'data'			  : '/db/data',
						'plugin'		  : '/plugins',
						'gui' 			  : '/plugins/gui',
						'img'             : '/plugins/gui/img',
						'sensorLib'       : '/plugins/lib',
						'robotController' : '/plugin/robotController'						

					 } 
 		#create database client
		self.client = pymongo.MongoClient()
		#get tablet's hostname 
		self.hostname = socket.gethostname()
		#retrieve general info
		self.general = self.client.general.hostnames.find_one({'host':self.hostname})
		#set root address
		self.root = str(self.general['path_lokomat'])
		
		print('-----------setting directory address-------------')
		for i in self.paths:
			print(i +" directory: "+ self.root +self.paths[i])
			self.paths[i] = self.root + self.paths[i] 

		print('-------------------------------------------------')

		def get_root(self):
			return self.root




class DbHandler(object):
	def __init__(self, settings = { 
									'TestMode': True
								  }
				):

		#load settings
		self.settings = settings
		#create database client
		self.client  = pymongo.MongoClient()
		#load database
		if self.settings['TestMode']:
			self.db  = self.client.test_lokomat
		else:
			self.db = self.client.lokomat

	#save personal data into the database
	def save_person_data(self, data):
		is_patient = self.check_patient(data)
		if is_patient:
			return [1, is_patient]
		else:
			logging.debug('saving')
			res = self.db.patients.insert_one(data)
			logging.debug("data saved")
			logging.debug(res)
			return [2, data]



	#compares the incoming patient with existing in the database
	def check_patient(self, patient):
	        #items = ["name", "age", "gender", "height", "times"]
	        p = self.get_all_patients()
	        for a in p:
	        	print a['id_number']
	        	print patient
	        	
	        	if str(a["id_number"]) == str(patient):
	        		print "already in database"
	        		return a
	        return {}

	#returns the patients stored in the database
	def get_all_patients(self):
		return self.db.patients.find()

	#Load complete dataset to the database
	def update_sensor_reading(self, name, date, sensor_reading):
		result = self.db.sessions.update({'patient':name, 'date':str(date)},{'$push':{'sensors':sensor_reading}})
		#print result
		return result

def main():
	
	d = DataManager()
	
	d.register( name = "sergio sierra", age = 21, gender = "male", height = 180, crotch= 0.8, id_number = '1031137228')




if __name__ == '__main__':
	main()




        