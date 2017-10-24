import tkinter as ttk
import logging
import os

from PIL import Image, ImageTk

class Monitor:
	"""class to create a monitor block
		Attributes:
			- monitor_query = list of dict items with variable names and data types
	"""
	def __init__(self,master,name):
		self.master = master
		self.name = name

		self.monitor_frame = ttk.LabelFrame(self.master,text=self.name)
		self.members = {}
		self.query_items = []

		self.logger = logging.getLogger('gui')

class Setpoint:
	""" class to keep track of setpoint and actual value"""
	def __init__(self,name,unit=''):
		self.name = name
		self.unit = unit

		#special display variables
		self.entry_value = ttk.DoubleVar()
		self.entry_value.trace('w',self.set_new_entry)

		self.actual_value = ttk.StringVar()
		self.actual_value.set('----')
		self.display_vars = [self.entry_value, self.actual_value]

		self.new_entry = False

	def set_new_entry(self,*args):
		self.new_entry = True

	def create_gui_elements(self,master):
		self.frame = ttk.Frame(master)

		self.setpoint_description_label = ttk.Label(self.frame,text=self.name)
		self.setpoint_description_label.grid(column=1,row=1)

		self.actual_value_label = ttk.Label(self.frame,textvariable = self.actual_value)
		self.actual_value_label.grid(column=3,row=1)

		#self.target_value_label = ttk.Label(self.frame,textvariable = self.target_value)#text='{:3.2f}'.format(self.target_value))
		#self.target_value_label.grid(column=2,row=1)

		self.setpoint_entry = ttk.Entry(self.frame,width=7,textvariable = self.entry_value)
		self.setpoint_entry.grid(column=4,row=1)

		self.target_value_label = ttk.Label(self.frame,text = self.unit)
		self.target_value_label.grid(column=5,row=1)

	def get_new_entry_value(self):
		if self.new_entry:
			self.new_entry = False
			return self.entry_value.get()
		else:
			return False




class SetpointMonitor(Monitor):
	def __init__(self,master,name):
		Monitor.__init__(self,master,name)

	def update(self,actual_values={}):
		for name,value in actual_values.items():
			try:
				self.members[name].actual_value.set('{:3.2f}'.format(value))
			except KeyError:
				logging.warning(name + ' query_item not found!')
			except TypeError:
				self.members[name].actual_value.set('NaN')

	def add_setpoint(self,setpoint_name,unit=''):
		self.members[setpoint_name.lower()] = Setpoint(setpoint_name,unit)
		self.query_items.append(setpoint_name.lower())
		self.members[setpoint_name.lower()].create_gui_elements(self.monitor_frame)
		self.members[setpoint_name.lower()].frame.pack()

	def get_new_setpoint_value(self,setpoint_name):
		try:
			val = self.members[setpoint_name].get_new_entry_value()
			try:
				nVal = float(val)
			except ValueError:
				nVal = val

			if nVal:
				return nVal
			else:
				return False

		except KeyError:
			logging.warning('Key {1} does not exist in {2}'.format(setpoint_name,self.name))
			return False

class Interlock:
	def __init__(self,name):
		self.name = name
		self.status = False

		self.logger = logging.getLogger('gui')

	def create_gui_elements(self,master):
		self.frame = ttk.Frame(master)
		self.size = {'width':25,'height':25}

		self.canvas = ttk.Canvas(self.frame,**self.size)

		#self.red_light = ttk.PhotoImage(file='images/red_light.gif'
		package_path = os.path.dirname(os.path.dirname(__file__))
		red_light_image = Image.open(package_path + '/GUI/images/red_light.png')
		self.red_light_photo = ImageTk.PhotoImage(red_light_image)
		self.canvas.create_image((12.5,12.5),image=self.red_light_photo,anchor=ttk.CENTER)

		green_light_image = Image.open(package_path + '/GUI/images/green_light.png')
		self.green_light_photo = ImageTk.PhotoImage(green_light_image)
		#self.canvas.create_image((12.5,12.5),image=self.green_light_photo,anchor=ttk.CENTER)

		#self.canvas.create_image(0,0,image=self.red_light,anchor=ttk.NW)
		self.canvas.grid(column=1,row=1)

		self.member_description_label = ttk.Label(self.frame,text=self.name)
		self.member_description_label.grid(column=2,row=1)

		red_label = ttk.Label(image=self.red_light_photo)
		red_label.image = self.red_light_photo

		green_label = ttk.Label(image=self.green_light_photo)
		green_label.image = self.green_light_photo

	def set_false(self):
		self.status = False
		self.canvas.delete(self.canvas.find_all()[0])
		self.canvas.create_image((12.5,12.5),image=self.red_light_photo,anchor=ttk.CENTER)

	def set_true(self):
		self.status = True
		self.canvas.delete(self.canvas.find_all()[0])
		self.canvas.create_image((12.5,12.5),image=self.green_light_photo,anchor=ttk.CENTER)


class InterlockMonitor(Monitor):
	def __init__(self,master,name):
		Monitor.__init__(self,master,name)


	def add_interlock(self,interlock_name):
		self.members[interlock_name.lower()] = Interlock(interlock_name)
		self.query_items.append(interlock_name.lower())
		self.members[interlock_name.lower()].create_gui_elements(self.monitor_frame)
		self.members[interlock_name.lower()].frame.pack(fill=ttk.X)

	def update(self,actual_values={}):
		for name,value in actual_values.items():
			try:
				if value:
					self.members[name].set_true()
				else:
					self.members[name].set_false()
			except KeyError:
				logging.warning('Key {1} does not exist in {2}'.format(setpoint_name,self.name))
