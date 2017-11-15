
import os
import time
'''
import imu_sensor as IMU
import ecg_sensor as ECG
'''
if __name__== "__main__":
    import IMU_BNO055_rpi as IMU
    import ecg_sensor as ECG
else:
    import IMU_BNO055_rpi as IMU
    import ecg_sensor as ECG

import threading

class Manager(object):
	
	def __init__(self,
				 imu1_settings = {'port': 0x28, 'sample': 1, 'bus': 1},
				 imu2_settings = {'port': 0x29, 'sample': 1, 'bus': 1},
				 ecg_settings = {'port': 'COM3', 'sample': 1}
				 ):

		self.ECG_ON  = False
		self.IMU1_ON = False
		self.IMU2_ON = False

		self.data = {
		             'ecg': {'hr' : 0},
		 			 'imu1': {'yaw' : 0, 'pitch' : 0,'roll' : 0},
		 			 'imu2': {'yaw' : 0, 'pitch' : 0,'roll' : 0}
					}

		self.imu1_settings = imu1_settings
		self.imu2_settings = imu2_settings
		self.ecg_settings = ecg_settings


	def set_sensors(self, ecg = True, imu1 = True, imu2 = False):

		self.ECG_ON = ecg
		self.IMU1_ON = imu1
		self.IMU2_ON = imu2

		if self.IMU1_ON:
			print ('imu1 created')
			self.imu1 = IMU.ImuHandler(
									  sample = self.imu1_settings['sample'],
									  dev1 = self.imu1_settings['port'],
									  b = self.imu1_settings['bus']
									 )
		if self.IMU2_ON:
			print ('imu2 created')
			self.imu2 = IMU.ImuHandler(
									  sample = self.imu2_settings['sample'],
									  dev1 = self.imu2_settings['port'],
									  b = self.imu2_settings['bus']
									 )
		if self.ECG_ON:
			self.ecg = ECG.EcgSensor(
									  port = self.ecg_settings['port'],
									  sample = self.ecg_settings['sample']
									)


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
		#launch ecg thread
		if self.ECG_ON:
			self.ecg.start()
			threading.Thread(target = self.ecg.process).start()

	def play_sensors(self):

		#start acquiring data
		if self.ECG_ON:
			self.ecg.play()

		
		if self.IMU1_ON:
			self.imu1.play()
			print ('imu1 played')

		
		if self.IMU2_ON:
			self.imu2.play()
			print ('imu2 played')


	def update_data(self):
		if self.ECG_ON:
			ecg = self.ecg.get_data()
			if not ecg:
				ecg = {'hr' : 0}

		else:
			ecg = {'hr' : 0}

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

		self.data = {'ecg': ecg, 'imu1': imu1, 'imu2': imu2 }


	def get_data(self):
         print('data returned : ' + str(self.data))
         return self.data


	def shutdown(self):
		#shutdown Imu
		if self.IMU1_ON:
			self.imu1.shutdown()

		if self.IMU2_ON:
			self.imu2.shutdown()
		#shutdown Ecg
		if self.ECG_ON:
			self.ecg.shutdown()



def main():
	manager = Manager(
					  imu1_settings = {'port': 0x28, 'sample': 1, 'bus': 1},
					  imu2_settings = {'port': 0x29, 'sample': 1, 'bus': 1},
					  ecg_settings = {'port': 'COM3', 'sample': 1}
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

if __name__ == '__main__':
	main()
