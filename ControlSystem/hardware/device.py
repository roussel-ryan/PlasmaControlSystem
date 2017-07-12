
import serial
import visa
import logging
import time
from serial import serialutil

from . import handler

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

		self.name = device_name
		self.status = NO_COMM
		self.logger = logging.getLogger('device')


	def send_command(self,command,*args,**kwargs):
		"""check current state of device and then
			if active pass the command on to the inherited send_command method
		"""
		if self.status == NO_COMM:
			self.logger.error('No communication')
			return None
		elif self.status == LOCKED:
			self.logger.error('Device "{}" locked, clear interlock before proceeding'.format(self.name))
			return None
		else:
			return command(*args,**kwargs)

	def unlock(self):
		if self.status > NO_COMM:
			self.status = ACTIVE

	def lock(self):
		if self.status > NO_COMM:
			self.status = LOCKED
