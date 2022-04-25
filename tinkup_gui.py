#!/usr/bin/env python3

import tkinter.filedialog
import tkinter as tk
from tkinter.ttk import Progressbar
import time
import serial
import serial.tools.list_ports
import sys
import os
import serial

class TinkupApp(tk.Tk):

    def browse(self):
        filename = tk.filedialog.askopenfilename(
            initialdir = '.',
            title = 'Select a File',
            filetypes = (('Hex Files', '*.hex*'), ('All Files', '*.*')))
        self.filename = filename
        self.filename_disp.set(os.path.basename(filename))

    def go(self):
        self.progress['value'] += 10

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, 'tinkup')
        self.protocol('WM_DELETE_WINDOW', self.on_closing)
        self.filename = None
        self.filename_disp = tk.StringVar()
        self.filename_disp.set('No hex file selected')

        comports = [comport.device for comport in serial.tools.list_ports.comports()]
        self.com_dropdown = tk.StringVar(self)
        if len(comports) == 0:
            comports.append('No devices found')
        self.com_dropdown.set(comports[0])

        # Device selection
        com_label = tk.Label(self, text='Select RetroTINK')
        com_drop = tk.OptionMenu(self, self.com_dropdown, *comports)

        # Firmware selection
        fw_label = tk.Label(self, textvariable=self.filename_disp)
        fw_button = tk.Button(self, text='Browse...', command=self.browse)

        self.progress = Progressbar(self, mode='determinate')
        go = tk.Button(self, text='Go', command=self.go)
        
        # GUI element layout
        com_label.grid(row=0, column=0)
        com_drop.grid(row=0, column=1)
        fw_label.grid(row=1, column=0)
        fw_button.grid(row=1, column=1)
        go.grid(row=2, column=1)
        self.progress.grid(row=3, column=0, columnspan=2)

    def on_closing(self):
        self.destroy()
        sys.exit(0)

if __name__ == '__main__':
    app = TinkupApp()
    app.mainloop()

