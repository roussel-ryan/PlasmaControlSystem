import tkinter as ttk
import logging
import os

from PIL import Image, ImageTk

"""class for controlling individual data labels"""
class _DataLabel:
	def __init__(self,master,loc,var):
		self.x = loc[0]
		self.y = loc[1]

		self.label = ttk.Label(master,textvariable=var,bg='white')
		self.label.place(x=self.x,y=self.y,anchor=ttk.CENTER)

def add_image(filename):
	image = Image.open(filename)
	photo_image = ImageTk.PhotoImage(image)
	label = ttk.Label(image=photo_image)
	label.image = photo_image
	return [photo_image,label]

class ControlDiagram:
	"""Class for displaying plasma source readings in a large diagram"""
	def __init__(self,master):
		self.control_frame =  ttk.Frame(master)
		self.size = {'width':800,'height':654}

		self.logger = logging.getLogger('GUI')

		self.canvas = ttk.Canvas(self.control_frame,**self.size)

		package_path = os.path.dirname(os.path.dirname(__file__))
		self.image_data = {}
		self.image_data_names = ['base','gas','gas_plasma','gas_solenoid','gas_solenoid_plasma']
		for name in self.image_data_names:
			self.image_data[name] = add_image('/images/diagram_'.join((package_path,name)) + '.png')

		self.canvas.create_image(0,0,anchor=ttk.NW,image=self.image_data['base'][0])
		self.canvas.grid()

		self.display_data = {}

		self.display_data['heater_current'] = ttk.StringVar()
		self.display_data['heater_voltage'] = ttk.StringVar()
		self.display_data['discharge_current'] = ttk.StringVar()
		self.display_data['discharge_voltage'] = ttk.StringVar()
		self.display_data['solenoid_current'] = ttk.StringVar()
		self.display_data['solenoid_voltage'] = ttk.StringVar()
		self.display_data['vacuum_pressure'] = ttk.StringVar()

		for name,element in self.display_data.items():
			element.set('----')

		locations = ((418,87),
			(418,135),
			(549,495),
			(549,448),
			(140,618),
			(140,573),
			(360,448)
			)

		#populate the image with data labels
		self.data_labels = []
		self.query_items = {}
		for i,item in enumerate(self.display_data.items()):
			self.data_labels.append(_DataLabel(self.canvas,locations[i],item[1]))
			try:
				self.query_items[item[0].split('_')[0]].append(item[0].split('_')[1])
			except KeyError:
				self.query_items[item[0].split('_')[0]] = [item[0].split('_')[1]]

		self.logger.debug(self.query_items)

	def update(self,data={}):
		for name,item in data.items():
			for item_name,value in item.items():
				full_name = '_'.join([name,item_name])
				self.display_data[full_name].set('{:3.2f}'.format(value))

	def change_diagram(self,new_diagram):
		self.canvas.delete(self.canvas.find_all()[0])
		self.canvas.create_image(0,0,anchor=ttk.NW,image=self.image_data['gas_solenoid'][0])
