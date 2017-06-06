
import serial
import visa
import logging
from serial import serialutil

NO_COMM = 0
LOCKED = 1
ACTIVE = 2


class Device:
	def __init__(self,device_name):
		"""Device super class
			Device(device_name)
			Attributes:
				- device_name = name of device
				- device_state = current state of device
					-States are as follows
						- 0 NO_COMM = currently not communicating
						- 1 LOCKED = communicating but currently interlocked
						- 2 ACTIVE = communicating and not interlocked
					- States are numbered s.t. ACTIVE state can do everything, similar to logging
		"""
		
		self.device_name = device_name
		self.device_status = NO_COMM
	def send_command(self,command):
		"""check current state of device and then 
			if active pass the command on to the inherited send_command method
		"""
		if self.device_status == NO_COMM:
			logging.error('No communication')
			return None
		elif self.device_status == LOCKED:
			logging.error('Device locked, clear interlock before proceeding')
			return None
		else:
			return command

class VISADevice(Device):
	def __init__(self,device_name,

class SerialDevice(Device):
	"""super-class for storing serial configuration data for serial devices"""
	def __init__(self,device_name,device_port):
		Device.__init__(self,device_name)
		self.device_port = device_port
		self.connect()

	def connect(self):
		try:
			self.ser = serial.Serial(self.device_port)
		except serialutil.SerialException:
			self.device_status = NO_COMM
			
	def send_command(self,command_string):
		command = super(Device,SerialDevice,self).send_command(command_string)	
		try:
			self.ser.write(command)
		except serialutil.SerialException:
			self.device_status = NO_COMM
		
	def query(self,query_string):
		try:
			self.ser.write(query_string)
			data = self.ser.read(20)
		except serialutil.SerialException:
			self.device_status = NO_COMM
		return data	

		
class TDKPowerSupply(SerialDevice):
	def __init__(self,device_name,device_port):
		SerialDevice.__init__(self,device_name,device_port)
		self.set_commands = {'voltage':'PV {:3.2f}','current':'PC {:3.2f}'}
		self.get_commands = {'voltage':'MV?','current':'MC?'}

	def set(self,name,value):
		try:
			self.send_command(self.set_command[name].format(value))
		except KeyError:
			logging.error('Incorrect set key for TDKPowerSupply object')
		
	def get(self,name):
		try:
			var = self.query(self.get_commands[name])
		except KeyError:
			logging.error('Incorrect get key for TDKPowerSupply object')
			var = 0.0
		return 0.0
	
	def reset(self):
		self.send_command('RST')
		
		
