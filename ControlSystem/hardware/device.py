
import serial
import visa
import logging
import time
from serial import serialutil

NO_COMM = 0
LOCKED = 1
ACTIVE = 2

rm = visa.ResourceManager()

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
	def send_command(self,command,*args,**kwargs):
		"""check current state of device and then 
			if active pass the command on to the inherited send_command method
		"""
		if self.status == NO_COMM:
			logging.error('No communication')
			return None
		elif self.status == LOCKED:
			logging.error('Device locked, clear interlock before proceeding')
			return None
		else:
			return command(*args,**kwargs)
	
	def unlock(self):
		if self.status > NO_COMM:
			self.status = ACTIVE
	
	def lock(self):
		if self.status > NO_COMM:
			self.status = LOCKED

class VISAHandler:
	"""
		VISAHandler(address,RS485_enabled=False)
		Attributes:
			- rm = resource manager object
			- inst = visa instrument object
			- current_RS485_address = current RS485 address if RS485_enabled = True
		
		Methods:
			connect() - attempt to connect to device, if it fails it returns False
			list_resources() - utility function showing avalible resources
			write(cmd) - write cmd to device and return True if it succeeds, False if it does not
			query(cmd) - write cmd to device and read afterwards return read if it succeeds, False if it does not
			select_RS485_device(RS485_address) - change to device with RS485_address as the address
			close() - close resource
	"""
	
	def __init__(self,address='',RS485_enabled=False):
		self.rm = visa.ResourceManager()
		self.address = address
		
		if RS485_enabled:
			self.RS485_enabled = True
			self.current_RS485_address = ''
		
		self.connect()
		
	def connect(self):
		if not self.address == '':
			try:
				self.inst = self.rm.open_resource(self.address)
				return True
			except visa.VisaIOError as e:
				logging.error(e.arg[0])
				return False
		else:
			logging.error('No address specified')
			return False
	
	def list_resources(self):
		logging.info(self.rm.list_resources())
		
	def write(self,cmd):
		try:
			self.inst.write(cmd)
			return True
		except AttributeError:
			logging.error('Resource was not connected')
			return False
		except visa.VisaIOError as e:
			logging.error(e.arg[0])
			return False	
	
	def query(self,cmd):
		try:
			return self.inst.query(cmd)
		except AttributeError:
			logging.error('Resource was not connected')
			return False
		except visa.VisaIOError as e:
			logging.error(e.arg[0])
			return False
	
	def select_RS485_device(self,RS485_address):			
		if self.RS485_enabled:
			if not RS485_address == self.current_RS485_address:
				self.write('INST:SEL {}'.format(RS485_address))
	
	def close(self):
		try:
			self.instrument.close()
			return True
		except AttributeError:
			logging.error('Resource was not connected')
			return False
		except visa.VisaIOError as e:
			logging.error(e.arg[0])
			return False
					
class TDKPowerSupply(Device):
	def __init__(self,device_name,visa_handler,device_RS485_address = 6):
		Device.__init__(self,device_name)
		self.set_commands = {'voltage':':VOLT {:3.2f}','current':':CURR {:3.2f}'}
		self.get_commands = {'voltage':'MEAS:VOLT?','current':'MEAS:CURR?'}
		self.RS485_address = device_RS485_address
		self.handler = visa_handler
		
		self.unlock()
		
		#clear errors
		self.handler.write('*CLS')
		
		if self.handler.query('OUTP:STAT?') == 'OFF':
			logging.info('Turning device on')
			self.handler.write('OUTP:STAT ON')
		self.check_errors()
		
		self.set('voltage',0.0)
		self.set('current',0.0)
	def set(self,name,value):
		try:
			self.send_command(self.handler.write,self.set_commands[name].format(value))
			self.check_errors('set {},{}'.format(name,value))
			#time.sleep(1)
		except KeyError:
			logging.error('Incorrect set key for TDKPowerSupply object')
		
	def get(self,name):
		try:
			var = self.handler.query(self.get_commands[name])
			self.check_errors('get '+name)
		except KeyError:
			logging.error('Incorrect get key for TDKPowerSupply object')
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
			logging.error('code:' + error_description[0] + ' ' +error_description[1] + ' in ' + self.name + ' with cmd ' + cmd)
		elif float(error_description[0]) > 0:
			#warning
			logging.warning(error_description[1] + ' in ' + self.name)
		else:
			#no error
			logging.debug('No error')
		
		
if __name__=='__main__':
	tdk = TDKPowerSupply('tdk_ps','TCPIP0::169.254.223.84::inst0::INSTR')
	tdk.unlock()
	tdk.set('voltage',7.5)
	print(tdk.get('voltage'))
	tdk.set('voltage',5.0)
	print(tdk.get('voltage'))
	tdk.clean()
	