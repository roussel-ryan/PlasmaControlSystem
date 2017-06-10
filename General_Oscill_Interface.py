from tkinter import *
import visa, numpy as np, matplotlib 
from struct import unpack
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure 
from matplotlib import style 
style.use('ggplot')
import matplotlib.patches as patch
import pandas as pd 
from time import *

scope=visa.ResourceManager()
scope.list_resources()
scope=scope.open_resource('USB::0x0699::0x0408::C031986::INSTR')
scope.write('DATA:SOU CH1')  
scope.write('DATA:WIDTH 1') 
scope.write('DATA:ENC RPB')  
ymult=float(scope.ask('WFMPRE:YMULT?')) 
yzero=float(scope.ask('WFMPRE:YZERO?'))
yoff=float(scope.ask('WFMPRE:YOFF?'))

Channels=[]
for j in [1,2,3,4]: 
	try: 
		scope.write('DATA:SOU CH%s' % j)
		scope.write('DATA:WIDTH 1')
		scope.write('DATA:ENC RPB')
		scope.write('CURVE?')
		x=float(scope.ask('WFMPRE:XINCR?'))
		Channels+=[j]
	except visa.VisaIOError:
		pass 
print(Channels)

def read_instrument(): 
	v1,v2,v3,v4=np.zeros(1),np.zeros(1),np.zeros(1),np.zeros(1)
	for j in Channels:
		try:
			scope.write('DATA:SOU CH%s' % j) 
			scope.write('DATA:WIDTH 1')
			scope.write('DATA:ENC RPB')
			xincr=float(scope.ask('WFMPRE:XINCR?'))
			scope.write('CURVE?')
			reading=scope.read_raw()

			headerlen=2+int(reading[1])
			header=reading[:headerlen]
			ADC_Wave=reading[headerlen:-1]
			ADC_Wave=np.array(unpack('%sB'%len(ADC_Wave),ADC_Wave))
			Volts=(ADC_Wave-yoff)*ymult+yzero
			Time=np.arange(0,xincr*len(Volts)/10,xincr/10)
			if j==1: 
				v1=Volts
			elif j==2: 
				v2=Volts
			elif j==3:
				v3=Volts
			elif j==4:
				v4=Volts 
		except visa.VisaIOError:
			pass
	return Time,v1,v2,v3,v4

f=plt.figure()
ax=f.add_subplot(111)
xarray=np.arange(0,0.005,0.0001)
ax.set_ylim(-11,11)
data,=ax.plot(xarray,xarray)

t,v1,v2,v3,v4=read_instrument()
tmin,tmax=np.amin(t),np.amax(t)
ax.set_xlim(tmin,tmax)
ax.set_xlabel('Time (s)')
ax.set_ylabel('Voltage (V)')
ch1label=patch.Patch(color='red',label='Channel One')
ch2label=patch.Patch(color='blue',label='Channel Two')
ch3label=patch.Patch(color='green',label='Channel Three')
ch4label=patch.Patch(color='yellow',label='Channel Four')
handles=[]
for j in Channels: 
	if j==1:
		handles+=[ch1label]
	elif j==2:
		handles+=[ch2label]
	elif j==3:
		handles+=[ch3label]
	elif j==4:
		handles+=[ch4label]
ax.legend(handles=handles)

def get_max1(): 
	t,v1,v2,v3,v4=read_instrument()
	return np.amax(v1)
def get_max2(): 
	t,v1,v2,v3,v4=read_instrument()
	return np.amax(v2)
def get_max3(): 
	t,v1,v2,v3,v4=read_instrument()
	return np.amax(v3)
def get_max4(): 
	t,v1,v2,v3,v4=read_instrument()
	return np.amax(v4)

def get_min1(): 
	t,v1,v2,v3,v4=read_instrument()
	return np.amin(v1)
def get_min2(): 
	t,v1,v2,v3,v4=read_instrument()
	return np.amin(v2)
def get_min3(): 
	t,v1,v2,v3,v4=read_instrument()
	return np.amin(v3)
def get_min4(): 
	t,v1,v2,v3,v4=read_instrument()
	return np.amin(v4)

def update_max():
	for j in Channels: 
		if j==1:
			max1['text']='Ch1 Max Value: %s' %get_max1()
		elif j==2:
			max2['text']='Ch2 Max Value: %s' % get_max2()
		elif j==3:
			max3['text']='Ch3 Max Value: %s' % get_max3()
		elif j==4:
			max4['text']='Ch4 Max Value: %s' % get_max4()
	root.after(1,update_max)

def update_min():
	for j in Channels: 
		if j==1:
			min1['text']='Ch1 Min Value: %s' %get_min1()
		elif j==2:
			min2['text']='Ch2 Min Value: %s' % get_min2()
		elif j==3:
			min3['text']='Ch3 Min Value: %s' % get_min3()
		elif j==4:
			min4['text']='Ch4 Min Value: %s' % get_min4()
	root.after(1,update_min)

