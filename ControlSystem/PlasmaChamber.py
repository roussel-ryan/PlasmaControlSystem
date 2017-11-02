from . import QueueManager


class PlasmaChamber(object):

    def __init__(self):
        self._queue_manager = QueueManager.QueueManager()
        self._setpoints = {
            'solenoid_current': None, 'solenoid_voltage': None,
            'heater_current': None, 'heater_voltage': None,
            'discharge_current': None, 'discharge_voltage': None,
            'chamber_pressure': None
        }

    def stop(self):
        self._queue_manager.stop()

    def get(self, name):
        assert name in ('solenoid_current', 'solenoid_voltage',
        'heater_current', 'heater_voltage', 'discharge_current',
        'discharge_voltage', 'chamber_pressure')
        if name == 'solenoid_current':
            return self._queue_manager.getState('solenoid_current')
        elif name == 'solenoid_voltage':
            return self._setpoints['solenoid_voltage']
        elif name == 'chamber_pressure':
            return self._queue_manager.getState('chamber_pressure')
        else:
            return None

    def set(self, name, value):
        assert name in ('solenoid_current', 'solenoid_voltage',
        'heater_current', 'heater_voltage', 'discharge_current',
        'discharge_voltage')
        if value == self._setpoints[name]:
            return
        if name == 'solenoid_current':
            self._setpoints['solenoid_current'] = value
            self._queue_manager.addCommand('SET_SOLENOID_CURRENT {}'.format(value))
        elif name == 'solenoid_voltage':
            self._setpoints['solenoid_voltage'] = value
            self._queue_manager.addCommand('SET_SOLENOID_VOLTAGE {}'.format(value))

    def getSetpoint(self, name):
        assert name in ('solenoid_current', 'solenoid_voltage',
        'heater_current', 'heater_voltage', 'discharge_current',
        'discharge_voltage', 'chamber_pressure')
        return self._setpoints[name]
