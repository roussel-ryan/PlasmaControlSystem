import logging
import time
import serial


class SerialConnection(object):

    def __init__(self, name, port, baudrate = 9600):
        self.name = name
        self._logger = logging.getLogger('SerialConnection "{}"'.format(self.name))
        self._state = True
        try:
            self._connection = serial.Serial(
                port = port,
                baudrate = baudrate,
                timeout = 1, # second
                write_timeout = 1 # second
            )
        except serial.SerialException as e:
            self._logger.error("unable to establish initial connection")
            self._state = False
            self._connection = None
        self.receive()

    def is_ok(self):
        return self._state

    def send(self, message):
        if self._state:
            try:
                self._connection.write((message + '\n').encode())
            except serial.SerialException as e:
                self._logger.error("connection lost while sending message")
                self._state = False

    def receive(self):
        if self._state:
            time.sleep(0.1)
            try:
                return self._connection.readline().decode().strip()
            except SerialException as e:
                self._logger.log("connection lost while reading message")
                self._state = False
        return None
