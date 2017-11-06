import logging
import visa


class VisaHandler(object):

    _resource_manager = visa.ResourceManager()

    def __init__(self, address, RS485_enabled=True):
        self._address = address
        self._RS485_address = None
        self._RS485_enabled = RS485_enabled
        self._connection = None
        self._logger = logging.getLogger('VisaHandler')
        self.connect()

    def connect(self):
        assert self._connection is None
        self._logger.debug('connecting to visa device'.format(self._address))
        try:
            self._connection = self._resource_manager.open_resource(self._address)
        except visa.VisaIOError as e:
            self._logger.exception(e)
            self._logger.debug('\033[31munable to connect to visa device\033[0m')

    def disconnect(self):
        if self._connection is not None:
            self._logger.debug('disconnecting from visa device')
            print(dir(self._connection))
            assert False
            self._connection = None
            self._RS485_address = None

    def write(self, command):
        if self._connection is not None:
            assert self._RS485_address is not None
            self._logger.debug('sending command \'{}\' to visa device (write)'.format(command))
            self._connection.write(command)
            self.checkErrors()

    def query(self, command):
        if self._connection is not None:
            assert self._RS485_address is not None
            self._logger.debug('sending command \'{}\' to visa device'.format(command))
            result = self._connection.query(command)
            self._logger.debug('recieved response \'{}\' from visa device'.format(result))
            self.checkErrors()
            return result
        return None

    def select_RS485_device(self, RS485_address):
        assert self._RS485_enabled
        if self._connection:
            if self._RS485_address != RS485_address:
                self.write('INST:SEL {}'.format(RS485_address))
                self._RS485_address = RS485_address

    def checkErrors(self):
        if self._connection:
            assert self._RS485_address
            assert self._connection.query('SYST:ERR?') is None
