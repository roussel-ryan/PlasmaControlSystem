import serial
import time 

ser=serial.Serial('COM5',9600)

def getPressure(): 
	ser.write(b'p')
	time.sleep(0.1)
	Pressure=ser.readline()
	return Pressure

def __main__(): 
	action=input("Input 'getpressure' to read the pressure of the gas\n")
	if action=='getpressure':
		pressure=getPressure()
		#return pressure
		print(pressure)
	else: 
		return None

exitstate=False 
while not exitstate:
	exitcheck=input("Type 'exit' if you would like to close the program, otherwise input 'no'\n")
	if exitcheck=='exit':
		ser.close()
		exitstate=True 
	else:
		__main__()


