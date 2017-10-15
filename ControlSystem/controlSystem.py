import worker

class PlasmaSourceControl:
    def __init__(self):
        '''
        Initilazation of plasma source controller
        '''
        self.solenoid_current = None
        self.solenoid_voltage = None

        self.heater_current = None
        self.heater_voltage = None

        self.discharge_current = None
        self.discharge_volatge = None

        self.pressure = None

        self.water_interlock = False
        self.pressure_interlock = False

        self.command_queue = []


        #spawn a thread to take care of the device communication
        self.worker = worker.PlasmaQueueWorker()

        self.run_plasma_source()

    def run_plasma_source(self):
        while len(command_queue):
            if self.water_interlock and self.pressure_interlock:
                self.worker.process_command(self.command_queue.popleft())

        wait(0.1)
        self.run_plasma_source()

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
