class PlasmaChamber(object):

    state_variables = ('solenoid_current', 'solenoid_voltage', 'heater_current',
       'heater_voltage','discharge_current', 'discharge_voltage',
       'chamber_pressure', 'water_interlock', 'pressure_interlock')

    def __init__(self):
        self.water_interlock = False
        self.pressure_interlock = False

    def stop(self):
        pass

    @property
    def solenoid_current(self):
        return 0.0

    @property
    def solenoid_voltage(self):
        return 0.0

    @property
    def discharge_voltage(self):
        return 0.0

    @property
    def discharge_current(self):
        return 0.0

    @property
    def heater_current(self):
        return 0.0

    @property
    def heater_voltage(self):
        return 0.0

    @property
    def chamber_pressure(self):
        return 0.0

    @solenoid_current.setter
    def solenoid_current(self, solenoid_current):
        pass

    @solenoid_voltage.setter
    def solenoid_voltage(self, solenoid_voltage):
        pass

    @heater_current.setter
    def heater_current(self, heater_current):
        pass

    @heater_voltage.setter
    def heater_voltage(self, heater_voltage):
        pass

    @discharge_current.setter
    def discharge_current(self, discharge_current):
        pass

    @discharge_voltage.setter
    def discharge_voltage(self, discharge_voltage):
        pass
