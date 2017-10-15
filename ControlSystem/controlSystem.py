import worker

class PlasmaSourceControl(object):
    def __init__(self,queue,thread):
        '''
        Initilazation of plasma source controller
        '''
        self.solenoid_current = 0.0
        self.solenoid_voltage = 0.0

        self.heater_current = 0.0
        self.heater_voltage = 0.0

        self.discharge_current = 0.0
        self.discharge_volatge = 0.0

        self.pressure = 0.0

        self.water_interlock = False
        self.pressure_interlock = False

        self.command_queue = queue


        self.worker = worker.PlasmaQueueWorker()

    def start(self):
        self.run_plasma_source()

    def _run_plasma_source(self):
        while len(command_queue):
            cmd = self.command_queue.popleft().split(' ')
            if cmd[0] == 'GET':
                self.__dict__['_{}_{}'.format(cmd[1].lower(),cmd[2].lower())] = self.worker.process_command(cmd)
            elif cmd[0] == 'SET':
                if self.water_interlock and self.pressure_interlock:
                        self.worker.process_command(cmd)
            else:
                raise ValueError('Command {} not supported'.format(cmd[0]))

        wait(0.1)
        self._run_plasma_source()

    @property
    def solenoid_current(self):
        return self._solenoid_current

    @property
    def solenoid_voltage(self):
        return self._solenoid_voltage

    @solenoid_current.setter
    def solenoid_current(self,solenoid_current):
        '''
        send command to queue to set the solenoid_current
        '''
        self.command_queue.append('SET SOLENOID CURRENT {:3.2f}').format(solenoid_current)
        self.solenoid_current_setpoint = solenoid_current
