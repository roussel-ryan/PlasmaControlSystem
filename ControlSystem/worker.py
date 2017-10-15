
class PlasmaQueueWorker:
    '''
    worker class to process the plasma queue
    '''
    def __init__(self):
        '''
        start connections with all devices
        '''
        self._TDK_handler = VISAHandler('TCPIP0::169.254.223.84::inst0::INSTR',RS485_enabled=True)
        self._Arduino_handler = ArduinoHandler()



    def process_command(self,cmd):
        '''
            parse and execute cmd
            cmd ex. "SET SOLENOID CURRENT 0.005"
        '''
        self._tdk_set_commands = {'VOLTAGE':':VOLT {:3.2f}','CURRENT':':CURR {:3.2f}'}
        self._tdk_query_commands = {'VOLTAGE':'MEAS:VOLT?','CURRENT':'MEAS:CURR?'}
        self._tdk_RS485_addresses = {'HEATER':6,'DISCHARGE':1}

        split_command = cmd.split(' ')
        cmd_type = split_command[0]
        cmd_device = split_command[1]
        cmd_attribute = split_command[2]

        if cmd_type == 'SET':
            cmd_value = split_command[3]
            if cmd_device == 'HEATER' or cmd_device == 'DISCHARGE':
                self._TDK_handler.select_RS485_device(self._tdk_RS485_addresses[cmd_device])
                self._TDK_handler.write(self._tdk_set_commands[cmd_attribute].format(cmd_value))
            elif cmd_device == 'SOLENOID':
                #do something to set solenoid attr
        elif cmd_type == 'GET':
            if cmd_device == 'HEATER' or cmd_device == 'DISCHARGE':
                self._TDK_handler.select_RS485_device(self._tdk_RS485_addresses[cmd_device])
                return self._TDK_handler.query(self._tdk_query_commands[cmd_attribute])
