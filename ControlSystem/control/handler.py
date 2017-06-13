
import numpy as np
import logging
import threading
import queue
import time

from ..hardware import device
from ..hardware import handler



class PlasmaHandler:

	"""PlasmaHandler class
		- Stores plasma state variables
		- Receives calls from the GUI for data and plasma state as well as commands for control
		- Sends commands to hardware controlling software and querys hardware control software 
		
		Attributes:
			devices = dictionary of hardware objects for interfacing with
			state = dictonary of state reporting from devices
		
		Queuing: queue commands need to have the following dict form:
			cmd['type'] = <'get'> <'set'> <'return'>
			cmd['device'] = 'device_name'
			cmd['attribute'] = 'attribute_name'
			cmd['value'] = attribute_value
			
			<'get'> = call a get function, get function should add a queue object <'return'> to 
						give the GUI the value
			<'set'> = call a set fucntion, can add to queue to return success status
			<'return'> = added by a <'get'> function of update function to set value in GUI
	"""
	
	def __init__(self,queue):
		"""Initialization:
			create hardware objects
			create self storage for attributes
			send initialization data to GUI
			
		"""
		self.name = 'PlasmaHandler'
		self.logger = logging.getLogger('plasma_handler')
		
		tdk_bank_handler = handler.VISAHandler('TDKPowerSupplies','TCPIP0::169.254.223.84::inst0::INSTR',RS485_enabled=True)
		
		tdk = device.TDKPowerSupply('discharge',tdk_bank_handler) 
		tdk2 = device.TDKPowerSupply('heater',tdk_bank_handler,1)
		tdk.unlock()
		tdk2.unlock()
		self.devices = {'discharge':tdk,'heater':tdk2}
		
		self.panels = []
		
		self.queue = queue	
		
	def process_queue(self):
		self.logger.info('processing queue with length {}'.format(self.queue.qsize()))
		while self.queue.qsize():
			self.logger.debug('Looping thru queue')
			try:
				cmd = self.queue.get(0)
				type = cmd['type']
				device_name = cmd['device_name']
				attribute = cmd['attribute']
				self.logger.debug(cmd)
				
				if type == 'get':
					val = self.devices[device_name].get(attribute)
					self.queue.put({'type':'return','device':device_name,'attribute':attribute,'value': val})
				elif type == 'set':
					self.devices[device_name].set(attribute,cmd['value'])
				elif type == 'return':
					#logging.info('Returning data to GUI {}'.format(cmd))
					for panel in self.panels:
						#logging.info(panel.members)
						panel.update({device_name:{attribute:cmd['value']}})
				else:
					self.logger.warning('Queue command {} of incorrect type'.format(type))
			except KeyError as e:
				self.logger.warning(e.args[0])
			
			except queue.Empty:
				pass
			self.logger.info('Done processing queue')
			self.queue.task_done()
		
		#self.queue.join()
	
	def add_panel(self,panel):
		self.panels.append(panel)
		
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

	def send_user_inputs(self,monitor_panel_object):
		"""get user inputs from interface and send commands to supplies"""
		inputs = monitor_panel_object.get_input()
		for device_name,item in inputs.items():
			for param_name,param_value in item.items():
				try:
					self.queue.put({'type':'set','device_name':device_name,'attribute':param_name,'value':param_value})
				except KeyError:
					self.logger.warning('Device {} does not exist'.format(device_name))
	
	def close(self):
		for name,item in self.power_supplies.items():
			item.clean()
		

class UpdateDevices(threading.Thread):
	def __init__(self,name,devices,queue):
		threading.Thread.__init__(self,name=name)
		self.queue = queue
		self.logger = logging.getLogger('update')
		self.devices = devices
	
	def run(self):
		while True:
			for device_name,device in self.devices.items():
				return_data = self.get_device_data(device)
				try:
					self.queue.put(return_data[0])
					self.queue.put(return_data[1])
				except:
					self.logger.debug('Queue is busy')
			time.sleep(2)
	
	def get_device_data(self,device):
		return [{'type':'return','device_name':device.name,'attribute':'current','value': device.get('current')},\
			{'type':'return','device_name':device.name,'attribute':'voltage','value': device.get('voltage')}]
	
	
