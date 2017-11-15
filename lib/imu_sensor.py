import serial
import numpy as np
import time
import threading

class ImuSensor(object):
	def __init__(self, port = 'COM4', br = 9600, print_values = False):
		self.port  = port
		self.baudrate = br
		self.serial = serial.Serial(self.port, self.baudrate)
		self.go_on = False
		self.pause = True
		self.data ={'x': None, 'y': None, 'z': None}
		self.PRINT = print_values

	def process(self):

		while self.go_on:
			if not self.pause:
				try:
					#adquire data
					#print('1')
					data = self.serial.readline()
					#print('2')
					#print(str(data))
					data = str(data)
					data_split = data.split(',')
					#print('3')
					#print(data_split[2])
					#print(data_split[2].rstrip('\\r\\n\''))
					x = float(data_split[0].lstrip('b\''))
					y = float(data_split[1])
					z = float(data_split[2].rstrip('\\r\\n\''))
					#print('4')
					if self.PRINT:
						print(self.data)
					self.data ={'x': x, 'y': y, 'z': z}

				except Exception as e :
					print(e)
					print('no Imu data')

			else:
				time.sleep(1)

		self.serial.close()

	def get_data(self):
		return self.data

	def pause(self):
		self.pause = True

	def play(self):
		self.pause = False

	def start(self):
		self.go_on = True

	def shutdown(self):
		self.go_on = False


def main():
	imu = ImuSensor()
	imu.start()
	imu.play()
	threading.Thread(target = imu.process).start()
	time.sleep(5)
	d = imu.get_data()
	print(d)
	imu.pause()
	imu.shutdown()


if __name__ == '__main__':
	main()
