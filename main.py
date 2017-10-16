
import logging
import logging.config
import time
import threading
import queue
import yaml

import numpy as np
import tkinter as ttk

from GUI import app
from ControlSystem import controlSystem

def main():
	master_queue = queue.Queue()
	#make a thread here and start it running
	#thread = ???
	dummy_thread = None
	plasma_controller = controlSystem.PlasmaSourceControl(master_queue,dummy_thread)
	#plasma_controller.start()

	root = ttk.Tk()
	app.PlasmaApp(root,master_queue,plasma_controller)

	root.mainloop()

def load_logging_config():
	with open("logging_config.yml", 'r') as stream:
		try:
			config = yaml.load(stream)
		except yaml.YAMLError as exc:
			print(exc)
	logging.config.dictConfig(config)
	PIL_logger = logging.getLogger('PIL')
	PIL_logger.setLevel(logging.CRITICAL)

if __name__=='__main__':
	main()
