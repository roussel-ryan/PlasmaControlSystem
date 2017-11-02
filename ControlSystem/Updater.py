import logging
import threading
import time
import os


class Updater(object):

    time_interval = 5

    commands = (
        'GET_SOLENOID_CURRENT',
        'GET_PRESSURE'
    )

    def __init__(self, queue):
        self._logger = logging.getLogger('Updater')
        self._queue = queue
        self._index_of_next_command = 0
        self._terminate = False
        self._terminate_lock = threading.Lock()
        self._thread = threading.Thread(target=self.run)
        self._thread.start()

    def stop(self):
        self._logger.debug('terminating update thread')
        with self._terminate_lock:
            self._terminate = True
        self._thread.join()

    def run(self):
        try:
            self._logger.debug('update thread starting')
            while True:
                time.sleep(self.time_interval)
                with self._terminate_lock:
                    if self._terminate:
                        return
                command = self.commands[self._index_of_next_command]
                self._index_of_next_command += 1
                if self._index_of_next_command == len(self.commands):
                    self._index_of_next_command = 0
                self._logger.debug('adding command \'{}\' to queue'.format(command))
                self._queue.put(command)
        except Exception as e:
            self._logger.exception(e)
            os._exit(1)
