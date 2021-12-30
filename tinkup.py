#!/usr/bin/env python3

import intelhex
import queue
import serial
import serial.tools.list_ports
from signal import signal, SIGINT
import sys
import threading
import time

COM_OVERRIDE=None
DEBUG=True
VERSION=1

running = True

def on_closing():
    global running
    running = False

def sig_handler(signal_received, frame):
    print('Got SIGINT, quitting')
    on_closing()


class Tink:
    cmd = {
            'CmdGetVer':    b'\x01', 
            'ResGetVer':    b'\x01\x01\x00\x01\x04',
            'CmdErase':     b'\x02',
            'ResErase':     b'\x02\x42\x20',
            'CmdWrite':     b'\x03',
            'ResWrite':     b'\x03\x63\x30',
            'JumpApp':      b'\x05',
            'SOH':          1,
            'EOT':          4,
            'DLE':          16,
            }
    
    serial = None
    rx_buffer = []

    def timer(self, timestamp):
        # 100ms interval timer
        if running:
            timestamp += 0.1
            self.timer_thread = threading.Timer(timestamp - time.time(), self.timer, args=(timestamp,)).start()

    def rx_parse(self, b, debug=DEBUG):
        if debug:
            print('RX: %s' % b.hex())

    def rx(self):
        while running:
            if self.serial:
                try:
                    b = self.serial.read(1)
                    if b:
                        self.rx_parse(b)
                    else:
                        print('RX timeout?')
                except:
                    print('Serial device failure, quitting')
                    on_closing()
            else:
                print('Lost serial port')
                time.sleep(1)

    def calc_crc(self, b):
        # NOTE: This is the CRC lookup table for polynomial 0x1021
        # TODO: Needs testing
        lut = [
            0, 4129, 8258, 12387,\
            16516, 20645, 24774, 28903,\
            33032, 37161, 41290, 45419,\
            49548, 53677, 57806, 61935]

        num1 = 0
        for num2 in b:
            num3 = (num1 >> 12) ^ (num2 >> 4)
            num4 = (lut[num3 & 0x0F] ^ (num1 << 4)) & 0xFFFF
            num5 = (num4 >> 12) ^ num2
            num1 = (lut[num5 & 0x0F] ^ (num4 << 4)) & 0xFFFF

        return num1

    def tx(self, b, debug=DEBUG):
        if debug:
            print('TX: %s' % b.hex())
        if self.serial and self.serial.is_open:
            try:
                self.serial.write(b)
                self.serial.flush()
            except:
                print('TX failure')
        else:
            print('TX failure, serial port not writeable')

    def tx_packet(self, b):
        b = list(b)
        crc = self.calc_crc(b)
        b.append(crc & 0xFF)
        b.append((crc >> 8) & 0xFF)
        b_tx = [int(self.cmd['SOH'])]
        for bb in b:
            if bb == self.cmd['SOH'] or bb == self.cmd['EOT'] or bb == self.cmd['DLE']:
                b_tx.append(self.cmd['DLE'])
            b_tx.append(bb)
        b_tx.append(self.cmd['EOT'])
        print(b_tx)
        self.tx(bytearray(b_tx))

    def __init__(self, port=None):
        comports = []
        if port == None:
            comports_all = [comport for comport in serial.tools.list_ports.comports()]
            for com in comports_all:
                if com.manufacturer == 'FTDI':
                    comports.append(com.device)
        else:
            comports.append(port)

        if comports:
            for com in comports:
                try:
                    self.serial = serial.Serial(com, baudrate=115200, timeout=None, rtscts=True)
                    print('Opened device at %s' % com)
                    self.running = True
                except:
                    print('Could not open device at %s' % com)
        else:
            print('No RetroTINK devices found')

        if self.serial:
            self.rx_process_thread = threading.Thread(target=self.rx, args=())
            self.rx_process_thread.daemon = True
            self.rx_process_thread.start()

            self.timer_thread = threading.Thread(target=self.timer, args=(time.time() + 0.1,))
            self.timer_thread.daemon = True
            self.timer_thread.start()
        else:
            sys.exit(-1)

        retries=5
        while retries and running:
            retries = retries - 1
            self.tx_packet(self.cmd['CmdGetVer'])
            time.sleep(1)

if __name__ == '__main__':
    signal(SIGINT, sig_handler)

    tink = Tink(COM_OVERRIDE)

    while running:
        time.sleep(0.1)

    on_closing()

