#!/usr/bin/env python

# Built-in modules
import logging
import tkinter as ttk

class TextHandler(logging.Handler):
    """This class allows you to log to a Tkinter Text or ScrolledText widget"""
    def __init__(self, *args):
        # run the regular Handler __init__
        logging.Handler.__init__(self)
        # Store a reference to the Text it will log to
        self.text = args
        self.level_colors={'debug':'green','info':'white','warning':'yellow','error':'red','critical':'orange'}
		
        self.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
		
    def emit(self, record):
        msg = self.format(record)
        def append():
            self.text.configure(state='normal')
            self.text.insert(ttk.END, msg + '\n')
            self.text.itemconfigure(ttk.END,background='black')#self.level_colors[msg.split(':')[0].lower()])
            self.text.configure(state='disabled')
            # Autoscroll to the bottom
            self.text.yview(ttk.END)
        # This is necessary because we can't modify the Text from other threads
        self.text.after(0, append)


# Sample usage
if __name__ == '__main__':
    # Create the GUI
    root = ttk.Tk()
    
    st = ttk.Listbox(root)
    st.pack()

    # Create textLogger
    text_handler = TextHandler(st)

    # Add the handler to logger
    logger = logging.getLogger()
    logger.addHandler(text_handler)

    # Log some messages
    logger.debug('debug message')
    logger.info('info message')
    logger.warn('warn message')
    logger.error('error message')
    logger.critical('critical message')

    root.mainloop()