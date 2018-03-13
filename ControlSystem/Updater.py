import logging
import threading
import time
import os


class Updater(object):
    """
    Creates a thread which at regularly spaced time intervals adds a command to
    a queue.
    """

    time_delay = 1
    """
    The number of seconds to wait between adding commands. The actual amount of
    time may be different than this, but should be roughly proportional.
    """

    commands = (
        'GET_SOLENOID_CURRENT',
        'GET_PRESSURE',
        'GET_HEATER_VOLTAGE',
        'GET_HEATER_CURRENT',
        'GET_DISCHARGE_VOLTAGE',
        'GET_DISCHARGE_CURRENT'
    )
    """
    Which commands to add. Only one command is added at a time, and the Updater
    object goes through the commands in order when deciding which command to
    add.
    """

    def __init__(self, queue):
        self._logger = logging.getLogger('Updater')
        self._queue = queue
        self._index_of_next_command = 0
        self._terminate = False
        self._terminate_lock = threading.Lock()
        self._thread = threading.Thread(target=self._run)
        self._thread.start()

    def stop(self):
        """ Terminates the update thread. """
        self._logger.debug('terminating update thread')
        with self._terminate_lock:
            self._terminate = True
        self._thread.join()

    def _run(self):
        """ The function run by the update thread. """
        try:
            self._logger.debug('update thread starting')
            while True:
                # wait for the specified number of seconds
                time.sleep(self.time_delay)
                # check if the terminate boolean has been set
                with self._terminate_lock:
                    if self._terminate:
                        return
                # get the next command from the list of commands
                command = self.commands[self._index_of_next_command]
                self._index_of_next_command += 1
                if self._index_of_next_command == len(self.commands):
                    self._index_of_next_command = 0
                self._logger.debug('adding command \'{}\' to queue'.format(command))
                # add the command to the queue
                self._queue.put(command)
        except Exception as e:
            self._logger.exception(e)
            os._exit(1)
