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

		if not os.path.exists(folder):
			os.makedirs(folder)

		self.filename = folder +  "/" + session_file + ".txt"
		self.DataWrapper = SessionDataWrapper(self.RegisterStatus[1]["name"], self.filename)
		self.patient_name = self.RegisterStatus[1]["name"]
		print self.RegisterStatus   		



	def get_sensor_reading(self, speed ="no data" ,
								 heart_rate = "no data",
								 steplength = "no data", 
								 cadence = "no data", 
								 blood_pressure = "no data",
								 imu_head = "no data",
								 imu_torso = "no data"
						   ):
		w = {  
              "speed" : speed, 
              "heart_rate" : heart_rate, 
              "steplength" : steplength,
              "cadence" : cadence,
              "blood_pressure" : blood_pressure,
			  "imu_head" : imu_head,
			  "imu_torso" : imu_torso,	
              "timestamp" : datetime.datetime.utcnow()   
            }
        #self.data_handler.load_sensor_data(w)



class SessionDataWrapper(object):
	def __init__(self, person, backup_file = "backup.csv"):
		
		self.backup_file = backup_file
		self.person = person
		
		self.file  = open(self.backup_file, 'w+')
		
		self.events = []
		self.wrapped_data = {}



	def loadSensorData(self, w):
		pickle.dump(w, self.file)

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
						'gui' 			  : '/gui',
						'lib' 			  : '/lib',
						'robotController' : '/robotController'
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

	def save_person_data(self, data):
		is_patient = self.check_patient(data)
		if is_patient:
			return [False, is_patient]
		else:
			logging.debug('saving')
			res = self.db.patients.insert_one(data)
			logging.debug("data saved")
			logging.debug(res)
			return [True, data]



	#compares the incoming patient with existing in the database
	def check_patient(self, patient):
	        #items = ["name", "age", "gender", "height", "times"]
	        p = self.get_all_patients()
	        for a in p:
	            if a["name"]==patient["name"]:
	                print "already in database"
	                return a
	        return {}

	#returns the patients stored in the database
	def get_all_patients(self):
		return self.db.patients.find()


def main():
	
	d = DataManager()
	
	d.register( name = "sergio sierra", age = 21, gender = "male", height = 180, crotch= 0.8, id_number = '1031137228')

if __name__ == '__main__':
	main()




        