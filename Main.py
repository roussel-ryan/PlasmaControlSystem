from ControlSystem.PlasmaChamber import PlasmaChamber
from UserInterface.Application import Application
#from GUI.app import App
import logging
import tkinter as ttk


def main():
    logging.basicConfig(level=logging.DEBUG)
    try:
        plasma_chamber = PlasmaChamber()
        root = ttk.Tk()
        Application(root, plasma_chamber)
        root.mainloop()
        print('\033[32mterminating normally\033[0m')
    except Exception as e:
        print('\033[31mterminating abnormally\033[0m')
        raise e
    finally:
        plasma_chamber.stop()



if __name__ == '__main__':
    main()
