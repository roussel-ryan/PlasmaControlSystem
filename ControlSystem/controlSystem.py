import ControlSystem.worker as worker

from functools import wraps

class PlasmaSourceControl(object):
    def __init__(self):
        '''
        Initilazation of plasma source controller
        '''
        self._source = worker.PlasmaSource()
        self.setpoints = {}

        self.solenoid_current = 0.0
        self.solenoid_voltage = 0.0

        self.heater_current = 0.0
        self.heater_voltage = 0.0

        self.discharge_current = 0.0
        self.discharge_voltage = 0.0

        self.chamber_pressure = 0.0

        self.water_interlock = False
        self.pressure_interlock = False



    def stop(self):
        self._source.stop()

    ##########################################################################
    #Property definitions

    #decorator to add setpoint variables to public access
    def _update_setpoint(function):
        @wraps(function)
        def wrapper(*args,**kwargs):
            self.setpoints[function.__name__] = args[1]
            function(*args,**kwargs)
        return wrapper

    #decorator to add set command to queue
    def _append_set_command_to_queue(function):
        @wraps(function)
        def wrapper(*args,**kwargs):
            self._worker.add_command('SET {} {:3.2f}'.format(__name__.upper(),args[1]))
            function(*args,**kwargs)
        return wrapper

    @property
    def solenoid_current(self):
        return self._source.get_state('solenoid_current')

    @property
    def solenoid_voltage(self):
        return self._source.get_state('solenoid_voltage')

    @property
    def discharge_voltage(self):
        return self._source.get_state('discharge_voltage')

    @property
    def discharge_current(self):
        return self._source.get_state('discharge_current')

    @property
    def heater_current(self):
        return self._source.get_state('heater_current')

    @property
    def heater_voltage(self):
        return self._source.get_state('heater_voltage')

    @solenoid_current.setter
    @_append_set_command_to_queue
    @_update_setpoint
    def solenoid_current(self,solenoid_current):
        pass

    @solenoid_voltage.setter
    @_update_setpoint
    @_append_set_command_to_queue
    def solenoid_voltage(self,solenoid_voltage):
        pass

    @heater_current.setter
    @_append_set_command_to_queue
    @_update_setpoint
    def heater_current(self,heater_current):
        pass

    @heater_voltage.setter
    @_update_setpoint
    @_append_set_command_to_queue
    def heater_voltage(self,heater_voltage):
        pass

    @discharge_current.setter
    @_append_set_command_to_queue
    @_update_setpoint
    def discharge_current(self,discharge_current):
        pass

    @discharge_voltage.setter
    @_update_setpoint
    @_append_set_command_to_queue
    def discharge_voltage(self,discharge_voltage):
        pass



if __name__=='__main__':
    s = PlasmaSourceControl([],None)
    s.solenoid_current = 5.0

    print(s.solenoid_current)
    print(s.__dict__)
