import worker

from functools import wraps

class PlasmaSourceControl(object):
    def __init__(self,queue,thread):
        '''
        Initilazation of plasma source controller
        '''
        self._command_queue = queue
        self._worker = worker.PlasmaQueueWorker()

        self.solenoid_current = 0.0
        self.solenoid_voltage = 0.0

        self.heater_current = 0.0
        self.heater_voltage = 0.0

        self.discharge_current = 0.0
        self.discharge_volatge = 0.0

        self.pressure = 0.0

        self.water_interlock = False
        self.pressure_interlock = False


    def start(self):
        self.run_plasma_source()

    def _run_plasma_source(self):
        while len(self._command_queue):
            cmd = self._command_queue.popleft().split(' ')
            if cmd[0] == 'GET':
                self.__dict__['_{}_{}'.format(cmd[1].lower(),cmd[2].lower())] = self.worker.process_command(cmd)
            elif cmd[0] == 'SET':
                if self.water_interlock and self.pressure_interlock:
                        self.worker.process_command(cmd)
            else:
                raise ValueError('Command {} not supported'.format(cmd[0]))

        wait(0.1)
        self._run_plasma_source()


    ##########################################################################
    #Property definitions

    #decorator to add setpoint variables to public access
    def _update_setpoint(function):
        @wraps(function)
        def wrapper(*args,**kwargs):
            setattr(args[0],function.__name__ + '_setpoint',args[1])
            function(*args,**kwargs)
        return wrapper

    #decorator to add set command to queue
    def _append_set_command_to_queue(function):
        @wraps(function)
        def wrapper(*args,**kwargs):
            device = function.__name__.split('_')[0].upper()
            attribute = function.__name__.split('_')[1].upper()
            args[0]._command_queue.append('SET {} {} {:3.2f}'.format(device,attribute,args[1]))
            function(*args,**kwargs)
        return wrapper

    @property
    def solenoid_current(self):
        return self._solenoid_current

    @property
    def solenoid_voltage(self):
        return self._solenoid_voltage

    @property
    def discharge_voltage(self):
        return self._discharge_voltage

    @property
    def discharge_current(self):
        return self._discharge_current

    @property
    def heater_current(self):
        return self._heater_current

    @property
    def heater_voltage(self):
        return self._heater_voltage

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
    s.solenoid_current = 5
    print(s.__dict__)
    #print(s.solenoid_current_setpoint)
    print(s._command_queue)
