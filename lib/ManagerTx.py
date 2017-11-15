
print('enter')

import os
import time

if __name__== "__main__":
    import ecg_sensor as ECG
else:
    import lib.ecg_sensor as ECG

import threading
import serial




class ManagerRx(object):

	def __init__(self, settings = {
									'joy_port'  : 'COM4',
									'imu_port'  : 'COM5',
									'ecg_port'  : 'COM6',
									'joy_sample': 0.1,
									'imu_sample': 1,
									'joy_baud'  : 9600,
									'imu_baud'  : 9600,
									'ecg_sample': 1
						           } 
				):
		
		print(settings)

		self.settings = settings

		self.JOY_ON = True
		self.IMU_ON = True
		self.ECG_ON = True

		self.joySerial = None
		self.imuSerial = None

		self.joy_function  =  None
		self.imu_function = None

		self.data   = {
						'joy'  : 0,
						'ecg'  : {'hr' : 0},
			 			'imu1' : {'yaw' : 0, 'pitch' : 0,'roll' : 0},
			 			'imu2' : {'yaw' : 0, 'pitch' : 0,'roll' : 0}
		 			  }

	def set_sensors(self, imu = False, joy = False, ecg = False):
		
		self.JOY_ON = joy
		self.IMU_ON = imu
		self.ECG_ON = ecg
		
		if self.JOY_ON:
			print('open joy port')
			self.joySerial = serial.Serial(self.settings['joy_port'], self.settings['joy_baud'], timeout = 1)
			time.sleep(3)

			'''
			while self.joySerial.in_waiting:	
				a = self.joySerial.read()
				print('set sensors')
				print(a)
			'''
		if self.IMU_ON:
			
			print('open imu port')
			self.imuSerial = serial.Serial(self.settings['imu_port'], self.settings['imu_baud'], timeout = 1)
			time.sleep(3)
			'''
			self.imuSerial = serial.Serial(self.settings['imu_port'], self.settings['imu_baud'])
			self.imuThread = threading.Thread(target = self.imu_thread)
			'''

		if self.ECG_ON:
			self.ecg = ECG.EcgSensor(
									  port   = self.settings['ecg_port'],
									  sample = self.settings['ecg_sample']
									)
			self.ecg.play()
			self.ecgThread = threading.Thread(target = self.ecg_thread) 


	def joy_gui_bind(self, f):
		self.joy_function = f

	def imu_gui_bind(self, f):
		self.imu_function = f	


	def imu_thread(self):

		if self.imuSerial:
			self.imuSerial.write('A')
			time.sleep(1)
			s = self.imuSerial.read()
			print('response recieved:')
			print(s)
			c = 0
			while not(s == "B"):
				s = self.imuSerial.read()
				c = c + 1
				if c > 10:
					c = 00
					self.IMU_ON	 = False
					break
				time.sleep(self.settings['imu_sample'])

			while self.IMU_ON:
				self.imuSerial.write("A")
				s = self.imuSerial.readline()
				d = s.split(",")
				print(d)
				#read and process data
				if len(d) == 6:
					imu1 = {'yaw' : d[2], 'pitch' : d[0], 'roll' : d[1]}
					imu2 = {'yaw' : d[5], 'pitch' : d[3], 'roll' : d[4]}
					self.data['imu1'] = imu1
					self.data['imu2'] = imu2
				
				else:
					continue

				print(self.data)
				#run the bind callback function of the interface
				if self.imu_function:	
					self.imu_function(self.data)
				
				time.sleep(self.settings['imu_sample'])

			self.imuSerial.write("C")
			time.sleep(1)
			self.imuSerial.close()
			print('going out...imu thread')




	def joy_thread(self):
		
		if self.joySerial:
			print('sending signal')

			self.joySerial.write("A")
			time.sleep(1)
			print('waiting response')
			#if self.joySerial.in_waiting:
			s = self.joySerial.read()
			print('response recieved:')
			print(s)
			c  = 0
			while not(s == "B"):
				s = self.joySerial.read()
				c = c + 1
				if c > 10:
					c = 00
					self.JOY_ON = False
					break
				time.sleep(self.settings['joy_sample'])

			print('pass') 

			while self.JOY_ON:
				self.joySerial.write("A")
				s = self.joySerial.read()
				self.data['joy'] = s
				print(self.data)
				if self.joy_function:	
					self.joy_function(self.data)
				time.sleep(self.settings['joy_sample'])


			print('going out...joy thread')
			

	'''
	def imu_thread(self):
		
		while self.IMU_ON:
		
			s = self.imuSerial.read()
			print(s)
			d = s.split(',')

			if d.len() == 6:
				imu1 = {'yaw' : d[0], 'pitch' : d[1], 'roll' : d[2]}
				imu2 = {'yaw' : d[3], 'pitch' : d[4], 'roll' : d[5]}
				self.data['imu1'] = imu1
				self.data['imu2'] = imu2
			
			else:
				continue	
			
			time.sleep(self.settings['imu_sample'])
	'''		

	def get_data(self):
		return self.data	

	def ecg_thread(self):

		while self.ECG_ON:
			ecg = self.ecg.get_data()
			if not ecg:
				ecg = {'hr' : 0}
			self.data['ecg'] = ecg
			time.sleep(self.settings['ecg_sample'])


	def launchJoyThread(self):
		self.joyThread = threading.Thread(target = self.joy_thread)
		self.joyThread.start()


	def launchSensorsThread(self):
		
		if self.IMU_ON:
			self.imuThread.start()
		
		if self.ECG_ON:
			self.ecgThread.start()


	def joy_shutdown(self):
		if self.joySerial.is_open:
			self.joySerial.write("C")
			

		self.JOY_ON = False


	def imu_shutdown(self):
		
		self.IMU_ON = False



	def ecg_shutdown(self):
		
		self.ECG_ON = False	


	def shutdown(self):
		
		self.joy_shutdown()
		if self.joySerial:
			self.joySerial.close()
		self.imu_shutdown()
		self.ecg_shutdown()




