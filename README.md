# tinkup

A multiplatform utility for performing firmware updates on the RetroTINK
family of retrogaming devices.

See the [RetroTINK homepage](https://www.retrotink.com) for more information
about RetroTINK devices.

Information about firmware updates for each of the RetroTINK devices, as well
as links to the canonical (Windows-only) firmware update utility and links to
the firmware images (hex files) themselves can be found at the [RetroTINK
Blog](https://www.retrotink.com/blog).

## Liability

This is a third party utility that is not maintained by the official RetroTINK
team. Use at your own risk. Please review the following:

- The RetroTINK bootloader exists in protected memory space, and this tool is
  only able to erase the firmware application. Thus, it should not be possible
to brick your RetroTINK, but you will be able to erase your firmware and render
your device unbootable until a successful firmware update is performed.

- This utility does not attempt to verify that the hex file you specify
  matches the hardware platform you are updating. Please ensure that you are
downloading the hex file that is appropriate for the device you are updating.

- If something goes wrong mid-update and you are left with an unbootable
  RetroTINK, simply reattempt the update from the beginning and all should be
recoverable.

This project does not handle general RetroTINK support requests. If something
goes wrong specifically while using tinkup.py, please feel free to reach out
here on Github and we'll see what we can do to improve this software.

## Installation

### Dependencies

- Python 3

See [Python.org](https://www.python.org) for installation details.

Windows users: Check the optional box for "Adding Python to PATH" during the
installation wizard. This allows the python executable to be accessed from the
command line without needing to specify its absolute path.

- pySerial

Install with Python's package manager pip from a command line:

`python3 -m pip install pyserial`

Your system might have Python 3 installed simply as `python` rather than
`python3`, so try that if `python3` is not found. If neither are found, please
double check your Python installation, and Windows users should note the "Add
Python to PATH" requirement mentioned above.

More info about pySerial [here](https://github.com/pyserial/pyserial).

- Driver support for FTDI serial devices.

This depends on your operating system. If your RetroTINK is not detected by
tinkup on the first try, look for the VCP drivers for your platform on the
[FTDI website](https://ftdichip.com/drivers/vcp-drivers/). You shouldn't need
to bother with these if attaching the RetroTINK in firmware update mode causes
a new USB serial device to be detected by your OS.

Linux users: You will need read/write permission on the serial device used to
communicate with your RetroTINK, typically /dev/ttyUSB0. This can be achieved
using `sudo` or running `tinkup.py` as root. A better way may be to add your
user to the group that owns the serial device, which will grant your user
indefinite access without requiring elevation to root. With the RetroTINK
plugged in and the serial device available at /dev/ttyUSB0, run the following
command (substitute your username for "youruser") and then reboot:

`sudo usermod -a -G $(ls -l /dev/ttyUSB0 | cut -d" " -f4) youruser`

## Usage

1. Download the hex file for your specific model of RetroTINK by visiting the
[RetroTINK Blog](https://www.retrotink.com/blog).

2. Attach a USB cable between your host PC and the RetroTINK while holding the
   correct button on the RetroTINK to put it in update mode. Details about this
procedure can be seen on [YouTube](https://www.youtube.com/watch?v=Bva0JXLoq7E).

3. Run tinkup.py with a path to your firmware hex file specified as the only
argument:

`python3 tinkup.py firmware.hex`

As with the pySerial installation, if your system has installed Python 3 simply
named `python`, use that instead of `python3`.

tinkup should automatically identify your RetroTINK and proceed with the
update. It will print an error if it can't identify your RetroTINK or if it
detects several RetroTINKs connected to the same system (since it doesn't know
which one it should be updating).

