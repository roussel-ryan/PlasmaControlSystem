import logging
import threading
import queue
import time


from ..hardware import device
from ..hardware import visa_connection
from ..hardware import tdk_power_supply
from ..hardware import solenoid_power_supply


class PlasmaDeviceManager(object):

	def __init__(self):
		self.name = 'PlasmaHandler'
		self._logger = logging.getLogger('PlasmaHandler')
		self._devices = {}
		self._devices_lock = threading.Lock()
		self._panels = []
		self._queue = queue.Queue()
		self._update_thread = threading.Thread(target=self.update_thread_run, name='update thread')

		self._logger.info('\033[32mConnecting to TDK Power Supply Bank\033[0m')
		tdk_bank_connection = visa_connection.VisaConnection('TDKPowerSupplies', 'TCPIP0::169.254.223.84::inst0::INSTR', True)
		self._devices['discharge'] = tdk_power_supply.TDKPowerSupply('discharge', tdk_bank_connection, 6)
		self._devices['heater'] = tdk_power_supply.TDKPowerSupply('heater', tdk_bank_connection, 1)

		self._logger.info('\033[32mConnecting to Solenoid Power Supply\033[0m')
		self._devices['solenoid'] = solenoid_power_supply.SolenoidPowerSupply('solenoid')
		foo = solenoid_power_supply.SolenoidPowerSupply('bah')


	def start(self):
		self._logger.info('\033[32mSpinning up Update Thread\033[0m')
		self._update_thread.start()

	def update_thread_run(self):
		while True:
			with self._devices_lock:
				for device_name, device in self._devices.items():
					self._queue.put({
						'type': 'return',
						'device_name': device_name,
						'attribute': 'current',
						'value': device.get('current')
					})
					self._queue.put({
						'type': 'return',
						'device_name': device_name,
						'attribute': 'voltage',
						'value': device.get('voltage')
					})
			time.sleep(1)

	def process_queue(self):
		while self._queue.qsize():
			try:
				command = self._queue.get(0)
				#if command['type'] == 'get':
				#	value = self._devices[command['device_name']].get(command['attribute'])
				#	self._queue.put({'type': 'return','device': command['device_name'],'attribute': command['attribute'],'value': value})
				if command['type'] == 'set':
					with self._devices_lock:
						print("setting: ", command['device_name'], command['attribute'], command['value'])
						self._devices[command['device_name']].set(command['attribute'], command['value'])
				elif command['type'] == 'return':
					for panel in self._panels:
						panel.update({command['device_name']: {command['attribute']: command['value']}})
				else:
					assert False
			except queue.Empty:
				self._queue.task_done()

	def add_panel(self, panel):
		self._panels.append(panel)

	def send_user_inputs(self,monitor_panel_object):
		inputs = monitor_panel_object.get_input()
		for device_name, item in inputs.items():
			for param_name,param_value in item.items():
				self._queue.put({'type':'set','device_name':device_name,'attribute':param_name,'value':param_value})

'''
	def update_monitor_panel(self,monitor_panel_object):
		"""Handle updating the monitor panel values for display
			send the panel a dict with the same shape but replace the var name with dict {var_name:value}
		"""
		self.monitor_panel_data = {}
		for device_ID,device_obj in self.power_supplies.items():
			if device_obj.status == device.ACTIVE:
				self.queue.put({'type':'return','device_name':device_name,'attribute':'current','value':None})
				self.queue.put({'type':'return','device_name':device_name,'attribute':'voltage','value':None})


	def update_diagram_panel(self,diagram_panel_object):
		self.diagram_panel_data = {}
		for device_ID,device in self.power_supplies.items():
			self.diagram_panel_data[device_ID] = {}
			self.diagram_panel_data[device_ID]['current'] = device.get('current')
			self.diagram_panel_data[device_ID]['voltage'] = device.get('voltage')
			self.diagram_panel_data[device_ID]['pressure'] = device.get('pressure')
		diagram_panel_object.update(self.diagram_panel_data)


	def update_interlock_panel(self,interlock_panel_object):
		self.interlock_panel_data = {}
		for device_ID,device in self.interlock_devices.items():
			self.interlock_panel_data[device_ID]['status'] = device.query('STATUS')


	def close(self):
		for name,item in self.power_supplies.items():
			item.clean()
'''
