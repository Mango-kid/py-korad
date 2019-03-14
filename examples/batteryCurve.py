"""This sample program will use the kel103 to test a batteries capacity and 
show this information in matplotlib. This method is an aproximation and its resolution
can be increase with sampling rate. 
"""
import socket
import time
import re
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from korad import kel103

#test proporties
cutOffVoltage = 2.0
dischargeRate = 5.0

# setup the device (the IP of your ethernet/wifi interface, the IP of the Korad device)
kel = kel103.kel103("192.168.8.126", "192.168.8.128", 18190)
kel.checkDevice()

# a quick battery test
kel.setOutput(False)        
voltage = kel.measureVolt()
kel.setCurrent(dischargeRate)
voltageData = []
timeData = []
current = 0
capacity = 0
kel.setOutput(True)

# run the test
startTime = time.time()
while voltage > cutOffVoltage:
    timeData.append(time.time()- startTime)
    voltage = kel.measureVolt()
    voltageData.append(voltage)

    #solve the current stuff as a running acumulation
    current = kel.measureCurrent()
    capacity = ((startTime - time.time())/60/60) * current

    print ("Voltage: " + str(voltage) +  " V DC, Capacity: " + str(capacity) + " Ah")
    time.sleep(0.5)

# disable the output
kel.setOutput(False)
kel.endComm()

# plot the finished data
fig, ax = plt.subplots()
ax.plot(timeData, voltageData)

ax.set(xlabel='time (s)', ylabel='voltage (V DC)',
    title='Battery Discharge Test 4A')
ax.grid()

fig.savefig("test_" + str(time.time()) + ".png")
plt.show()