class ManagerTx(object):
	def __init__(self,
				 imu1_settings = {'port': 0x28, 'sample': 1, 'bus': 1},
				 imu2_settings = {'port': 0x29, 'sample': 1, 'bus': 1},
				 imu_port      = "/dev/ttyAMA0",
				 imu_baud      = 9600
				 ):

		self.IMU1_ON = False
		self.IMU2_ON = False

		self.data = {
		 			 'imu1': {'yaw' : 0, 'pitch' : 0, 'roll' : 0},
		 			 'imu2': {'yaw' : 0, 'pitch' : 0, 'roll' : 0}
					}
		
		self.imu1_settings = imu1_settings
		self.imu2_settings = imu2_settings
		
		self.imu_port = imu_port
		self.imu_baud = imu_baud

		self.READ = 0x0A
		self.NOREAD  = 0x0B


	def set_sensors(self,  imu1 = True, imu2 = False):

		
		self.IMU1_ON = imu1
		self.IMU2_ON = imu2

		if self.IMU1_ON:
			print ('imu1 created')
			self.imu1 = IMU.ImuHandler(
									  sample = self.imu1_settings['sample'],
									  dev1   = self.imu1_settings['port'],
									  b      = self.imu1_settings['bus']
									 )
		if self.IMU2_ON:
			print ('imu2 created')
			self.imu2 = IMU.ImuHandler(
									  sample = self.imu2_settings['sample'],
									  dev1   = self.imu2_settings['port'],
									  b      = self.imu2_settings['bus']
									 )

		#open ports
		self.imuSerial = serial.Serial(self.imu_port, baudrate = self.imu_baud)


	def launch_sensors(self):
		#launch imu thread
		if self.IMU1_ON:
			self.imu1.launch_thread()
			#threading.Thread(target = self.imu.process).start()
			print ('imu started and launched')

		if self.IMU2_ON:
			self.imu2.launch_thread()
			#threading.Thread(target = self.imu.process).start()
			print ('imu started and launched')
		
	
	def play_sensors(self):
		#start acquiring data
		if self.IMU1_ON:
			self.imu1.play()
			print ('imu1 played')

		if self.IMU2_ON:
			self.imu2.play()
			print ('imu2 played')


	def update_data(self):
		
		if self.IMU1_ON:
			imu1 = self.imu1.get_data()
			if not imu1:
				imu1 = {'yaw' : 0, 'pitch' : 0, 'roll' : 0}
			#print 'imu data updated: ' + str(imu)
		else:
			imu1 = {'yaw' : 0, 'pitch' : 0, 'roll' : 0}

		if self.IMU2_ON:
			imu2 = self.imu2.get_data()
			if not imu2:
				imu2 = {'yaw' : 0, 'pitch' : 0, 'roll' : 0}
			#print 'imu data updated: ' + str(imu)
		else:
			imu2 = {'yaw' : 0, 'pitch' : 0, 'roll' : 0}

		self.data['imu1'] = imu1
		self.data['imu2'] = imu2


	def get_data(self):
         print('data returned : ' + str(self.data))
         return self.data

	
	def shutdown(self):
		#shutdown Imu
		if self.IMU1_ON:
			self.imu1.shutdown()

		if self.IMU2_ON:
			self.imu2.shutdown()
	

def main():
	manager = Manager(
					  imu1_settings  = {'port': 0x28, 'sample': 1, 'bus': 1},
					  imu2_settings  = {'port': 0x29, 'sample': 1, 'bus': 1},
					  ecg_settings   = {'port': 'COM3', 'sample': 1}
					  )

	manager.set_sensors(ecg = False, imu1 = True, imu2 = True )
	manager.launch_sensors()
	manager.play_sensors()
	print('waiting...')
	time.sleep(5)
	for i in range(10):
		manager.update_data()
		d = manager.get_data()
		print (d)
		time.sleep(1)

	manager.shutdown()

def testRXman():

	a = True
	print('manager create')
	m = ManagerRx(settings = {
								'joy_port'  : 'COM9',
								'imu_port'  : 'COM4',
								'ecg_port'  : 'COM6',
								'joy_sample': 0.1,
								'imu_sample': 1,
								'joy_baud'  : 9600,
								'imu_baud'  : 9600,
								'ecg_sample': 1
						      }
				 )
	print('setting sensors')
	m.set_sensors(imu = False, ecg = False, joy = True)

	print('launch joy thread')
	m.launchJoyThread()

	try:
		while a:
			time.sleep(1)
	except KeyboardInterrupt:
		print('keyboard exception')
		a = False
		m.joy_shutdown()

	m.launchJoyThread()

	try:
		while a:
			time.sleep(1)
	except KeyboardInterrupt:
		print('keyboard exception')
		a = False
		m.joy_shutdown()

	m.shutdown()	
		



if __name__ == '__main__':
	testRXman()
	

