from . import ArduinoHandler
from . import Updater
import logging
import os
import platform
import queue
import threading


class QueueManager(object):

    def __init__(self):
        self._arduino_handler = ArduinoHandler.ArduinoHandler('/dev/cu.usbmodem1421' if platform.system() == 'Darwin' else 'COM3')
        self._state = {
            'solenoid_current': None, 'chamber_pressure': None
        }
        self._logger = logging.getLogger('QueueManager')
        self._queue = queue.Queue()
        self._updater = Updater.Updater(self._queue)
        self._state_lock = threading.Lock()
        self._terminate = False
        self._terminate_lock = threading.Lock()
        self._thread = threading.Thread(target=self.processQueue)
        self._thread.start()

    def stop(self):
        self._updater.stop()
        self._logger.debug('terminating queue processing thread')
        with self._terminate_lock:
            self._terminate = True
        self._thread.join()
        self._arduino_handler.disconnect()

    def addCommand(self, command):
        self._logger.debug('adding command \'{}\' to the queue'.format(command))
        self._queue.put(command)

    def getState(self, name):
        with self._state_lock:
            return self._state[name]

    def executeCommand(self, command):
        self._logger.debug('executing command \'{}\' (queue length is now {})'.format(command, self._queue.qsize()))
        if command == 'GET_SOLENOID_CURRENT':
            values = []
            for _ in range(10):
                value = self._arduino_handler.query('GET_SOLENOID_CURRENT')
                if value is None:
                    result = None
                    break
                values.append(float(value))
            else:
                result = sum(values) / len(values)
            with self._state_lock:
                self._state['solenoid_current'] = result
        elif command == 'GET_PRESSURE':
            value = self._arduino_handler.query('GET_PRESSURE')
            if value is None:
                result = None
            else:
                result = float(value)
            with self._state_lock:
                self._state['chamber_pressure'] = result
        elif command.startswith('SET_SOLENOID_CURRENT'):
            self._arduino_handler.query(command)
        elif command.startswith('SET_SOLENOID_VOLTAGE'):
            self._arduino_handler.query(command)
        else:
            assert False

    def processQueue(self):
        try:
            self._logger.debug('queue processing thread starting')
            while True:
                with self._terminate_lock:
                    if self._terminate:
                        return
                command = self._queue.get()
                self.executeCommand(command)
                self._queue.task_done()
        except Exception as e:
            self._logger.exception(e)
            os._exit(1)
