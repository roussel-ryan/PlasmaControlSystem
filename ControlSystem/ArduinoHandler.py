import logging
import serial
import time


class ArduinoHandler(object):

    def __init__(self, port, baud_rate=9600):
        self._port = port
        self._baud_rate = baud_rate
        self._connection = None
        self._logger = logging.getLogger('ArduinoHandler')
        self.connect()

    def connect(self):
        self._logger.debug('connecting to arduino')
        try:
            self._connection = serial.Serial(self._port, self._baud_rate)
            self._logger.debug('\033[32mconnected to arduino\033[0m')
        except serial.SerialException as e:
            self._logger.exception(e)
            self._logger.debug('\033[31munable to connect to arduino\033[0m')

    def disconnect(self):
        if self._connection is not None:
            self._logger.debug('disconnecting from arduino')
            self._connection.close()

    def query(self, command):
        if self._connection is None:
            return None
        self._logger.debug('sending command \'{}\' to arduino'.format(command))
        self._connection.write(command.encode())
        time.sleep(0.1)
        result = self._connection.readline()
        if result == '':
            raise Exception('query \'{}\' did not return anything'.format(command))
        self._logger.debug('received reply \'{}\' from arduino'.format(result))
        return result
