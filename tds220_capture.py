# Python 3 script to read TDS220 screen capture via serial port
##################
Copyright 2021 Kris Young

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in the
Software without restriction, including without limitation the rights to use, 
copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the
Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#####################
import serial
from PIL import Image

print("Capturing TDS220 BMP from COM5 - press the HARDCOPY button now")
total_expected_bytes = 38462 # Expected size of TDS220 BMP file
total_received_bytes = 0

# configure the serial connections
ser = serial.Serial(
    port='COM5',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=10 # initial timeout - have this much time to press the button
)

file=open("capture.bmp","wb")

ser.flushInput()

while True:
    try:
        ser_bytes = ser.read(999)
        #print(f"Received {len(ser_bytes)}bytes.")
        if (len(ser_bytes) == 0):
            print("\nDone!")
            break
        # We received some bytes - let's lower the timeout
        #  so we exit faster when the transfer is completed
        ser.timeout = 1
        total_received_bytes = total_received_bytes + len(ser_bytes)
        #print(ser_bytes.hex())
        # Print progress in percent on the same line
        print(f'\rDownloading capture... {round((total_received_bytes/total_expected_bytes)*100)}%', end='')
        file.write(ser_bytes)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        print("Exiting")
        break

file.close()

# Rotate 90 degrees clockwise (270 degrees CCW)
im = Image.open("capture.bmp")
out = im.transpose(Image.ROTATE_270)
out.save("capture.bmp", "BMP")
