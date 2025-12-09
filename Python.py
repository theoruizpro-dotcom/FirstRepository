# -*- coding: utf-8 -*-
"""
Created on Tue Dec  9 08:13:33 2025

@author: TheoR
"""

# Step 3 - Comptage temporel
import serial
import sys
import time
from serial.serialutil import SerialException

serialPort = serial.Serial()
serialPort.baudrate = 1000000
serialPort.port = 'COM4'  # À adapter à votre port
serialPort.parity = serial.PARITY_NONE
serialPort.stopbits = serial.STOPBITS_ONE
serialPort.bytesize = serial.EIGHTBITS

try:
    serialPort.open()
except SerialException as serialException:
    print(serialException)
    sys.exit()

if not serialPort.isOpen():
    print('Serial port not opened')
    sys.exit()

try:
    print('Serial port opened. Write run character.')
    cmd = "r"
    serialPort.write(cmd.encode(encoding="ascii"))
    
    startTime = time.time()
    endTime = startTime
    
    # Durée d'acquisition : 10 secondes
    while (endTime - startTime < 10):
        if serialPort.in_waiting:
            # Lire et afficher le comptage temporel
            line = serialPort.readline().decode('utf-8').strip()
            print(f"Temps écoulé: {line} s")
        
        endTime = time.time()
    
    # Envoi du signal de redémarrage
    print("Envoi du signal de redémarrage...")
    cmd = "s"
    serialPort.write(cmd.encode(encoding="ascii"))
    serialPort.close()
    print('Port closed')
    
except Exception as exception:
    print('Exception occurred')
    print(exception)
    serialPort.close()
    print('Port closed')
