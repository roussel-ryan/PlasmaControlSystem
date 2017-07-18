from . import device


class TDKPowerSupply(device.Device):

	def __init__(self, name, visa_connection, RS485_address = 6):
		super().__init__(name)
		self._RS485_address = RS485_address
		self._connection = visa_connection
		self._connection.write('*CLS')
		self._connection.select_RS485_device(self._RS485_address)
		if self._connection.query('OUTP:STAT?') == 'OFF':
			self._logger.info('Turning "{}" on'.format(self.name))
			self._connection.write('OUTP:STAT ON')
		self.set('voltage',0.0)
		self.set('current',0.0)

	@device.Device.first_check_state
	def set(self, name, value):
		if name != 'current' and name != 'voltage':
			assert False
		self._connection.select_RS485_device(self._RS485_address)
		if name == 'voltage':
			self._connection.write(':VOLT {:3.2f}'.format(value))
		elif name == 'current':
			self._connection.write(':CURR {:3.2f}'.format(value))
		self.check_errors()

	@device.Device.first_check_state
	def get(self, name):
		if name != 'current' and name != 'voltage':
			assert False
		self._connection.select_RS485_device(self._RS485_address)
		if name == 'voltage':
			value = self._connection.query('MEAS:VOLT?')
		elif name == 'current':
			value = self._connection.query('MEAS:CURR?')
		self.check_errors()
		return None if value is None else float(value)

	@device.Device.first_check_state
	def check_errors(self):
		# check for device errors
		error_description = self._connection.query('SYST:ERR?')
		if error_description is not None:
			error_description = error_description.split(',')
			if float(error_description[0]) < 0:
				self._logger.error('code: {}'.format(error_description[0]))
				self.set_error()
				return
			if float(error_description[0]) > 0:
				self._logger.warning(error_description[1])
				self.set_error()
				return
		if not self._connection.is_ok():
			self.set_error()



'''


import serial
import visa
import logging
import time
from serial import serialutil
from . import visa_connection
from . import device


class TDKPowerSupply(device.Device):
	def __init__(self, name, visa_connection, RS485_address = 6):
		super().__init__(name)
		self.set_commands = {'voltage':':VOLT {:3.2f}','current':':CURR {:3.2f}'}
		self.get_commands = {'voltage':'MEAS:VOLT?','current':'MEAS:CURR?'}
		self.RS485_address = RS485_address
		self._connection = visa_connection

		#clear errors
		self._connection.write('*CLS')
		self._connection.select_RS485_device(self.RS485_address)
		if self._connection.query('OUTP:STAT?') == 'OFF':
			self._logger.info('Turning "{}" on'.format(self._name))
			self._connection.write('OUTP:STAT ON')
		self.check_errors()



		self.set('voltage',0.0)
		self.set('current',0.0)

	@device.Device.first_check_state
	def set(self,name,value):
		try:
			self._connection.select_RS485_device(self.RS485_address)
			self._connection.write(self.set_commands[name].format(value))
			self.check_errors('set {},{}'.format(name,value))
			#time.sleep(1)
		except visa.VisaIOError as e:
			self._logger.error(e.args[0])
		except KeyError:
			self._logger.error('Incorrect set key for TDKPowerSupply {}'.format(self._name))

	@device.Device.first_check_state
	def get(self,name):
		try:
			self._connection.select_RS485_device(self.RS485_address)
			var = self._connection.query(self.get_commands[name])
			self.check_errors('get '+name)
		except visa.VisaIOError as e:
			self._logger.error(e.args[0])
		except KeyError:
			self._logger.error('Incorrect get key for TDKPowerSupply {}'.format(self._name))
			var = None

		try:
			nVar = float(var)
		except TypeError:
			nVar = var
		return nVar

	def check_errors(self,cmd='UNKNOWN'):
		if self._state == 'ok':
			error_description = self._connection.query('SYST:ERR?')
			if not isinstance(error_description, bool):
			 	error_description = error_description.split(',')
		else:
			error_description = ['0']

		if float(error_description[0]) < 0 :
			#error
			self._logger.error('code:' + error_description[0] + ' ' +error_description[1] + ' in ' + self._name + ' with cmd ' + cmd)
		elif float(error_description[0]) > 0:
			#warning
			self._logger.warning(error_description[1] + ' in ' + self._name)
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
'''
