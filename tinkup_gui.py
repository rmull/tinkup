#!/usr/bin/env python3

from threading import Thread, Timer
import tinkup
import tkinter.filedialog
import tkinter as tk
from tkinter.ttk import Progressbar
import time
import serial
import serial.tools.list_ports
import sys
import os
import serial

running = True

class TinkupApp(tk.Tk):

    def browse(self):
        filename = tk.filedialog.askopenfilename(
            initialdir = '.',
            title = 'Select a File',
            filetypes = (('Hex Files', '*.hex*'), ('All Files', '*.*')))
        self.filename = filename
        self.filename_disp.set(os.path.basename(filename))
        if self.filename != None and self.filename != '':
            self.go['state'] = 'normal'
        else:
            self.filename_disp.set('No hex file selected')
            self.go['state'] = 'disabled'

    def go(self):
        self.com_selected = self.com_dropdown.get()

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, 'tinkup')
        self.protocol('WM_DELETE_WINDOW', self.on_closing)
        self.filename = None
        self.com_selected = None
        self.filename_disp = tk.StringVar()
        self.filename_disp.set('No hex file selected')

        self.com_dropdown = tk.StringVar(self)
        comports_all = [comport for comport in serial.tools.list_ports.comports()]
        comports = []

        for com in comports_all:
            if com.manufacturer == 'FTDI':
                comports.append(com.device)

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
        self.go = tk.Button(self, text='Go', command=self.go)
        self.go['state'] = 'disabled'
        
        # GUI element layout
        com_label.grid(row=0, column=0)
        com_drop.grid(row=0, column=1)
        fw_label.grid(row=1, column=0)
        fw_button.grid(row=1, column=1)
        self.go.grid(row=2, column=1)
        self.progress.grid(row=3, column=0, columnspan=2)

        self.tink = None

    def timer(self, timestamp):
        # 100ms interval timer
        if running:
            if self.progress:
                timestamp += 0.1
                timer_thread = Timer(timestamp - time.time(), self.timer, args=(timestamp,)).start()
                if self.tink:
                    self.progress['value'] = self.tink.progress() * 100


    def on_closing(self):
        self.destroy()
        sys.exit(0)

if __name__ == '__main__':

    app = TinkupApp()

    timer_thread = Thread(target=app.timer, args=(time.time() + 0.1,))
    timer_thread.daemon = True
    timer_thread.start()

    app.mainloop()

    running = False
