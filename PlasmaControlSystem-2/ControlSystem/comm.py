'''
from hardware.handler import VISAHandler

class UniversalCommunicatior:
    def __init__(self):

        self._tdk_set_commands = {'voltage':':VOLT {:3.2f}','current':':CURR {:3.2f}'}
        self._tdk_query_commands = {'voltage':'MEAS:VOLT?','current':'MEAS:CURR?'}

    def connect_To_Ardino(self,timeout = 1.0):

            #attempt to connect to the ardino, nothing is returned before <timeout> throw a connection error


    def write_To_Arduino(self,msg, timeout = 1.0):

        #Writes message to Arduino and waits for <timeout> seconds for response, if timeout is 0.0 do not look for a response


    def write_To_TDKSupplies(self,attr,type='query',set_value=0.0):
        if type == 'query':
            self.TDK_handler.write

    def connect_To_TDKSupplies(self,address='TCPIP0::169.254.223.84::inst0::INSTR'):
        self.TDK_handler = VISAHandler(address,RS485_enabled=True)
        self.TDK_handler.write('*CLS')

	    if self.handler.query('OUTP:STAT?') == 'OFF':
            self.handler.write('OUTP:STAT ON')
'''
