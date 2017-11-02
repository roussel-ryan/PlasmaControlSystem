import tkinter as tk
import os
import PIL.ImageTk


class Diagram(tk.Frame):

    data_names = (
        'heater_current', 'heater_voltage', 'discharge_current',
        'discharge_voltage', 'solenoid_current', 'solenoid_voltage',
        'chamber_pressure'
    )

    data_locations = (
        (418, 87), (418, 135), (549, 495), (549, 448), (140, 618),
        (140, 573), (360, 448)
    )

    def __init__(self, master, plasma_chamber):
        self.plasma_chamber = plasma_chamber
        # initialize and pack the diagram frame
        super().__init__(master)
        # create canvas with image
        self.canvas = tk.Canvas(self, width=800, height=654)
        self.canvas.pack()
        self.canvas.image = PIL.ImageTk.PhotoImage(file=os.path.dirname(__file__) + '/Images/Diagram.png')
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.canvas.image)
        # create displayed_data
        self.display_data = {}
        for i in range(7):
            name = self.data_names[i]
            location = self.data_locations[i]
            string_var = tk.StringVar()
            string_var.set('----')
            self.display_data[name] = string_var
            label = tk.Label(self.canvas, textvariable=string_var, bg='white')
            label.place(x=location[0], y=location[1], anchor=tk.CENTER)

    def update(self):
        foo = lambda x: str(x) if x is not None else '----'
        for name in ('solenoid_current', 'solenoid_voltage',
        'heater_current', 'heater_voltage', 'discharge_current',
        'discharge_voltage', 'chamber_pressure'):
            self.display_data[name].set(foo(self.plasma_chamber.get(name)))
