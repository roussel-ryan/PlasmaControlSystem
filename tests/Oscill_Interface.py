from tkinter import *
import visa, numpy as np, matplotlib
from struct import unpack
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure 
from matplotlib import style 
style.use('ggplot')
import matplotlib.patches as patch
import pandas as pd 
from time import *

scope=visa.ResourceManager()
scope=scope.open_resource('USB::0x0699::0x0408::C031986::INSTR')
scope.write('DATA:SOU CH1')  
scope.write('DATA:WIDTH 1') 
scope.write('DATA:ENC RPB')  
ymult1=float(scope.ask('WFMPRE:YMULT?')) 
yzero1=float(scope.ask('WFMPRE:YZERO?'))
yoff1=float(scope.ask('WFMPRE:YOFF?'))

def read_instrument(): 
	scope.write('DATA:SOU CH1') 
	scope.write('DATA:WIDTH 1') 
	scope.write('DATA:ENC RPB') 
	xincr1=float(scope.ask('WFMPRE:XINCR?'))
	scope.write('CURVE?')
	data1=scope.read_raw()

	scope.write('DATA:SOU CH2')
	scope.write("DATA:WIDTH 1")
	scope.write("DATA:ENC RPB")
	scope.write('CURVE?')
	data2=scope.read_raw()

	headerlen=2+int(data1[1])
	header=data1[:headerlen]
	ADC_Wave=data1[headerlen:-1]
	ADC_Wave=np.array(unpack('%sB'% len(ADC_Wave),ADC_Wave))
	Volts_Ch1=(ADC_Wave-yoff1)*ymult1 + yzero1
	Time_Ch1=np.arange(0,xincr1*len(Volts_Ch1)/10,xincr1/10)

	headerlen=2+int(data2[1])
	header=data2[:headerlen]
	ADC_Wave=data2[headerlen:-1]
	ADC_Wave=np.array(unpack('%sB'% len(ADC_Wave),ADC_Wave))
	Volts_Ch2=(ADC_Wave-yoff1)*ymult1 + yzero1

	return Time_Ch1, Volts_Ch1, Volts_Ch2

f=plt.figure()
ax=f.add_subplot(111)
xarray=np.arange(0,0.005,0.0001)
ax.set_ylim(-11,11)
data,=ax.plot(xarray,xarray)
data2,=ax.plot(xarray,xarray,'b')

t,v1,v2=read_instrument()
tmin1,tmax1=np.amin(t),np.amax(t)
ax.set_xlim(tmin1,tmax1)
ax.set_xlabel('Time (s)')
ax.set_ylabel('Voltage (V)')
firstguy=patch.Patch(color='red',label='Channel One')
secondguy=patch.Patch(color='blue',label='Channel Two')
ax.legend(handles=[firstguy,secondguy])

def get_max(): 
	t,v1, v2=read_instrument()
	return np.amax(v1),np.amax(v2)

def get_min(): 
	t,v1,v2=read_instrument()
	return np.amin(v1),np.amin(v2)

def update_max():
	maxval1,maxval2=get_max()
	maximum['text']='Ch1 Max Value: %s \n Ch2 Max Value: %s' % (maxval1,maxval2)
	root.after(20,update_max)

def update_min():
	minval1,minval2=get_min()
	minimum['text']='Ch1 Min Value: %s \n Ch2 Min Value: %s' % (minval1,minval2)
	root.after(20,update_min)

def exit_guy(): 
	quit()

def get_filename(): 
	name=entrylabel.get()
	return name

def save_data(): 
	dtpoints=ax[0].get_data()
	t=dtpoints[0]
	v1=dtpoints[1]
	v2=dtpoints[3]
	data=pd.DataFrame({'Time (s)':t,'Ch1 Volts (V)':v1,'Ch2 Volts (V)':v2},columns=['Time (s)','Ch1 Volts (V)','Ch2 Volts (V)'])
	file=get_filename()
	data.to_csv(r'%s'%(file)+'.txt',mode='a',sep='\t')

def update_graph():
	t,v1,v2=read_instrument()
	ax.clear()
	ax.plot(t,v1,'r',t,v2,'b')
	ax.set_ylim(-11,11)
	extrema=[np.amin(v1),np.amin(v2),np.amax(v1),np.amax(v2)]
	if max(extrema)>10 or min(extrema)<-10: 
		ax.set_ylim(min(extrema)-2,max(extrema)+2)
	tmin,tmax=np.amin(t),np.amax(t)
	ax.set_xlim(tmin,tmax)
	canvas.show()
	root.after(1,update_graph)

def pause_collection(): 
	return None

root=Tk()
graphframe=Frame(root)
graphframe.pack()

canvas=FigureCanvasTkAgg(f,graphframe)
canvas.show()
canvas.get_tk_widget().pack(side=TOP,expand=False)
maximum=Label(graphframe,text='Ch1 Max Value: %s \n Ch2 Max Value: %s' % get_max()).pack(pady=10)
minimum=Label(graphframe,text='Ch1 Min Value: %s \n Ch2 Min Value: %s' % get_min()).pack(pady=10)
save=Button(graphframe,text='Save',command=save_data).pack(side=LEFT,padx=10)
savelabel=Label(graphframe,text="to ").pack(side=LEFT)
entrylabel=Entry(graphframe).pack(side=LEFT)
savelabel2=Label(graphframe,text='.txt').pack(side=LEFT)
pause=Button(graphframe,text='Pause',command=pause_collection).pack()
exit=Button(graphframe,text='Exit',command=exit_guy).pack()

root.after(20,update_max)
root.after(20,update_min)

root.after(1,update_graph)
root.mainloop()