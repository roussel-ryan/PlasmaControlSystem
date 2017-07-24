import threading
import time
import platform
from . import device
from . import serial_connection


port = '/dev/cu.usbmodem1411' if platform.system() == 'Darwin' else 'COM3'


class SolenoidPowerSupply(device.Device):

    def __init__(self, name):
        super().__init__(name)
        self._connection = serial_connection.SerialConnection(self.name, port)
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
        if abs(self._actual_current - self._target_current) > 1:
            self._logger.error("actual current different from target current by more than 1 amp")

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
            if value != self._target_voltage:
                if (value < 0 or value > 100):
                    raise ValueError("solenoid power supply voltage must be between 0 and 100 volts")
                print("sending set volt", value)
                self._connection.send("SET_VOLT {}".format(value))
                self._connection.receive()
                self._target_voltage = value
        elif name == 'current':
            if value != self._target_current:
                if (value < 0 or value > 100):
                    raise ValueError("solenoid power supply current must be between 0 and 100 amps")
                print("sending set curr", value)
                self._connection.send("SET_CURR {}".format(value))
                self._connection.receive()
                self._target_current = value
        else:
            raise ValueError('invalid attribute name (expected voltage or current)')
        if not self._connection.is_ok():
            self.set_error()
