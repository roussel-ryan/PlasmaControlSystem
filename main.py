
import logging
import logging.config
import time
import threading
import queue
#import yaml

import numpy as np
import tkinter as ttk

from GUI import app
from ControlSystem import controlSystem

def main():
	logging.basicConfig(level=logging.INFO)

	PIL_logger = logging.getLogger('PIL')
	PIL_logger.setLevel(logging.CRITICAL)
	#logging_level = logging.INFO
	#logger = logging.getLogger(__name__)
	#logger.setLevel(logging_level)

	#ch = logging.StreamHandler()
	#ch.setLevel(logging_level)

	#formatter = logging.Formatter('[%(levelname)s] %(name)s: %(message)s')
	#ch.setFormatter(formatter)

	#logger.addHandler(ch)

	try:
		logging.info('Starting application')
		plasma_controller = controlSystem.PlasmaSourceControl()
		root = ttk.Tk()
		app.PlasmaApp(root,plasma_controller)
		root.mainloop()
	except Exception as e:
		logging.exception(e)
	finally:
		plasma_controller.stop()
		root.destroy()

#def load_logging_config():
#	with open("logging_config.yml", 'r') as stream:
#		try:
#			config = yaml.load(stream)
#		except yaml.YAMLError as exc:
#			print(exc)
#	logging.config.dictConfig(config)
#	PIL_logger = logging.getLogger('PIL')
#	PIL_logger.setLevel(logging.CRITICAL)

if __name__=='__main__':
	main()
