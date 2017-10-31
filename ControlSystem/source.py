import os
import queue
import threading
import logging

from ControlSystem.hardware.handler import VISAHandler
from ControlSystem.hardware.handler import ArduinoHandler

class PlasmaSource:
    '''
    worker class to process the plasma queue
    '''
    def __init__(self,intial_state):
        '''
        start connections with all devices
        '''
        #self._logger = logging.getLogger('__main__.'+__name__)
        #self._logger.info('Starting PlasmaSource object')
        #self._logger.info('Beginning connections to devices')
        logging.info('Starting PlasmaSource object')
        logging.info('Beginning connections to devices')

        #self._TDK_handler = VISAHandler('TCPIP0::169.254.223.84::inst0::INSTR',RS485_enabled=True)
        self._Arduino_handler = ArduinoHandler('COM4')

        #start threads and queue
        #self._logger.info('Starting queue')
        self._queue = queue.Queue()
        #self._logger.info('Spawing thread and starting')
        self._thread = threading.Thread(target=self.process_queue)
        self._thread.start()

        self._state = {}
        #intialize variable dict
        for ele in intial_state:
            self._state[ele] = 0.0
        self._state_lock = threading.Lock()


    def stop(self):
        self._updater.stop()
        self._queue.put('TERMINATE')
        self._thread.join()
        self._Arduino_handler.close()


    def add_command(self,cmd):
        #self._logger.info('Adding cmd {} to the queue, queue length now {}'.format(cmd,self._queue.qsize()))
        logging.debug('Adding cmd {} to the queue, queue length now {}'.format(cmd,self._queue.qsize()))
        self._queue.put(cmd)

    def get_state(self,name):
        with self._state_lock:
            return self._state[name]

    def process_queue(self):
        '''
            execute cmd
            cmd ex. 'SET SOLENOID_CURRENT 0.005'
        '''
        self._tdk_set_commands = {'VOLTAGE':':VOLT {:3.2f}','CURRENT':':CURR {:3.2f}'}
        self._tdk_query_commands = {'VOLTAGE':'MEAS:VOLT?','CURRENT':'MEAS:CURR?'}
        self._tdk_RS485_addresses = {'HEATER':6,'DISCHARGE':1}

        try:
            while True:
                cmd = self._queue.get()
                logging.debug('Processing {}, {} cmds remain'.format(cmd,self._queue.qsize()))
                cmd_type = cmd.split(' ')[0]
                if cmd_type == 'TERMINATE':
                    return
                if cmd_type == 'SET':
                     cmd_device = cmd.split(' ')[1].split('_')[0]
                     cmd_attribute = cmd.split(' ')[1].split('_')[1]
                     cmd_value = float(cmd.split(' ')[2])

                     if cmd_device == 'HEATER' or cmd_device == 'DISCHARGE':
                         pass
                         #self._TDK_handler.select_RS485_device(self._tdk_RS485_addresses[cmd_device])
                         #self._TDK_handler.write(self._tdk_set_commands[cmd_attribute].format(cmd_value))
                     elif cmd_device == 'SOLENOID':
                         pass
                        #do something to set solenoid attr
                elif cmd_type == 'GET':
                    cmd_device = cmd.split(' ')[1].split('_')[0]
                    cmd_attribute = cmd.split(' ')[1].split('_')[1]
                    if cmd_device == 'HEATER' or cmd_device == 'DISCHARGE':
                        #self._TDK_handler.select_RS485_device(self._tdk_RS485_addresses[cmd_device])

                        #self._state[cmd_device+'_'+cmd_attribute] = #self._TDK_handler.query(self._tdk_set_commands[cmd_attribute].format(cmd_value))
                        with self._state_lock:
                            pass
                            #self._state['_'.join(cmd_device.lower(),cmd_attribute.lower())] = self._TDK_handler.query(self._tdk_query_commands[cmd_attribute])
                    elif cmd_device == 'SOLENOID':
                        pass
                    elif cmd_device == 'CHAMBER':
                        with self._state_lock:
                            logging.debug('Getting pressure')
                            self._state['_'.join((cmd_device.lower(),cmd_attribute.lower()))] = float(self._Arduino_handler.query('GET_PRESSURE').decode().strip())
                            logging.debug('Pressure reading is {}'.format(self._state['chamber_pressure']))
                        #do something to return solenoid attribute
                else:
                    assert False
                self._queue.task_done()

        except Exception as e:
            logging.exception(e)
            os._exit(1)
