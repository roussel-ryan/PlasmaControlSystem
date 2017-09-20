import logging


class Device(object):
	"""
	Representation of a single device in the plasma system
	Handles device interlocks
	
	Attributes:
    	-----------
	name        	= human reference name of device
	_logger     	= object specific logger object
	_state      	= current enable/disable/error status of device


    	Methods:
    	--------
    	lock()		= locks device
    	unlock()   	= unlocks device
    	set_error()   	= sets device status to error 
	
	"""
	def __init__(self, name):
		"""
		Creates device object with name and logger
		"""
		self.name = name
		self._state = 'ok'
		self._logger = logging.getLogger('[Device "{}"]'.format(self.name))

	def lock(self):
		if self._state == 'ok':
			self._state = 'locked'

	def unlock(self):
		if self._state == 'locked':
			self._state = 'ok'

	def set_error(self):
		self._state = 'error'

	@staticmethod
	def first_check_state(method):
		"""
		Decorator for device implementation which checks device status before 
		executing commnad
		"""
		def wrapper(self, *args, **kwargs):
			if self._state == 'ok':
				return method(self, *args, **kwargs)
			elif self._state == 'error' or self._state == 'locked':
				return None
			else:
				assert False
		return wrapper
