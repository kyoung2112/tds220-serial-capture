# tds220-serial-capture
This is a Python 3 script to download a screen capture from the TDS220 (with installed communications module) via serial port. The Tektronix TDS220 oscilloscope exports a screen capture when you press the "HARDCOPY" button on the front of the unit. The screen capture is a BMP file that's transmitted directly from the serial port on the communications module (9600, 8, N, 1).

This script starts listening for the image (with a 10 second timeout), and then starts receiving it with a dynamic progress indicator. Upon reception, the  image is then fixed (it comes from the TDS220 needing to be rotated).
