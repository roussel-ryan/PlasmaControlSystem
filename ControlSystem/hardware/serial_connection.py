import logging
import time
import serial


class SerialConnection(object):
    """
    Creates and interfaces with a single serial device.
    
    Attributes:
    -----------
    name        = human reference name of device
    _logger     = object specific logger object
    _state      = enable/disable state of the device
    _connection = pySerial object
    
    Methods:
    --------
    is_ok()     = returns enable/disable state of device
    send(msg)   = sends msg to device
    receive()   = reads one line of serial buffer and returns data 
    """

    def __init__(self, name, port, baudrate = 9600):
        """
        Initialization of serial device
        
        Creates device object and attempts to read, writes error message if it fails
        
        Parameters:
        -----------
        name        = human reference name of device, str
        port        = device port, int
        baudrate    = data read rate in bytes/sec NOTE: only specific rates are allowed 
                        and must match device baudrate, int
        """
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
        """ returns last known state of device"""
        return self._state

    def send(self, message):
        """
        Writes a message to the serial device
        
        Parameters:
        -----------
        message     = message to be written to device, str
        """
        if self._state:
            try:
                self._connection.write((message + '\n').encode())
            except serial.SerialException as e:
                self._logger.error("connection lost while sending message")
                self._state = False

    def receive(self):
        """
        Reads one line of buffer from serial device
        
        Returns:
        --------
        str     = first line of current device buffer, NoneType if it fails
        """
        if self._state:
            time.sleep(0.1)
            try:
                return self._connection.readline().decode().strip()
            except SerialException as e:
                self._logger.log("connection lost while reading message")
                self._state = False
        return None
