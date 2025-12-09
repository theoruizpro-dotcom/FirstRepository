# Step 5 Capteur Ultra-son 

import serial
from serial.serialutil import SerialException
import time

serialPort = serial.Serial()
serialPort.baudrate = 1000000
serialPort.port = 'COM3'
serialPort.parity = serial.PARITY_NONE
serialPort.stopbits = serial.STOPBITS_ONE
serialPort.bytesize = serial.EIGHTBITS

try:
    serialPort.open()
except SerialException as serialException:
    print(serialException)
    if not serialPort.isOpen():
        print('Serial port not opened')
        exit()

try:
    print('Serial port opened. Write run character.')
    cmd = "r"
    serialPort.write(cmd.encode(encoding="ascii"))
    serialPort.flush()
    startTime = time.time()
    endTime = startTime
    lines = []
    while endTime - startTime < 10:
        endTime = time.time()
        line = serialPort.readline()
        lines.append(line)

    cmd = "s"
    serialPort.write(cmd.encode(encoding="ascii"))
    serialPort.flush()
    serialPort.close()
    print('Port closed')

    # Tableaux pour stocker le temps et la distance
    times = []
    distances = []

    for row in lines:
        txt = row.decode('ascii').strip()
        if txt:  # évite les lignes vides
            parts = txt.split(',')
            if len(parts) == 2:
                times.append(float(parts[0]))
                distances.append(float(parts[1]))

    print(f"Nombre de mesures: {len(times)}")
    print(f"Dernier temps: {times[-1]:.6f} s")
    print(f"Dernière distance: {distances[-1]:.2f} cm")

except Exception as exception:
    print('Exception occurred while writing/reading characters')
    print(exception)
    serialPort.close()
    print('Port closed')
