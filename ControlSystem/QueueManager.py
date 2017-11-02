from . import ArduinoHandler
import logging
import os
import queue
import threading


class QueueManager(object):

    def __init__(self):
        self._arduino_handler = ArduinoHandler.ArduinoHandler('/dev/cu.usbmodem1421')
        self._queue = queue.Queue()
        self._update_timer = 0
        self._state = {
            'solenoid_current': 0.0, 'solenoid_voltage': 0.0,
            'heater_current': 0.0, 'heater_voltage': 0.0,
            'discharge_current': 0.0, 'discharge_voltage': 0.0,
            'chamber_pressure': 0.0
        }
        self._state_lock = threading.Lock()
        self._thread = threading.Thread(target=self.processQueue)
        self._thread.start()

    def stop(self):
        self._queue.put('TERMINATE')
        self._thread.join()
        self._arduino_handler.close()

    def getState(self, name):
        with self._state_lock:
            return self._state[name]

    def processQueue(self):
        try:
            while True:
                #if self._update_timer == 10:
                #    self.update_timer = 0
                #    self.addUpdateCommands()
                #else:
                #    self._update_timer += 1
                command = self._queue.get()
                logging.debug('executing command \'{}\' from queue'.format(command))
                if command == 'TERMINATE':
                    return
                self.executeCommand(command)
                self._queue.task_done()
        except Exception as e:
            logging.exception(e)
            os._exit(1)

    def addUpdateCommands(self):
        self._queue.put('GET_SOLENOID_CURRENT')

    def executeCommand(self, command):
        if command == 'GET_SOLENOID_CURRENT':
            values = []
            for _ in range(10):
                value = self._arduino_handler.query('GET_SOLENOID_CURRENT')
                values.append(value)
            if None in values:
                result = None
            else:
                result = sum(values) / len(values)
            with self._state_lock:
                self._state['solenoid_current'] = result
        else:
            assert False
