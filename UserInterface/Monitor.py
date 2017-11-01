import tkinter as tk


class MonitorPart(tk.Frame):

    def __init__(self, master, plasma_chamber, name, unit):
        super().__init__(master)
        self.plasma_chamber = plasma_chamber
        self.entered_value = tk.DoubleVar()
        self.displayed_value = tk.StringVar()
        name_label = tk.Label(self, text=name)
        name_label.grid(column=1, row=1)
        displayed_value_label = tk.Label(self, textvariable=self.displayed_value)
        displayed_value_label.grid(column=2, row=1)
        entered_value_label = tk.Entry(self, width=7, textvariable=self.entered_value)
        entered_value_label.grid(column=3, row=1)
        unit_label = tk.Label(self, text=unit)
        unit_label.grid(column=4, row=1)
        self.pack()

    def update(self):
        try:
            entered_value = self.entered_value.get()
        except Exception as e:
            return
        self.displayed_value.set('{0:.2f}'.format(entered_value))


class MonitorBox(tk.LabelFrame):

    def __init__(self, master, plasma_chamber, name):
        super().__init__(master, text=name)
        self.current = MonitorPart(self, plasma_chamber, 'Current', 'A')
        self.voltage = MonitorPart(self, plasma_chamber, 'Voltage', 'V')
        self.pack()

    def update(self):
        self.current.update()
        self.voltage.update()


class Monitor(tk.Frame):

    def __init__(self, master, plasma_chamber):
        super().__init__(master)
        self.heater_monitor = MonitorBox(self, plasma_chamber, 'Heater')
        self.discharge_monitor = MonitorBox(self, plasma_chamber, 'Discharge')
        self.solenoid_monitor = MonitorBox(self, plasma_chamber, 'Solenoid')

    def update(self):
        self.heater_monitor.update()
        self.discharge_monitor.update()
        self.solenoid_monitor.update()
