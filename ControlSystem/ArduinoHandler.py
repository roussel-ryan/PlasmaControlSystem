import logging
import serial
import time


class ArduinoHandler(object):
    """
    Handles the serial connection to the arduino. ArduinoHandler objects are
    always either in a connected state or in a disconnected state.
    """

    arduino_time_delay = 0.1
    """
    After sending a message to the arduino, an ArduinoHandler waits this amount
    of time before reading a response.
    """

    def __init__(self, port, baud_rate=9600):
        """
        Initializes the ArduinoHandler object and attempts to connect. If this
        fails, the object is left in a disconnected state.
        """
        self._port = port
        self._baud_rate = baud_rate
        self._connection = None
        self._logger = logging.getLogger('ArduinoHandler')
        self.connect()

    def connect(self):
        """
        Attempts to establish a serial connection. If this fails, the object is
        left in a disconnected state.
        """
        assert self._connection is None
        self._logger.debug('connecting to arduino')
        try:
            self._connection = serial.Serial(self._port, self._baud_rate)
            self._logger.debug('\033[32mconnected to arduino\033[0m')
        except serial.SerialException as e:
            self._logger.exception(e)
            self._logger.debug('\033[31munable to connect to arduino\033[0m')

    def disconnect(self):
        """
        If the object is in a connected state, this closes the connection and
        sets it to a disconnected state. Otherwise nothing happens.
        """
        if self._connection is not None:
            self._logger.debug('disconnecting from arduino')
            self._connection.close()
            self._connection = None

    def query(self, command):
        """
        If the object is in a disconnected state, this does nothing and returns
        None. Otherwise, this sends a command to the arduino and returns the
        response given by the arduino. If sending or receiving a reply fails,
        an exception is thrown.
        """
        if self._connection is None:
            return None
        self._logger.debug('sending command \'{}\' to arduino'.format(command))
        self._connection.write(command.encode())
        time.sleep(self.arduino_time_delay)
        result = self._connection.readline()
        if result == '':
            raise Exception('query \'{}\' did not return anything'.format(command))
        self._logger.debug('received reply \'{}\' from arduino'.format(result))
        return result
