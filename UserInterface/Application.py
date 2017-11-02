from . import Diagram
from . import Monitor
import tkinter as tk


class Application(tk.Frame):
    """
    Represents the entire GUI.
    """

    refresh_rate = 100

    def __init__(self, master, plasma_chamber):
        super().__init__(master)
        self.pack()
        self.diagram = Diagram.Diagram(self, plasma_chamber)
        self.diagram.grid(column=0, row=0)
        self.monitor = Monitor.Monitor(self, plasma_chamber)
        self.monitor.grid(column=1, row=0)
        self.update()

    def update(self):
        """
        Updates all the values in the GUI.
        """
        self.diagram.update()
        self.monitor.update()
        self.master.after(self.refresh_rate, self.update)
