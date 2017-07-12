import logging


class Device(object):

	def __init__(self, name):
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
		def wrapper(self, *args, **kwargs):
			if self._state == 'ok':
				return method(self, *args, **kwargs)
			elif self._state == 'error' or self._state == 'locked':
				return None
			else:
				assert False
		return wrapper
