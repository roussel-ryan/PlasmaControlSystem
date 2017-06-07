
import logging
import numpy as np

import tkinter as ttk

from ControlSystem.GUI import panel
from ControlSystem.control import handler

class App:
	def __init__(self,master):
		
		self.handler = handler.PlasmaHandler()
		
		self.master_frame = ttk.Frame(master)
		self.master_frame.pack()
		
		logging_panel = panel.LogBox(self.master_frame)
		logging_panel.frame.grid(column=2,row=2)
		
		control_monitor_frame = ttk.Frame(self.master_frame) 
		
		self.monitor_panel = panel.MonitorPanel(control_monitor_frame)
		self.monitor_panel.frame.grid(column=1,row=1)
		
		interlock_panel = panel.InterlockPanel(control_monitor_frame)
		interlock_panel.frame.grid(column=1,row=2)
		
		control_panel = panel.ControlPanel(self.master_frame)
		control_panel.frame.grid(column=1,row=1)
		
		control_monitor_frame.grid(column=2,row=1)
		
		button_panel = panel.BottomButtons(self.master_frame)
		button_panel.frame.grid(column=1,row=2)
		
		#define button functionality
		button_panel.members['Apply'].config(command = lambda: self.handler.power_supplies['discharge'].set('voltage',self.monitor_panel.members['discharge'].get_setpoint('voltage')))
		
		
		
		# button_t = ttk.Button(master,text='True',command = interlock_panel.interlock.members['water'].set_true)
		# button_f = ttk.Button(master,text='False',command = interlock_panel.interlock.members['water'].set_false)
		# button_inc = ttk.Button(master,text='rand',command =lambda: handler.update_monitor_panel(monitor_panel))
		# button_im_change = ttk.Button(master,text='img_change',command =lambda: control_panel.members['control_diagram'].change_diagram(''))
		# button_inc.pack()
		# button_im_change.pack()
		# button_t.pack()
		# button_f.pack()
		
		for child in self.master_frame.winfo_children(): child.grid_configure(padx=5,pady=5)
		
		self.update()
		
	def update(self):
		"""
			does all the polling for current data
		"""
		self.handler.update_monitor_panel(self.monitor_panel)
		self.master_frame.after(10,self.update)
		
		
def example():
	root = ttk.Tk()
	
	app = App(root)
	root.mainloop()
	
if __name__=='__main__':
	logging.basicConfig(level=logging.INFO)
	#handler = handler.PlasmaHandler()
	#handler.close()
	example()

