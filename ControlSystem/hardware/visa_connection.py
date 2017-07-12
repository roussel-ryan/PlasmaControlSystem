import visa
import threading
import logging


class VisaConnection(object):

    _resource_manager = visa.ResourceManager()

    def __init__(self, name, address, RS485_enabled):
        self._name = name
        self._logger = logging.getLogger('VisaConnection "{}"'.format(self._name))
        self._lock = threading.Lock()
        self._state = True
        self._RS485_enabled = RS485_enabled
        self._RS485_address = None
        self._connection = None
        try:
            self._connection = self._resource_manager.open_resource(address)
        except visa.VisaIOError as e:
            self._logger.error('VisaConnection {}: unable to connect to {}: {}'.format(self._name, address, e.args[0]))
            self._state = False

    def write(self, command):
        if self._state:
            with self._lock:
                try:
                    self._connection.write(command)
                except visa.VisaIOError as e:
                    self._logger.error('VisaConnection {}: write failed'.format(self._name))
                    self._state = False

    def query(self, command):
        if self._state:
            with self._lock:
                try:
                    return self._connection.query(command)
                except visa.VisaIOError as e:
                    self._logger.error('VisaConnection {}: query failed'.format(self._name))
                    self._state = False
        return None

    def select_RS485_device(self, RS485_address):
        assert self._RS485_enabled
        if self._state:
            if self._RS485_address != RS485_address:
                self.write('INST:SEL {}'.format(RS485_address))
                self._RS485_address = RS485_address if self._state else None

    def is_ok(self):
        return not self._state

    @classmethod
    def list_resources(self):
        self._logger.info(self._resource_manager.list_resources())
