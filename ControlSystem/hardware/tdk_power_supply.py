import serial
import visa
import logging
import time
from serial import serialutil
from . import handler
from . import device


class TDKPowerSupply(device.Device):
	def __init__(self, name, visa_handler, RS485_address = 6):
		super().__init__(name)
		self.set_commands = {'voltage':':VOLT {:3.2f}','current':':CURR {:3.2f}'}
		self.get_commands = {'voltage':'MEAS:VOLT?','current':'MEAS:CURR?'}
		self.RS485_address = RS485_address
		self.handler = visa_handler

		#clear errors
		self.handler.write('*CLS')
		self.handler.select_RS485_device(self.RS485_address)
		if self.handler.query('OUTP:STAT?') == 'OFF':
			self.logger.info('Turning "{}" on'.format(self._name))
			self.handler.write('OUTP:STAT ON')
		self.check_errors()



		self.set('voltage',0.0)
		self.set('current',0.0)

	@device.Device.first_check_state
	def set(self,name,value):
		try:
			self.handler.select_RS485_device(self.RS485_address)
			self.handler.write(self.set_commands[name].format(value))
			self.check_errors('set {},{}'.format(name,value))
			#time.sleep(1)
		except visa.VisaIOError as e:
			self.logger.error(e.args[0])
		except KeyError:
			self.logger.error('Incorrect set key for TDKPowerSupply {}'.format(self._name))

	@device.Device.first_check_state
	def get(self,name):
		try:
			self.handler.select_RS485_device(self.RS485_address)
			var = self.handler.query(self.get_commands[name])
			self.check_errors('get '+name)
		except visa.VisaIOError as e:
			self.logger.error(e.args[0])
		except KeyError:
			self.logger.error('Incorrect get key for TDKPowerSupply {}'.format(self._name))
			var = None

		try:
			nVar = float(var)
		except TypeError:
			nVar = var
		return nVar

	def check_errors(self,cmd='UNKNOWN'):
		if self._state == 'ok':
			error_description = self.handler.query('SYST:ERR?')
			if not isinstance(error_description, bool):
			 	error_description = error_description.split(',')
		else:
			error_description = ['0']

		if float(error_description[0]) < 0 :
			#error
			self.logger.error('code:' + error_description[0] + ' ' +error_description[1] + ' in ' + self._name + ' with cmd ' + cmd)
		elif float(error_description[0]) > 0:
			#warning
			self.logger.warning(error_description[1] + ' in ' + self._name)
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
