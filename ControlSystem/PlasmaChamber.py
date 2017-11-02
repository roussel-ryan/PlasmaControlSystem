from . import QueueManager


class PlasmaChamber(object):

    def __init__(self):
        self._queue_manager = QueueManager.QueueManager()
        self._solenoid_current_setpoint = None

    def stop(self):
        self._queue_manager.stop()

    @property
    def solenoid_current(self):
        return self._queue_manager.get_state('solenoid_current')

    @solenoid_current.setter
    def solenoid_current(self, value):
        self._solenoid_current_setpoint = value
        self._queue_manager.add_command('SET_SOLENOID_CURRENT {}'.format(value))

    @property
    def solenoid_current_setpoint(self):
        return self._solenoid_current_setpoint

    @property
    def solenoid_voltage(self):
        return None

    @solenoid_voltage.setter
    def solenoid_voltage(self, value):
        pass

    @property
    def solenoid_voltage_setpoint(self):
        return None

    @property
    def chamber_pressure(self):
        return None

    @property
    def heater_current(self):
        return None

    @heater_current.setter
    def heater_current(self, value):
        pass

    @property
    def heater_current_setpoint(self):
        return None

    @property
    def heater_voltage(self):
        return None

    @heater_voltage.setter
    def heater_voltage(self, value):
        pass

    @property
    def heater_voltage_setpoint(self):
        return None

    @property
    def discharge_current(self):
        return None

    @discharge_current.setter
    def discharge_current(self, value):
        pass

    @property
    def discharge_current_setpoint(self):
        return None

    @property
    def discharge_voltage(self):
        return None

    @discharge_voltage.setter
    def discharge_voltage(self, value):
        pass

    @property
    def discharge_voltage_setpoint(self):
        return None
