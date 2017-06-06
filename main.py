
import logging
import numpy as np

import tkinter as ttk

from ControlSystem.GUI import panel
from ControlSystem.control import handler

class App:
	def __init__(self,master):
		master_frame = ttk.Frame(master)
		master_frame.pack()
		
		logging_panel = panel.LogBox(master_frame)
		logging_panel.frame.grid(column=2,row=2)
		
		control_monitor_frame = ttk.Frame(master_frame) 
		
		monitor_panel = panel.MonitorPanel(control_monitor_frame)
		monitor_panel.frame.grid(column=1,row=1)
		
		interlock_panel = panel.InterlockPanel(control_monitor_frame)
		interlock_panel.frame.grid(column=1,row=2)
		
		control_panel = panel.ControlPanel(master_frame)
		control_panel.frame.grid(column=1,row=1)
		
		control_monitor_frame.grid(column=2,row=1)
		
		button_panel = panel.BottomButtons(master_frame)
		button_panel.frame.grid(column=1,row=2)
		
		
		
		
		
		button_t = ttk.Button(master,text='True',command = interlock_panel.interlock.members['water'].set_true)
		button_f = ttk.Button(master,text='False',command = interlock_panel.interlock.members['water'].set_false)
		button_inc = ttk.Button(master,text='rand',command =lambda: handler.update_monitor_panel(monitor_panel))
		button_im_change = ttk.Button(master,text='img_change',command =lambda: control_panel.members['control_diagram'].change_diagram(''))
		button_inc.pack()
		button_im_change.pack()
		button_t.pack()
		button_f.pack()
		
		for child in master_frame.winfo_children(): child.grid_configure(padx=5,pady=5)
		
		hand = handler.PlasmaHandler()
		
	def say_hi(self):
		print('Hello')
		
		
def example():
	root = ttk.Tk()
	
	app = App(root)
	root.mainloop()
	
if __name__=='__main__':
	logging.basicConfig(level=logging.DEBUG)
	

	example()

