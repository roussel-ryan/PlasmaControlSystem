import logging
import serial
import time


class ArduinoHandler(object):

    def __init__(self, port, baud_rate=9600):
        self._port = port
        self._baud_rate = baud_rate
        self._connection = None
        self.connect()

    def connect(self):
        logging.debug('attempting to establish connection to arduino')
        try:
            self._connection = serial.Serial(self._port, self._baud_rate)
            logging.debug('arduino connection established')
        except serial.SerialException as e:
            logging.info('\033[31mcould not connect to arduino\033[0m')


    def disconnect(self):
        logging.debug('disconnecting from arduino')
        if self._connection is not None:
            self._connection.close()

    def query(self, command):
        if self._connection is None:
            return None
        logging.debug('sending command \'{}\' to arduino'.format(command))
        self._connection.write(command.encode())
        time.sleep(0.1)
        result = self._connection.readline()
        if result == '':
            raise Exception('query \'{}\' did not return anything'.format(command))
        logging.debug('arduino replied \'{}\''.format(result))
        return result
