import visa
import logging


class VisaConnection(object):
    """
    Creates and interfaces with a single VISA device.
    
    Multiple Device Control:
    ------------------------
    VISA devices may have the ability to control other devices through the use of
    RS485 serial protocall, Example: TDK Power Supply. If this is used, interfacing to
    devices requires both the VISA address and the RS485 address.
    
    If this is used, the user needs to select a device before every write/query action
    or it will get sent to the previous selection.
    
    Attributes:
    -----------
    name            = human reference name of device
    _logger         = object specific logger object
    _state          = enable/disable state of the device
    _RS485_enabled  = enable/disable RS485 forwarding to control other devices
    _RS485_address  = RS485 address within the VISA connection
    _connection     = pyVISA object
    
    Methods:
    --------
    is_ok()         = returns enable/disable state of device
    write(command)  = writes command to currently selected device (if enabled)
    query(command)  = reads one line of serial buffer and returns data 
    """
    _resource_manager = visa.ResourceManager()

    def __init__(self, name, address, RS485_enabled):
        self._name = name
        self._logger = logging.getLogger('VisaConnection "{}"'.format(self._name))
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
            try:
                self._connection.write(command)
            except visa.VisaIOError as e:
                self._logger.error('VisaConnection {}: write failed'.format(self._name))
                self._state = False

    def query(self, command):
        if self._state:
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
        return self._state

    @classmethod
    def list_resources(self):
        self._logger.info(self._resource_manager.list_resources())
