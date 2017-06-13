
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
					
class TDKPowerSupply(Device):
	def __init__(self,device_name,visa_handler,RS485_address = 6):
		Device.__init__(self,device_name)
		self.set_commands = {'voltage':':VOLT {:3.2f}','current':':CURR {:3.2f}'}
		self.get_commands = {'voltage':'MEAS:VOLT?','current':'MEAS:CURR?'}
		self.RS485_address = RS485_address
		self.handler = visa_handler
		
		if self.handler.connection_status:
			self.status = LOCKED
		
		self.unlock()
		
		#clear errors
		self.handler.write('*CLS')
		self.handler.select_RS485_device(self.RS485_address)
		if self.handler.query('OUTP:STAT?') == 'OFF':
			self.logger.info('Turning "{}" on'.format(self.name))
			self.handler.write('OUTP:STAT ON')
		self.check_errors()
		
		
		
		self.set('voltage',0.0)
		self.set('current',0.0)
		
	def set(self,name,value):
		try:
			self.handler.select_RS485_device(self.RS485_address)
			self.send_command(self.handler.write,self.set_commands[name].format(value))
			self.check_errors('set {},{}'.format(name,value))
			#time.sleep(1)
		except visa.VisaIOError as e:
			self.logger.error(e.args[0])
		except KeyError:
			self.logger.error('Incorrect set key for TDKPowerSupply {}'.format(self.name))
		
	def get(self,name):
		try:
			self.handler.select_RS485_device(self.RS485_address)
			var = self.handler.query(self.get_commands[name])
			self.check_errors('get '+name)
		except visa.VisaIOError as e:
			self.logger.error(e.args[0])
		except KeyError:
			self.logger.error('Incorrect get key for TDKPowerSupply {}'.format(self.name))
			var = None
			
		try:
			nVar = float(var)
		except TypeError:
			nVar = var
		return nVar
	
	def check_errors(self,cmd='UNKNOWN'):
		if self.status == ACTIVE:
			error_description = self.send_command(self.handler.query,'SYST:ERR?').split(',')
		else:
			error_description = ['0']
			
		if float(error_description[0]) < 0 :
			#error
			self.logger.error('code:' + error_description[0] + ' ' +error_description[1] + ' in ' + self.name + ' with cmd ' + cmd)
		elif float(error_description[0]) > 0:
			#warning
			self.logger.warning(error_description[1] + ' in ' + self.name)
		else:
			#no error
			pass
		
		
if __name__=='__main__':
	tdk = TDKPowerSupply('tdk_ps','TCPIP0::169.254.223.84::inst0::INSTR')
	tdk.unlock()
	tdk.set('voltage',7.5)
	print(tdk.get('voltage'))
	tdk.set('voltage',5.0)
	print(tdk.get('voltage'))
	tdk.clean()
	