from ControlSystem.PlasmaChamber import PlasmaChamber
from UserInterface.Application import Application
import logging
import tkinter as tk


def main():
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('PIL').setLevel(logging.CRITICAL) # turn off excessive logging from PIL
    try:
        plasma_chamber = PlasmaChamber()
        root = tk.Tk()
        Application(root, plasma_chamber)
        root.mainloop()
    except Exception as e:
        print('\033[31mterminating abnormally\033[0m')
        raise e
    finally:
        plasma_chamber.stop()


if __name__ == '__main__':
    main()
