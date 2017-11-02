from . import ArduinoHandler
import logging
import os
import queue
import threading


class QueueManager(object):

    def __init__(self):
        self._arduino_handler = ArduinoHandler.ArduinoHandler('/dev/cu.usbmodem1421')
        self._queue = queue.Queue()
        self._state = {
            'solenoid_current': None, 'solenoid_voltage': None,
            'heater_current': None, 'heater_voltage': None,
            'discharge_current': None, 'discharge_voltage': None,
            'chamber_pressure': None
        }
        self._state_lock = threading.Lock()
        self._thread = threading.Thread(target=self.process_queue)
        self._thread.start()

    def stop(self):
        self._queue.put('TERMINATE')
        self._thread.join()
        self._arduino_handler.close()

    def add_command(self, command):
        logging.debug('adding command \'{}\' to the queue (length is now {})'.format(command, self._queue.qsize()))
        self._queue.put(command)

    def get_state(self, name):
        with self._state_lock:
            return self._state[name]

    def process_queue(self):
        try:
            while True:
                command = self._queue.get()
                logging.debug('executing command \'{}\' (queue length is now {})'.format(command, self._queue.qsize()))
                if command == 'TERMINATE':
                    return
                self._queue.task_done()
        except Exception as e:
            print(e)
            import sys
            sys.stdout.flush()
            os._exit(1)
