from . import QueueManager


class PlasmaChamber(object):

    def __init__(self):
        self._queue_manager = QueueManager.QueueManager()
        self.solenoid_current_setpoint = None

    def stop(self):
        self._queue_manager.stop()

    @property
    def solenoid_current(self):
        return self._queue_manager.get_state('solenoid_current')

    @solenoid_current.setter
    def solenoid_current(self, value):
        self.solenoid_current_setpoint = value
        self._queue_manager.add_command('SET_SOLENOID_CURRENT {}'.format(value))
