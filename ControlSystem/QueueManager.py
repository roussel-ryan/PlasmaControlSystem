from . import ArduinoHandler
from . import Updater
from . import VisaHandler
import logging
import os
import platform
import queue
import threading


discharge_RS485_address = 6
heater_RS485_address = 1


class QueueManager(object):
    """
    Holds the thread that executes commands at the front of the queue. Also
    holds intermediate values for things like the solenoid_current which take a
    long time to read.
    """

    def __init__(self):
        self._arduino_handler = ArduinoHandler.ArduinoHandler('/dev/cu.usbmodem1421' if platform.system() == 'Darwin' else 'COM3')
        self._visa_handler = VisaHandler.VisaHandler('TCPIP0::169.254.223.84::inst0::INSTR')
        self._visa_handler.write('*CLS')
        for RS485_address in (discharge_RS485_address, heater_RS485_address):
            self._visa_handler.select_RS485_device(RS485_address)
            if self._visa_handler.query('OUTP:STAT?') == 'OFF':
                self._visa_handler.write('OUTP:STAT ON')
        self._intermediate_value = {
            'solenoid_current': None,
            'chamber_pressure': None
        }
        self._logger = logging.getLogger('QueueManager')
        self._queue = queue.Queue()
        self._updater = Updater.Updater(self._queue)
        self._intermediate_value_lock = threading.Lock()
        self._terminate = False
        self._terminate_lock = threading.Lock()
        self._thread = threading.Thread(target=self.processQueue)
        self._thread.start()

    def stop(self):
        """ Terminates all theads and closes all connections. """
        # stop the updater thread
        self._updater.stop()
        # stop the queue processing thread
        self._logger.debug('terminating queue processing thread')
        with self._terminate_lock:
            self._terminate = True
        self._queue.put(None) # prevents deadlocks if the the queue processing
            # thread is blocked waiting for new objects to be added to the queue.
        self._thread.join()
        # disconnect from the arduino
        self._arduino_handler.disconnect()
        # disconnect from visa device
        self._visa_handler.disconnect()

    def addCommand(self, command):
        """ Adds a command to the queue. """
        self._logger.debug('adding command \'{}\' to the queue (queue length is now {})'.format(command, self._queue.qsize()))
        self._queue.put(command)

    def getIntermediateValue(self, name):
        with self._intermediate_value_lock:
            return self._intermediate_value[name]

    def processQueue(self):
        try:
            self._logger.debug('queue processing thread starting')
            while True:
                # get a command from the queue
                command = self._queue.get()
                # check if the terminate variable is set
                with self._terminate_lock:
                    if self._terminate:
                        return
                # execute the command
                self.executeCommand(command)
                # signal to the queue that the command is done executing
                self._queue.task_done()
        except Exception as e:
            self._logger.exception(e)
            os._exit(1)

    def executeCommand(self, command):
        """
        Executes a command from the queue. Run by the queue processing thread
        which calls it from processQueue().
        """
        self._logger.debug('executing command \'{}\' (queue length is now {})'.format(command, self._queue.qsize()))

        if command == 'GET_SOLENOID_CURRENT':
            values = []
            for _ in range(3):
                value = self._arduino_handler.query('GET_SOLENOID_CURRENT')
                if value is None:
                    result = None
                    break
                values.append(float(value))
            else:
                result = sum(values) / len(values)
            with self._intermediate_value_lock:
                self._intermediate_value['solenoid_current'] = result

        elif command == 'GET_PRESSURE':
            value = self._arduino_handler.query('GET_PRESSURE')
            if value is None:
                result = None
            else:
                result = float(value)
            with self._intermediate_value_lock:
                self._intermediate_value['chamber_pressure'] = result

        elif command.startswith('SET_SOLENOID_CURRENT'):
            self._arduino_handler.query(command)

        elif command.startswith('SET_SOLENOID_VOLTAGE'):
            self._arduino_handler.query(command)

        elif command == 'GET_HEATER_CURRENT':
            self._visa_handler.select_RS485_device(heater_RS485_address)
            result = self._visa_handler.query('MEAS:CURR?')
            with self._intermediate_value_lock:
                self._intermediate_value['heater_current'] = None if result is None else float(result)

        elif command == 'GET_HEATER_VOLTAGE':
            self._visa_handler.select_RS485_device(heater_RS485_address)
            result = self._visa_handler.query('MEAS:VOLT?')
            with self._intermediate_value_lock:
                self._intermediate_value['heater_voltage'] = None if result is None else float(result)

        elif command == 'GET_DISCHARGE_CURRENT':
            self._visa_handler.select_RS485_device(discharge_RS485_address)
            result = self._visa_handler.query('MEAS:CURR?')
            with self._intermediate_value_lock:
                self._intermediate_value['discharge_current'] = None if result is None else float(result)

        elif command == 'GET_DISCHARGE_VOLTAGE':
            self._visa_handler.select_RS485_device(discharge_RS485_address)
            result = self._visa_handler.query('MEAS:VOLT?')
            with self._intermediate_value_lock:
                self._intermediate_value['discharge_voltage'] = None if result is None else float(result)

        elif command.startswith('SET_HEATER_CURRENT'):
            self._visa_handler.select_RS485_device(heater_RS485_address)
            self._visa_handler.write(':CURR {:3.2f}'.format(float(command.split()[1])))

        elif command.startswith('SET_HEATER_VOLTAGE'):
            self._visa_handler.select_RS485_device(heater_RS485_address)
            self._visa_handler.write(':VOLT {:3.2f}'.format(float(command.split()[1])))

        elif command.startswith('SET_DISCHARGE_CURRENT'):
            self._visa_handler.select_RS485_device(discharge_RS485_address)
            self._visa_handler.write(':CURR {:3.2f}'.format(float(command.split()[1])))

        elif command.startswith('SET_DISCHARGE_VOLTAGE'):
            self._visa_handler.select_RS485_device(discharge_RS485_address)
            self._visa_handler.write(':VOLT {:3.2f}'.format(float(command.split()[1])))

        else:
            assert False
