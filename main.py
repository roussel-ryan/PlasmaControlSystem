
import logging
import logging.config
import time
import threading
import queue
import yaml

import numpy as np
import tkinter as ttk

from ControlSystem.GUI import panel
from ControlSystem.control import handler

class App:
	def __init__(self,master,io_queue):
		self.logger = logging.getLogger('main')

		self.logger.info('Starting intialization process')

		self.plasma_handler = handler.PlasmaHandler(io_queue)

		self.master_frame = ttk.Frame(master)
		self.master_frame.pack()

		logging_panel = panel.LogBox(self.master_frame)
		logging_panel.frame.grid(column=2,row=2)

		control_monitor_frame = ttk.Frame(self.master_frame)

		monitor_panel = panel.MonitorPanel(control_monitor_frame)
		monitor_panel.frame.grid(column=1,row=1)

		interlock_panel = panel.InterlockPanel(control_monitor_frame)
		interlock_panel.frame.grid(column=1,row=2)

		control_panel = panel.ControlPanel(self.master_frame)
		control_panel.frame.grid(column=1,row=1)

		control_monitor_frame.grid(column=2,row=1)

		button_panel = panel.BottomButtons(self.master_frame)
		button_panel.frame.grid(column=1,row=2)

		self.plasma_handler.add_panel(monitor_panel)
		self.plasma_handler.add_panel(interlock_panel)
		self.plasma_handler.add_panel(control_panel)
		self.plasma_handler.add_panel(button_panel)

		#define button functionality
		button_panel.members['Apply'].config(command = lambda: self.plasma_handler.send_user_inputs(monitor_panel))



		# button_t = ttk.Button(master,text='True',command = interlock_panel.interlock.members['water'].set_true)
		# button_f = ttk.Button(master,text='False',command = interlock_panel.interlock.members['water'].set_false)
		# button_inc = ttk.Button(master,text='rand',command =lambda: handler.update_monitor_panel(monitor_panel))
		# button_im_change = ttk.Button(master,text='img_change',command =lambda: control_panel.members['control_diagram'].change_diagram(''))
		# button_inc.pack()
		# button_im_change.pack()
		# button_t.pack()
		# button_f.pack()

		for child in self.master_frame.winfo_children(): child.grid_configure(padx=5,pady=5)

		self.update_count = 0
		self.update()


	def update(self):
		"""
			does all the polling for current data,temporarily raises the logger level
			to info to suppress pyvisa debug messages which slow program
		"""

		self.plasma_handler.process_queue()

		#try:
		#	if self.plasma_handler.queue.qsize():
		#		logging.info(self.plasma_handler.queue.get(0,2))
		#		self.plasma_handler.queue.tasks_done()
		#	else:
		#		logging.debug('Queue empty')
		#except:
		#	logging.debug('Queuing error')
		# if self.update_count % 100:
			# t0 = time.time()

		# logger = logging.getLogger()
		# orig_level = logger.getEffectiveLevel()
		# logger.setLevel(logging.INFO)
		# self.handler.update_monitor_panel(self.monitor_panel)
		# logger.setLevel(orig_level)

		# if self.update_count % 100:
			# logging.info('elapsed time for update: {} s'.format(time.time()-t0))

		# self.update_count +=1

		self.master_frame.after(1000,self.update)


def example():
	master_queue = queue.Queue()

	root = ttk.Tk()


	app = App(root,master_queue)

	update_thread = handler.UpdateDevices('UpdateThread',app.plasma_handler.devices,master_queue)
	update_thread.start()

	root.mainloop()

def set_global_logging_level(level):
	for name,logger in logging.Logger.manager.loggerDict.items():
		try:
			logger.setLevel(level)
		except:
			pass
		#print(' '.join((name,str(logger))))

def load_logging_config():
	with open("logging_config.yml", 'r') as stream:
		try:
			config = yaml.load(stream)
		except yaml.YAMLError as exc:
			print(exc)
	logging.config.dictConfig(config)
	set_global_logging_level(logging.INFO)

	PIL_logger = logging.getLogger('PIL')
	PIL_logger.setLevel(logging.CRITICAL)

if __name__=='__main__':
	load_logging_config()
	example()
