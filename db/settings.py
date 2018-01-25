import pymongo
import database

d = database.DataManager()

a = d.get_settings()

print a['sensor']
'''
c = pymongo.MongoClient()
b = c.test_lokomat.settings.find()

D = {'sensor': {'ecg_sample': 1.0,
			    'use': 'False',
			    'imu_baud': 9600.0,
			    'ecg_baud': 9600.0,
			    'ecg_port': 'COM6',
			    'imu_port': 'COM4',
			    'imu_sample': 1.0},
	
	'robot': {'ip'             : '192.168.1.2',
	          'name'           : 'palin',
	          'port'           :  9559,
	          'UseSpanish'     :  True,
		      'MotivationTime' :  300000000,
		      'use'            :  False			
	         }}
for i in b:
	print i['robot']['ip']
	print i['sensor']['use']
'''
