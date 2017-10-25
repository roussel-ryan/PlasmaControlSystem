import visa
import logging
import time
import threading
import serial

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

	def __init__(self,address,RS485_enabled=False):

		self.rm = visa.ResourceManager()
		self.address = address
		self.connection_status = False

		if RS485_enabled:
			self.RS485_enabled = True
			self.current_RS485_address = ''

		self.connection_status = self.connect()

	def connect(self):
		try:
			self.inst = self.rm.open_resource(self.address)
			return True
		except visa.VisaIOError as e:

			return False


	def list_resources(self):
		pass

	def write(self,cmd):
		try:
			self.inst.write(cmd)
			return True
		except AttributeError:
			pass
			return False
		except visa.VisaIOError as e:

			return False
		finally:
			self.lock.release()

	def query(self,cmd):
		try:
			return self.inst.query(cmd)
		except AttributeError:
			return False
		except visa.VisaIOError as e:
			return False


	def select_RS485_device(self,RS485_address):
		if self.RS485_enabled:
			if not RS485_address == self.current_RS485_address:
				#self.lock.acquire()
				try:
					self.write('INST:SEL {}'.format(RS485_address))
					self.current_RS485_address = RS485_address
					return True
				except visa.VisaIOError as e:
					return False
				finally:
					#self.lock.release()
					pass
			else:
				return True
		else:
			return False

	def close(self):
		try:
			self.instrument.close()
			return True
		except AttributeError:
			return False
		except visa.VisaIOError as e:
			return False

class ArduinoHandler:
	"""
		ArduinoHandler(port,baud_rate=9600)
		Attributes:
			-

		Methods:
			connect() - attempt to connect to device, if it fails it returns False
			write(cmd) - write cmd to device and return True if it succeeds, False if it does not
			query(cmd) - write cmd to device and read afterwards return read if it succeeds, False if it does not
			close() - close connection
	"""
	def __init__(self,port,baud_rate=9600):
		self._port = port
		self._baud_rate = baud_rate

		self._connect()

	def _connect(self):
		try:
			logging.debug('Connecting to Arduino at Port: {}'.format(self._port))
			self._ser = serial.Serial(self._port,self._baud_rate)
			time.sleep(2)
			logging.debug('Pinging')
			self.query('PING')
			logging.debug('Saw response from arduino')
		except Exception as e:
			logging.exception(e)

	def write(self,cmd):
		self._ser.write(cmd.encode())
		time.sleep(0.1)
		if 'Done' in self._ser.readline():
			pass
		else:
			raise TimeoutError('{} did not execute'.format(cmd))

	def query(self,cmd):
		self._ser.write(b'PING')
		time.sleep(0.1)
		result = self._ser.readline()
		logging.debug(result)
		if not result == '':
			return result
		else:
			raise TimeoutError('{} did not return anything'.format(cmd))

	def close(self):
		self._ser.close()
