import tkinter as ttk
import GUI.panel as panel
class PlasmaApp:
	def __init__(self,master,io_queue,controller):
		self.controller = controller

		self.master_frame = ttk.Frame(master)
		self.master_frame.pack()

		logging_panel = panel.LogBox(self.master_frame)
		logging_panel.frame.grid(column=2,row=2)

		control_monitor_frame = ttk.Frame(self.master_frame)

		self.monitor_panel = panel.MonitorPanel(control_monitor_frame)
		self.monitor_panel.frame.grid(column=1,row=1)

		self.interlock_panel = panel.InterlockPanel(control_monitor_frame)
		self.interlock_panel.frame.grid(column=1,row=2)

		self.control_panel = panel.ControlPanel(self.master_frame)
		self.control_panel.frame.grid(column=1,row=1)

		control_monitor_frame.grid(column=2,row=1)

		button_panel = panel.BottomButtons(self.master_frame)
		button_panel.frame.grid(column=1,row=2)

		#define button functionality
		#button_panel.members[''].config(command = lambda: self.plasma_handler.send_user_inputs(monitor_panel))

		#populate system data dict
		self.system_data = {}
		for name,value in self.controller.__dict__.items():
			if not name[0] == '_':
				device_name = name.split('_')[0]
				self.system_data[device_name] = {}

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
		#populate system data for periodic monitoring
		for name,value in self.controller.__dict__.items():
			if not name[0] == '_':
				device_name = name.split('_')[0]
				attribute = name.split('_')[1]
				self.system_data[device_name][attribute] = value
		print(self.system_data)
		self.monitor_panel.update(self.system_data)
		self.interlock_panel.update(self.system_data)
		self.control_panel.update(self.system_data)
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

		self.update_count +=1
		if self.update_count < 10:
			self.master_frame.after(1000,self.update)
