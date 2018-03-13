from . import QueueManager


class PlasmaChamber(object):
    """ Represents the plasma chamber. """

    def __init__(self):
        self._queue_manager = QueueManager.QueueManager()
        self._setpoints = {
            'solenoid_current': None, 'solenoid_voltage': None,
            'heater_current': None, 'heater_voltage': None,
            'discharge_current': None, 'discharge_voltage': None,
            'chamber_pressure': None
        }

    def stop(self):
        """
        Halts all threads and closes all connections. Must be called before the
        PlasmaChamber object goes out of scope.
        """
        self._queue_manager.stop()

    def get(self, name):
        """
        Name should be one of the following:
        • solenoid_current
        • solenoid_voltage
        • heater_current
        • heater_voltage
        • discharge_current
        • discharge_voltage
        • chamber_pressure
        """
        assert name in ('solenoid_current', 'solenoid_voltage',
        'heater_current', 'heater_voltage', 'discharge_current',
        'discharge_voltage', 'chamber_pressure')
        if name == 'solenoid_current':
            return self._queue_manager.getIntermediateValue('solenoid_current')
        elif name == 'solenoid_voltage':
            return self._setpoints['solenoid_voltage']
        elif name == 'chamber_pressure':
            return self._queue_manager.getIntermediateValue('chamber_pressure')
        elif name == 'heater_current':
            return self._queue_manager.getIntermediateValue('chamber_pressure')
        elif name == 'heater_voltage':
            return self._queue_manager.getIntermediateValue('chamber_pressure')
        elif name == 'discharge_current':
            return self._queue_manager.getIntermediateValue('chamber_pressure')
        elif name == 'discharge_voltage':
            return self._queue_manager.getIntermediateValue('chamber_pressure')
        else:
            return None

    def set(self, name, value):
        """
        Name should be one of the following:
        • solenoid_current
        • solenoid_voltage
        • heater_current
        • heater_voltage
        • discharge_current
        • discharge_voltage
        """
        assert name in ('solenoid_current', 'solenoid_voltage',
        'heater_current', 'heater_voltage', 'discharge_current',
        'discharge_voltage')
        # prevent setting something to a value which it is already set to
        if value == self._setpoints[name]:
            return

        if name == 'solenoid_current':
            self._setpoints['solenoid_current'] = value
            self._queue_manager.addCommand('SET_SOLENOID_CURRENT {}'.format(value))
        elif name == 'solenoid_voltage':
            self._setpoints['solenoid_voltage'] = value
            self._queue_manager.addCommand('SET_SOLENOID_VOLTAGE {}'.format(value))
        elif name == 'heater_current':
            self._setpoints['heater_current'] = value
            self._queue_manager.addCommand('SET_HEATER_CURRENT {}'.format(value))
        elif name == 'heater_voltage':
            self._setpoints['heater_voltage'] = value
            self._queue_manager.addCommand('SET_HEATER_VOLTAGE {}'.format(value))
        elif name == 'discharge_current':
            self._setpoints['discharge_current'] = value
            self._queue_manager.addCommand('SET_DISCHARGE_VOLTAGE {}'.format(value))
        elif name == 'discharge_voltage':
            self._setpoints['discharge_voltage'] = value
            self._queue_manager.addCommand('SET_DISCHARGE_VOLTAGE {}'.format(value))

    def getSetpoint(self, name):
        """
        Name should be one of the following:
        • solenoid_current
        • solenoid_voltage
        • heater_current
        • heater_voltage
        • discharge_current
        • discharge_voltage
        """
        assert name in ('solenoid_current', 'solenoid_voltage',
        'heater_current', 'heater_voltage', 'discharge_current',
        'discharge_voltage')
        return self._setpoints[name]
