import os
import sys
import threading
import logging

class Updater(object):
    time_interval = 1.0
    #commands to execute as part of the update event
    commands = (
        'GET SOLENOID_CURRENT',
        'GET SOLENODD_VOLTAGE',
        'GET DISCHARGE_CURRENT',
        'GET DISCHARGE_VOLTAGE',
        'GET HEATER_CURRENT',
        'GET HEATER_VOLTAGE',
        'GET WATER_INTERLOCK',
        'GET PRESSURE_INTERLOCK',
        'GET CHAMBER_PRESSURE'
    )

    def __init__(self, queue):
        self._logger = logging.getLogger('__main__.'+__name__)
        self._logger.info('Starting Updater object')

        self._queue = queue
        self._index_of_next_command = 0
        self._stop_flag = False
        self._stop_flag_lock = threading.Lock()
        self._timer = threading.Timer(self.time_interval, self._update)
        self._timer.start()

    def stop(self):
        with self._stop_flag_lock:
            self._stop_flag = True
        self._timer.join()

    def _update(self):
        try:
            # Check the stop flag
            with self._stop_flag_lock:
                if self._stop_flag:
                    return
            # Add command to queue
            command = self.commands[self._index_of_next_command]
            self._index_of_next_command += 1
            if self._index_of_next_command == len(self.commands):
                self._index_of_next_command = 0
            self._logger.debug('Adding cmd {} to the queue'.format(command))
            self._queue.put(command)
            # Setup new timer
            self._timer = threading.Timer(self.time_interval, self._update)
            self._timer.start()
        except Exception as e:
            print(e)
            sys.stdout.flush()
            os.exit(1)