def exit_guy(): 
	quit()

def get_filename(): 
	name=entrylabel.get()
	return name

def save_data():
	graphdata=f.gca()
	v1,v2,v3,v4=np.zeros(1),np.zeros(1),np.zeros(1),np.zeros(1)
	k=0
	while k<len(Channels):
		for j in Channels: 
			if j==1:
				Ch1_Data=graphdata.lines[k]
				v1=Ch1_Data.get_ydata()
				t=Ch1_Data.get_xdata()
			elif j==2:
				Ch2_Data=graphdata.lines[k]
				v2=Ch2_Data.get_ydata()
				t=Ch2_Data.get_xdata()
			elif j==3:
				Ch3_Data=graphdata.lines[k]
				v3=Ch3_Data.get_ydata()
				t=Ch3_Data.get_xdata()
			elif j==4:
				Ch4_Data=graphdata.lines[k]
				v4=Ch4_Data.get_ydata()
				t=Ch4_Data.get_xdata()
		k+=1
	data=pd.DataFrame({'Time (s)':t,'Ch1 Volts (V)':v1,'Ch2 Volts (V)':v2,'Ch3 Volts (V)':v3,'Ch4 Volts (V)':v4},
		columns=['Time (s)','Ch1 Volts (V)','Ch2 Volts (V)','Ch3 Volts (V)','Ch4 Volts (V)'])
	file=get_filename()
	data.to_csv(r'%s'%(file)+'.txt',mode='a',sep='\t')

def update_graph(): 
	t,v1,v2,v3,v4=read_instrument()
	#for j in range(len(Channels)):
	#	try:
	#		del ax.lines[j]
	#	except IndexError:
	#		pass
	ax.cla()
	handles=[]
	for j in Channels: 
		if j==1:
			ax.plot(t,v1,'r')
			handles+=[ch1label]
		elif j==2:
			ax.plot(t,v2,'b')
			handles+=[ch2label]
		elif j==3:
			ax.plot(t,v3,'g')
			handles+=[ch3label]
		elif j==4:
			ax.plot(t,v4,'y')
			handles+=[ch4label]
	ax.legend(handles=handles,bbox_to_anchor=(1,1),bbox_transform=plt.gcf().transFigure)
	ax.set_xlabel('Time (s)')
	ax.set_ylabel('Volts (V)')
	ax.set_ylim(-11,11)
	extrema=[np.amin(v1),np.amin(v2),np.amax(v1),np.amax(v2),np.amin(v3),np.amax(v3),np.amin(v4),np.amax(v4)]
	if max(extrema)>11 or min(extrema)<-11: 
		ax.set_ylim(min(extrema)-2,max(extrema)+2)
	tmin,tmax=np.amin(t),np.amax(t)
	ax.set_xlim(tmin,tmax)
	canvas.show()
	root.after(1,update_graph)

root=Tk()
graphframe=Frame(root)
graphframe.pack()

canvas=FigureCanvasTkAgg(f,graphframe)
canvas.show()
canvas.get_tk_widget().pack(side=TOP,expand=False)
for j in Channels: 
	if j==1:
		max1=Label(graphframe,text='Ch1 Max Value: %s' % get_max1())
		max1.pack()
		min1=Label(graphframe,text='Ch1 Min Value: %s' % get_min1())
		min1.pack()
	elif j==2:
		max2=Label(graphframe,text='Ch2 Max Value: %s' % get_max2())
		max2.pack()
		min2=Label(graphframe,text='Ch2 Min Value: %s' % get_min2())
		min2.pack()
	elif j==3:
		max3=Label(graphframe,text='Ch3 Max Value: %s' % get_max3())
		max3.pack()
		min3=Label(graphframe,text='Ch3 Min Value: %s' % get_min3())
		min3.pack()
	elif j==4:
		max4=Label(graphframe,text='Ch4 Max Value: %s' % get_max4())
		max4.pack()
		min4=Label(graphframe,text='Ch4 Min Value: %s' % get_min4())
		min4.pack()
save=Button(graphframe,text='Save',command=save_data)
save.pack(side=LEFT,padx=10)
savelabel=Label(graphframe,text="to ")
savelabel.pack(side=LEFT)
entrylabel=Entry(graphframe)
entrylabel.pack(side=LEFT)
savelabel2=Label(graphframe,text='.txt')
savelabel2.pack(side=LEFT)
exit=Button(graphframe,text='Exit',command=exit_guy)
exit.pack()

root.after(1,update_max)
root.after(1,update_min)
root.after(1,update_graph)
root.mainloop()