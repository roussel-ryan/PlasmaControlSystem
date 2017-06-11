import tkinter as ttk
import logging

from . import monitors
from . import control_diagram
from . import logging_to_tkinter

class Panel:
	def __init__(self,master):
		self.frame = ttk.Frame(master)
		self.members = {}
		self.query_items = {}
		
	def gather_and_pack(self):
		for name,item in self.members.items():
			item.monitor_frame.pack()
			self.query_items[name.lower()] = []
			for value in item.query_items:
				self.query_items[item.name.lower()].append(value)
		logging.debug(self.query_items)
		
	def update(self,data={}):
		"""
			Updates gui monitors
			Data needs to be in the form of {monitor_name:{attribute,value}}
			members refers to each monitor
		"""
		for object_name,value_dict in data.items():
			try:
				if issubclass(type(self.members[object_name]),monitors.Monitor):
					self.members[object_name].update(value_dict)
			except KeyError:
				pass
					
	
		
class MonitorPanel(Panel):	
	def __init__(self,master):
		Panel.__init__(self,master)
		
		self.heater_monitor = monitors.SetpointMonitor(self.frame,'Heater')
		self.heater_monitor.add_setpoint('Current','A')
		self.heater_monitor.add_setpoint('Voltage','V')
		self.members[self.heater_monitor.name.lower()] = self.heater_monitor
		
		self.discharge_monitor = monitors.SetpointMonitor(self.frame,'Discharge')
		self.discharge_monitor.add_setpoint('Current','A')
		self.discharge_monitor.add_setpoint('Voltage','V')
		self.members[self.discharge_monitor.name.lower()] = self.discharge_monitor
		
		self.solenoid_monitor = monitors.SetpointMonitor(self.frame,'Solenoid')
		self.solenoid_monitor.add_setpoint('Current','A')
		self.solenoid_monitor.add_setpoint('Voltage','V')
		self.members[self.solenoid_monitor.name.lower()] = self.solenoid_monitor
		
		self.gather_and_pack()
	
	def get_input(self):
		self.inputs = {}
		for monitor_name,monitor in self.members.items():
			self.inputs[monitor_name] = {}
			for setpoint_name,setpoint in monitor.members.items():
				val = monitor.get_new_setpoint_value(setpoint_name)
				if val:
					self.inputs[monitor_name][setpoint_name] = val
			
		return self.inputs

class ControlPanel(Panel):
	def __init__(self,master):
		Panel.__init__(self,master)
		self.control = control_diagram.ControlDiagram(self.frame)
		self.members['control_diagram'] = self.control
		for name,item in self.members.items():
			item.control_frame.pack()
		

class InterlockPanel(Panel):
	def __init__(self,master):
		Panel.__init__(self,master)
		self.interlock = monitors.InterlockMonitor(self.frame,'Interlocks')
		self.interlock.add_interlock('Water')
		self.interlock.add_interlock('Low Vac')
		self.interlock.add_interlock('High Vac')
		self.interlock.add_interlock('Comm')
		self.members[self.interlock.name] = self.interlock
		self.gather_and_pack()
		
class BottomButtons(Panel):
	def __init__(self,master):
		Panel.__init__(self,master)
		self.members['Save'] = ttk.Button(self.frame,text='Save',command=self.test)
		self.members['Load'] = ttk.Button(self.frame,text='Load',command=self.test)
		self.members['Apply'] = ttk.Button(self.frame,text='Apply Settings',command=self.test)
		for name,item in self.members.items():
			item.pack(side=ttk.LEFT)

	def test(self):
		logging.debug('click')
		
class LogBox(Panel):
	def __init__(self,master):
		Panel.__init__(self,master)
		st = ttk.Listbox(self.frame,width=70)#,bg='black',fg='white',font=('Ariel',12,'bold'))
		logging_handler = logging_to_tkinter.TextHandler(st)
		logger = logging.getLogger()
		logger.addHandler(logging_handler)
		st.pack()
			
			