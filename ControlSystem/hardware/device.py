
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

class VISADevice(Device):
	def __init__(self,device_name,device_port):
		Device.__init__(self,device_name)
		self.port = device_port
		
		self.connect(self.port)
		self.check_connection()
	
	def check_connection(self):
		"""
			check connection to device by sending a test
		"""
		try:
			self.instrument.write('w')
			self.status = LOCKED
		except AttributeError:
			logging.warning('Check_connection failed, device {} does not exist due to no connection'.format(self.name))
		except visa.VisaIOError as e:
			logging.warning(e.args[0])
			self.status = NO_COMM
			
	def connect(self,port):
		"""
			Attempt a connection to the device
		"""
		try:
			rm = visa.ResourceManager()
			self.instrument = rm.get_instrument(port)
			self.status = LOCKED
		except visa.VisaIOError as e:
			logging.warning('Connection to device {} failed '.format(self.name) + e.args[0])
			self.status = NO_COMM
		#del(rm)
	
	def write(self,cmd):
		try:
			self.send_command(self.instrument.write,cmd)
		except visa.VisaIOError as e:
			logging.error(e.args[0])
		except AttributeError:
			logging.warning('Write cmd failed, device {} does not exist due to no connection'.format(self.name))
	
			
	def query(self,cmd):
		try:
			ret = self.send_command(self.instrument.query,cmd)
		except visa.VisaIOError as e:
			logging.error(e.args[0])
			ret = None
		except AttributeError:
			logging.warning('Query cmd failed, device {} does not exist due to no connection'.format(self.name))
			ret = None
			
		return ret
		
	def clean(self):
		self.instrument.close()
		
		
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
			self.status = NO_COMM
			
	def send_command(self,command_string):
		command = super(Device,SerialDevice,self).send_command(command_string)	
		try:
			self.ser.write(command)
		except serialutil.SerialException:
			self.status = NO_COMM
		
	def query(self,query_string):
		try:
			self.ser.write(query_string)
			data = self.ser.read(20)
		except serialutil.SerialException:
			self.status = NO_COMM
		return data

				
class TDKPowerSupply(VISADevice):
	def __init__(self,device_name,device_port):
		VISADevice.__init__(self,device_name,device_port)
		self.set_commands = {'voltage':':VOLT {:3.2f}',':CURR':'PC {:3.2f}'}
		self.get_commands = {'voltage':'MEAS:VOLT?','current':'MEAS:CURR?'}
		
	def set(self,name,value):
		try:
			logging.info(value)
			self.send_command(self.write,self.set_commands[name].format(value))
			#time.sleep(1)
		except KeyError:
			logging.error('Incorrect set key for TDKPowerSupply object')
		
	def get(self,name):
		try:
			var = self.query(self.get_commands[name])
		except KeyError:
			logging.error('Incorrect get key for TDKPowerSupply object')
			var = None
		return float(var)
	
	def reset(self):
		self.send_command('RST')
		
		
if __name__=='__main__':
	tdk = TDKPowerSupply('tdk_ps','TCPIP0::169.254.223.84::inst0::INSTR')
	tdk.unlock()
	tdk.set('voltage',7.5)
	print(tdk.get('voltage'))
	tdk.set('voltage',5.0)
	print(tdk.get('voltage'))
	tdk.clean()
	