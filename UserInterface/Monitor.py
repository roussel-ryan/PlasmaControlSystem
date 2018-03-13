import tkinter as tk


def format(value):
    if value is None:
        return '----'
    else:
        return '{0:.2f}'.format(value)


class MonitorPart(tk.Frame):
    """
    Represents one line inside a box. Conisists of a name label, a displayed
    value representing the measured value, a displayed value representing the
    setpoint, a box for entering in a new setpoint, and finally a label with the
    unit.
    """

    def __init__(self, master, plasma_chamber, attribute_name, name, unit):
        super().__init__(master)
        self.plasma_chamber = plasma_chamber
        self.attribute_name = attribute_name
        self.displayed_value = tk.StringVar()
        self.setpoint_value = tk.StringVar()
        self.entered_value = tk.DoubleVar()
        name_label = tk.Label(self, text=name)
        name_label.grid(column=1, row=1)
        displayed_value_label = tk.Label(self, textvariable=self.displayed_value)
        displayed_value_label.grid(column=2, row=1)
        setpoint_label = tk.Label(self, textvariable=self.setpoint_value)
        setpoint_label.grid(column=3, row=1)
        entered_value_label = tk.Entry(self, width=7, textvariable=self.entered_value)
        entered_value_label.grid(column=4, row=1)
        unit_label = tk.Label(self, text=unit)
        unit_label.grid(column=5, row=1)
        self.pack()

    def update(self):
        self.displayed_value.set(format(self.plasma_chamber.get(self.attribute_name)))
        self.setpoint_value.set(format(self.plasma_chamber.getSetpoint(self.attribute_name)))

    def set(self):
        try:
            entered_value = self.entered_value.get()
        except Exception as e:
            return
        self.plasma_chamber.set(self.attribute_name, entered_value)


class MonitorBox(tk.LabelFrame):
    """ Represents one monitor box. """

    def __init__(self, master, plasma_chamber, current_attribute_name, voltage_attribute_name, name):
        super().__init__(master, text=name)
        self.current = MonitorPart(self, plasma_chamber, current_attribute_name, 'Current', 'A')
        self.voltage = MonitorPart(self, plasma_chamber, voltage_attribute_name, 'Voltage', 'V')
        self.pack()

    def update(self):
        self.current.update()
        self.voltage.update()

    def set(self):
        self.current.set()
        self.voltage.set()


class Monitor(tk.Frame):
    """ Represents all three monitor boxes and the set button. """

    def __init__(self, master, plasma_chamber):
        super().__init__(master)
        self.heater_monitor = MonitorBox(self, plasma_chamber, 'heater_current', 'heater_voltage', 'Heater')
        self.discharge_monitor = MonitorBox(self, plasma_chamber, 'discharge_current', 'discharge_voltage', 'Discharge')
        self.solenoid_monitor = MonitorBox(self, plasma_chamber, 'solenoid_current', 'solenoid_voltage', 'Solenoid')
        self.set_button = tk.Button(self, text='set', command=self.set)
        self.set_button.pack()

    def update(self):
        self.heater_monitor.update()
        self.discharge_monitor.update()
        self.solenoid_monitor.update()

    def set(self):
        self.heater_monitor.set()
        self.discharge_monitor.set()
        self.solenoid_monitor.set()
