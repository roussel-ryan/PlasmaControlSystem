from . import device
from . import serial_connection


class SolenoidPowerSupply(device.Device):


    def __init__(self, name):
        super().__init__(name)
        self._connection = serial_connection.SerialConnection(self.name, '/dev/cu.usbmodem1411')
        self._target_current = 0.0
        self._target_voltage = 0.0
        self._actual_current = 0.0

    def set_error(self):
        super().set_error()
        self._target_current = None
        self._target_voltage = None
        self._actual_current = None

    def updateActualCurrent(self):
        currents = []
        for _ in range(10):
            self._connection.send('READ_CURR')
            result = self._connection.receive()
            if not self._connection.is_ok():
                self.set_error()
                return
            currents.append(float(result))
        self._actual_current = sum(currents) / len(currents)


    @device.Device.first_check_state
    def get(self, name):
        if name == 'voltage':
            return self._target_voltage
        elif name == 'current':
            self.updateActualCurrent()
            return self._actual_current
        else:
            raise ValueError('invalid attribute name (expected voltage or current)')

    @device.Device.first_check_state
    def set(self, name, value):
        if name == 'voltage':
            if (target_voltage < 0 or target_voltage > 100):
                raise ValueError("solenoid power supply voltage must be between 0 and 100 volts")
            self._connection.send("SET_VOLT {}".format(target_voltage))
            self._target_voltage = target_voltage
        elif name == 'current':
            if (target_current < 0 or target_current > 100):
                raise ValueError("solenoid power supply current must be between 0 and 100 amps")
            self._connection.send("SET_CURR {}".format(target_current))
            self._target_current = target_current
            time.sleep(0.5)
            self.updateActualCurrent()
            if self._actual_current is not None:
                if abs(self._actual_current - self._target_current) > 1:
                    self._logger.error("actual current different from target current by more than 1 amp")
        else:
            raise ValueError('invalid attribute name (expected voltage or current)')
        if not self._connection.is_ok():
            self.set_error()
